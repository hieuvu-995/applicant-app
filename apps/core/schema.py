from marshmallow import Schema, ValidationError as MarshValidationError, schema, fields
from rest_framework.exceptions import ValidationError

from apps.core.responses import ResponseObject


def validate_data(schema_cls: Schema, data: dict or object) -> dict:
    """Validate data using Marshmallow schema

    Return validated data if success, raise ValidationError if failed
    """
    try:
        valid_data = schema_cls().load(data)
    except MarshValidationError as err:
        _resp = ResponseObject()
        msg = (
            f"Missing data for required field: "
            f"{str(', '.join(err.messages.keys()))}"
        )
        _resp.meta = {"code": 400, "message": msg}
        data = serialize_data(MetaErr, _resp)
        raise ValidationError(data)
    return valid_data


def serialize_data(schema_cls: Schema, data: dict or object, many=False) -> dict:
    return schema_cls().dump(data, many=many)


class Meta(schema.Schema):
    code = fields.Int(default=200)
    message = fields.Str(default="success")


class MetaErr(schema.Schema):
    meta = fields.Nested(Meta)
    data = fields.Raw(default=None)
