from my_app import db

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    
    default_currency_id = db.Column(db.Integer, db.ForeignKey("currencies.id"), nullable=True)
    default_currency = db.relationship("CurrencyModel")
    
    records = db.relationship("RecordModel", back_populates="user", lazy="dynamic", cascade="all, delete-orphan")