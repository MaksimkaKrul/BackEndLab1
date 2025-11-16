from marshmallow import Schema, fields

class PlainCategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class PlainRecordSchema(Schema):
    id = fields.Int(dump_only=True)
    amount = fields.Float(required=True)
    created_at = fields.Str(dump_only=True)

class UserUpdateSchema(Schema):
    name = fields.Str()

class PlainCurrencySchema(Schema):
    id = fields.Int(dump_only=True)
    code = fields.Str(required=True)
    name = fields.Str(required=True)

class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    default_currency_id = fields.Int(load_only=True) 

class UserSchema(PlainUserSchema):
    default_currency = fields.Nested(PlainCurrencySchema(), dump_only=True)

class RecordSchema(PlainRecordSchema):
    user_id = fields.Int(required=True, load_only=True)
    category_id = fields.Int(required=True, load_only=True)
    user = fields.Nested(PlainUserSchema(), dump_only=True)
    category = fields.Nested(PlainCategorySchema(), dump_only=True)
    currency_id = fields.Int(load_only=True)
    currency = fields.Nested(PlainCurrencySchema(), dump_only=True)

