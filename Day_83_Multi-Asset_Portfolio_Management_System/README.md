# Multi-Asset Portfolio Management System

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![Plotly](https://img.shields.io/badge/Plotly-5.16.1-blue.svg)
![Status](https://img.shields.io/badge/Status-Active-green.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

A comprehensive web application for managing and analyzing multi-asset investment portfolios. Built with Python and Flask, this project demonstrates how to use different data structures to organize financial data as covered in Chapter 5 of [Practical Python for Effective Algorithmic Trading](https://www.amazon.com/dp/B0F3S8FQ7C).

## ✨ Features

- **Beautiful Dashboard**: Modern, responsive design with Bootstrap 5
- **Multi-Asset Support**: Track stocks, ETFs, bonds and other asset classes
- **Portfolio Analysis**: View allocation by asset class and sector with interactive charts
- **Performance Metrics**: Identify best/worst performers and positions exceeding thresholds
- **Watchlist Management**: Find complementary securities to improve diversification
- **Rebalancing Suggestions**: Get actionable recommendations to maintain target allocations

## 🔥 Demo

Try the application live on Replit: [Multi-Asset Portfolio Management System](https://replit.com/@rathorekuldeeps/Stock-Screener-System-)

## 📋 Prerequisites

- Python 3.7+
- Flask 2.3.3+
- NumPy 1.25.2+
- pandas 2.1.0+
- Plotly 5.16.1+

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/thekuldeepsingh/Multi_Asset_Portfolio_Management_System.git
   cd Multi_Asset_Portfolio_Management_System

   ```

2. **Create and activate a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5001`

## 🔍 Usage

1. **Dashboard**
   - View portfolio summary with key metrics
   - Analyze asset allocation and sector diversification
   - Track performance with interactive charts

2. **Portfolio Management**
   - See detailed information on all holdings
   - Identify best and worst performing assets
   - Get rebalancing suggestions based on target allocations

3. **Watchlist Analysis**
   - Manage potential investments
   - Find complementary securities for better diversification
   - Compare securities in similar sectors

## 📊 Technical Implementation

The system is built on several core concepts from Chapter 5 of [Practical Python for Effective Algorithmic Trading](https://www.amazon.com/dp/B0F3S8FQ7C):

- **Dictionaries**: Nested dictionaries for storing portfolio and security data
- **Lists**: For tracking purchase history and sorted performance metrics
- **Tuples**: For representing immutable data like purchase records
- **Sets**: For efficient lookups and finding relationships between securities

The web application extends these concepts with:

- **Flask Backend**: Provides routes and handles data processing
- **Plotly Visualizations**: Creates interactive financial charts
- **Bootstrap Frontend**: Delivers a responsive, modern user interface

## 🤝 Community

Join [The Quantitative Elite](https://www.skool.com/the-quantitative-elite) community to:
- Share your implementations and improvements
- Get help with customization and advanced portfolio strategies
- Connect with other algorithmic traders
- Learn advanced Python trading techniques

Subscribe to our [YouTube Channel](https://www.youtube.com/@KuldeepSinghAlgo) for video tutorials and live coding sessions.

## 🔧 Extending the Project

The portfolio management system can be extended in several ways:

1. **Connect to Real Market Data**
   - Integrate with Yahoo Finance, Alpha Vantage, or other data providers
   - Auto-update prices and portfolio metrics

2. **Add Database Storage**
   - Implement SQL or NoSQL database for persistent data
   - Track historical portfolio performance

3. **Implement Authentication**
   - Add user accounts for personal portfolios
   - Enable sharing and collaboration features

4. **Enhanced Analytics**
   - Calculate risk metrics (alpha, beta, Sharpe ratio)
   - Implement portfolio optimization algorithms
   - Add tax-lot tracking and tax-loss harvesting

For more advanced techniques and a deeper understanding of financial data structures with Python, refer to [Practical Python for Effective Algorithmic Trading](https://www.amazon.com/dp/B0F3S8FQ7C).

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👏 Acknowledgments

- Based on concepts from [Practical Python for Effective Algorithmic Trading](https://www.amazon.com/dp/B0F3S8FQ7C)
- Portfolio management strategies inspired by modern finance theory
- Web application designed to make portfolio analysis accessible to all investors

---

Happy investing and coding! 📈
