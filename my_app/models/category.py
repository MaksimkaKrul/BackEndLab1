from my_app import db

class CategoryModel(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    records = db.relationship("RecordModel", back_populates="category", lazy="dynamic", cascade="all, delete-orphan")