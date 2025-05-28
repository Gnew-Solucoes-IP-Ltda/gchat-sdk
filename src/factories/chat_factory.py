from entities import Chat, Contact


def get_contact_instance(data: dict) -> Contact:
    contact_id = data.get('contact', {}).get('id')
    name = data.get('contact', {}).get('name')
    number = data.get('contact', {}).get('number')
    return Contact(contact_id, name, number)


def get_chat_instance(data: dict) -> Chat:
    chat_id = data.get('attendanceId')
    last_message_date = data.get('lastMessage', {}).get('utcDhMessage')
    is_me = data.get('lastMessage', {}).get('sender', {}).get('isMe')
    return Chat(
        id=chat_id,
        last_message_date=last_message_date,
        is_me=is_me,
        contact=get_contact_instance(data)
    )