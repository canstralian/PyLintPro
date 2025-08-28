#!/usr/bin/env python3
"""
Database initialization script for Mendicant AI.
Creates the PostgreSQL database schema with all required tables.
"""

import os
import sys
import asyncio
import asyncpg
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from src.config import DATABASE_URL
from src.utils import setup_logging

logger = setup_logging(__name__)

# Database schema
SCHEMA_SQL = """
-- Repository Health Tracking
CREATE TABLE repositories (
    id SERIAL PRIMARY KEY,
    github_id BIGINT UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    owner VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    default_branch VARCHAR(255) DEFAULT 'main',
    languages JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_analyzed_at TIMESTAMP,
    health_score INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT true
);

-- Health Check Results
CREATE TABLE health_checks (
    id SERIAL PRIMARY KEY,
    repository_id INTEGER REFERENCES repositories(id) ON DELETE CASCADE,
    check_type VARCHAR(100) NOT NULL, -- 'code_quality', 'security', 'testing', 'documentation'
    check_name VARCHAR(200) NOT NULL,
    status VARCHAR(50) NOT NULL, -- 'passed', 'failed', 'warning', 'info'
    severity VARCHAR(20) DEFAULT 'medium', -- 'low', 'medium', 'high', 'critical'
    message TEXT,
    details JSONB DEFAULT '{}',
    file_path VARCHAR(500),
    line_number INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Pull Request Tracking
CREATE TABLE pull_requests (
    id SERIAL PRIMARY KEY,
    repository_id INTEGER REFERENCES repositories(id) ON DELETE CASCADE,
    github_pr_id BIGINT UNIQUE NOT NULL,
    pr_number INTEGER NOT NULL,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'open', -- 'open', 'closed', 'merged'
    fixes_check_ids INTEGER[] DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    merged_at TIMESTAMP
);

-- Organization/User Management
CREATE TABLE installations (
    id SERIAL PRIMARY KEY,
    github_installation_id BIGINT UNIQUE NOT NULL,
    account_type VARCHAR(20) NOT NULL, -- 'user' or 'organization'
    account_login VARCHAR(255) NOT NULL,
    account_id BIGINT NOT NULL,
    permissions JSONB DEFAULT '{}',
    installed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

-- Pilot Program Tracking
CREATE TABLE pilot_programs (
    id SERIAL PRIMARY KEY,
    installation_id INTEGER REFERENCES installations(id) ON DELETE CASCADE,
    contact_email VARCHAR(255) NOT NULL,
    contact_name VARCHAR(255),
    company_name VARCHAR(255),
    pilot_start_date DATE,
    pilot_end_date DATE,
    status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'active', 'completed', 'cancelled'
    success_metrics JSONB DEFAULT '{}',
    payment_status VARCHAR(50) DEFAULT 'pending',
    stripe_customer_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Webhook Event Log
CREATE TABLE webhook_events (
    id SERIAL PRIMARY KEY,
    github_event_id VARCHAR(255) UNIQUE,
    event_type VARCHAR(100) NOT NULL,
    action VARCHAR(100),
    repository_id INTEGER REFERENCES repositories(id) ON DELETE SET NULL,
    installation_id INTEGER REFERENCES installations(id) ON DELETE SET NULL,
    payload JSONB NOT NULL,
    processed_at TIMESTAMP,
    status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'processed', 'failed'
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX idx_repositories_github_id ON repositories(github_id);
CREATE INDEX idx_repositories_full_name ON repositories(full_name);
CREATE INDEX idx_health_checks_repository_id ON health_checks(repository_id);
CREATE INDEX idx_health_checks_type_status ON health_checks(check_type, status);
CREATE INDEX idx_pull_requests_repository_id ON pull_requests(repository_id);
CREATE INDEX idx_pull_requests_github_id ON pull_requests(github_pr_id);
CREATE INDEX idx_webhook_events_type ON webhook_events(event_type);
CREATE INDEX idx_webhook_events_status ON webhook_events(status);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Add triggers for updated_at columns
CREATE TRIGGER update_repositories_updated_at BEFORE UPDATE ON repositories
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_pull_requests_updated_at BEFORE UPDATE ON pull_requests
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_pilot_programs_updated_at BEFORE UPDATE ON pilot_programs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
"""

async def init_database():
    """Initialize the database with required schema."""
    try:
        # Parse database URL
        if not DATABASE_URL:
            raise ValueError("DATABASE_URL environment variable is required")
        
        # Extract database name from URL for initial connection
        # Format: postgresql://user:pass@host:port/dbname
        parts = DATABASE_URL.split('/')
        db_name = parts[-1]
        base_url = '/'.join(parts[:-1])
        
        logger.info(f"Connecting to PostgreSQL at {base_url}")
        
        # Connect to postgres database to create our database if it doesn't exist
        postgres_url = f"{base_url}/postgres"
        try:
            conn = await asyncpg.connect(postgres_url)
            
            # Check if database exists
            db_exists = await conn.fetchval(
                "SELECT 1 FROM pg_database WHERE datname = $1", db_name
            )
            
            if not db_exists:
                logger.info(f"Creating database: {db_name}")
                await conn.execute(f'CREATE DATABASE "{db_name}"')
            else:
                logger.info(f"Database {db_name} already exists")
                
            await conn.close()
        except Exception as e:
            logger.error(f"Error creating database: {e}")
            # Continue anyway - database might already exist
        
        # Now connect to our database and create schema
        logger.info(f"Initializing schema in database: {db_name}")
        conn = await asyncpg.connect(DATABASE_URL)
        
        # Execute schema
        await conn.execute(SCHEMA_SQL)
        
        logger.info("Database schema created successfully")
        
        # Insert initial data if needed
        await conn.execute("""
            INSERT INTO installations (github_installation_id, account_type, account_login, account_id)
            VALUES (0, 'system', 'mendicant-ai', 0)
            ON CONFLICT (github_installation_id) DO NOTHING
        """)
        
        await conn.close()
        logger.info("Database initialization completed successfully")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(init_database())