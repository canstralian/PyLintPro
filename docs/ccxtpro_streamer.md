# CCXT Pro Streamer Documentation

## Overview

The `@ccxtpro_streamer` decorator provides a simple way to create streaming handlers for cryptocurrency market data. This module is part of PyLintPro and demonstrates decorator-based streaming functionality.

## Features

- **Decorator-based streaming**: Simple `@ccxtpro_streamer` decorator to convert any async function into a streaming handler
- **Multiple exchange support**: Configure different exchanges (binance, coinbase, etc.)
- **Symbol filtering**: Stream specific trading pairs
- **Timeframe configuration**: Set candlestick timeframes (1m, 5m, 1h, etc.)
- **Auto-reconnection**: Automatic reconnection on connection failures
- **Mock implementation**: Safe demo implementation that doesn't require real API credentials

## Installation

The ccxtpro_streamer module is included with PyLintPro. No additional installation required.

## Basic Usage

```python
from src.ccxtpro_streamer import ccxtpro_streamer

@ccxtpro_streamer(exchange="binance", symbols=["BTC/USDT"])
async def my_handler(data):
    print(f"Price: {data['symbol']} @ ${data['price']:.2f}")
    
# Run the handler
await my_handler()
```

## Configuration Options

- `exchange`: Exchange name (default: "binance")
- `symbols`: List of trading pairs (default: ["BTC/USDT", "ETH/USDT"])
- `timeframe`: Candlestick timeframe (default: "1m")
- `auto_reconnect`: Enable auto-reconnection (default: True)

## Examples

### Basic Market Data Handler

```python
@ccxtpro_streamer(exchange="binance", symbols=["BTC/USDT", "ETH/USDT"])
async def market_data_handler(data):
    symbol = data['symbol']
    price = data['price']
    volume = data['volume']
    
    print(f"{symbol}: ${price:.2f} (Volume: {volume})")
```

### Price Alert System

```python
@ccxtpro_streamer(
    exchange="coinbase", 
    symbols=["BTC/USD"], 
    timeframe="5m"
)
async def price_alert_handler(data):
    if data['price'] > 50000:
        print(f"🚨 Alert: {data['symbol']} above $50,000!")
        
    # Return False to stop streaming
    return False
```

### Multi-Stream Processing

```python
from src.ccxtpro_streamer import create_multi_stream_handler

# Create multiple handlers
@ccxtpro_streamer(exchange="binance")
async def binance_handler(data):
    print(f"Binance: {data}")

@ccxtpro_streamer(exchange="coinbase")
async def coinbase_handler(data):
    print(f"Coinbase: {data}")

# Run them simultaneously
multi_handler = create_multi_stream_handler(binance_handler, coinbase_handler)
await multi_handler()
```

## Data Format

Each streaming data packet contains:

```python
{
    "symbol": "BTC/USDT",      # Trading pair
    "price": 50000.00,         # Current price
    "volume": 100.0,           # Volume
    "timestamp": 1234567890,   # Unix timestamp
    "exchange": "binance"      # Exchange name
}
```

## Utility Functions

### get_streamer_info()

Get configuration information from a decorated function:

```python
from src.ccxtpro_streamer import get_streamer_info

info = get_streamer_info(my_handler)
print(info)  # {'exchange': 'binance', 'symbols': ['BTC/USDT'], ...}
```

## Error Handling

The decorator automatically handles:
- Connection failures
- Streaming errors
- Reconnection (if enabled)

Functions can stop streaming by returning `False`:

```python
@ccxtpro_streamer()
async def limited_handler(data):
    # Process some data...
    
    if some_condition:
        return False  # Stop streaming
```

## Testing

Run the included demo:

```bash
python demo_ccxtpro_streamer.py
```

Run the test suite:

```bash
python -m pytest tests/test_ccxtpro_streamer.py -v
```

## Notes

- This is a mock implementation for demonstration purposes
- In production, you would integrate with the actual CCXT Pro library
- The mock streamer generates synthetic data for testing
- Real implementation would require API credentials and proper error handling

## Integration with PyLintPro

The ccxtpro_streamer module is fully integrated with PyLintPro:

```python
# Import from main package
from src import ccxtpro_streamer

# Or import specific components
from src.ccxtpro_streamer import ccxtpro_streamer, StreamerConfig
```

## License

This module is part of PyLintPro and follows the same licensing terms.