
def notification_formatted(notification):
    response = {
        "uuid": notification.uuid if notification else None,
        "created_at": notification.created_at,
        "updated_at": notification.updated_at
    }
    return response
