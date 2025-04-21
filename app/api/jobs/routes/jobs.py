import uuid

from fastapi import APIRouter, Depends, HTTPException

from ..utils.airflow import airflow_dag_trigger
from ..utils.jobs import job_formatted
from ..models.jobs import Job, Job_Type

from ..auth.main import validate_token, UserSession
from ..schemas.jobs import GenericJob
from ..schemas.jobs import JobTypeEnum, JobStatus, JobOutput
from ..database.conf import db_jobs

from jsonschema import SchemaError, ValidationError, validate

router = APIRouter()


@router.get("/{job_uuid}", response_description="Update Session")
async def get_job_details(job_uuid: uuid.UUID,
                          current_user: UserSession = Depends(validate_token),
                          database=Depends(db_jobs)):
    if (job := database.query(Job).filter(
            Job.uuid == job_uuid).first()) is None:
        raise HTTPException(status_code=404, detail="Resource not found")

    return job_formatted(job)





def internal_create_generic_job(body: GenericJob, job_type: str, database):
    job_type_details = database.query(Job_Type).filter(
        Job_Type.name == str(job_type)).first()

    if job_type_details is None:
        raise HTTPException(status_code=404, detail="Job Type Not Found")

    try:
        validate(body.params, job_type_details.params_schema)
    except ValidationError as error:
        raise HTTPException(
            status_code=400, detail=f"Params Schema Validation Error: {error}"
        )
    except SchemaError as error:
        raise HTTPException(
            status_code=400, detail=f"Schema Error: {error}"
        )

    default_params = job_type_details.default_params if job_type_details.default_params else {}
    # Create Job
    new_job = Job(
        type=job_type,
        params={**default_params, **body.params}
    )
    database.add(new_job)
    database.commit()

    # Launch airflow dag
    airflow_response = airflow_dag_trigger(
        job_type_details.dag_name, {'job': str(new_job.uuid)})
    return job_formatted(new_job)


@router.post("/{job_type}", response_description="Triggers a generic job")
async def create_generic_job(body: GenericJob,
                             job_type: JobTypeEnum,
                             current_user: UserSession = Depends(
                                 validate_token),
                             database=Depends(db_jobs)):
    # Validate Job params
    return internal_create_generic_job(body, job_type, database)
#
#
# @router.post("/{job_uuid}/{job_type}", response_description="Triggers a generic job")
# async def cast_job(body: GenericJob,
#                    job_type: JobTypeEnum,
#                    job_uuid: uuid.UUID,
#                    current_user: UserSession = Depends(
#                        validate_token),
#                    database=Depends(db_jobs)):
#     if (original_job := database.query(Job).filter(
#             Job.uuid == job_uuid).first()) is None:
#         raise HTTPException(status_code=404, detail="Resource not found")
#
#     # Validate Job params
#     job_type_details = database.query(Job_Type).filter(
#         Job_Type.name == str(job_type)).first()
#
#     if job_type_details is None:
#         raise HTTPException(status_code=404, detail="Job Type Not Found")
#
#     try:
#         validate(body.params, job_type_details.params_schema)
#     except ValidationError as error:
#         raise HTTPException(
#             status_code=400, detail=f"Params Schema Validation Error: {error}"
#         )
#     except SchemaError as error:
#         raise HTTPException(
#             status_code=400, detail=f"Schema Error: {error}"
#         )
#
#     if "job_cast" not in original_job.output:
#         raise HTTPException(status_code=400, detail="Original job not found")
#     if original_job.output['job_cast']:
#         raise HTTPException(status_code=409, detail="Job Already Cast")
#
#     original_job.output = {**original_job.output, **{"job_cast": True}}
#     default_params = job_type_details.default_params if job_type_details.default_params else {}
#     # Create Job
#     new_job = Job(
#         type=job_type,
#         params={**default_params, **original_job.params, **body.params},
#         output={**original_job.output, **{'original_job_uuid': str(job_uuid)}},
#     )
#     database.add(new_job)
#     database.commit()
#
#     # Launch airflow dag
#     airflow_response = airflow_dag_trigger(
#         job_type_details.dag_name, {'job': str(new_job.uuid)})
#     return job_formatted(new_job)
#
#
# @router.post("/{job_uuid}/{job_type}/cast_status", response_description="Check cast status")
# async def post_job_cast_status(job_uuid: uuid.UUID,
#                                job_type: JobTypeEnum,
#                                current_user: UserSession = Depends(validate_token),
#                                database=Depends(db_jobs)):
#     if (job := database.query(Job).with_for_update(of=Job.output, nowait=True).filter(
#             Job.uuid == job_uuid).first()) is None:
#         raise HTTPException(status_code=409, detail="Resource not found")
#
#     if job.output is None:
#         job.output = {}
#     if "job_cast" not in job.output:
#         original_output = job.output
#         job.output = {**original_output, **{"job_cast": False}}
#     database.commit()
#
#     return job_formatted(job)


@router.patch('/{job_uuid}/status')
async def set_job_status(job_uuid: uuid.UUID,
                         status_update: JobStatus,
                         current_user: UserSession = Depends(validate_token),
                         database=Depends(db_jobs)):
    job = database.query(Job).filter(Job.uuid == job_uuid)

    if job.first() is None:
        raise HTTPException(status_code=404, detail="Not found")

    job.update({'status': status_update.status.value,
                'status_message': status_update.status_message})
    database.commit()

    return job_formatted(job.first())


@router.patch('/{job_uuid}/output')
async def join_output(job_uuid: uuid.UUID,
                      body: JobOutput,
                      current_user: UserSession = Depends(validate_token),
                      database=Depends(db_jobs)):
    job = database.query(Job).filter(Job.uuid == job_uuid)

    if job.first() is None:
        raise HTTPException(status_code=404, detail="Not found")

    original_output = job.first().output
    if original_output is None:
        original_output = {}

    job.update(
        {'output': {**original_output, **body.output}})
    database.commit()

    return job_formatted(job.first())
