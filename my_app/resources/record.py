from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from my_app import db
from my_app.models import RecordModel, UserModel
from my_app.schemas import RecordSchema

blp = Blueprint("Records", "records", description="Operations on records")


@blp.route("/record/<int:record_id>")
class Record(MethodView):
    @blp.response(200, RecordSchema)
    def get(self, record_id):
        record = RecordModel.query.get_or_404(record_id)
        return record

    def delete(self, record_id):
        record = RecordModel.query.get_or_404(record_id)
        db.session.delete(record)
        db.session.commit()
        return {"message": "Record deleted."}, 200


@blp.route("/record")
class RecordList(MethodView):
    @blp.response(200, RecordSchema(many=True))
    def get(self):
        user_id = request.args.get('user_id')
        category_id = request.args.get('category_id')
        
        query = RecordModel.query

        if user_id:
            query = query.filter(RecordModel.user_id == user_id)
        
        if category_id:
            query = query.filter(RecordModel.category_id == category_id)

        return query.all()

    @blp.arguments(RecordSchema)
    @blp.response(201, RecordSchema)
    def post(self, record_data):
        currency_id_provided = record_data.get("currency_id")

        if not currency_id_provided:
            user = UserModel.query.get_or_404(record_data["user_id"])
            
            if user.default_currency_id:
                record_data["currency_id"] = user.default_currency_id
            else:
                pass 

        record = RecordModel(**record_data)

        try:
            db.session.add(record)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=f"An error occurred while inserting the record: {e}")
            
        return record