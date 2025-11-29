from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required

from my_app import db
from my_app.models import CategoryModel
from my_app.schemas import PlainCategorySchema

blp = Blueprint("Categories", "categories", description="Operations on categories")

@blp.route("/category/<int:category_id>")
class Category(MethodView):
    @jwt_required()
    @blp.response(200, PlainCategorySchema)
    def get(self, category_id):
        category = CategoryModel.query.get_or_404(category_id)
        return category

    @jwt_required()
    def delete(self, category_id):
        category = CategoryModel.query.get_or_404(category_id)
        db.session.delete(category)
        db.session.commit()
        return {"message": "Category deleted."}

@blp.route("/category")
class CategoryList(MethodView):
    @jwt_required()
    @blp.response(200, PlainCategorySchema(many=True))
    def get(self):
        return CategoryModel.query.all()

    @jwt_required()
    @blp.arguments(PlainCategorySchema)
    @blp.response(201, PlainCategorySchema)
    def post(self, category_data):
        category = CategoryModel(**category_data)
        try:
            db.session.add(category)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A category with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the category.")
        return category