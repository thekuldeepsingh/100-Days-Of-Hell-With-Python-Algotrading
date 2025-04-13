"""
Enhanced Interactive Stock Screener System - Chapter 4 Project
From the book: Practical Python for Effective Algorithmic Trading
Available at: https://www.amazon.com/dp/B0F3S8FQ7C

This interactive stock screener categorizes stocks based on technical and fundamental 
criteria using concepts from Chapter 4.
"""

import time  # Standard library, no external dependencies

# ASCII Art Title (using only basic strings - Chapter 3 concept)
def display_title():
    print("\033[1;36m") # Cyan color
    print("""
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║                                                                       ║
    ║   ███████╗████████╗ ██████╗  ██████╗██╗  ██╗                         ║
    ║   ██╔════╝╚══██╔══╝██╔═══██╗██╔════╝██║ ██╔╝                         ║
    ║   ███████╗   ██║   ██║   ██║██║     █████╔╝                          ║
    ║   ╚════██║   ██║   ██║   ██║██║     ██╔═██╗                          ║
    ║   ███████║   ██║   ╚██████╔╝╚██████╗██║  ██╗                         ║
    ║   ╚══════╝   ╚═╝    ╚═════╝  ╚═════╝╚═╝  ╚═╝                         ║
    ║                                                                       ║
    ║   ███████╗ ██████╗██████╗ ███████╗███████╗███╗   ██╗███████╗██████╗  ║
    ║   ██╔════╝██╔════╝██╔══██╗██╔════╝██╔════╝████╗  ██║██╔════╝██╔══██╗ ║
    ║   ███████╗██║     ██████╔╝█████╗  █████╗  ██╔██╗ ██║█████╗  ██████╔╝ ║
    ║   ╚════██║██║     ██╔══██╗██╔══╝  ██╔══╝  ██║╚██╗██║██╔══╝  ██╔══██╗ ║
    ║   ███████║╚██████╗██║  ██║███████╗███████╗██║ ╚████║███████╗██║  ██║ ║
    ║   ╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ║
    ║                                                                       ║
    ╚═══════════════════════════════════════════════════════════════════════╝
    """)
    print("\033[0m") # Reset color
    print("\033[1;33m📊 Interactive Python Stock Screening System 📊\033[0m")
    print("\033[3;37mBased on Chapter 4 of 'Practical Python for Effective Algorithmic Trading'\033[0m")
    print()

# Loading animation (using simple string manipulation and loops - Chapters 3 & 4 concepts)
def display_loading_animation(text, duration=1.5):
    animation = "|/-\\"
    iterations = int(duration * 10)
    
    for i in range(iterations):
        idx = i % len(animation)
        print(f"\r\033[1;32m{animation[idx]} {text}...\033[0m", end="")
        time.sleep(0.1)
    print("\r" + " " * (len(text) + 10) + "\r", end="")

# Function to create a visual progress bar (using simple loops - Chapter 4 concept)
def display_progress_bar(progress, total, text="Processing", bar_length=30):
    filled_length = int(bar_length * progress // total)
    bar = '█' * filled_length + '░' * (bar_length - filled_length)
    percent = 100 * (progress / float(total))
    print(f"\r{text}: |{bar}| {percent:.1f}% Complete", end='')
    
    if progress == total:
        print()

# Function to display section headers with decorative elements
def display_section(title):
    print(f"\n\033[1;35m{'═' * 30} {title} {'═' * 30}\033[0m\n")

# Function to display a rating with visual indicators
def display_rating(rating, explanation):
    if "Strong Buy" in rating:
        color = "\033[1;32m"  # Green
        symbol = "🔥"
        stars = "★★★★★"
    elif "Moderate Buy" in rating:
        color = "\033[1;36m"  # Cyan
        symbol = "✅"
        stars = "★★★★☆"
    elif "Hold" in rating:
        color = "\033[1;33m"  # Yellow
        symbol = "⏹️"
        stars = "★★★☆☆"
    else:
        color = "\033[1;31m"  # Red
        symbol = "❌"
        stars = "★★☆☆☆"

    print(f"\n{color}{'═' * 70}")
    print(f"  RATING: {symbol} {rating} {symbol}  {stars}")
    print(f"{'═' * 70}\033[0m")
    
    for line in explanation:
        print(f"  {line}")

# Interactive menu function
def display_menu():
    print("\n\033[1;36m╔══════════════════════════════════════╗")
    print("║           SCREENING OPTIONS           ║")
    print("╚══════════════════════════════════════╝\033[0m")
    print("1. Screen All Stocks")
    print("2. Screen by Sector")
    print("3. View Screening Criteria")
    print("4. Exit")
    
    choice = ""
    while choice not in ["1", "2", "3", "4"]:
        choice = input("\n\033[1mEnter your choice (1-4): \033[0m")
    
    return choice

# Function to display criteria information
def display_criteria():
    display_section("SCREENING CRITERIA INFORMATION")
    
    print("\033[1;36m[TECHNICAL ANALYSIS]\033[0m")
    print("  • Price above both MAs (+2 points)")
    print("  • Price above 50-day MA only (+1 point)")
    print("  • Price below both MAs (-2 points)")
    print("  • Golden Cross: 50-day MA above 200-day MA (+1 point)")
    
    print("\n\033[1;36m[VALUE ANALYSIS]\033[0m")
    print("  • P/E Ratio < 15 (+2 points) - Very attractive valuation")
    print("  • P/E Ratio < 25 (+1 point) - Reasonable valuation")
    print("  • P/E Ratio > 40 (-1 point) - Expensive valuation")
    
    print("\n\033[1;36m[FINANCIAL HEALTH]\033[0m")
    print("  • Debt/Equity < 0.3 (+2 points) - Very low debt")
    print("  • Debt/Equity < 0.7 (+1 point) - Moderate debt")
    print("  • Debt/Equity > 1.5 (-2 points) - High debt burden")
    
    print("\n\033[1;36m[INCOME POTENTIAL]\033[0m")
    print("  • Dividend Yield > 4.0% (+2 points) - High income")
    print("  • Dividend Yield > 2.0% (+1 point) - Moderate income")
    
    print("\n\033[1;36m[OVERALL RATING]\033[0m")
    print("  • Strong Buy 🔥: Total Score ≥ 5")
    print("  • Moderate Buy ✅: Total Score ≥ 2")
    print("  • Hold ⏹️: Total Score ≥ -1")
    print("  • Sell ❌: Total Score < -1")
    
    input("\n\033[1mPress Enter to return to main menu...\033[0m")

# Create a list of dictionaries representing stocks with their attributes
stocks = [
    {
        "symbol": "AAPL",
        "current_price": 173.50,
        "ma_50": 168.30,
        "ma_200": 165.75,
        "pe_ratio": 28.5,
        "debt_equity": 1.2,
        "dividend_yield": 0.6,
        "sector": "Technology"
    },
    {
        "symbol": "MSFT",
        "current_price": 369.85,
        "ma_50": 358.20,
        "ma_200": 340.15,
        "pe_ratio": 33.8,
        "debt_equity": 0.4,
        "dividend_yield": 0.8,
        "sector": "Technology"
    },
    {
        "symbol": "JNJ",
        "current_price": 152.30,
        "ma_50": 156.40,
        "ma_200": 160.25,
        "pe_ratio": 15.2,
        "debt_equity": 0.5,
        "dividend_yield": 3.2,
        "sector": "Healthcare"
    },
    {
        "symbol": "JPM",
        "current_price": 178.20,
        "ma_50": 170.15,
        "ma_200": 155.40,
        "pe_ratio": 12.5,
        "debt_equity": 1.1,
        "dividend_yield": 2.4,
        "sector": "Financial"
    },
    {
        "symbol": "NFLX",
        "current_price": 604.75,
        "ma_50": 580.20,
        "ma_200": 520.35,
        "pe_ratio": 42.1,
        "debt_equity": 0.8,
        "dividend_yield": 0.0,
        "sector": "Technology"
    },
    {
        "symbol": "XOM",
        "current_price": 114.30,
        "ma_50": 118.60,
        "ma_200": 111.25,
        "pe_ratio": 9.2,
        "debt_equity": 0.2,
        "dividend_yield": 3.6,
        "sector": "Energy"
    },
    {
        "symbol": "WMT",
        "current_price": 59.80,
        "ma_50": 60.40,
        "ma_200": 55.75,
        "pe_ratio": 30.5,
        "debt_equity": 0.7,
        "dividend_yield": 1.5,
        "sector": "Retail"
    },
    {
        "symbol": "PFE",
        "current_price": 27.15,
        "ma_50": 29.30,
        "ma_200": 34.80,
        "pe_ratio": 7.4,
        "debt_equity": 0.6,
        "dividend_yield": 5.8,
        "sector": "Healthcare"
    }
]

# Main function to analyze stocks
def analyze_stocks(stock_list):
    # Initialize counters for each rating category
    strong_buy_count = 0
    moderate_buy_count = 0
    hold_count = 0
    sell_count = 0
    
    # Store results to display later
    results = []
    
    # Show loading animation
    display_loading_animation("Initializing stock analysis", 1)
    
    # Iterate through each stock and apply screening logic
    for i, stock in enumerate(stock_list):
        # Display progress
        display_progress_bar(i+1, len(stock_list), "Analyzing stocks")
        time.sleep(0.25)  # Simulate processing time
        
        # Extract values for easier reference
        symbol = stock["symbol"]
        current_price = stock["current_price"]
        ma_50 = stock["ma_50"]
        ma_200 = stock["ma_200"]
        pe_ratio = stock["pe_ratio"]
        debt_equity = stock["debt_equity"]
        dividend_yield = stock["dividend_yield"]
        sector = stock["sector"]
        
        # Initialize scores for different aspects
        technical_score = 0
        value_score = 0
        financial_health_score = 0
        income_score = 0
        
        # Technical analysis
        if current_price > ma_50 and current_price > ma_200:
            technical_score += 2  # Price above both moving averages
        elif current_price > ma_50:
            technical_score += 1  # Price above 50-day MA but below 200-day MA
        elif current_price < ma_50 and current_price < ma_200:
            technical_score -= 2  # Price below both moving averages
        
        # Check for golden cross (50-day MA crossing above 200-day MA)
        if ma_50 > ma_200:
            technical_score += 1
        
        # Value analysis
        if pe_ratio < 15:
            value_score += 2  # Very low P/E ratio
        elif pe_ratio < 25:
            value_score += 1  # Moderate P/E ratio
        elif pe_ratio > 40:
            value_score -= 1  # High P/E ratio
        
        # Financial health analysis
        if debt_equity < 0.3:
            financial_health_score += 2  # Very low debt
        elif debt_equity < 0.7:
            financial_health_score += 1  # Moderate debt
        elif debt_equity > 1.5:
            financial_health_score -= 2  # High debt
        
        # Income analysis (dividends)
        if dividend_yield > 4.0:
            income_score += 2  # High dividend yield
        elif dividend_yield > 2.0:
            income_score += 1  # Moderate dividend yield
        
        # Calculate total score
        total_score = technical_score + value_score + financial_health_score + income_score
        
        # Determine rating based on total score
        if total_score >= 5:
            rating = "Strong Buy"
            strong_buy_count += 1
        elif total_score >= 2:
            rating = "Moderate Buy"
            moderate_buy_count += 1
        elif total_score >= -1:
            rating = "Hold"
            hold_count += 1
        else:
            rating = "Sell"
            sell_count += 1
        
        # Prepare technical analysis details
        tech_details = []
        if current_price > ma_50:
            tech_details.append(f"  ▲ Price (${current_price}) above 50-day MA (${ma_50})")
        else:
            tech_details.append(f"  ▼ Price (${current_price}) below 50-day MA (${ma_50})")
            
        if current_price > ma_200:
            tech_details.append(f"  ▲ Price (${current_price}) above 200-day MA (${ma_200})")
        else:
            tech_details.append(f"  ▼ Price (${current_price}) below 200-day MA (${ma_200})")
        
        if ma_50 > ma_200:
            tech_details.append(f"  ✓ Golden Cross: 50-day MA above 200-day MA")
        else:
            tech_details.append(f"  ✗ Death Cross: 50-day MA below 200-day MA")
        
        # Prepare explanation based on rating
        if rating == "Strong Buy":
            explanation = [
                "This stock shows strong technical and fundamental indicators.",
                "It has a positive trend and solid financial metrics."
            ]
        elif rating == "Moderate Buy":
            explanation = [
                "This stock has more positive indicators than negative ones.",
                "There are some cautions, but overall outlook is positive."
            ]
        elif rating == "Hold":
            explanation = [
                "This stock shows mixed signals in technical and fundamental analysis.",
                "There's no clear advantage to buying or selling at current levels."
            ]
        else:
            explanation = [
                "This stock has multiple negative indicators that suggest caution.",
                "Technical trends and/or fundamentals are unfavorable."
            ]
            
        # Store the results for this stock
        results.append({
            "symbol": symbol,
            "sector": sector,
            "current_price": current_price,
            "rating": rating,
            "total_score": total_score,
            "technical_score": technical_score,
            "value_score": value_score,
            "financial_score": financial_health_score,
            "income_score": income_score,
            "tech_details": tech_details,
            "pe_ratio": pe_ratio,
            "debt_equity": debt_equity,
            "dividend_yield": dividend_yield,
            "explanation": explanation
        })
    
    return results, {
        "strong_buy": strong_buy_count,
        "moderate_buy": moderate_buy_count,
        "hold": hold_count,
        "sell": sell_count
    }

# Function to display an individual stock analysis
def display_stock_analysis(stock):
    symbol = stock["symbol"]
    sector = stock["sector"]
    current_price = stock["current_price"]
    rating = stock["rating"]
    tech_details = stock["tech_details"]
    
    print(f"\n\033[1;36m📊 Analysis for {symbol}\033[0m (\033[3m{sector}\033[0m) - Current Price: \033[1;33m${current_price}\033[0m")
    print("\033[1;37m" + "-" * 70 + "\033[0m")
    
    # Display technical analysis with colors
    print("\033[1;34mTechnical Analysis:\033[0m")
    for detail in tech_details:
        if "▲" in detail or "✓" in detail:
            print(f"\033[1;32m{detail}\033[0m")  # Green for positive indicators
        else:
            print(f"\033[1;31m{detail}\033[0m")  # Red for negative indicators
    
    # Display fundamental analysis with formatted values
    print("\n\033[1;34mFundamental Analysis:\033[0m")
    
    # P/E Ratio with color based on value
    pe_color = "\033[1;32m" if stock["pe_ratio"] < 15 else "\033[1;33m" if stock["pe_ratio"] < 25 else "\033[1;31m"
    print(f"  • P/E Ratio: {pe_color}{stock['pe_ratio']}\033[0m")
    
    # Debt-to-Equity with color based on value
    debt_color = "\033[1;32m" if stock["debt_equity"] < 0.3 else "\033[1;33m" if stock["debt_equity"] < 0.7 else "\033[1;31m"
    print(f"  • Debt-to-Equity: {debt_color}{stock['debt_equity']}\033[0m")
    
    # Dividend Yield with color based on value
    div_color = "\033[1;32m" if stock["dividend_yield"] > 2.0 else "\033[1;33m" if stock["dividend_yield"] > 0 else "\033[1;31m"
    print(f"  • Dividend Yield: {div_color}{stock['dividend_yield']}%\033[0m")
    
    # Show score breakdown with bar visualization
    print("\n\033[1;34mScore Breakdown:\033[0m")
    
    def score_bar(score, label, max_score=3):
        # Ensure score is an integer for display
        score_int = int(score)  # Convert to integer to fix the formatting issue
        
        bar_chars = 20
        mid_point = bar_chars // 2
        
        # Determine color based on score
        if score_int > 0:
            color = "\033[1;32m"  # Green for positive
            char = "█"
        elif score_int < 0:
            color = "\033[1;31m"  # Red for negative
            char = "█"
            score_int = abs(score_int)  # Use absolute value for display
        else:
            color = "\033[1;37m"  # White for zero
            char = "░"
            score_int = 0.5  # Small visual marker for zero
        
        # Calculate bar length based on score
        bar_length = int((score_int / max_score) * (bar_chars // 2))
        
        # Create the bar
        if score_int > 0:
            left = " " * mid_point
            right = color + char * bar_length + "\033[0m" + " " * (mid_point - bar_length)
        else:
            right = " " * mid_point
            left = " " * (mid_point - bar_length) + color + char * bar_length + "\033[0m"
        
        # Determine score text color
        score_color = "\033[1;32m" if score_int > 0 else "\033[1;31m" if score_int < 0 else "\033[1;37m"
        
        # Print the bar with label and score
        print(f"  {label.ljust(12)} |{left}|{right}| {score_color}{score_int:+}\033[0m")
    
    score_bar(stock["technical_score"], "Technical")
    score_bar(stock["value_score"], "Value")
    score_bar(stock["financial_score"], "Financial")
    score_bar(stock["income_score"], "Income")
    
    # Total score with visual indicator
    total_color = "\033[1;32m" if stock["total_score"] >= 2 else "\033[1;31m" if stock["total_score"] < 0 else "\033[1;33m"
    print(f"  {'Total'.ljust(12)} {total_color}{stock['total_score']:+}\033[0m")
    
    # Display the rating
    display_rating(rating, stock["explanation"])

# Function to display summary results
def display_summary(counts, results):
    display_section("SCREENING SUMMARY")
    
    # Calculate total
    total = sum(counts.values())
    
    # Display counts with visual bars
    categories = [
        ("Strong Buy 🔥", counts["strong_buy"], "\033[1;32m"),  # Green
        ("Moderate Buy ✅", counts["moderate_buy"], "\033[1;36m"),  # Cyan
        ("Hold ⏹️", counts["hold"], "\033[1;33m"),  # Yellow
        ("Sell ❌", counts["sell"], "\033[1;31m")  # Red
    ]
    
    for category, count, color in categories:
        if total > 0:
            percentage = (count / total) * 100
            bar_length = int((count / total) * 30)
        else:
            percentage = 0
            bar_length = 0
            
        bar = color + "█" * bar_length + "\033[0m" + "░" * (30 - bar_length)
        print(f"{category.ljust(15)} |{bar}| {count} ({percentage:.1f}%)")
    
    # Top performers by sector
    if total > 0:
        display_section("TOP PERFORMERS BY SECTOR")
        
        # Get sectors
        sectors = set(stock["sector"] for stock in results)
        
        for sector in sectors:
            # Filter stocks by sector
            sector_stocks = [stock for stock in results if stock["sector"] == sector]
            
            # Find best stock in sector
            best_stock = max(sector_stocks, key=lambda x: x["total_score"])
            
            # Display best stock in each sector
            rating_symbol = "🔥" if best_stock["rating"] == "Strong Buy" else "✅" if best_stock["rating"] == "Moderate Buy" else "⏹️" if best_stock["rating"] == "Hold" else "❌"
            score_color = "\033[1;32m" if best_stock["total_score"] > 0 else "\033[1;31m"
            
            print(f"\033[1;35m{sector}:\033[0m {best_stock['symbol']} (${best_stock['current_price']}) - {rating_symbol} {best_stock['rating']} - Score: {score_color}{best_stock['total_score']:+d}\033[0m")

# Main program
def main():
    display_title()
    
    while True:
        choice = display_menu()
        
        if choice == "1":  # Screen All Stocks
            display_section("SCREENING ALL STOCKS")
            results, counts = analyze_stocks(stocks)
            
            # Display individual stock analysis
            for stock in results:
                display_stock_analysis(stock)
                time.sleep(0.5)  # Pause between stocks for readability
            
            # Display summary
            display_summary(counts, results)
            
        elif choice == "2":  # Screen by Sector
            display_section("SCREEN BY SECTOR")
            
            # Get unique sectors
            sectors = sorted(set(stock["sector"] for stock in stocks))
            
            print("Available sectors:")
            for i, sector in enumerate(sectors, 1):
                print(f"{i}. {sector}")
            
            # Get sector choice
            sector_choice = ""
            while not sector_choice.isdigit() or int(sector_choice) < 1 or int(sector_choice) > len(sectors):
                sector_choice = input("\n\033[1mSelect a sector (number): \033[0m")
            
            selected_sector = sectors[int(sector_choice) - 1]
            
            # Filter stocks by sector
            sector_stocks = [stock for stock in stocks if stock["sector"] == selected_sector]
            
            display_section(f"SCREENING {selected_sector.upper()} SECTOR")
            
            # Analyze sector stocks
            results, counts = analyze_stocks(sector_stocks)
            
            # Display individual stock analysis
            for stock in results:
                display_stock_analysis(stock)
                time.sleep(0.5)  # Pause between stocks for readability
            
            # Display summary
            display_summary(counts, results)
            
        elif choice == "3":  # View Screening Criteria
            display_criteria()
            
        elif choice == "4":  # Exit
            display_loading_animation("Exiting", 1)
            print("\n\033[1;36mThank you for using the Interactive Stock Screener!\033[0m")
            print("\033[3mBased on concepts from 'Practical Python for Effective Algorithmic Trading'\033[0m")
            print("\033[3mVisit https://www.skool.com/the-quantitative-elite for more trading resources\033[0m")
            break
        
        if choice != "3":
            input("\n\033[1mPress Enter to return to main menu...\033[0m")

if __name__ == "__main__":
    main()