from my_app import db
from sqlalchemy.sql import func

class RecordModel(db.Model):
    __tablename__ = "records"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float(precision=2), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=func.now())
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    currency_id = db.Column(db.Integer, db.ForeignKey("currencies.id"), nullable=True)
    currency = db.relationship("CurrencyModel")
    
    user = db.relationship("UserModel", back_populates="records")
    category = db.relationship("CategoryModel", back_populates="records")