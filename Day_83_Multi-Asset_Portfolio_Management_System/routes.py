from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app, db
from models import Security, Transaction, PortfolioSnapshot
from portfolio_manager import PortfolioManager

@app.route('/')
def index():
    """Home page showing portfolio overview"""
    summary = PortfolioManager.get_portfolio_summary()
    metrics = PortfolioManager.calculate_portfolio_metrics()
    risk = PortfolioManager.calculate_risk_metrics()
    
    # Record today's snapshot if not already recorded
    PortfolioManager.record_snapshot()
    
    # Get latest securities
    latest_securities = Security.query.order_by(Security.created_at.desc()).limit(5).all()
    
    return render_template('index.html', 
                           summary=summary, 
                           metrics=metrics, 
                           risk=risk,
                           latest_securities=latest_securities)

@app.route('/portfolio')
def portfolio():
    """Page showing detailed portfolio"""
    securities = Security.query.all()
    summary = PortfolioManager.get_portfolio_summary()
    
    return render_template('portfolio.html', securities=securities, summary=summary)

@app.route('/add_security', methods=['GET', 'POST'])
def add_security():
    """Page for adding a new security to the portfolio"""
    if request.method == 'POST':
        try:
            # Get form data
            ticker = request.form.get('ticker').upper()
            name = request.form.get('name')
            asset_class = request.form.get('asset_class')
            purchase_price = float(request.form.get('purchase_price'))
            current_price = float(request.form.get('current_price'))
            quantity = float(request.form.get('quantity'))
            purchase_date = datetime.strptime(request.form.get('purchase_date'), '%Y-%m-%d')
            sector = request.form.get('sector')
            country = request.form.get('country')
            currency = request.form.get('currency', 'USD')
            notes = request.form.get('notes')
            
            # Create new security
            security = Security(
                ticker=ticker,
                name=name,
                asset_class=asset_class,
                purchase_price=purchase_price,
                current_price=current_price,
                quantity=quantity,
                purchase_date=purchase_date,
                sector=sector,
                country=country,
                currency=currency,
                notes=notes
            )
            
            db.session.add(security)
            db.session.commit()
            
            # Create transaction record
            transaction = Transaction(
                security_id=security.id,
                transaction_type='buy',
                price=purchase_price,
                quantity=quantity,
                transaction_date=purchase_date
            )
            
            db.session.add(transaction)
            db.session.commit()
            
            flash(f"Security {ticker} added successfully!", "success")
            return redirect(url_for('portfolio'))
        
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding security: {str(e)}", "danger")
    
    # Asset classes for dropdown
    asset_classes = [
        'Stock', 'ETF', 'Mutual Fund', 'Government Bonds', 'Corporate Bonds', 
        'Municipal Bonds', 'Cash', 'Cryptocurrency', 'Real Estate', 
        'Commodity', 'Options', 'Futures', 'Other'
    ]
    
    return render_template('add_security.html', asset_classes=asset_classes)

@app.route('/edit_security/<int:security_id>', methods=['GET', 'POST'])
def edit_security(security_id):
    """Page for editing an existing security"""
    security = Security.query.get_or_404(security_id)
    
    if request.method == 'POST':
        try:
            # Update security data
            security.name = request.form.get('name')
            security.asset_class = request.form.get('asset_class')
            security.current_price = float(request.form.get('current_price'))
            security.quantity = float(request.form.get('quantity'))
            security.sector = request.form.get('sector')
            security.country = request.form.get('country')
            security.currency = request.form.get('currency', 'USD')
            security.notes = request.form.get('notes')
            security.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            flash(f"Security {security.ticker} updated successfully!", "success")
            return redirect(url_for('portfolio'))
        
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating security: {str(e)}", "danger")
    
    # Asset classes for dropdown
    asset_classes = [
        'Stock', 'ETF', 'Mutual Fund', 'Government Bonds', 'Corporate Bonds', 
        'Municipal Bonds', 'Cash', 'Cryptocurrency', 'Real Estate', 
        'Commodity', 'Options', 'Futures', 'Other'
    ]
    
    return render_template('add_security.html', asset_classes=asset_classes, security=security, edit=True)

@app.route('/delete_security/<int:security_id>', methods=['POST'])
def delete_security(security_id):
    """Route for deleting a security"""
    security = Security.query.get_or_404(security_id)
    
    try:
        # Delete associated transactions first
        Transaction.query.filter_by(security_id=security_id).delete()
        
        # Delete the security
        db.session.delete(security)
        db.session.commit()
        
        flash(f"Security {security.ticker} deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting security: {str(e)}", "danger")
    
    return redirect(url_for('portfolio'))

@app.route('/analysis')
def analysis():
    """Page for displaying portfolio analysis"""
    summary = PortfolioManager.get_portfolio_summary()
    metrics = PortfolioManager.calculate_portfolio_metrics()
    risk = PortfolioManager.calculate_risk_metrics()
    
    return render_template('analysis.html', summary=summary, metrics=metrics, risk=risk)

@app.route('/reports')
def reports():
    """Page for generating and displaying portfolio reports"""
    report = PortfolioManager.generate_report()
    
    return render_template('reports.html', report=report)

@app.route('/api/portfolio_performance')
def portfolio_performance():
    """API endpoint for fetching portfolio performance data"""
    days = request.args.get('days', 30, type=int)
    performance = PortfolioManager.get_historical_performance(days)
    
    return jsonify(performance)

@app.route('/api/asset_allocation')
def asset_allocation():
    """API endpoint for fetching asset allocation data"""
    summary = PortfolioManager.get_portfolio_summary()
    
    return jsonify({
        'labels': list(summary['asset_allocation'].keys()),
        'data': list(summary['asset_allocation'].values())
    })

@app.route('/api/sector_allocation')
def sector_allocation():
    """API endpoint for fetching sector allocation data"""
    summary = PortfolioManager.get_portfolio_summary()
    
    return jsonify({
        'labels': list(summary['sector_allocation'].keys()),
        'data': list(summary['sector_allocation'].values())
    })

@app.route('/api/update_prices', methods=['POST'])
def update_prices():
    """API endpoint for updating current prices"""
    data = request.json
    
    try:
        for security_update in data:
            security_id = security_update.get('id')
            current_price = security_update.get('current_price')
            
            if security_id and current_price:
                security = Security.query.get(security_id)
                if security:
                    security.current_price = float(current_price)
                    security.updated_at = datetime.utcnow()
        
        db.session.commit()
        return jsonify({'status': 'success'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)})

@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 page"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    """Custom 500 page"""
    return render_template('500.html'), 500
