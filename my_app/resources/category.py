from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from my_app import db
from my_app.models import CategoryModel
from my_app.schemas import PlainCategorySchema

blp = Blueprint("Categories", "categories", description="Operations on categories")


@blp.route("/category/<int:category_id>")
class Category(MethodView):
    @blp.response(200, PlainCategorySchema)
    def get(self, category_id):
        category = CategoryModel.query.get_or_404(category_id)
        return category

    def delete(self, category_id):
        category = CategoryModel.query.get_or_404(category_id)
        db.session.delete(category)
        db.session.commit()
        return {"message": "Category deleted."}, 200


@blp.route("/category")
class CategoryList(MethodView):
    @blp.response(200, PlainCategorySchema(many=True))
    def get(self):
        return CategoryModel.query.all()

    @blp.arguments(PlainCategorySchema)
    @blp.response(201, PlainCategorySchema)
    def post(self, category_data):
        category = CategoryModel(**category_data)
        try:
            db.session.add(category)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A category with that name already exists.")
        except SQLAlchemyError as e:
            abort(500, message=f"An error occurred while inserting the category: {e}")
            
        return category