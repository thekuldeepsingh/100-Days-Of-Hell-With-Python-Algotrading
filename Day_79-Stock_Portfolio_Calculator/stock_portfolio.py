#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stock Portfolio Summary Calculator
==================================
From the book: Practical Python for Effective Algorithmic Trading
Available at: https://www.amazon.com/dp/B0F3S8FQ7C

This script implements a simple portfolio calculator that:
- Collects information about 3 stocks in your portfolio
- Calculates position value, profit/loss, and percentage return
- Displays a comprehensive summary of your investments

Author: Kuldeep Singh Rathore
YouTube: Kuldeep Singh Rathore
Community: https://www.skool.com/the-quantitative-elite
"""

import os

def clear_screen():
    """Clear the terminal screen for better readability."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_welcome():
    """Display a welcome message with instructions."""
    print("=" * 60)
    print("📊 STOCK PORTFOLIO SUMMARY CALCULATOR 📊")
    print("=" * 60)
    print("This program will help you analyze your stock portfolio.")
    print("You'll enter information for 3 stocks and get a summary report.")
    print("=" * 60)

def get_float_input(prompt, min_value=0):
    """
    Get and validate float input from user.
    
    Args:
        prompt (str): The input prompt to display
        min_value (float): Minimum acceptable value
        
    Returns:
        float: Validated user input
    """
    while True:
        try:
            value = float(input(prompt))
            if value <= min_value:
                print(f"  ❌ Value must be greater than {min_value}. Try again.")
                continue
            return value
        except ValueError:
            print("  ❌ Invalid input. Please enter a numeric value.")

def get_int_input(prompt, min_value=0):
    """
    Get and validate integer input from user.
    
    Args:
        prompt (str): The input prompt to display
        min_value (int): Minimum acceptable value
        
    Returns:
        int: Validated user input
    """
    while True:
        try:
            value = int(input(prompt))
            if value <= min_value:
                print(f"  ❌ Value must be greater than {min_value}. Try again.")
                continue
            return value
        except ValueError:
            print("  ❌ Invalid input. Please enter a whole number.")

def collect_stock_info():
    """
    Collect information about each stock in the portfolio.
    
    Returns:
        tuple: Lists containing symbols, purchase prices, current prices, and share counts
    """
    symbols = []
    purchase_prices = []
    current_prices = []
    share_counts = []
    
    for i in range(3):
        print(f"\n📈 Stock #{i+1} Information:")
        
        # Get stock symbol
        symbol = input("  Enter stock symbol (e.g., AAPL): ").upper()
        symbols.append(symbol)
        
        # Get purchase price
        purchase_price = get_float_input(f"  Enter purchase price for {symbol} ($): ")
        purchase_prices.append(purchase_price)
        
        # Get current price
        current_price = get_float_input(f"  Enter current price for {symbol} ($): ")
        current_prices.append(current_price)
        
        # Get share count
        shares = get_int_input(f"  Enter number of {symbol} shares: ")
        share_counts.append(shares)
    
    return symbols, purchase_prices, current_prices, share_counts

def calculate_metrics(symbols, purchase_prices, current_prices, share_counts):
    """
    Calculate performance metrics for each stock and the overall portfolio.
    
    Args:
        symbols (list): Stock symbols
        purchase_prices (list): Purchase prices for each stock
        current_prices (list): Current prices for each stock
        share_counts (list): Number of shares for each stock
        
    Returns:
        tuple: Lists of position values, dollar gains, percent gains, and portfolio totals
    """
    position_values = []
    dollar_gains = []
    percent_gains = []
    
    # Calculate metrics for each stock
    for i in range(len(symbols)):
        # Position value
        position_value = current_prices[i] * share_counts[i]
        position_values.append(position_value)
        
        # Dollar gain/loss
        cost_basis = purchase_prices[i] * share_counts[i]
        dollar_gain = position_value - cost_basis
        dollar_gains.append(dollar_gain)
        
        # Percentage gain/loss
        percent_gain = (dollar_gain / cost_basis) * 100
        percent_gains.append(percent_gain)
    
    # Calculate portfolio totals
    total_value = sum(position_values)
    total_cost = sum([purchase_prices[i] * share_counts[i] for i in range(len(symbols))])
    total_gain_dollars = sum(dollar_gains)
    total_gain_percent = (total_gain_dollars / total_cost) * 100
    
    return position_values, dollar_gains, percent_gains, (total_value, total_cost, total_gain_dollars, total_gain_percent)

def display_summary(symbols, purchase_prices, current_prices, share_counts, position_values, 
                   dollar_gains, percent_gains, portfolio_totals):
    """
    Display a comprehensive summary of the portfolio.
    
    Args:
        symbols (list): Stock symbols
        purchase_prices (list): Purchase prices for each stock
        current_prices (list): Current prices for each stock
        share_counts (list): Number of shares for each stock
        position_values (list): Current value of each position
        dollar_gains (list): Dollar gain/loss for each position
        percent_gains (list): Percentage gain/loss for each position
        portfolio_totals (tuple): Total portfolio metrics
    """
    total_value, total_cost, total_gain_dollars, total_gain_percent = portfolio_totals
    
    # Display individual stock performance
    print("\n" + "=" * 70)
    print(f"{'STOCK PORTFOLIO SUMMARY':^70}")
    print("=" * 70)
    print(f"{'Symbol':<10}{'Shares':<10}{'Buy Price':<12}{'Current':<12}{'Value':<15}{'Gain/Loss':<15}{'%':<8}")
    print("-" * 70)
    
    for i in range(len(symbols)):
        print(f"{symbols[i]:<10}{share_counts[i]:<10}${purchase_prices[i]:<11.2f}${current_prices[i]:<11.2f}${position_values[i]:<14.2f}${dollar_gains[i]:<14.2f}{percent_gains[i]:<8.2f}%")
    
    # Display portfolio totals
    print("-" * 70)
    print(f"{'TOTAL':<10}{'':<10}{'':<12}{'':<12}${total_value:<14.2f}${total_gain_dollars:<14.2f}{total_gain_percent:<8.2f}%")
    print("=" * 70)
    
    # Display summary analysis
    print("\n📊 PORTFOLIO ANALYSIS:")
    print("-" * 30)
    
    # Determine best and worst performing stocks
    best_stock_index = percent_gains.index(max(percent_gains))
    worst_stock_index = percent_gains.index(min(percent_gains))
    
    print(f"🔼 Best performer: {symbols[best_stock_index]} ({percent_gains[best_stock_index]:.2f}%)")
    print(f"🔽 Worst performer: {symbols[worst_stock_index]} ({percent_gains[worst_stock_index]:.2f}%)")
    
    # Determine overall portfolio status
    if total_gain_percent > 0:
        print(f"🟢 Overall portfolio is UP {total_gain_percent:.2f}% (${total_gain_dollars:.2f})")
    elif total_gain_percent < 0:
        print(f"🔴 Overall portfolio is DOWN {abs(total_gain_percent):.2f}% (${total_gain_dollars:.2f})")
    else:
        print("⚪ Overall portfolio is EVEN (no gain or loss)")

def main():
    """Main function to run the portfolio calculator."""
    clear_screen()
    display_welcome()
    
    # Collect information
    symbols, purchase_prices, current_prices, share_counts = collect_stock_info()
    
    # Calculate metrics
    position_values, dollar_gains, percent_gains, portfolio_totals = calculate_metrics(
        symbols, purchase_prices, current_prices, share_counts
    )
    
    # Display summary
    display_summary(
        symbols, purchase_prices, current_prices, share_counts,
        position_values, dollar_gains, percent_gains, portfolio_totals
    )
    
    # Closing message
    print("\nThank you for using the Stock Portfolio Summary Calculator!")
    print("For more advanced portfolio analysis techniques, check out:")
    print("📘 'Practical Python for Effective Algorithmic Trading'")
    print("🔗 https://www.amazon.com/dp/B0F3S8FQ7C")

if __name__ == "__main__":
    main()

# This project demonstrates basic Python concepts from Chapter 3 of
# "Practical Python for Effective Algorithmic Trading" by Kuldeep Singh Rathore.
# For more advanced algorithmic trading implementations and community support, visit:
# https://www.skool.com/the-quantitative-elite