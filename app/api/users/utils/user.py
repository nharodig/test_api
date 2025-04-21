
def user_formatted(user, tmp=False):
    response = {
        "uuid": user.uuid if user else None,
        "email": user.email,
        "name": user.name,
        "airtableID": user.airtableID if hasattr(user,'airtableID') else None,
        "user_data": user.user_data if user.user_data else None,
        "createdAt": user.createdAt,
        "modifiedAt": user.modifiedAt,
        "tmp": tmp
    }
    return response
