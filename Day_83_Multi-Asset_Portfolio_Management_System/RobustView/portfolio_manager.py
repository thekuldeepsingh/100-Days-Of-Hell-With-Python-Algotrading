import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from models import Security, Transaction, PortfolioSnapshot
from app import db

class PortfolioManager:
    """Class to handle portfolio calculations and analysis"""
    
    @staticmethod
    def get_portfolio_summary():
        """Get a summary of the current portfolio"""
        securities = Security.query.all()
        
        total_value = sum(security.current_value for security in securities)
        total_cost = sum(security.purchase_value for security in securities)
        total_gain_loss = sum(security.gain_loss for security in securities)
        
        if total_cost == 0:
            total_gain_loss_pct = 0
        else:
            total_gain_loss_pct = (total_gain_loss / total_cost) * 100
        
        # Get asset allocation
        asset_allocation = {}
        for security in securities:
            if security.asset_class in asset_allocation:
                asset_allocation[security.asset_class] += security.current_value
            else:
                asset_allocation[security.asset_class] = security.current_value
        
        # Convert to percentages
        for asset_class in asset_allocation:
            asset_allocation[asset_class] = (asset_allocation[asset_class] / total_value) * 100 if total_value > 0 else 0
        
        # Get sector allocation
        sector_allocation = {}
        for security in securities:
            if security.sector:
                if security.sector in sector_allocation:
                    sector_allocation[security.sector] += security.current_value
                else:
                    sector_allocation[security.sector] = security.current_value
        
        # Convert to percentages
        for sector in sector_allocation:
            sector_allocation[sector] = (sector_allocation[sector] / total_value) * 100 if total_value > 0 else 0
        
        return {
            'total_value': total_value,
            'total_cost': total_cost,
            'total_gain_loss': total_gain_loss,
            'total_gain_loss_pct': total_gain_loss_pct,
            'securities_count': len(securities),
            'asset_allocation': asset_allocation,
            'sector_allocation': sector_allocation
        }
    
    @staticmethod
    def calculate_portfolio_metrics():
        """Calculate various portfolio metrics"""
        securities = Security.query.all()
        
        # Create a DataFrame for easier calculations
        df = pd.DataFrame([{
            'ticker': s.ticker,
            'asset_class': s.asset_class,
            'sector': s.sector,
            'current_value': s.current_value,
            'purchase_value': s.purchase_value,
            'gain_loss': s.gain_loss,
            'gain_loss_pct': s.gain_loss_percentage
        } for s in securities])
        
        if df.empty:
            return {
                'volatility': 0,
                'sharpe_ratio': 0,
                'top_performers': [],
                'bottom_performers': []
            }
        
        # Calculate portfolio volatility (simplified)
        # In a real application, this would use historical price data
        if len(df) > 1:
            # Using gain_loss_pct as a proxy for volatility
            volatility = df['gain_loss_pct'].std()
        else:
            volatility = 0
        
        # Calculate Sharpe ratio (simplified)
        # Using average gain_loss_pct as a proxy for return
        # Assuming risk-free rate of 2%
        risk_free_rate = 2.0
        if volatility > 0:
            avg_return = df['gain_loss_pct'].mean()
            sharpe_ratio = (avg_return - risk_free_rate) / volatility
        else:
            sharpe_ratio = 0
        
        # Get top and bottom performers
        df_sorted = df.sort_values(by='gain_loss_pct', ascending=False)
        top_performers = df_sorted.head(3).to_dict('records')
        bottom_performers = df_sorted.tail(3).to_dict('records')
        
        return {
            'volatility': volatility,
            'sharpe_ratio': sharpe_ratio,
            'top_performers': top_performers,
            'bottom_performers': bottom_performers
        }
    
    @staticmethod
    def calculate_risk_metrics():
        """Calculate portfolio risk metrics"""
        securities = Security.query.all()
        
        # Create a basic risk assessment based on asset classes
        risk_levels = {
            'Cash': 1,
            'Government Bonds': 2,
            'Corporate Bonds': 3,
            'Municipal Bonds': 3,
            'ETF': 4,
            'Mutual Fund': 4,
            'Stock': 5,
            'Commodity': 5,
            'Cryptocurrency': 7,
            'Options': 7,
            'Futures': 7,
            'Real Estate': 4,
            'Other': 4
        }
        
        weighted_risk = 0
        total_value = sum(s.current_value for s in securities)
        
        if total_value == 0:
            return {
                'portfolio_risk_score': 0,
                'risk_level': 'No investments',
                'risk_breakdown': {}
            }
        
        # Calculate weighted risk score
        risk_breakdown = {}
        for security in securities:
            risk_score = risk_levels.get(security.asset_class, 4)
            weight = security.current_value / total_value
            weighted_risk += risk_score * weight
            
            if security.asset_class in risk_breakdown:
                risk_breakdown[security.asset_class]['value'] += security.current_value
                risk_breakdown[security.asset_class]['weight'] += weight
            else:
                risk_breakdown[security.asset_class] = {
                    'value': security.current_value,
                    'weight': weight,
                    'risk_score': risk_score
                }
        
        # Determine risk level
        risk_level = 'Unknown'
        if weighted_risk < 2:
            risk_level = 'Very Low'
        elif weighted_risk < 3:
            risk_level = 'Low'
        elif weighted_risk < 4:
            risk_level = 'Moderate'
        elif weighted_risk < 5:
            risk_level = 'Medium'
        elif weighted_risk < 6:
            risk_level = 'Medium-High'
        elif weighted_risk < 7:
            risk_level = 'High'
        else:
            risk_level = 'Very High'
        
        return {
            'portfolio_risk_score': round(weighted_risk, 2),
            'risk_level': risk_level,
            'risk_breakdown': risk_breakdown
        }
    
    @staticmethod
    def record_snapshot(date=None):
        """Record a snapshot of the portfolio for the specified date"""
        if date is None:
            date = datetime.utcnow().date()
        
        securities = Security.query.all()
        total_value = sum(security.current_value for security in securities)
        
        # Check if a snapshot already exists for this date
        existing_snapshot = PortfolioSnapshot.query.filter_by(date=date).first()
        
        if existing_snapshot:
            existing_snapshot.total_value = total_value
            db.session.commit()
            return existing_snapshot
        else:
            new_snapshot = PortfolioSnapshot(
                date=date,
                total_value=total_value
            )
            db.session.add(new_snapshot)
            db.session.commit()
            return new_snapshot
    
    @staticmethod
    def get_historical_performance(days=30):
        """Get historical portfolio performance data"""
        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=days)
        
        snapshots = PortfolioSnapshot.query.filter(
            PortfolioSnapshot.date >= start_date,
            PortfolioSnapshot.date <= end_date
        ).order_by(PortfolioSnapshot.date).all()
        
        dates = []
        values = []
        for snapshot in snapshots:
            dates.append(snapshot.date.strftime('%Y-%m-%d'))
            values.append(snapshot.total_value)
        
        return {
            'dates': dates,
            'values': values
        }
    
    @staticmethod
    def generate_report():
        """Generate a comprehensive portfolio report"""
        summary = PortfolioManager.get_portfolio_summary()
        metrics = PortfolioManager.calculate_portfolio_metrics()
        risk = PortfolioManager.calculate_risk_metrics()
        performance = PortfolioManager.get_historical_performance()
        
        # Get all securities
        securities = Security.query.all()
        securities_data = []
        
        for security in securities:
            securities_data.append({
                'id': security.id,
                'ticker': security.ticker,
                'name': security.name,
                'asset_class': security.asset_class,
                'purchase_price': security.purchase_price,
                'current_price': security.current_price,
                'quantity': security.quantity,
                'purchase_date': security.purchase_date.strftime('%Y-%m-%d'),
                'purchase_value': security.purchase_value,
                'current_value': security.current_value,
                'gain_loss': security.gain_loss,
                'gain_loss_pct': security.gain_loss_percentage,
                'sector': security.sector,
                'country': security.country,
                'currency': security.currency
            })
        
        report = {
            'summary': summary,
            'metrics': metrics,
            'risk': risk,
            'performance': performance,
            'securities': securities_data,
            'generated_at': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return report
