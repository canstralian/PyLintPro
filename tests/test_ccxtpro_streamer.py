"""
Tests for the CCXT Pro Streamer module.
"""

import asyncio
import pytest
from unittest.mock import AsyncMock, patch
from src.ccxtpro_streamer import (
    ccxtpro_streamer,
    StreamerConfig,
    MockStreamer,
    get_streamer_info,
    create_multi_stream_handler
)


class TestStreamerConfig:
    """Test cases for StreamerConfig class."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = StreamerConfig()
        assert config.exchange == "binance"
        assert config.symbols == ["BTC/USDT", "ETH/USDT"]
        assert config.timeframe == "1m"
        assert config.max_retries == 3
        assert config.reconnect_delay == 5.0
    
    def test_custom_config(self):
        """Test custom configuration values."""
        config = StreamerConfig(
            exchange="coinbase",
            symbols=["BTC/USD"],
            timeframe="5m",
            max_retries=5,
            reconnect_delay=10.0
        )
        assert config.exchange == "coinbase"
        assert config.symbols == ["BTC/USD"]
        assert config.timeframe == "5m"
        assert config.max_retries == 5
        assert config.reconnect_delay == 10.0


class TestMockStreamer:
    """Test cases for MockStreamer class."""
    
    @pytest.fixture
    def config(self):
        """Fixture providing a test configuration."""
        return StreamerConfig(exchange="test", symbols=["TEST/USDT"])
    
    @pytest.fixture
    def streamer(self, config):
        """Fixture providing a test streamer."""
        return MockStreamer(config)
    
    @pytest.mark.asyncio
    async def test_connect_disconnect(self, streamer):
        """Test connection and disconnection."""
        assert not streamer.is_connected
        
        await streamer.connect()
        assert streamer.is_connected
        
        await streamer.disconnect()
        assert not streamer.is_connected
    
    @pytest.mark.asyncio
    async def test_stream_data(self, streamer):
        """Test data streaming functionality."""
        await streamer.connect()
        
        data_count = 0
        async for data in streamer.stream_data():
            assert "symbol" in data
            assert "price" in data
            assert "volume" in data
            assert "timestamp" in data
            assert "exchange" in data
            assert data["exchange"] == "test"
            
            data_count += 1
            if data_count >= 2:  # Test a few iterations
                break
        
        await streamer.disconnect()
        assert data_count == 2


class TestCCXTProStreamerDecorator:
    """Test cases for the ccxtpro_streamer decorator."""
    
    def test_decorator_metadata(self):
        """Test that decorator adds correct metadata."""
        @ccxtpro_streamer(exchange="binance", symbols=["BTC/USDT"])
        async def test_handler(data):
            pass
        
        assert hasattr(test_handler, '_is_ccxtpro_streamer')
        assert test_handler._is_ccxtpro_streamer is True
        assert hasattr(test_handler, '_streamer_config')
        
        config = test_handler._streamer_config
        assert config["exchange"] == "binance"
        assert config["symbols"] == ["BTC/USDT"]
        assert config["timeframe"] == "1m"  # default
        assert config["auto_reconnect"] is True  # default
    
    def test_get_streamer_info(self):
        """Test get_streamer_info utility function."""
        @ccxtpro_streamer(exchange="coinbase", symbols=["ETH/USD"])
        async def streamer_func(data):
            pass
        
        async def normal_func():
            pass
        
        # Test decorated function
        info = get_streamer_info(streamer_func)
        assert info is not None
        assert info["exchange"] == "coinbase"
        assert info["symbols"] == ["ETH/USD"]
        
        # Test non-decorated function
        info = get_streamer_info(normal_func)
        assert info is None
    
    @pytest.mark.asyncio
    async def test_decorator_execution(self):
        """Test that decorated function executes correctly."""
        call_count = 0
        received_data = []
        
        @ccxtpro_streamer(exchange="test", symbols=["TEST/USDT"])
        async def test_handler(data):
            nonlocal call_count
            call_count += 1
            received_data.append(data)
            
            # Stop after 2 calls for testing
            if call_count >= 2:
                return False
        
        # Mock the streamer to limit execution time
        with patch('src.ccxtpro_streamer.MockStreamer') as mock_streamer_class:
            mock_streamer = AsyncMock()
            mock_streamer_class.return_value = mock_streamer
            
            # Create an async generator for mock_stream
            async def mock_stream():
                for i in range(3):
                    yield {
                        "symbol": "TEST/USDT",
                        "price": 100.0 + i,
                        "volume": 50.0,
                        "timestamp": 1234567890 + i,
                        "exchange": "test"
                    }
            
            # Set the mock to return the async generator
            mock_streamer.stream_data = mock_stream
            
            await test_handler()
            
            # Verify the handler was called
            assert call_count == 2
            assert len(received_data) == 2
            assert received_data[0]["price"] == 100.0
            assert received_data[1]["price"] == 101.0


class TestMultiStreamHandler:
    """Test cases for multi-stream functionality."""
    
    def test_create_multi_stream_handler(self):
        """Test creating a multi-stream handler."""
        @ccxtpro_streamer(exchange="binance")
        async def handler1(data):
            pass
        
        @ccxtpro_streamer(exchange="coinbase")
        async def handler2(data):
            pass
        
        async def regular_function():
            pass
        
        multi_handler = create_multi_stream_handler(
            handler1, handler2, regular_function
        )
        
        assert callable(multi_handler)
        # The function should be created successfully
        assert multi_handler is not None


# Integration test
class TestIntegration:
    """Integration tests for the complete streaming system."""
    
    @pytest.mark.asyncio
    async def test_end_to_end_streaming(self):
        """Test complete streaming workflow."""
        messages = []
        
        @ccxtpro_streamer(
            exchange="integration_test",
            symbols=["INT/TEST"],
            timeframe="1s"
        )
        async def integration_handler(data):
            messages.append(f"Processed {data['symbol']} at ${data['price']:.2f}")
            # Stop after first message for test
            return False
        
        # Run the handler
        with patch('src.ccxtpro_streamer.MockStreamer') as mock_streamer_class:
            mock_streamer = AsyncMock()
            mock_streamer_class.return_value = mock_streamer
            
            async def mock_stream():
                yield {
                    "symbol": "INT/TEST",
                    "price": 999.99,
                    "volume": 100.0,
                    "timestamp": 1234567890,
                    "exchange": "integration_test"
                }
            
            # Set the mock to return the async generator
            mock_streamer.stream_data = mock_stream
            
            await integration_handler()
            
            # Verify connection was attempted
            mock_streamer.connect.assert_called_once()
            mock_streamer.disconnect.assert_called_once()
            
            # Verify message was processed
            assert len(messages) == 1
            assert "INT/TEST" in messages[0]
            assert "999.99" in messages[0]


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])