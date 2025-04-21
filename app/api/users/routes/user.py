from fastapi import APIRouter, Depends, HTTPException, Request
import uuid
from ..utils.user import user_formatted
from ..models.User import User, UserTMP
from ..schemas.users import UserData, UserUpdate, UserUpdateEmail, UserUpdateFloidClaveBancaria, \
    UserUpdateFloidClaveUnica, UserUpdateFloidClaveBancariaStatus, UserUpdateFloidClaveUnicaStatus, UserUpdateCaseId
from ..models.userPayload import UserBody
from ..auth.main import validate_token, UserSession
from ..database.conf import db_users
from datetime import datetime, timedelta

router = APIRouter()


@router.get("/{user_uuid}", response_description="Get user by id", summary="user")
async def get_user(user_uuid: uuid.UUID, current_user: UserSession = Depends(validate_token), database=Depends(db_users)):
    try:
        user = database.query(User).filter(User.uuid == user_uuid).first()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Error")
    else:
        if user is not None:
            return user_formatted(user, tmp=False)
        else:
            raise HTTPException(status_code=404, detail="User not found")

@router.get("/tmp/{user_uuid}", response_description="Get tmp user by id", summary="user")
async def get_user(user_uuid: uuid.UUID, current_user: UserSession = Depends(validate_token), database=Depends(db_users)):
    try:
        user = database.query(UserTMP).filter(UserTMP.uuid == user_uuid).first()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Error")
    else:
        if user is not None:
            return user_formatted(user, tmp = True)
        else:
            raise HTTPException(status_code=404, detail="User not found")

@router.get("/{email}/email", response_description="Get user by email", summary="user")
async def get_user_by_email(email: str, current_user: UserSession = Depends(validate_token), database=Depends(db_users)):
    try:
        user = database.query(User).filter(User.email == email.lower().strip()).first()
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
    else:
        if user is not None:
            return user_formatted(user, tmp=False)
        else:
            raise HTTPException(status_code=404, detail="User not found")


@router.get("/tmp/{email}/email", response_description="Get tmp user by email", summary="user")
async def get_user_by_email(email: str, current_user: UserSession = Depends(validate_token), database=Depends(db_users)):
    try:
        user = database.query(UserTMP).filter(UserTMP.email == email.lower().strip()).first()
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
    else:
        if user is not None:
            return user_formatted(user, tmp=True)
        else:
            raise HTTPException(status_code=404, detail="User not found")

@router.get("/{dni}/dni", response_description="Get user by dni", summary="user")
async def get_user_by_dni(dni: str, current_user: UserSession = Depends(validate_token), database=Depends(db_users)):
    try:
        user = database.query(User).filter(
            User.user_data['dniValidation']['dni'].astext == dni.lower().strip()
        ).first()
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
    else:
        if user is not None:
            return user_formatted(user, tmp=False)
        else:
            raise HTTPException(status_code=404, detail="User not found")


@router.post("/", response_description="Create new user", summary="user")
async def save_user(req: Request, user_body: UserBody,
                    current_user: UserSession = Depends(validate_token), database=Depends(db_users)):
    user = database.query(User).filter(User.email == user_body.email.lower().strip())

    if user.first() is not None:
        raise HTTPException(status_code=409, detail="Conflict: user already exist")

    new_user = User(
        email=user_body.email.lower().strip(),
        name=user_body.name,
        airtableID=user_body.airtableID,
        user_data=user_body.user_data
    )

    database.add(new_user)
    database.commit()

    return user_formatted(new_user, tmp=False)


@router.post("/tmp", response_description="Create new tmp user", summary="user")
async def save_user(req: Request, user_body: UserBody,
                    current_user: UserSession = Depends(validate_token), database=Depends(db_users)):
    filter_after = datetime.now() - timedelta(minutes=45)

    user = database.query(UserTMP).filter(UserTMP.email == user_body.email.lower().strip(),
                                          UserTMP.createdAt > filter_after)

    if user.first() is not None:
        existing_user = user.first()
        existing_user.email = user_body.email.lower().strip()
        existing_user.name = user_body.name
        existing_user.user_data = {**existing_user.user_data, **user_body.user_data}
        database.commit()
        return user_formatted(user.first(), tmp=True)

    new_user = UserTMP(
        email=user_body.email.lower().strip(),
        name=user_body.name,
        user_data=user_body.user_data
    )

    database.add(new_user)
    database.commit()

    return user_formatted(new_user, tmp=True)

@router.patch('/{user_uuid}/user_data', response_description="Update user params", summary="user")
async def join_output(user_uuid: uuid.UUID, body: UserData, current_user: UserSession = Depends(validate_token),
                      database=Depends(db_users)):
    user = database.query(User).filter(User.uuid == user_uuid)

    if user.first() is None:
        raise HTTPException(status_code=404, detail="Not found")

    original_user_data = user.first().user_data
    if original_user_data is None:
        original_user_data = {}

    user.update(
        {'user_data': {**original_user_data, **body.user_data}})
    database.commit()

    return user_formatted(user.first(), tmp=False)

@router.patch('/tmp/{user_uuid}/user_data', response_description="Update user params", summary="user")
async def join_output(user_uuid: uuid.UUID, body: UserData, current_user: UserSession = Depends(validate_token),
                      database=Depends(db_users)):
    user = database.query(UserTMP).filter(UserTMP.uuid == user_uuid)

    if user.first() is None:
        raise HTTPException(status_code=404, detail="Not found")

    original_user_data = user.first().user_data
    if original_user_data is None:
        original_user_data = {}

    user.update(
        {'user_data': {**original_user_data, **body.user_data}})
    database.commit()

    return user_formatted(user.first(), tmp=False)


@router.patch('/{user_uuid}/airtableID', response_description="Update User airtableID", summary="user")
async def join_output(user_uuid: uuid.UUID, body: UserUpdate, current_user: UserSession = Depends(validate_token),
                      database=Depends(db_users)):
    user = database.query(User).filter(User.uuid == user_uuid)

    if user.first() is None:
        raise HTTPException(status_code=404, detail="Not found")

    user.update(
        {'airtableID': body.airtableID})
    database.commit()

    return user_formatted(user.first(), tmp=False)


@router.patch('/{user_uuid}/email', response_description="Update User airtableID", summary="user")
async def join_output(user_uuid: uuid.UUID, body: UserUpdateEmail, current_user: UserSession = Depends(validate_token),
                      database=Depends(db_users)):
    user = database.query(User).filter(User.uuid == user_uuid)

    if user.first() is None:
        raise HTTPException(status_code=404, detail="Not found")

    user.update(
        {'email': body.email.lower().strip()})
    database.commit()

    return user_formatted(user.first(), tmp=False)


@router.patch('/{user_uuid}/floid/clave_bancaria', response_description="Update User Floid Status Bank Details",
              summary="user")
async def clave_bancaria(user_uuid: uuid.UUID, body: UserUpdateFloidClaveBancaria,
                         current_user: UserSession = Depends(validate_token),
                         database=Depends(db_users)):
    user = database.query(User).filter(User.uuid == user_uuid)

    if user.first() is None:
        raise HTTPException(status_code=404, detail="Not found")

    original_user_data = user.first().user_data

    if original_user_data is None:
        original_user_data = {}

    if 'floid_details' not in original_user_data:
        original_user_data['floid_details'] = {}

    if 'clave_bancaria' not in original_user_data['floid_details']:
        original_user_data['floid_details']['clave_bancaria'] = {}

    if body.bank not in original_user_data['floid_details']['clave_bancaria']:
        original_user_data['floid_details']['clave_bancaria'][body.bank] = {}

    original_user_data['floid_details']['clave_bancaria'][body.bank]['status'] = body.status

    if body.date is not None:
        original_user_data['floid_details']['clave_bancaria'][body.bank]['last_update'] = body.date

    global_status = 'finished'
    for key in original_user_data['floid_details']['clave_bancaria'].keys():
        if key != 'status':
            if 'status' in original_user_data['floid_details']['clave_bancaria'][key]:
                if original_user_data['floid_details']['clave_bancaria'][key]['status'] != 'finished':
                    global_status = 'processing'

    original_user_data['floid_details']['clave_bancaria']['status'] = global_status

    user.update(
        {
            'user_data': original_user_data
        }
    )
    database.commit()

    return user_formatted(user.first(), tmp=False)


@router.patch('/{user_uuid}/floid/clave_bancaria/status', response_description="Update User Floid General Status",
              summary="user")
async def update_clave_bancaria(user_uuid: uuid.UUID, body: UserUpdateFloidClaveBancariaStatus,
                                current_user: UserSession = Depends(validate_token),
                                database=Depends(db_users)):
    user = database.query(User).filter(User.uuid == user_uuid)

    if user.first() is None:
        raise HTTPException(status_code=404, detail="Not found")

    original_user_data = user.first().user_data

    if original_user_data is None:
        original_user_data = {}

    if 'floid_details' not in original_user_data:
        original_user_data['floid_details'] = {}

    if 'clave_bancaria' not in original_user_data['floid_details']:
        original_user_data['floid_details']['clave_bancaria'] = {}

    original_user_data['floid_details']['clave_bancaria']['status'] = body.status
    print({
        'user_data': original_user_data
    })
    user.update(
        {
            'user_data': original_user_data
        }
    )
    database.commit()

    return user_formatted(user.first(), tmp=False)


@router.patch('/{user_uuid}/floid/clave_unica/status', response_description="Update User Floid Clave Unica Status",
              summary="user")
async def update_clave_unica(user_uuid: uuid.UUID, body: UserUpdateFloidClaveUnicaStatus,
                             current_user: UserSession = Depends(validate_token),
                             database=Depends(db_users)):
    user = database.query(User).filter(User.uuid == user_uuid)

    if user.first() is None:
        raise HTTPException(status_code=404, detail="Not found")

    original_user_data = user.first().user_data

    if original_user_data is None:
        original_user_data = {}

    if 'floid_details' not in original_user_data:
        original_user_data['floid_details'] = {}

    if 'clave_unica' not in original_user_data['floid_details']:
        original_user_data['floid_details']['clave_unica'] = {}

    original_user_data['floid_details']['clave_unica']['status'] = body.status

    user.update(
        {
            'user_data': original_user_data
        }
    )
    database.commit()

    return user_formatted(user.first(), tmp=False)


@router.patch('/{user_uuid}/floid/clave_unica', response_description="Update User Floid Status Clave Unica Details",
              summary="user")
async def clave_unica(user_uuid: uuid.UUID, body: UserUpdateFloidClaveUnica,
                      current_user: UserSession = Depends(validate_token),
                      database=Depends(db_users)):
    user = database.query(User).filter(User.uuid == user_uuid)

    if user.first() is None:
        raise HTTPException(status_code=404, detail="Not found")

    original_user_data = user.first().user_data

    if original_user_data is None:
        original_user_data = {}

    if 'floid_details' not in original_user_data:
        original_user_data['floid_details'] = {}

    if 'clave_unica' not in original_user_data:
        original_user_data['floid_details']['clave_unica'] = {}

    original_user_data['floid_details']['clave_unica']['AFC'] = body.AFC
    original_user_data['floid_details']['clave_unica']['SII'] = body.SII
    original_user_data['floid_details']['clave_unica']['CMF'] = body.CMF
    original_user_data['floid_details']['clave_unica']['status'] = body.status

    if body.date is not None:
        original_user_data['floid_details']['clave_unica']['last_update'] = body.date

    user.update(
        {
            'user_data': original_user_data
        }
    )
    database.commit()

    return user_formatted(user.first(), tmp=False)


@router.patch('/tmp/{user_uuid}/floid/clave_unica', response_description="Update User Floid Status Clave Unica Details",
              summary="user")
async def clave_unica_TMP(user_uuid: uuid.UUID, body: UserUpdateFloidClaveUnica,
                      current_user: UserSession = Depends(validate_token),
                      database=Depends(db_users)):
    user = database.query(UserTMP).filter(UserTMP.uuid == user_uuid)

    if user.first() is None:
        raise HTTPException(status_code=404, detail="Not found")

    original_user_data = user.first().user_data

    if original_user_data is None:
        original_user_data = {}

    if 'floid_details' not in original_user_data:
        original_user_data['floid_details'] = {}

    if 'clave_unica' not in original_user_data:
        original_user_data['floid_details']['clave_unica'] = {}

    original_user_data['floid_details']['clave_unica']['AFC'] = body.AFC
    original_user_data['floid_details']['clave_unica']['SII'] = body.SII
    original_user_data['floid_details']['clave_unica']['CMF'] = body.CMF
    original_user_data['floid_details']['clave_unica']['status'] = body.status

    if body.date is not None:
        original_user_data['floid_details']['clave_unica']['last_update'] = body.date

    user.update(
        {
            'user_data': original_user_data
        }
    )
    database.commit()

    return user_formatted(user.first(), tmp=False)


@router.patch("/{user_uuid}/floid/case_id", response_description="Update User Case ID", summary="user")
async def update_case_id(user_uuid: uuid.UUID, body: UserUpdateCaseId,
                         current_user: UserSession = Depends(validate_token),
                         database=Depends(db_users)):
    user = database.query(User).filter(User.uuid == user_uuid)

    if user.first() is None:
        raise HTTPException(status_code=404, detail="Not found")

    original_user_data = user.first().user_data

    if original_user_data is None:
        original_user_data = {}

    if 'floid_cases_id' not in original_user_data:
        original_user_data['floid_cases_id'] = []
        original_user_data['floid_cases_id'].append({
            'case_id': body.case_id,
            'notification_type': body.notification_type,
            'uuid': body.uuid
        })
        user.update(
            {
                'user_data': original_user_data
            }
        )
    else:
        case_id_found = False
        for case in original_user_data['floid_cases_id']:
            if case['case_id'] == body.case_id:
                case['notification_type'] = body.notification_type
                case['uuid'] = body.uuid
                case_id_found = True

        if not case_id_found:
            original_user_data['floid_cases_id'].append(
                {
                    'case_id': body.case_id,
                    'notification_type': body.notification_type,
                    'uuid': body.uuid
                }
            )

        user.update(
            {
                'user_data': original_user_data
            }
        )

    database.commit()

    return user_formatted(user.first(), tmp=False)
