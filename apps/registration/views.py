import logging

from django.db import transaction
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.throttling import UserRateThrottle

from apps.registration import schema
from apps.core.responses import ResponseObject
from apps.core.schema import validate_data, serialize_data
from . import utils
from ..core.consts import ApplicantStatus

_logger = logging.getLogger(__name__)


class ApplicantManagement(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        _resp = ResponseObject()
        valid_data = validate_data(
            schema.GetApplicantRequestSchema, request.data
        )
        email = valid_data.get("email")
        applicant = utils.get_user_by_email(email)
        if not applicant:
            _resp.meta = {
                "code": status.HTTP_404_NOT_FOUND,
                "message": f"Cannot find applicant with email address: {email}",
            }
            data = serialize_data(schema.RegistrationAccountResponse, _resp)
            _logger.error(f"Applicant not found with email address :{email}")
            return Response(data, status.HTTP_400_BAD_REQUEST)
        _resp.data = {"applicant_id": applicant.applicant_id, "status": applicant.status}
        data = serialize_data(schema.RegistrationAccountResponse, _resp)
        _logger.info(f"Get applicant's info success with applicant's email: {email}")
        return Response(data, status=status.HTTP_201_CREATED)

    def post(self, request):
        throttle_classes = [UserRateThrottle]
        _resp = ResponseObject()
        valid_data = validate_data(
            schema.RegistrationApplicantRequestSchema, request.data
        )
        name = valid_data.get("name")
        email = valid_data.get("email")
        dob = valid_data.get("dob")
        country = valid_data.get("country")
        country_code = utils.get_country_code(country)
        data, resp_status = utils.check_valid_email(
            email=email,
            _resp=_resp
        )

        if resp_status != status.HTTP_200_OK:
            _logger.error(f"Applicant's email is invalid format or existed: {email}")
            return Response(data, resp_status)
        dob = utils.check_valid_dob(dob, _resp)
        if not dob:
            _resp.meta = {
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Dob is incorrect format!",
            }
            data = serialize_data(schema.RegistrationAccountResponse, _resp)
            _logger.error(f"Create applicant's info fail due to invalid dob :{dob}")
            return Response(data, status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            # Create applicant
            applicant = utils.create_applicant(
                name=name,
                email=email,
                dob=dob,
                country=country_code,
            )
        _resp.data = {"applicant_id": applicant.applicant_id, "status": applicant.status}
        _logger.info(f"Create applicant's info success with applicant_id: {applicant.applicant_id}, "
                     f"applicant's email: {email}")
        data = serialize_data(schema.RegistrationAccountResponse, _resp)
        return Response(data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        throttle_classes = [UserRateThrottle]
        _resp = ResponseObject()
        valid_data = validate_data(
            schema.GetApplicantRequestSchema, request.data
        )
        email = valid_data.get("email")
        utils.delete_applicant(email)
        _logger.info(f"Deeleted applicant with email address :{email}")
        _resp.meta = {
            "code": status.HTTP_200_OK,
            "message": f"Applicant with email address {email} has ben deleted",
        }
        data = serialize_data(schema.RegistrationAccountResponse, _resp)
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request):
        throttle_classes = [UserRateThrottle]
        _resp = ResponseObject()
        valid_data = validate_data(
            schema.UpdateApplicantInfo, request.data
        )
        name = valid_data.get("name")
        email = valid_data.get("email")
        dob = valid_data.get("dob")
        country = valid_data.get("country")
        country_code = utils.get_country_code(country)

        if dob:
            dob = utils.check_valid_dob(dob, _resp)
            if not dob:
                _resp.meta = {
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Dob is incorrect format!",
                }
                data = serialize_data(schema.RegistrationAccountResponse, _resp)
                _logger.error(f"Update applicant's info fail due to invalid dob :{dob}")
                return Response(data, status.HTTP_400_BAD_REQUEST)

        applicant = utils.get_user_by_email(email)
        if not applicant:
            _resp.meta = {
                "code": status.HTTP_404_NOT_FOUND,
                "message": f"Cannot find applicant with email address: {email}",
            }
            data = serialize_data(schema.RegistrationAccountResponse, _resp)
            _logger.error(f"Update applicant's info fail due to invalid email address :{email}")
            return Response(data, status.HTTP_404_NOT_FOUND)

        utils.update_applicant_infor(
            name=name,
            email=email,
            dob=dob,
            country=country_code,
        )
        _resp.meta = {
            "code": status.HTTP_200_OK,
            "message": f"Update applicant's info successful with applicant's email': {email}!",
        }
        _resp.data = {"applicant_id": applicant.applicant_id, "status": applicant.status}
        _logger.info(f"Update applicant's info successful with applicant's email': {email}, "
                     f"applicant's email: {email}")
        data = serialize_data(schema.RegistrationAccountResponse, _resp)
        return Response(data, status=status.HTTP_200_OK)


class GetListApplicant(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        _resp = ResponseObject()

        list_account = utils.get_all_applicant()
        _logger.info(f"Get list applicant successful")
        data_load = {
            "list_account": list_account,
        }
        _resp.data = data_load
        data = serialize_data(schema.ListApplicantRes, _resp)
        return Response(data=data, status=status.HTTP_200_OK)


class ApproveApplicant(APIView):
    throttle_classes = [UserRateThrottle]
    permission_classes = (AllowAny,)

    def post(self, request):
        _resp = ResponseObject()
        list_account = utils.get_all_applicant()
        approve_list = []
        reject_list = []
        for account in list_account:
            if account.dob.day % 2 == 0:
                approve_list.append(account.email)
            else:
                reject_list.append(account.email)
        for email in approve_list:
            utils.update_applicant_status(email, ApplicantStatus.PROCESS.value)
        for email in reject_list:
            utils.update_applicant_status(email, ApplicantStatus.FAIL.value)
        _logger.info("Update applicants' status done")
        _resp.meta = {
            "code": status.HTTP_200_OK,
            "message": f"Update applicants' status done",
        }
        data = serialize_data(schema.RegistrationAccountResponse, _resp)
        return Response(data, status.HTTP_200_OK)
