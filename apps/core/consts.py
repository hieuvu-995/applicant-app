from enum import Enum


class ApplicantStatus(Enum):
    PENDING = "pending"
    PROCESS = "process"
    FAIL = "fail"



class CountryCode(Enum):
    VIETNAM = "VN"
    USA = "US"
    UNITED_KINGDOM = "GB"
    UNDEFINED = "UNDEFINED"


VN = "Vietnam"
USA = "United States"
