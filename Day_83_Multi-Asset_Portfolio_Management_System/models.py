from datetime import datetime
from app import db

class Security(db.Model):
    """Model for storing security information in the portfolio"""
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    asset_class = db.Column(db.String(50), nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    purchase_date = db.Column(db.Date, nullable=False)
    sector = db.Column(db.String(50))
    country = db.Column(db.String(50))
    currency = db.Column(db.String(3), default="USD")
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Security {self.ticker}>"
    
    @property
    def purchase_value(self):
        """Calculate the value of the security at purchase"""
        return self.purchase_price * self.quantity
    
    @property
    def current_value(self):
        """Calculate the current value of the security"""
        return self.current_price * self.quantity
    
    @property
    def gain_loss(self):
        """Calculate the gain/loss in value"""
        return self.current_value - self.purchase_value
    
    @property
    def gain_loss_percentage(self):
        """Calculate the gain/loss as a percentage"""
        if self.purchase_value == 0:
            return 0
        return (self.gain_loss / self.purchase_value) * 100


class Transaction(db.Model):
    """Model for tracking security transactions"""
    id = db.Column(db.Integer, primary_key=True)
    security_id = db.Column(db.Integer, db.ForeignKey('security.id'), nullable=False)
    transaction_type = db.Column(db.String(10), nullable=False)  # 'buy' or 'sell'
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    transaction_date = db.Column(db.Date, nullable=False)
    fees = db.Column(db.Float, default=0.0)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    security = db.relationship('Security', backref=db.backref('transactions', lazy=True))
    
    def __repr__(self):
        return f"<Transaction {self.transaction_type} {self.security.ticker}>"
    
    @property
    def total_value(self):
        """Calculate the total value of the transaction including fees"""
        if self.transaction_type == 'buy':
            return (self.price * self.quantity) + self.fees
        else:  # sell
            return (self.price * self.quantity) - self.fees


class PortfolioSnapshot(db.Model):
    """Model for storing historical portfolio snapshots for performance tracking"""
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    total_value = db.Column(db.Float, nullable=False)
    cash_value = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<PortfolioSnapshot {self.date}>"
