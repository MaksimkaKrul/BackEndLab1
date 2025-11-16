from flask.views import MethodView
from flask_smorest import Blueprint, abort

from my_app import db
from my_app.models import CurrencyModel
from my_app.schemas import PlainCurrencySchema

blp = Blueprint("Currencies", "currencies", description="Operations on currencies")

@blp.route("/currency")
class CurrencyList(MethodView):
    @blp.response(200, PlainCurrencySchema(many=True))
    def get(self):
        return CurrencyModel.query.all()

    @blp.arguments(PlainCurrencySchema)
    @blp.response(201, PlainCurrencySchema)
    def post(self, currency_data):
        currency = CurrencyModel(**currency_data)
        db.session.add(currency)
        db.session.commit()
        return currency