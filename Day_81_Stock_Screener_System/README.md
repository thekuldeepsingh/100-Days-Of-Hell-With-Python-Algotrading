# Stock Screener System - Interactive Python Trading Project

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![Status](https://img.shields.io/badge/Status-Active-green.svg)
![Beginner Friendly](https://img.shields.io/badge/Level-Beginner-brightgreen.svg)
![Algorithmic Trading](https://img.shields.io/badge/Domain-Algorithmic_Trading-orange.svg)

## 🚀 Transform Your Trading with Python

Discover how **Python control flow** can revolutionize your investment decisions with this engaging Stock Screener project from [Practical Python for Effective Algorithmic Trading](https://www.amazon.com/dp/B0F3S8FQ7C). This interactive tool analyzes stocks using both technical and fundamental metrics, helping you identify potential opportunities in seconds rather than hours of manual research.

> "The difference between amateur and professional traders isn't just their analysis but their tools. This stock screener demonstrates how even beginners can build professional-grade trading tools with just basic Python concepts." — Kuldeep Singh Rathore, Algorithmic Trading Expert

Join over Elite Network Of Algorithmic traders who have transformed their investment approach using the techniques discussed in the community. Get started today and gain the algorithmic edge used by quantitative funds!

Need personalized support? Join [The Quantitative Elite Community](https://www.skool.com/the-quantitative-elite) where thousands of algorithmic traders share implementations, optimization tips, and market insights daily.

## 🌟 Features

- **Visual Analysis Dashboard**: Color-coded ratings and interactive charts make stock assessment intuitive
- **Multi-Factor Evaluation**: Analyzes both technical indicators (price vs. moving averages) and fundamental metrics (P/E ratio, debt-to-equity, dividend yield)
- **Comprehensive Scoring System**: Quantifies each stock's strength with numerical scores across four dimensions
- **Rating Classification**: Categorizes stocks into four clear rating groups:
  - 🔥 Strong Buy
  - ✅ Moderate Buy
  - ⏹️ Hold
  - ❌ Sell
- **Sector-Based Filtering**: Focus your analysis on specific market sectors
- **Detailed Explanations**: Understand exactly why each stock received its rating
- **Performance Visualization**: View price trends, moving averages, and score breakdown charts

## 📋 Project Overview

This Stock Screener System implements a professional-grade stock filtering tool using only Python concepts from Chapter 4 of [Practical Python for Effective Algorithmic Trading](https://www.amazon.com/dp/B0F3S8FQ7C). 

The system evaluates stocks based on:

1. **Technical Analysis**
   - Price relationship to 50-day and 200-day moving averages
   - Golden Cross/Death Cross pattern detection

2. **Value Assessment**
   - P/E Ratio evaluation
   - Valuation categorization

3. **Financial Health**
   - Debt-to-Equity analysis
   - Balance sheet strength indication

4. **Income Potential**
   - Dividend yield assessment
   - Income generation capability

By combining these factors into a weighted scoring system, the screener provides actionable insights that would typically require multiple tools or platforms.

## 🛠️ Implementation Details

### Technical Components

- **Conditional Statements**: Uses if/elif/else constructs to evaluate multiple criteria
- **Nested Conditionals**: Implements complex decision trees for nuanced analysis
- **Loops**: Iterates through stock collections to process each security
- **Data Structures**: Organizes stock data in lists and dictionaries
- **Visual Formatting**: Implements color-coding and graphical elements for clarity

### Scoring System

The screener uses a point-based system to evaluate each stock:

| Factor | Criteria | Score |
|--------|----------|-------|
| **Technical** | Price > both MAs | +2 |
| | Price > 50-day MA only | +1 |
| | Price < both MAs | -2 |
| | Golden Cross present | +1 |
| **Value** | P/E < 15 | +2 |
| | P/E < 25 | +1 |
| | P/E > 40 | -1 |
| **Financial** | Debt/Equity < 0.3 | +2 |
| | Debt/Equity < 0.7 | +1 |
| | Debt/Equity > 1.5 | -2 |
| **Income** | Dividend > 4.0% | +2 |
| | Dividend > 2.0% | +1 |

The total score determines the final rating:
- **Strong Buy 🔥**: Score ≥ 5
- **Moderate Buy ✅**: Score ≥ 2
- **Hold ⏹️**: Score ≥ -1
- **Sell ❌**: Score < -1

## 🖥️ Installation and Usage

### Prerequisites

- Python 3.6 or higher
- Jupyter Notebook (for notebook version)
- Matplotlib and Pandas (only for notebook version with visualizations)

### Setup Instructions

1. **Clone or download this repository**:

git clone https://github.com/thekuldeepsingh/stock-screener-system.git

2. **Navigate to the project directory**:
cd stock-screener-system

3. **Run the script version**:
python stock_screener.py

4. **Or open the Jupyter Notebook version**:
jupyter notebook Stock_Screener_System.ipynb

## 📊 Example Output

### Command Line Version
🔍 STOCK SCREENER SYSTEM 🔍
Analyzing 8 stocks based on technical and fundamental criteria...
📊 Analysis for AAPL (Technology) - Current Price: $173.5
Technical Analysis:
▲ Price ($173.5) above 50-day MA ($168.3)
▲ Price ($173.5) above 200-day MA ($165.75)
✓ Golden Cross: 50-day MA above 200-day MA
Fundamental Analysis:
• P/E Ratio: 28.5
• Debt-to-Equity: 1.2
• Dividend Yield: 0.6%
Score Breakdown:
Technical     |          |██████████| +3
Value         |          |██        | +1
Financial     |          |          | 0
Income        |          |          | 0
Total                                 +4
═══════════════════════════════════════════════════════════════════
RATING: ✅ Moderate Buy ✅  ★★★★☆
═══════════════════════════════════════════════════════════════════
This stock has more positive indicators than negative ones.
There are some cautions, but overall outlook is positive.

### Jupyter Notebook Version
![Stock Screener Dashboard](https://i.imgur.com/placeholder-image.png)
*Note: Replace with actual screenshot of your notebook output when available*

## 📚 Learning Path

This project is part of a structured learning path for algorithmic trading:

1. **Chapter 3**: Understanding variables and data structures
2. **Chapter 4**: Implementing control flow (this project)
3. **Chapter 5**: Working with more complex data structures
4. **Chapters 7-8**: Fetching and analyzing financial data
5. **Chapters 10-11**: Building complete trading strategies

Follow the complete guide in [Practical Python for Effective Algorithmic Trading](https://www.amazon.com/dp/B0F3S8FQ7C) to build increasingly sophisticated trading tools.

## 🌐 Community and Support

Join [The Quantitative Elite Community](https://www.skool.com/the-quantitative-elite) to:
- Share your implementation of this screener
- Learn advanced customizations from expert traders
- Access additional trading projects and resources
- Connect with fellow algorithmic trading enthusiasts
- Watch tutorial videos from Kuldeep Singh Rathore on implementing these concepts

## 🚀 Extending Your Screener

Take your stock screener to the next level with these enhancements:

1. **Connect to Real-Time Data**: Replace static values with live market data
2. **Add More Technical Indicators**: Incorporate RSI, MACD, and other advanced indicators
3. **Create a Web Dashboard**: Build a browser-based interface for your screener
4. **Implement Alerts**: Add notification capabilities for rating changes
5. **Custom Scoring**: Adjust the weights and criteria to match your trading style

For implementation guidance on these enhancements, refer to later chapters in the book or ask in our community!

## 📺 Related Resources

- [Kuldeep Singh Rathore YouTube Channel](https://www.youtube.com/@KuldeepSinghAlgo) - Video tutorials on algorithmic trading
- [FreqTrade & FreqAI Implementation Guides](https://www.skool.com/the-quantitative-elite) - For more advanced trading systems
- [Python for Algorithmic Trading Documentation](https://www.amazon.com/dp/B0F3S8FQ7C) - Comprehensive guide for beginners to advanced traders



## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

*Developed based on concepts from [Practical Python for Effective Algorithmic Trading](https://www.amazon.com/dp/B0F3S8FQ7C). For more trading projects and algorithmic strategies, join [The Quantitative Elite Community](https://www.skool.com/the-quantitative-elite).*

*Keywords: algorithmic trading, Python for finance, quantitative trading, stock screener, technical analysis, fundamental analysis, trading algorithms, Python control flow, investment analysis, beginner Python projects*