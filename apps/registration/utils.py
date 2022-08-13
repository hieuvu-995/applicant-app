import datetime
import uuid

from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import status

from apps.core.consts import ApplicantStatus, CountryCode, VN, USA
from apps.registration import schema
from apps.core.schema import serialize_data
from . import models


def check_valid_email(email: str, _resp: object):
    try:
        validate_email(email)
    except ValidationError:
        _resp.meta = {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": f"Email address: {email} is invalid!",
        }
        data = serialize_data(schema.RegistrationAccountResponse, _resp)
        return data, status.HTTP_400_BAD_REQUEST
    if get_user_by_email(email=email):
        _resp.meta = {
            "code": status.HTTP_409_CONFLICT,
            "message": f"Applicant's email {email} already exist!",
        }
        data = serialize_data(schema.RegistrationAccountResponse, _resp)
        return data, status.HTTP_409_CONFLICT
    return "", status.HTTP_200_OK


def check_valid_dob(dob: str, _resp: object) -> bool:
    try:
        return datetime.datetime.strptime(dob, '%Y-%m-%d')
    except:
        return False


def get_country_code(country):
    if country == VN:
        return CountryCode.VIETNAM.value
    elif country == USA:
        return CountryCode.USA.value
    else:
        return CountryCode.UNDEFINED.value


def get_user_by_email(email: str) -> object:
    return models.Applicant.objects.filter(email=email).first()


def create_applicant(
        name,
        email,
        dob,
        country,
):
    applicant = create_user(
        email=email,
        name=name,
        dob=dob,
        country=country,
    )
    return applicant


def create_user(
        name: str = None,
        email: str = None,
        dob: str = None,
        country: str = None,
):
    now = timezone.now()
    partner = models.Applicant(
        name=name,
        email=email,
        dob=dob,
        country=country,
        created_dttm=now,
        status=ApplicantStatus.PENDING.value,
        client_key=uuid.uuid4()
    )
    partner.save()
    return partner


def update_applicant_infor(email: str, **kwargs):
    upd_fields = {k: v for k, v in kwargs.items() if v is not None}
    applicant = models.Applicant.objects.filter(email=email).update(**upd_fields)
    return applicant


def get_applicant_by_email(email):
    return models.Applicant.objects.filter(email=email)


def get_all_applicant() -> dict:
    return models.Applicant.objects.all()


def delete_applicant(email):
    return models.Applicant.objects.filter(email=email).delete()


def update_applicant_status(email: str, status: bool):
    models.Applicant.objects.filter(email=email).update(status=status)

