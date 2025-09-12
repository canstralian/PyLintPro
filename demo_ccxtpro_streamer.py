#!/usr/bin/env python3
"""
Demo script showing how to use the @ccxtpro_streamer decorator.

This script demonstrates the ccxtpro_streamer functionality that was
implemented for PyLintPro.
"""

import asyncio
import sys
import os

# Add src to Python path to import our module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ccxtpro_streamer import ccxtpro_streamer, get_streamer_info  # noqa: E402


@ccxtpro_streamer(exchange="binance", symbols=["BTC/USDT", "ETH/USDT"])
async def demo_handler(data):
    """Demo handler that processes streaming market data."""
    symbol = data['symbol']
    price = data['price']
    exchange = data['exchange']

    print(f"📈 {symbol} on {exchange}: ${price:.2f}")

    # For demo purposes, stop after processing 5 data points
    if hasattr(demo_handler, '_demo_count'):
        demo_handler._demo_count += 1
    else:
        demo_handler._demo_count = 1

    if demo_handler._demo_count >= 5:
        print("Demo complete - stopping stream")
        return False  # Stop streaming


@ccxtpro_streamer(
    exchange="coinbase",
    symbols=["BTC/USD"],
    timeframe="5m",
    auto_reconnect=False
)
async def price_alert_handler(data):
    """Demo handler for price alerts."""
    if data['price'] > 50000:
        print(f"🚨 Price Alert: {data['symbol']} above $50, 000!")

    # Stop after first alert for demo
    return False


async def main():
    """Main demo function."""
    print("🚀 CCXT Pro Streamer Demo")
    print("=" * 40)

    # Show configuration info
    print("\n📋 Handler Configurations:")

    demo_info = get_streamer_info(demo_handler)
    if demo_info:
        print(f"Demo Handler: {demo_info}")

    alert_info = get_streamer_info(price_alert_handler)
    if alert_info:
        print(f"Alert Handler: {alert_info}")

    print("\n🔄 Starting streaming demo...")
    print("(This uses mock data for demonstration)")

    try:
        # Run the demo handler
        await demo_handler()

        print("\n🔔 Testing price alert handler...")
        await price_alert_handler()

    except KeyboardInterrupt:
        print("\n⏹️  Demo stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")

    print("\n✅ Demo completed!")


if __name__ == "__main__":
    asyncio.run(main())
