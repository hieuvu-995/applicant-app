from marshmallow import schema, fields
from apps.core.schema import Meta


class RegistrationApplicantRequestSchema(schema.Schema):
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    dob = fields.Str(required=True)
    country = fields.Str(required=True)
    status = fields.Str()


class RegistrationApplicantRespSchema(schema.Schema):
    applicant_id = fields.Str()
    status = fields.Str()


class RegistrationAccountResponse(schema.Schema):
    meta = fields.Nested(Meta)
    data = fields.Nested(RegistrationApplicantRespSchema)


class UpdateApplicantInfo(schema.Schema):
    name = fields.Str(Nullable=True)
    email = fields.Str(required=True)
    dob = fields.Str(Nullable=True)
    country = fields.Str(Nullable=True)
    status = fields.Str(Nullable=True)


class GetApplicantRequestSchema(schema.Schema):
    email = fields.Str(required=True)


class ListApplicantDetail(schema.Schema):
    next_audit_date = fields.Str()
    list_account = fields.Nested(RegistrationApplicantRespSchema, many=True)


class ListApplicantRes(schema.Schema):
    meta = fields.Nested(Meta)
    data = fields.Nested(ListApplicantDetail)
