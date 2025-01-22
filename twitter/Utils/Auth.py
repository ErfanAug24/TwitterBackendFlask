from enum import Enum


class ReportOptions(Enum):
    SPAM = "SPAM"
    SEXUAL_CONTENT = "SEXUAL-CONTENT"
    HATE_SPEECH = "HATE-SPEECH"
    POLICY_VIOLATION = "POLICY-VIOLATION"
    OTHER = "OTHER"
