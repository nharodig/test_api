from pydantic import BaseModel
from typing import Optional, Dict
from uuid import UUID
from enum import Enum


class JobStatusEnum(str, Enum):
    DECLARED = 'DECLARED'
    PROCESSING = 'PROCESSING'
    FAILED = 'FAILED'
    FINISHED = 'FINISHED'


class JobStatus(BaseModel):
    status: JobStatusEnum
    status_message: Optional[str] = None


class JobOutput(BaseModel):
    output: Dict


class JobTypeEnum(str, Enum):
    APPLICATION_PROCESSING = 'APPLICATION_PROCESSING'
    FILES_PROCESSING = 'FILES_PROCESSING'
    FLOID_PROCESSING = 'FLOID_PROCESSING'
    BACKGROUND_PROCESSING = 'BACKGROUND_PROCESSING'
    PARTNER_PREAPPROVAL_WITH_CONFIRMATION_EMAIL = 'PARTNER_PREAPPROVAL_WITH_CONFIRMATION_EMAIL'
    PARTNER_REGISTRATION='PARTNER_REGISTRATION'
    APPLICATION_PROCESSING_WITH_COBORROWER='APPLICATION_PROCESSING_WITH_COBORROWER'
    COBORROWER_PREAPPROVAL_INVITATION='COBORROWER_PREAPPROVAL_INVITATION'
    PARTNER_PREAPPROVAL_WITH_CONFIRMATION_EMAIL_WITH_COBORROWER='PARTNER_PREAPPROVAL_WITH_CONFIRMATION_EMAIL_WITH_COBORROWER'
    FINANCIAL_INSTITUTION_NOTIFICATION='FINANCIAL_INSTITUTION_NOTIFICATION'
    CRM_EMAIL_NOTIFICATION='CRM_EMAIL_NOTIFICATION'
    TYPEFORM_CREATION='TYPEFORM_CREATION'
    MERCADOLIBRE_CODE_RETRIEVAL='MERCADOLIBRE_CODE_RETRIEVAL'


    def __str__(self):
        return str(self.value)


class GenericJob(BaseModel):
    params: Dict
