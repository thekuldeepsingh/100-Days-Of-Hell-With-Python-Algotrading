"""
Stock Portfolio Summary Calculator
From the book: Practical Python for Effective Algorithmic Trading
Available at: https://www.amazon.com/dp/B0F3S8FQ7C

This simple program helps you track your stock portfolio and calculate performance metrics.
Perfect for beginners learning Python for algorithmic trading!
"""

# Initialize empty lists to store stock information
symbols = []
purchase_prices = []
current_prices = []
share_counts = []

print("===== STOCK PORTFOLIO SUMMARY CALCULATOR =====")
print("Enter details for your stock positions below:")

# Collect information for 3 stocks
for i in range(3):
    print(f"\nStock #{i+1}:")
    symbol = input("Enter stock symbol (e.g., AAPL): ").upper()
    
    # Handle potential input errors with simple validation
    while True:
        try:
            purchase_price = float(input("Enter purchase price per share: $"))
            if purchase_price <= 0:
                print("Price must be positive! Please try again.")
                continue
            break
        except ValueError:
            print("Please enter a valid number!")
    
    while True:
        try:
            current_price = float(input("Enter current price per share: $"))
            if current_price <= 0:
                print("Price must be positive! Please try again.")
                continue
            break
        except ValueError:
            print("Please enter a valid number!")
    
    while True:
        try:
            shares = int(input("Enter number of shares: "))
            if shares <= 0:
                print("Shares must be a positive number! Please try again.")
                continue
            break
        except ValueError:
            print("Please enter a valid whole number!")
    
    # Add the information to our lists
    symbols.append(symbol)
    purchase_prices.append(purchase_price)
    current_prices.append(current_price)
    share_counts.append(shares)

# Initialize variables to track portfolio totals
total_current_value = 0
total_purchase_value = 0

# Display individual stock performance
print("\n" + "="*60)
print("📊 STOCK PORTFOLIO SUMMARY 📊")
print("="*60)
print("\n📈 INDIVIDUAL STOCK PERFORMANCE:")
print("-"*60)
print(f"{'SYMBOL':<8} {'SHARES':<8} {'PURCHASE':<10} {'CURRENT':<10} {'VALUE':<12} {'P/L($)':<12} {'P/L(%)':<10}")
print("-"*60)

for i in range(len(symbols)):
    # Calculate metrics for each stock
    purchase_value = purchase_prices[i] * share_counts[i]
    current_value = current_prices[i] * share_counts[i]
    profit_loss = current_value - purchase_value
    profit_loss_percent = (profit_loss / purchase_value) * 100
    
    # Update portfolio totals
    total_purchase_value += purchase_value
    total_current_value += current_value
    
    # Display stock information and metrics with color indicators
    profit_indicator = "🟢" if profit_loss >= 0 else "🔴"
    
    print(f"{symbols[i]:<8} {share_counts[i]:<8} ${purchase_prices[i]:<9.2f} ${current_prices[i]:<9.2f} ${current_value:<11.2f} ${profit_loss:<11.2f} {profit_loss_percent:<8.2f}% {profit_indicator}")

# Calculate overall portfolio metrics
total_profit_loss = total_current_value - total_purchase_value
overall_profit_loss_percent = (total_profit_loss / total_purchase_value) * 100

# Display portfolio summary
print("\n💼 PORTFOLIO SUMMARY:")
print("-"*60)
print(f"Total Investment: ${total_purchase_value:.2f}")
print(f"Current Portfolio Value: ${total_current_value:.2f}")

# Add emoji based on performance
if total_profit_loss > 0:
    performance_indicator = "🟢 PROFIT"
elif total_profit_loss < 0:
    performance_indicator = "🔴 LOSS"
else:
    performance_indicator = "⚪ BREAK EVEN"

print(f"Overall Profit/Loss: ${total_profit_loss:.2f} ({overall_profit_loss_percent:.2f}%) {performance_indicator}")

# Determine overall performance message
if total_profit_loss > 0:
    print("\n🎉 Your portfolio is performing well with positive returns!")
elif total_profit_loss < 0:
    print("\n📉 Your portfolio is currently at a loss.")
else:
    print("\n⚖️ Your portfolio is breaking even.")

print("\nThanks for using this calculator from Practical Python for Effective Algorithmic Trading!")
print("➡️ For more advanced portfolio tools: https://www.amazon.com/dp/B0F3S8FQ7C")
print("➡️ Join our trading community: https://www.skool.com/the-quantitative-elite")

# Keep the console window open until the user presses a key
input("\nPress Enter to exit...")