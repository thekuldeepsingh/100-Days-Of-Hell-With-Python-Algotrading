"""
Trading Strategy Backtester - Web Application
From the book: Practical Python for Effective Algorithmic Trading
Available at: https://www.amazon.com/dp/B0F3S8FQ7C

This web application implements a moving average crossover strategy backtester
as covered in Chapter 4, with a modern web interface.
"""

from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
import random
import math
import json
import plotly
import plotly.graph_objs as go
from datetime import datetime, timedelta
import plotly.express as px

app = Flask(__name__)

# Function to generate simulated stock price data
def generate_price_data(start_price=100, days=100, volatility=0.01, upward_drift=0.0001):
    """
    Generate simulated daily stock prices with random walk and slight upward drift.
    
    Args:
        start_price: Initial price of the stock
        days: Number of days to simulate
        volatility: Daily price volatility (standard deviation)
        upward_drift: Slight upward bias in price movement
        
    Returns:
        List of simulated daily prices
    """
    prices = [start_price]
    current_price = start_price
    
    for _ in range(days - 1):
        # Random price change with slight upward bias
        change_percent = random.normalvariate(upward_drift, volatility)
        current_price = current_price * (1 + change_percent)
        # Ensure price doesn't go below 1
        current_price = max(current_price, 1.0)
        prices.append(current_price)
    
    return prices

# Function to calculate simple moving average
def calculate_sma(prices, period):
    """
    Calculate the Simple Moving Average for a given period.
    
    Args:
        prices: List of price data
        period: Number of days to include in the moving average
        
    Returns:
        List of moving averages (with None values for the first period-1 days)
    """
    sma_values = [None] * (period - 1)
    
    for i in range(period - 1, len(prices)):
        # Calculate average of the last 'period' prices
        period_prices = prices[i - (period - 1):i + 1]
        average = sum(period_prices) / period
        sma_values.append(average)
    
    return sma_values

# Function to calculate exponential moving average
def calculate_ema(prices, period, smoothing=2):
    """
    Calculate the Exponential Moving Average for a given period.
    
    Args:
        prices: List of price data
        period: Number of days to include in the moving average
        smoothing: Smoothing factor (default 2)
        
    Returns:
        List of EMA values (with None values for the first period-1 days)
    """
    ema_values = [None] * (period - 1)
    
    # Calculate first EMA as SMA
    sma = sum(prices[:period]) / period
    ema_values.append(sma)
    
    # Calculate subsequent EMAs
    multiplier = smoothing / (period + 1)
    
    for i in range(period, len(prices)):
        ema = (prices[i] - ema_values[-1]) * multiplier + ema_values[-1]
        ema_values.append(ema)
    
    return ema_values

# Main backtesting function
def backtest_strategy(prices, short_period=10, long_period=30, initial_capital=10000, 
                     stop_loss_percent=5, use_ema=False, ma_function=None):
    """
    Backtest a moving average crossover strategy on historical price data.
    
    Args:
        prices: List of historical daily prices
        short_period: Period for short-term moving average
        long_period: Period for long-term moving average
        initial_capital: Starting capital amount
        stop_loss_percent: Percentage of entry price for stop loss
        use_ema: Whether to use EMA instead of SMA
        ma_function: Custom MA function if provided
        
    Returns:
        Dictionary containing performance metrics
    """
    # Calculate moving averages based on selected type
    if ma_function:
        # Use custom MA function if provided
        short_ma = ma_function(prices, short_period)
        long_ma = ma_function(prices, long_period)
    elif use_ema:
        short_ma = calculate_ema(prices, short_period)
        long_ma = calculate_ema(prices, long_period)
    else:
        short_ma = calculate_sma(prices, short_period)
        long_ma = calculate_sma(prices, long_period)
    
    # Initialize variables
    capital = initial_capital
    shares = 0
    in_position = False
    entry_price = 0
    entry_day = 0
    stop_loss_price = 0
    
    # Performance tracking
    trades = []
    portfolio_values = [initial_capital]
    positions = [0]  # 0 = no position, 1 = long position
    max_portfolio_value = initial_capital
    max_drawdown = 0
    drawdowns = [0]
    
    # We can only start trading after both MAs are established
    start_day = max(short_period, long_period) - 1
    current_day = start_day
    
    # Simulate day-by-day trading
    while current_day < len(prices) - 1:  # Leave room for the next day
        current_price = prices[current_day]
        next_day_price = prices[current_day + 1]  # For trade execution
        
        # Calculate current portfolio value
        portfolio_value = capital
        if in_position:
            portfolio_value += shares * current_price
        
        # Update maximum portfolio value and drawdown
        if portfolio_value > max_portfolio_value:
            max_portfolio_value = portfolio_value
        
        current_drawdown = (max_portfolio_value - portfolio_value) / max_portfolio_value * 100
        if current_drawdown > max_drawdown:
            max_drawdown = current_drawdown
        
        # Store portfolio value history
        portfolio_values.append(portfolio_value)
        drawdowns.append(current_drawdown)
        
        # Get moving average signals
        if current_day >= long_period - 1:  # Both MAs are available
            short_ma_current = short_ma[current_day]
            long_ma_current = long_ma[current_day]
            
            # If we have data for yesterday as well, check for crossovers
            if current_day > long_period - 1:
                short_ma_prev = short_ma[current_day - 1]
                long_ma_prev = long_ma[current_day - 1]
                
                # Check for buy signal: short MA crosses above long MA
                buy_signal = short_ma_prev <= long_ma_prev and short_ma_current > long_ma_current
                
                # Check for sell signal: short MA crosses below long MA
                sell_signal = short_ma_prev >= long_ma_prev and short_ma_current < long_ma_current
                
                # Execute buy signal if not already in a position
                if buy_signal and not in_position:
                    # Calculate how many shares we can buy
                    shares = math.floor(capital / next_day_price)
                    
                    if shares > 0:
                        entry_price = next_day_price
                        capital -= shares * entry_price
                        in_position = True
                        entry_day = current_day + 1
                        
                        # Set stop loss
                        stop_loss_price = entry_price * (1 - stop_loss_percent / 100)
                
                # Execute sell signal if in a position
                elif (sell_signal or next_day_price <= stop_loss_price) and in_position:
                    # Sell all shares
                    capital += shares * next_day_price
                    
                    # Record the trade
                    exit_day = current_day + 1
                    exit_price = next_day_price
                    profit_loss = (exit_price - entry_price) * shares
                    profit_loss_percent = (exit_price / entry_price - 1) * 100
                    trade_duration = exit_day - entry_day
                    
                    trade_info = {
                        "entry_day": entry_day,
                        "entry_price": entry_price,
                        "exit_day": exit_day,
                        "exit_price": exit_price,
                        "shares": shares,
                        "profit_loss": profit_loss,
                        "profit_loss_percent": profit_loss_percent,
                        "duration": trade_duration,
                        "exit_reason": "Stop Loss" if next_day_price <= stop_loss_price else "Sell Signal"
                    }
                    
                    trades.append(trade_info)
                    
                    # Reset position tracking
                    shares = 0
                    in_position = False
                    entry_price = 0
                    stop_loss_price = 0
        
        # Track position for plotting
        positions.append(1 if in_position else 0)
        
        # Move to next day
        current_day += 1
    
    # Calculate final portfolio value
    final_portfolio_value = capital
    if in_position:
        final_portfolio_value += shares * prices[-1]
    
    # Calculate performance metrics
    total_return = (final_portfolio_value / initial_capital - 1) * 100
    
    winning_trades = [t for t in trades if t["profit_loss"] > 0]
    win_rate = len(winning_trades) / len(trades) * 100 if trades else 0
    
    # Calculate average win and loss
    avg_win = sum([t["profit_loss"] for t in winning_trades]) / len(winning_trades) if winning_trades else 0
    losing_trades = [t for t in trades if t["profit_loss"] < 0]
    avg_loss = sum([t["profit_loss"] for t in losing_trades]) / len(losing_trades) if losing_trades else 0
    
    # Calculate profit factor
    gross_profit = sum([t["profit_loss"] for t in winning_trades]) if winning_trades else 0
    gross_loss = abs(sum([t["profit_loss"] for t in losing_trades])) if losing_trades else 0
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')
    
    # Calculate annualized return
    trading_days = len(prices)
    annual_trading_days = 252  # Standard trading days in a year
    years = trading_days / annual_trading_days
    annualized_return = ((final_portfolio_value / initial_capital) ** (1 / years) - 1) * 100 if years > 0 else 0
    
    # Compile all metrics
    metrics = {
        "initial_capital": initial_capital,
        "final_portfolio_value": final_portfolio_value,
        "total_return_percent": total_return,
        "annualized_return_percent": annualized_return,
        "total_trades": len(trades),
        "winning_trades": len(winning_trades),
        "losing_trades": len(trades) - len(winning_trades),
        "win_rate_percent": win_rate,
        "avg_win": avg_win,
        "avg_loss": avg_loss,
        "profit_factor": profit_factor,
        "max_drawdown_percent": max_drawdown,
        "trade_history": trades,
        "portfolio_history": portfolio_values,
        "positions": positions,
        "drawdowns": drawdowns
    }
    
    return metrics

# Create date range for plotly charts
def create_date_range(num_days):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=num_days)
    dates = [start_date + timedelta(days=i) for i in range(num_days)]
    return [date.strftime("%Y-%m-%d") for date in dates]

# Create plotly figure for price and moving averages
def create_price_chart(prices, short_ma, long_ma, trades=None, dates=None):
    if dates is None:
        dates = create_date_range(len(prices))
    
    # Create figure
    fig = go.Figure()
    
    # Add price line
    fig.add_trace(go.Scatter(
        x=dates,
        y=prices,
        mode='lines',
        name='Price',
        line=dict(color='#2E86C1', width=2)
    ))
    
    # Add moving averages
    if short_ma[0] is None:
        # Remove None values from the beginning
        short_ma_dates = dates[len([x for x in short_ma if x is None]):]
        short_ma = [x for x in short_ma if x is not None]
    else:
        short_ma_dates = dates
    
    if long_ma[0] is None:
        # Remove None values from the beginning
        long_ma_dates = dates[len([x for x in long_ma if x is None]):]
        long_ma = [x for x in long_ma if x is not None]
    else:
        long_ma_dates = dates
    
    fig.add_trace(go.Scatter(
        x=short_ma_dates,
        y=short_ma,
        mode='lines',
        name='Short MA',
        line=dict(color='#F39C12', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=long_ma_dates,
        y=long_ma,
        mode='lines',
        name='Long MA',
        line=dict(color='#C0392B', width=2)
    ))
    
    # Add buy/sell markers if trades are provided
    if trades:
        buy_days = [t['entry_day'] for t in trades]
        buy_prices = [prices[day] for day in buy_days]
        buy_dates = [dates[day] for day in buy_days]
        
        sell_days = [t['exit_day'] for t in trades]
        sell_prices = [prices[day] for day in sell_days]
        sell_dates = [dates[day] for day in sell_days]
        
        # Add buy markers
        fig.add_trace(go.Scatter(
            x=buy_dates,
            y=buy_prices,
            mode='markers',
            name='Buy',
            marker=dict(
                color='green',
                size=10,
                symbol='triangle-up',
                line=dict(width=2, color='darkgreen')
            )
        ))
        
        # Add sell markers
        fig.add_trace(go.Scatter(
            x=sell_dates,
            y=sell_prices,
            mode='markers',
            name='Sell',
            marker=dict(
                color='red',
                size=10,
                symbol='triangle-down',
                line=dict(width=2, color='darkred')
            )
        ))
    
    # Update layout
    fig.update_layout(
        title='Price Chart with Moving Averages',
        xaxis_title='Date',
        yaxis_title='Price',
        template='plotly_white',
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

# Create equity curve chart
def create_equity_chart(portfolio_values, initial_capital, dates=None):
    if dates is None:
        dates = create_date_range(len(portfolio_values))
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=portfolio_values,
        mode='lines',
        name='Portfolio Value',
        line=dict(color='#2E86C1', width=2)
    ))
    
    # Add horizontal line for initial capital
    fig.add_trace(go.Scatter(
        x=[dates[0], dates[-1]],
        y=[initial_capital, initial_capital],
        mode='lines',
        name='Initial Capital',
        line=dict(color='red', width=1, dash='dash')
    ))
    
    # Update layout
    fig.update_layout(
        title='Portfolio Equity Curve',
        xaxis_title='Date',
        yaxis_title='Portfolio Value ($)',
        template='plotly_white',
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

# Create drawdown chart
def create_drawdown_chart(drawdowns, dates=None):
    if dates is None:
        dates = create_date_range(len(drawdowns))
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=[-d for d in drawdowns],  # Negate for better visualization (downward)
        mode='lines',
        name='Drawdown',
        fill='tozeroy',
        line=dict(color='#E74C3C', width=2)
    ))
    
    # Update layout
    fig.update_layout(
        title='Portfolio Drawdown',
        xaxis_title='Date',
        yaxis_title='Drawdown (%)',
        template='plotly_white',
        hovermode='x unified',
        yaxis=dict(autorange="reversed")  # Invert y-axis for better visualization
    )
    
    return fig

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/backtest', methods=['POST'])
def run_backtest():
    # Get parameters from request
    data = request.get_json()
    
    # Parse parameters
    days = int(data.get('days', 100))
    start_price = float(data.get('start_price', 100))
    volatility = float(data.get('volatility', 0.015))
    short_period = int(data.get('short_period', 10))
    long_period = int(data.get('long_period', 30))
    initial_capital = float(data.get('initial_capital', 10000))
    stop_loss = float(data.get('stop_loss', 5))
    ma_type = data.get('ma_type', 'sma')  # 'sma' or 'ema'
    
    # Generate price data
    prices = generate_price_data(
        start_price=start_price,
        days=days,
        volatility=volatility
    )
    
    # Calculate MAs for charting
    if ma_type == 'ema':
        short_ma = calculate_ema(prices, short_period)
        long_ma = calculate_ema(prices, long_period)
        use_ema = True
    else:
        short_ma = calculate_sma(prices, short_period)
        long_ma = calculate_sma(prices, long_period)
        use_ema = False
    
    # Run backtest
    results = backtest_strategy(
        prices,
        short_period=short_period,
        long_period=long_period,
        initial_capital=initial_capital,
        stop_loss_percent=stop_loss,
        use_ema=use_ema
    )
    
    # Generate date range for charts
    dates = create_date_range(len(prices))
    
    # Create charts
    price_chart = create_price_chart(prices, short_ma, long_ma, results['trade_history'], dates)
    equity_chart = create_equity_chart(results['portfolio_history'], initial_capital, dates)
    drawdown_chart = create_drawdown_chart(results['drawdowns'], dates)
    
    # Convert charts to JSON
    price_chart_json = json.dumps(price_chart, cls=plotly.utils.PlotlyJSONEncoder)
    equity_chart_json = json.dumps(equity_chart, cls=plotly.utils.PlotlyJSONEncoder)
    drawdown_chart_json = json.dumps(drawdown_chart, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Format trades for display
    formatted_trades = []
    for trade in results['trade_history']:
        formatted_trade = {
            'entry_date': dates[trade['entry_day']],
            'entry_price': f"${trade['entry_price']:.2f}",
            'exit_date': dates[trade['exit_day']],
            'exit_price': f"${trade['exit_price']:.2f}",
            'shares': trade['shares'],
            'profit_loss': f"${trade['profit_loss']:.2f}",
            'profit_loss_percent': f"{trade['profit_loss_percent']:.2f}%",
            'profit_loss_class': 'positive' if trade['profit_loss'] > 0 else 'negative',
            'duration': f"{trade['duration']} days",
            'exit_reason': trade['exit_reason']
        }
        formatted_trades.append(formatted_trade)
    
    # Return results
    return jsonify({
        'metrics': {
            'initial_capital': f"${results['initial_capital']:,.2f}",
            'final_value': f"${results['final_portfolio_value']:,.2f}",
            'total_return': f"{results['total_return_percent']:.2f}%",
            'total_return_class': 'positive' if results['total_return_percent'] >= 0 else 'negative',
            'annualized_return': f"{results['annualized_return_percent']:.2f}%",
            'annualized_return_class': 'positive' if results['annualized_return_percent'] >= 0 else 'negative',
            'total_trades': results['total_trades'],
            'winning_trades': results['winning_trades'],
            'losing_trades': results['losing_trades'],
            'win_rate': f"{results['win_rate_percent']:.2f}%",
            'avg_win': f"${results['avg_win']:.2f}" if results['avg_win'] else "$0.00",
            'avg_loss': f"${results['avg_loss']:.2f}" if results['avg_loss'] else "$0.00",
            'profit_factor': f"{results['profit_factor']:.2f}" if results['profit_factor'] != float('inf') else "∞",
            'max_drawdown': f"{results['max_drawdown_percent']:.2f}%"
        },
        'trades': formatted_trades,
        'charts': {
            'price_chart': price_chart_json,
            'equity_chart': equity_chart_json,
            'drawdown_chart': drawdown_chart_json
        }
    })

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/docs')
def docs():
    return render_template('docs.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# Standard template for all HTML pages
@app.template_filter('currency')
def format_currency(value):
    if isinstance(value, str):
        return value
    return f"${value:,.2f}"

# Provide year for footer copyright
@app.context_processor
def inject_year():
    return {'current_year': datetime.now().year}

if __name__ == '__main__':
    app.run(debug=True)
