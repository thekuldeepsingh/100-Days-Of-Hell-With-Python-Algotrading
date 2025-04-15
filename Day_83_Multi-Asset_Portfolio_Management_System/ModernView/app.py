"""
Multi-Asset Portfolio Management System - Web Application
From the book: Practical Python for Effective Algorithmic Trading
Available at: https://www.amazon.com/dp/B0F3S8FQ7C

This web application implements a comprehensive portfolio management system
as covered in Chapter 5, with a modern web interface.
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd
import numpy as np
import json
import plotly
import plotly.graph_objs as go
import plotly.express as px
from datetime import datetime, timedelta
import random

app = Flask(__name__)

# Create a sample portfolio with different asset classes and sectors
def create_sample_portfolio():
    """Create a sample portfolio with different asset classes and sectors"""
    today = datetime.today()
    
    portfolio = {
        "AAPL": {
            "ticker": "AAPL",
            "name": "Apple Inc.",
            "purchase_price": 150.75,
            "current_price": 173.50,
            "quantity": 50,
            "purchase_date": (today - timedelta(days=365)).strftime("%Y-%m-%d"),
            "asset_class": "Stocks",
            "sector": "Technology",
            "purchase_history": [
                ((today - timedelta(days=365)).strftime("%Y-%m-%d"), 25, 145.50),
                ((today - timedelta(days=180)).strftime("%Y-%m-%d"), 25, 156.00)
            ]
        },
        "MSFT": {
            "ticker": "MSFT",
            "name": "Microsoft Corporation",
            "purchase_price": 245.30,
            "current_price": 265.80,
            "quantity": 30,
            "purchase_date": (today - timedelta(days=300)).strftime("%Y-%m-%d"),
            "asset_class": "Stocks",
            "sector": "Technology",
            "purchase_history": [
                ((today - timedelta(days=300)).strftime("%Y-%m-%d"), 30, 245.30)
            ]
        },
        "JNJ": {
            "ticker": "JNJ",
            "name": "Johnson & Johnson",
            "purchase_price": 165.20,
            "current_price": 152.75,
            "quantity": 40,
            "purchase_date": (today - timedelta(days=400)).strftime("%Y-%m-%d"),
            "asset_class": "Stocks",
            "sector": "Healthcare",
            "purchase_history": [
                ((today - timedelta(days=400)).strftime("%Y-%m-%d"), 40, 165.20)
            ]
        },
        "VTI": {
            "ticker": "VTI",
            "name": "Vanguard Total Stock Market ETF",
            "purchase_price": 220.15,
            "current_price": 242.30,
            "quantity": 35,
            "purchase_date": (today - timedelta(days=500)).strftime("%Y-%m-%d"),
            "asset_class": "ETFs",
            "sector": "Diversified",
            "purchase_history": [
                ((today - timedelta(days=500)).strftime("%Y-%m-%d"), 35, 220.15)
            ]
        },
        "BND": {
            "ticker": "BND",
            "name": "Vanguard Total Bond Market ETF",
            "purchase_price": 82.40,
            "current_price": 78.65,
            "quantity": 100,
            "purchase_date": (today - timedelta(days=450)).strftime("%Y-%m-%d"),
            "asset_class": "Bonds",
            "sector": "Fixed Income",
            "purchase_history": [
                ((today - timedelta(days=450)).strftime("%Y-%m-%d"), 100, 82.40)
            ]
        },
        "XLE": {
            "ticker": "XLE",
            "name": "Energy Select Sector SPDR Fund",
            "purchase_price": 68.25,
            "current_price": 75.40,
            "quantity": 60,
            "purchase_date": (today - timedelta(days=250)).strftime("%Y-%m-%d"),
            "asset_class": "ETFs",
            "sector": "Energy",
            "purchase_history": [
                ((today - timedelta(days=250)).strftime("%Y-%m-%d"), 60, 68.25)
            ]
        },
        "TLT": {
            "ticker": "TLT",
            "name": "iShares 20+ Year Treasury Bond ETF",
            "purchase_price": 120.50,
            "current_price": 105.80,
            "quantity": 45,
            "purchase_date": (today - timedelta(days=350)).strftime("%Y-%m-%d"),
            "asset_class": "Bonds",
            "sector": "Government",
            "purchase_history": [
                ((today - timedelta(days=350)).strftime("%Y-%m-%d"), 45, 120.50)
            ]
        },
        "AMZN": {
            "ticker": "AMZN",
            "name": "Amazon.com Inc.",
            "purchase_price": 3250.00,
            "current_price": 3380.50,
            "quantity": 5,
            "purchase_date": (today - timedelta(days=280)).strftime("%Y-%m-%d"),
            "asset_class": "Stocks",
            "sector": "Technology",
            "purchase_history": [
                ((today - timedelta(days=280)).strftime("%Y-%m-%d"), 5, 3250.00)
            ]
        }
    }
    
    return portfolio

# Create a sample watchlist
def create_sample_watchlist():
    """Create a sample watchlist of potential securities"""
    watchlist = {
        "NVDA": {
            "ticker": "NVDA",
            "name": "NVIDIA Corporation",
            "current_price": 450.25,
            "asset_class": "Stocks",
            "sector": "Technology",
            "description": "Manufacturer of graphics processing units (GPUs)"
        },
        "PFE": {
            "ticker": "PFE",
            "name": "Pfizer Inc.",
            "current_price": 42.15,
            "asset_class": "Stocks",
            "sector": "Healthcare",
            "description": "Global pharmaceutical company"
        },
        "GLD": {
            "ticker": "GLD",
            "name": "SPDR Gold Shares",
            "current_price": 182.40,
            "asset_class": "ETFs",
            "sector": "Commodities",
            "description": "ETF tracking the price of gold bullion"
        },
        "MCD": {
            "ticker": "MCD",
            "name": "McDonald's Corporation",
            "current_price": 270.35,
            "asset_class": "Stocks",
            "sector": "Consumer Cyclical",
            "description": "Global fast food restaurant chain"
        },
        "VCIT": {
            "ticker": "VCIT",
            "name": "Vanguard Intermediate-Term Corporate Bond ETF",
            "current_price": 88.75,
            "asset_class": "Bonds",
            "sector": "Corporate",
            "description": "ETF of intermediate-term corporate bonds"
        },
        "DIS": {
            "ticker": "DIS",
            "name": "The Walt Disney Company",
            "current_price": 185.25,
            "asset_class": "Stocks",
            "sector": "Communication",
            "description": "Media and entertainment conglomerate"
        }
    }
    
    return watchlist

# Function to calculate total portfolio value
def calculate_total_value(portfolio):
    """Calculate the total value of the portfolio"""
    return sum(security["current_price"] * security["quantity"] for security in portfolio.values())

# Calculate allocation by asset class
def calculate_asset_class_allocation(portfolio):
    """Calculate the allocation percentages by asset class"""
    asset_class_values = {}
    total_value = calculate_total_value(portfolio)
    
    for ticker, security in portfolio.items():
        asset_class = security["asset_class"]
        security_value = security["current_price"] * security["quantity"]
        
        asset_class_values[asset_class] = asset_class_values.get(asset_class, 0) + security_value
    
    asset_class_allocation = {asset_class: (value / total_value) * 100 
                             for asset_class, value in asset_class_values.items()}
    
    return asset_class_allocation

# Calculate allocation by sector
def calculate_sector_allocation(portfolio):
    """Calculate the allocation percentages by sector"""
    sector_values = {}
    total_value = calculate_total_value(portfolio)
    
    for ticker, security in portfolio.items():
        sector = security["sector"]
        security_value = security["current_price"] * security["quantity"]
        
        sector_values[sector] = sector_values.get(sector, 0) + security_value
    
    sector_allocation = {sector: (value / total_value) * 100 
                        for sector, value in sector_values.items()}
    
    return sector_allocation

# Identify best and worst performing securities
def identify_best_worst_performers(portfolio):
    """Identify the best and worst performing securities"""
    performance_data = []
    
    for ticker, security in portfolio.items():
        purchase_price = security["purchase_price"]
        current_price = security["current_price"]
        percent_change = ((current_price - purchase_price) / purchase_price) * 100
        
        performance_data.append({
            "ticker": ticker,
            "name": security["name"],
            "percent_change": percent_change,
            "absolute_change": current_price - purchase_price
        })
    
    # Sort by performance
    sorted_data = sorted(performance_data, key=lambda x: x["percent_change"], reverse=True)
    
    # Get best and worst 3
    best_performers = sorted_data[:3]
    worst_performers = sorted_data[-3:]
    
    return best_performers, worst_performers

# Generate threshold report
def generate_threshold_report(portfolio, threshold=5.0):
    """Generate a report of positions exceeding a threshold percentage change"""
    positions_up = []
    positions_down = []
    
    for ticker, security in portfolio.items():
        purchase_price = security["purchase_price"]
        current_price = security["current_price"]
        percent_change = ((current_price - purchase_price) / purchase_price) * 100
        
        if percent_change >= threshold:
            positions_up.append({
                "ticker": ticker,
                "name": security["name"],
                "percent_change": percent_change,
                "current_value": current_price * security["quantity"]
            })
        elif percent_change <= -threshold:
            positions_down.append({
                "ticker": ticker,
                "name": security["name"],
                "percent_change": percent_change,
                "current_value": current_price * security["quantity"]
            })
    
    # Sort by percentage change
    positions_up = sorted(positions_up, key=lambda x: x["percent_change"], reverse=True)
    positions_down = sorted(positions_down, key=lambda x: x["percent_change"])
    
    return positions_up, positions_down

# Find complementary securities from watchlist
def find_complementary_securities(portfolio, watchlist):
    """Find securities in watchlist that would complement the portfolio"""
    portfolio_sectors = {security["sector"] for security in portfolio.values()}
    
    complementary_securities = []
    for ticker, security in watchlist.items():
        if security["sector"] not in portfolio_sectors:
            complementary_securities.append({
                "ticker": ticker,
                "name": security["name"],
                "asset_class": security["asset_class"],
                "sector": security["sector"],
                "current_price": security["current_price"],
                "description": security.get("description", "")
            })
    
    return complementary_securities

# Find similar sector securities from watchlist
def find_similar_sector_securities(portfolio, watchlist):
    """Find securities in watchlist that match portfolio sectors"""
    portfolio_sectors = {security["sector"] for security in portfolio.values()}
    
    sector_matches = {sector: [] for sector in portfolio_sectors}
    
    for ticker, security in watchlist.items():
        if security["sector"] in portfolio_sectors:
            sector_matches[security["sector"]].append({
                "ticker": ticker,
                "name": security["name"],
                "asset_class": security["asset_class"],
                "current_price": security["current_price"],
                "description": security.get("description", "")
            })
    
    # Remove empty sectors
    sector_matches = {k: v for k, v in sector_matches.items() if v}
    
    return sector_matches

# Get rebalancing suggestions
def suggest_rebalancing(portfolio, target_allocation):
    """Suggest portfolio rebalancing based on target allocations"""
    current_allocation = calculate_asset_class_allocation(portfolio)
    total_value = calculate_total_value(portfolio)
    
    rebalancing_suggestions = {}
    
    for asset_class, target_percent in target_allocation.items():
        current_percent = current_allocation.get(asset_class, 0)
        difference = current_percent - target_percent
        
        if abs(difference) >= 3:  # Only suggest rebalancing if difference is significant
            target_value = (target_percent / 100) * total_value
            current_value = (current_percent / 100) * total_value
            value_difference = current_value - target_value
            
            rebalancing_suggestions[asset_class] = {
                "current_allocation": current_percent,
                "target_allocation": target_percent,
                "difference": difference,
                "action": "Reduce" if difference > 0 else "Increase",
                "amount": abs(value_difference)
            }
    
    return rebalancing_suggestions

# Generate performance history data (simulated)
def generate_performance_history(portfolio, days=90):
    """Generate simulated historical performance data"""
    end_date = datetime.today()
    start_date = end_date - timedelta(days=days)
    
    dates = [(start_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days)]
    
    # Calculate current total value
    current_value = calculate_total_value(portfolio)
    
    # Generate random historical values with an upward trend
    np.random.seed(42)  # For reproducibility
    daily_changes = np.random.normal(0.0005, 0.01, days)  # Slight positive drift
    
    values = [current_value]
    for i in range(days-1, 0, -1):
        # Work backwards from current value
        values.insert(0, values[0] / (1 + daily_changes[i]))
    
    return list(zip(dates, values))

# Create visualizations for the portfolio
def create_portfolio_visualizations(portfolio):
    """Create portfolio visualization charts"""
    # Asset Allocation Chart
    asset_allocation = calculate_asset_class_allocation(portfolio)
    
    asset_fig = go.Figure(data=[go.Pie(
        labels=list(asset_allocation.keys()),
        values=list(asset_allocation.values()),
        hole=.4,
        marker=dict(colors=['#3366CC', '#DC3912', '#FF9900', '#109618', '#990099'])
    )])
    
    asset_fig.update_layout(
        title="Asset Class Allocation",
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    # Sector Allocation Chart
    sector_allocation = calculate_sector_allocation(portfolio)
    
    sector_fig = go.Figure(data=[go.Pie(
        labels=list(sector_allocation.keys()),
        values=list(sector_allocation.values()),
        hole=.4,
        marker=dict(colors=['#3366CC', '#DC3912', '#FF9900', '#109618', '#990099', '#3B3EAC', '#0099C6', '#DD4477', '#66AA00', '#B82E2E'])
    )])
    
    sector_fig.update_layout(
        title="Sector Allocation",
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    # Performance History Chart
    history_data = generate_performance_history(portfolio)
    
    history_fig = go.Figure()
    
    history_fig.add_trace(go.Scatter(
        x=[date for date, _ in history_data],
        y=[value for _, value in history_data],
        mode='lines',
        name='Portfolio Value',
        line=dict(color='#3366CC', width=2)
    ))
    
    history_fig.update_layout(
        title="Portfolio Performance (90 Days)",
        xaxis_title="Date",
        yaxis_title="Value ($)",
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    # Individual Holdings Chart
    holdings = []
    for ticker, security in portfolio.items():
        holdings.append({
            'ticker': ticker,
            'name': security['name'],
            'value': security['current_price'] * security['quantity']
        })
    
    # Sort by value
    holdings = sorted(holdings, key=lambda x: x['value'], reverse=True)
    
    holdings_fig = go.Figure(data=[
        go.Bar(
            x=[h['ticker'] for h in holdings],
            y=[h['value'] for h in holdings],
            marker_color=['#3366CC', '#DC3912', '#FF9900', '#109618', '#990099', '#3B3EAC', '#0099C6', '#DD4477']
        )
    ])
    
    holdings_fig.update_layout(
        title="Holdings by Value",
        xaxis_title="Security",
        yaxis_title="Value ($)",
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return {
        'asset_allocation': json.dumps(asset_fig, cls=plotly.utils.PlotlyJSONEncoder),
        'sector_allocation': json.dumps(sector_fig, cls=plotly.utils.PlotlyJSONEncoder),
        'performance_history': json.dumps(history_fig, cls=plotly.utils.PlotlyJSONEncoder),
        'holdings_chart': json.dumps(holdings_fig, cls=plotly.utils.PlotlyJSONEncoder)
    }

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/portfolio-dashboard')
def portfolio_dashboard():
    # Get portfolio data
    portfolio = create_sample_portfolio()
    watchlist = create_sample_watchlist()
    
    # Calculate portfolio metrics
    total_value = calculate_total_value(portfolio)
    
    # Calculate total investment
    total_investment = sum(security["purchase_price"] * security["quantity"] for security in portfolio.values())
    
    # Calculate overall gain/loss
    overall_gain_loss = total_value - total_investment
    overall_percent_change = (overall_gain_loss / total_investment) * 100
    
    # Get best and worst performers
    best_performers, worst_performers = identify_best_worst_performers(portfolio)
    
    # Get threshold report
    positions_up, positions_down = generate_threshold_report(portfolio)
    
    # Get asset class and sector allocations
    asset_allocation = calculate_asset_class_allocation(portfolio)
    sector_allocation = calculate_sector_allocation(portfolio)
    
    # Get rebalancing suggestions
    target_allocation = {
        "Stocks": 60,
        "ETFs": 20,
        "Bonds": 20
    }
    
    rebalancing_suggestions = suggest_rebalancing(portfolio, target_allocation)
    
    # Create visualizations
    visualizations = create_portfolio_visualizations(portfolio)
    
    # Transform portfolio for template
    portfolio_list = []
    for ticker, security in portfolio.items():
        security_value = security["current_price"] * security["quantity"]
        percent_change = ((security["current_price"] - security["purchase_price"]) / security["purchase_price"]) * 100
        
        portfolio_list.append({
            "ticker": ticker,
            "name": security["name"],
            "asset_class": security["asset_class"],
            "sector": security["sector"],
            "purchase_price": security["purchase_price"],
            "current_price": security["current_price"],
            "quantity": security["quantity"],
            "value": security_value,
            "percent_change": percent_change,
            "gain_loss": security["current_price"] - security["purchase_price"],
            "total_gain_loss": (security["current_price"] - security["purchase_price"]) * security["quantity"]
        })
    
    # Sort by value
    portfolio_list = sorted(portfolio_list, key=lambda x: x["value"], reverse=True)
    
    return render_template(
        'portfolio.html',
        portfolio=portfolio_list,
        total_value=total_value,
        total_investment=total_investment,
        overall_gain_loss=overall_gain_loss,
        overall_percent_change=overall_percent_change,
        best_performers=best_performers,
        worst_performers=worst_performers,
        positions_up=positions_up,
        positions_down=positions_down,
        asset_allocation=asset_allocation,
        sector_allocation=sector_allocation,
        rebalancing_suggestions=rebalancing_suggestions,
        visualizations=visualizations
    )

@app.route('/watchlist')
def watchlist():
    portfolio = create_sample_portfolio()
    watchlist = create_sample_watchlist()
    
    # Find complementary securities
    complementary_securities = find_complementary_securities(portfolio, watchlist)
    
    # Find similar sector securities
    similar_sector_securities = find_similar_sector_securities(portfolio, watchlist)
    
    # Transform watchlist for template
    watchlist_items = []
    for ticker, security in watchlist.items():
        watchlist_items.append({
            "ticker": ticker,
            "name": security["name"],
            "asset_class": security["asset_class"],
            "sector": security["sector"],
            "current_price": security["current_price"],
            "description": security.get("description", "")
        })
    
    return render_template(
        'watchlist.html',
        watchlist=watchlist_items,
        complementary_securities=complementary_securities,
        similar_sector_securities=similar_sector_securities
    )

@app.route('/add-security', methods=['GET', 'POST'])
def add_security():
    if request.method == 'POST':
        # In a real app, this would add to a database
        # For demo purposes, we'll just redirect back to the portfolio
        return redirect(url_for('portfolio_dashboard'))
    
    return render_template('add_security.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.template_filter('currency')
def format_currency(value):
    """Format a value as currency"""
    if value is None:
        return "$0.00"
    return "${:,.2f}".format(value)

@app.template_filter('percentage')
def format_percentage(value):
    """Format a value as percentage"""
    if value is None:
        return "0.00%"
    return "{:.2f}%".format(value)

@app.context_processor
def inject_year():
    """Inject current year into all templates"""
    return {'current_year': datetime.today().year}

if __name__ == '__main__':
    app.run(debug=True)