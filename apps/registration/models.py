from django.db import models

from apps.core.consts import ApplicantStatus, CountryCode


class Applicant(models.Model):
    applicant_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    dob = models.DateField()
    client_key = models.CharField(max_length=256, blank=True, null=True)
    email = models.CharField(max_length=256, unique=True)
    country = models.CharField(max_length=256, default=CountryCode.VIETNAM.value)
    status = models.CharField(max_length=10, default=ApplicantStatus.PENDING.value)
    created_dttm = models.DateField(blank=True, null=True)

    class Meta:
        db_table = "applicant"
