#!/usr/bin/env python3
"""
Trading Signal Generator
From the book: Practical Python for Effective Algorithmic Trading
Available at: https://www.amazon.com/dp/B0F3S8FQ7C

This script analyzes basic stock metrics and generates buy, sell, or hold signals
based on technical indicators. It demonstrates the use of Python's comparison and
logical operators to implement simple trading rules as taught in Chapter 3.
"""

def main():
    """
    Main function that prompts for stock metrics, analyzes the data,
    and generates a trading signal with explanation.
    """
    print("=" * 70)
    print("TRADING SIGNAL GENERATOR")
    print("=" * 70)
    print("Enter the following metrics for your stock:")

    # Get user inputs for stock metrics
    symbol = input("Enter stock symbol: ").upper()
    current_price = float(input("Enter current price: $"))
    ma_50 = float(input("Enter 50-day moving average price: $"))
    ma_200 = float(input("Enter 200-day moving average price: $"))
    rsi = float(input("Enter current RSI value (0-100): "))
    volume = int(input("Enter current trading volume: "))
    avg_volume = int(input("Enter average trading volume: "))

    print("\nAnalyzing metrics for", symbol, "...")
    print("-" * 70)

    # Check for Golden Cross or Death Cross
    golden_cross = ma_50 > ma_200
    death_cross = ma_50 < ma_200

    # Calculate percentage differences
    price_vs_ma50_percent = ((current_price - ma_50) / ma_50) * 100
    price_vs_ma200_percent = ((current_price - ma_200) / ma_200) * 100
    volume_vs_avg_percent = ((volume - avg_volume) / avg_volume) * 100

    # Print technical analysis
    print(f"Price vs 50-day MA: {price_vs_ma50_percent:.2f}%")
    print(f"Price vs 200-day MA: {price_vs_ma200_percent:.2f}%")
    print(f"Volume vs Average: {volume_vs_avg_percent:.2f}%")

    if golden_cross:
        print("GOLDEN CROSS DETECTED: 50-day MA above 200-day MA (Bullish)")
    elif death_cross:
        print("DEATH CROSS DETECTED: 50-day MA below 200-day MA (Bearish)")
    else:
        print("No cross pattern detected")

    # Define signal generation rules
    buy_signal = False
    sell_signal = False
    hold_signal = True  # Default position

    # Rule 1: Buy if price is above both moving averages AND RSI is below 70 AND volume is above average
    if current_price > ma_50 and current_price > ma_200 and rsi < 70 and volume > avg_volume:
        buy_signal = True
        hold_signal = False
        signal_reason = "Price is above both moving averages, RSI is not overbought, and volume is strong"

    # Rule 2: Sell if price is below both moving averages OR RSI is above 70
    elif (current_price < ma_50 and current_price < ma_200) or rsi > 70:
        sell_signal = True
        hold_signal = False
        if current_price < ma_50 and current_price < ma_200:
            signal_reason = "Price is below both moving averages"
        elif rsi > 70:
            signal_reason = "RSI indicates overbought conditions"
        else:
            signal_reason = "Multiple bearish conditions detected"

    # Output final recommendation
    print("\n" + "=" * 70)
    print("TRADING SIGNAL RECOMMENDATION FOR", symbol)
    print("=" * 70)

    if buy_signal:
        print("RECOMMENDATION: BUY")
        print(f"Reason: {signal_reason}")
        
        # Additional buy signal strength indicator
        if golden_cross:
            print("Signal strengthened by Golden Cross pattern")
        if volume > avg_volume * 1.5:
            print("Signal strengthened by significantly above-average volume")
        
    elif sell_signal:
        print("RECOMMENDATION: SELL")
        print(f"Reason: {signal_reason}")
        
        # Additional sell signal strength indicator
        if death_cross:
            print("Signal strengthened by Death Cross pattern")
        if rsi > 80:
            print("Signal strengthened by strongly overbought conditions")
        
    else:
        print("RECOMMENDATION: HOLD")
        print("Reason: Mixed or neutral signals - no clear buy or sell indication")
        
        # Additional context for hold recommendation
        if current_price > ma_50 and current_price < ma_200:
            print("Price is between 50-day and 200-day moving averages")
        elif rsi > 40 and rsi < 60:
            print("RSI indicates neutral momentum")

    print("-" * 70)
    print("Note: This is a simplified analysis. Always consider other factors")
    print("before making trading decisions.")
    
    # For more advanced trading strategies and systematic analysis approaches,
    # check out the complete book: https://www.amazon.com/dp/B0F3S8FQ7C
    # Join our community for implementation support: https://www.skool.com/the-quantitative-elite

if __name__ == "__main__":
    main()