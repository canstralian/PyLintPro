#!/usr/bin/env python3
"""
GitHub webhook handler for Mendicant AI.
Processes GitHub App webhook events and triggers repository analysis.
"""

import hashlib
import hmac
import json
import logging
from pathlib import Path
import sys
from typing import Dict, Any, Optional

from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
import asyncpg

# Add src to path for imports  
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from src.config import (
    DATABASE_URL, GITHUB_WEBHOOK_SECRET, 
    APP_NAME, APP_VERSION
)
from src.utils import setup_logging

logger = setup_logging(__name__)

class GitHubWebhookHandler:
    """Handles GitHub webhook events for repository monitoring."""
    
    def __init__(self):
        self.app = FastAPI(
            title=f"{APP_NAME} Webhook Handler",
            version=APP_VERSION,
            description="GitHub webhook handler for repository health monitoring"
        )
        self._setup_routes()
    
    def _setup_routes(self):
        """Set up FastAPI routes."""
        
        @self.app.get("/health")
        async def health_check():
            """Health check endpoint."""
            return {"status": "healthy", "service": "webhook-handler"}
        
        @self.app.post("/webhooks/github")
        async def github_webhook(request: Request, background_tasks: BackgroundTasks):
            """Handle GitHub webhook events."""
            
            # Verify webhook signature
            body = await request.body()
            if not self._verify_signature(body, request.headers.get("X-Hub-Signature-256")):
                raise HTTPException(status_code=401, detail="Invalid signature")
            
            # Parse event
            try:
                payload = json.loads(body)
                event_type = request.headers.get("X-GitHub-Event")
                action = payload.get("action")
                
                logger.info(f"Received GitHub event: {event_type} - {action}")
                
                # Log webhook event
                await self._log_webhook_event(
                    event_type=event_type,
                    action=action,
                    payload=payload,
                    event_id=request.headers.get("X-GitHub-Delivery")
                )
                
                # Process event in background
                background_tasks.add_task(
                    self._process_webhook_event,
                    event_type=event_type,
                    action=action,
                    payload=payload
                )
                
                return JSONResponse({"status": "accepted"})
                
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid JSON payload")
            except Exception as e:
                logger.error(f"Error processing webhook: {e}")
                raise HTTPException(status_code=500, detail="Internal server error")
    
    def _verify_signature(self, body: bytes, signature_header: Optional[str]) -> bool:
        """Verify GitHub webhook signature."""
        if not GITHUB_WEBHOOK_SECRET:
            logger.warning("GITHUB_WEBHOOK_SECRET not configured, skipping signature verification")
            return True
        
        if not signature_header:
            return False
        
        try:
            # Extract signature from header
            signature = signature_header.replace("sha256=", "")
            
            # Calculate expected signature
            expected_signature = hmac.new(
                GITHUB_WEBHOOK_SECRET.encode('utf-8'),
                body,
                hashlib.sha256
            ).hexdigest()
            
            return hmac.compare_digest(signature, expected_signature)
            
        except Exception as e:
            logger.error(f"Signature verification failed: {e}")
            return False
    
    async def _log_webhook_event(
        self, 
        event_type: str, 
        action: Optional[str],
        payload: Dict[str, Any],
        event_id: Optional[str]
    ):
        """Log webhook event to database."""
        try:
            conn = await asyncpg.connect(DATABASE_URL)
            
            # Extract repository and installation info
            repository_id = None
            installation_id = None
            
            if "repository" in payload:
                repo = payload["repository"]
                repository_id = await self._get_or_create_repository(conn, repo)
            
            if "installation" in payload:
                installation_id = await self._get_or_create_installation(
                    conn, payload["installation"]
                )
            
            # Insert webhook event
            await conn.execute("""
                INSERT INTO webhook_events 
                (github_event_id, event_type, action, repository_id, installation_id, payload)
                VALUES ($1, $2, $3, $4, $5, $6)
            """, event_id, event_type, action, repository_id, installation_id, json.dumps(payload))
            
            await conn.close()
            
        except Exception as e:
            logger.error(f"Failed to log webhook event: {e}")
    
    async def _get_or_create_repository(self, conn: asyncpg.Connection, repo_data: Dict) -> int:
        """Get or create repository record."""
        github_id = repo_data["id"]
        
        # Try to get existing repository
        repo_id = await conn.fetchval(
            "SELECT id FROM repositories WHERE github_id = $1", github_id
        )
        
        if repo_id:
            # Update repository info
            await conn.execute("""
                UPDATE repositories SET
                    full_name = $1, owner = $2, name = $3,
                    default_branch = $4, updated_at = CURRENT_TIMESTAMP
                WHERE github_id = $5
            """, 
                repo_data["full_name"],
                repo_data["owner"]["login"],
                repo_data["name"], 
                repo_data.get("default_branch", "main"),
                github_id
            )
            return repo_id
        else:
            # Create new repository
            repo_id = await conn.fetchval("""
                INSERT INTO repositories 
                (github_id, full_name, owner, name, default_branch, languages)
                VALUES ($1, $2, $3, $4, $5, $6)
                RETURNING id
            """,
                github_id,
                repo_data["full_name"],
                repo_data["owner"]["login"],
                repo_data["name"],
                repo_data.get("default_branch", "main"),
                json.dumps(repo_data.get("language", {}))
            )
            return repo_id
    
    async def _get_or_create_installation(self, conn: asyncpg.Connection, install_data: Dict) -> int:
        """Get or create installation record."""
        github_installation_id = install_data["id"]
        
        # Try to get existing installation
        install_id = await conn.fetchval(
            "SELECT id FROM installations WHERE github_installation_id = $1", 
            github_installation_id
        )
        
        if install_id:
            return install_id
        else:
            # Create new installation
            account = install_data["account"]
            install_id = await conn.fetchval("""
                INSERT INTO installations 
                (github_installation_id, account_type, account_login, account_id, permissions)
                VALUES ($1, $2, $3, $4, $5)
                RETURNING id
            """,
                github_installation_id,
                account["type"].lower(),
                account["login"],
                account["id"],
                json.dumps(install_data.get("permissions", {}))
            )
            return install_id
    
    async def _process_webhook_event(
        self,
        event_type: str,
        action: Optional[str], 
        payload: Dict[str, Any]
    ):
        """Process webhook event and trigger appropriate actions."""
        try:
            logger.info(f"Processing webhook event: {event_type} - {action}")
            
            # Handle different event types
            if event_type == "push":
                await self._handle_push_event(payload)
            elif event_type == "pull_request":
                await self._handle_pull_request_event(payload, action)
            elif event_type == "installation":
                await self._handle_installation_event(payload, action)
            elif event_type == "installation_repositories":
                await self._handle_installation_repositories_event(payload, action)
            else:
                logger.debug(f"Unhandled event type: {event_type}")
            
            # Mark event as processed
            await self._mark_event_processed(payload.get("delivery", {}).get("id"))
            
        except Exception as e:
            logger.error(f"Failed to process webhook event: {e}")
            await self._mark_event_failed(
                payload.get("delivery", {}).get("id"), 
                str(e)
            )
    
    async def _handle_push_event(self, payload: Dict[str, Any]):
        """Handle push events - trigger repository analysis."""
        repo = payload["repository"]
        ref = payload["ref"]
        
        # Only process pushes to default branch
        if ref != f"refs/heads/{repo.get('default_branch', 'main')}":
            logger.debug(f"Ignoring push to non-default branch: {ref}")
            return
        
        logger.info(f"Triggering analysis for repository: {repo['full_name']}")
        
        # TODO: Queue repository analysis job
        # For now, just log the intent
        conn = await asyncpg.connect(DATABASE_URL)
        try:
            await conn.execute("""
                UPDATE repositories SET last_analyzed_at = CURRENT_TIMESTAMP
                WHERE github_id = $1
            """, repo["id"])
        finally:
            await conn.close()
    
    async def _handle_pull_request_event(self, payload: Dict[str, Any], action: Optional[str]):
        """Handle pull request events."""
        if action not in ["opened", "synchronize", "closed"]:
            return
        
        pr = payload["pull_request"]
        repo = payload["repository"]
        
        logger.info(f"PR {action}: {repo['full_name']}#{pr['number']}")
        
        # TODO: Analyze PR changes and provide feedback
        
    async def _handle_installation_event(self, payload: Dict[str, Any], action: Optional[str]):
        """Handle installation events."""
        installation = payload["installation"]
        
        if action == "created":
            logger.info(f"New installation: {installation['account']['login']}")
            # TODO: Send welcome message, setup onboarding
        elif action == "deleted":
            logger.info(f"Installation deleted: {installation['account']['login']}")
            # TODO: Cleanup data, send feedback survey
    
    async def _handle_installation_repositories_event(self, payload: Dict[str, Any], action: Optional[str]):
        """Handle installation repository events."""
        if action == "added":
            repos = payload.get("repositories_added", [])
            for repo in repos:
                logger.info(f"Repository added to installation: {repo['full_name']}")
                # TODO: Queue initial repository analysis
        elif action == "removed":
            repos = payload.get("repositories_removed", [])
            for repo in repos:
                logger.info(f"Repository removed from installation: {repo['full_name']}")
                # TODO: Stop monitoring, cleanup data
    
    async def _mark_event_processed(self, event_id: Optional[str]):
        """Mark webhook event as successfully processed."""
        if not event_id:
            return
        
        try:
            conn = await asyncpg.connect(DATABASE_URL)
            await conn.execute("""
                UPDATE webhook_events SET 
                    status = 'processed', processed_at = CURRENT_TIMESTAMP
                WHERE github_event_id = $1
            """, event_id)
            await conn.close()
        except Exception as e:
            logger.error(f"Failed to mark event as processed: {e}")
    
    async def _mark_event_failed(self, event_id: Optional[str], error_message: str):
        """Mark webhook event as failed."""
        if not event_id:
            return
        
        try:
            conn = await asyncpg.connect(DATABASE_URL)
            await conn.execute("""
                UPDATE webhook_events SET 
                    status = 'failed', error_message = $1, processed_at = CURRENT_TIMESTAMP
                WHERE github_event_id = $2
            """, error_message, event_id)
            await conn.close()
        except Exception as e:
            logger.error(f"Failed to mark event as failed: {e}")

# Create global handler instance
webhook_handler = GitHubWebhookHandler()
app = webhook_handler.app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)