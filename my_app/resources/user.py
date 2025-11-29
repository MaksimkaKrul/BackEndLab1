from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from my_app import db
from my_app.models import UserModel
from my_app.schemas import PlainUserSchema, UserSchema, UserLoginSchema

blp = Blueprint("Users", "users", description="Operations on users")

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(PlainUserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        user = UserModel(
            name=user_data["name"],
            password=pbkdf2_sha256.hash(user_data["password"]),
            default_currency_id=user_data.get("default_currency_id")
        )
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A user with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the user.")
        return user

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserLoginSchema)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.name == user_data["name"]).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=str(user.id))
            return {"access_token": access_token}

        abort(401, message="Invalid credentials.")

@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    @jwt_required()
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}

@blp.route("/user")
class UserList(MethodView):
    @blp.response(200, UserSchema(many=True))
    @jwt_required()
    def get(self):
        return UserModel.query.all()