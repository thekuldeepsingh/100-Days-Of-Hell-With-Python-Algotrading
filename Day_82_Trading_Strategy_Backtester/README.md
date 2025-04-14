# Trading Strategy Backtester

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![Plotly](https://img.shields.io/badge/Plotly-5.16.1-blue.svg)
![Status](https://img.shields.io/badge/Status-Active-green.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

A full-featured web application for backtesting moving average crossover trading strategies. Built with Python and Flask, this project demonstrates how to implement trading strategies using control flow concepts from Chapter 4 of [Practical Python for Effective Algorithmic Trading](https://www.amazon.com/dp/B0F3S8FQ7C).

## ✨ Features

- **Interactive Web Interface:** Modern, responsive design with Bootstrap 5
- **Strategy Customization:** Configure all aspects of your trading strategy
- **Real-time Visualization:** Interactive charts with Plotly
- **Comprehensive Analysis:** Detailed performance metrics and trade history
- **Educational Tool:** Perfect for learning algorithmic trading concepts

## 🔥 Demo

Try the application live on Replit: [Stock Strategy Backtester](https://replit.com/@rathorekuldeeps/Stock-Screener-System-)

## 📋 Prerequisites

- Python 3.7+
- Flask 2.3.3+
- NumPy 1.25.2+
- pandas 2.1.0+
- Plotly 5.16.1+

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/thekuldeepsingh/Stock-Screener-System-
   cd Stock-Screener-System-
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
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## 🔍 Usage

1. **Configure Strategy Parameters**
   - Set the number of days to simulate
   - Adjust price volatility and starting price
   - Choose between Simple and Exponential Moving Averages
   - Set short-term and long-term MA periods
   - Configure initial capital and stop-loss percentage

2. **Run the Backtest**
   - Click "Run Backtest" to execute the simulation
   - View the results in the interactive dashboard

3. **Analyze Performance**
   - Check key metrics like total return, win rate, and drawdown
   - Examine the trade history for detailed analysis
   - Visualize price movements and portfolio value over time

## 📊 Technical Implementation

The backtester is built on several core concepts from Chapter 4 of [Practical Python for Effective Algorithmic Trading](https://www.amazon.com/dp/B0F3S8FQ7C):

- **Conditional Statements:** Using if/elif/else structures to make trading decisions
- **Loops:** Using while loops to simulate day-by-day trading
- **Logical Operators:** Combining conditions to trigger buy/sell signals
- **Nested Control Structures:** Creating complex decision trees for trading logic

The web application extends these concepts with:

- **Flask Backend:** Provides API endpoints and serves web pages
- **Plotly Visualizations:** Creates interactive trading charts
- **Bootstrap Frontend:** Delivers a responsive, modern user interface

## 🤝 Community

Join [The Quantitative Elite](https://www.skool.com/the-quantitative-elite) community to:
- Share your implementations and improvements
- Get help with customization and advanced strategies
- Connect with other algorithmic traders
- Learn advanced Python trading techniques

Subscribe to our [YouTube Channel](https://www.youtube.com/@KuldeepSinghAlgo) for video tutorials and live coding sessions.

## 🔧 Extending the Project

The backtester can be extended in several ways:

1. **Add New Strategy Types**
   - Implement RSI, MACD, or Bollinger Bands strategies
   - Create custom indicator combinations

2. **Connect to Real Market Data**
   - Integrate with Yahoo Finance, Alpha Vantage, or other data providers
   - Test strategies on historical market data

3. **Implement Parameter Optimization**
   - Add grid search functionality to find optimal parameters
   - Include walk-forward testing to prevent overfitting

4. **Enhance Risk Management**
   - Add trailing stops
   - Implement position sizing based on volatility
   - Add portfolio-level risk controls

For more advanced techniques and a deeper understanding of algorithmic trading with Python, refer to [Practical Python for Effective Algorithmic Trading](https://www.amazon.com/dp/B0F3S8FQ7C).

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👏 Acknowledgments

- Based on concepts from [Practical Python for Effective Algorithmic Trading](https://www.amazon.com/dp/B0F3S8FQ7C)
- Trading strategy inspired by classic technical analysis techniques
- Web application designed to make backtesting accessible to all traders

---

Happy trading! 📈
