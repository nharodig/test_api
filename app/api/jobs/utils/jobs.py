
def job_formatted(job):
    response = {
        "uuid": job.uuid if job else None,
        "type": job.type if job else None,
        "status": job.status,
        "status_message": job.status_message,
        "params": job.params,
        "error": job.error,
        "output": job.output,
        "created_at": job.created_at,
        "updated_at": job.updated_at
    }
    return response
