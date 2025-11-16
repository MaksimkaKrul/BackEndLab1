from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from my_app import db
from my_app.models import UserModel
from my_app.schemas import PlainUserSchema, UserSchema

blp = Blueprint("Users", "users", description="Operations on users")


@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}

    @blp.arguments(PlainUserSchema)
    @blp.response(200, UserSchema)
    def put(self, user_data, user_id):
        user = UserModel.query.get_or_404(user_id)

        if "name" in user_data:
            user.name = user_data["name"]
        if "default_currency_id" in user_data:
            user.default_currency_id = user_data["default_currency_id"]

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A user with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while updating the user.")
            
        return user


@blp.route("/user")
class UserList(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()
    
    @blp.arguments(PlainUserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        user = UserModel(**user_data)
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A user with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the user.")
        return user