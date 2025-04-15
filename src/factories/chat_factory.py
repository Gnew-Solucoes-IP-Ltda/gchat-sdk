from entities import Chat


def get_chat_instance(data: dict) -> Chat:
    chat_id = data.get('attendanceId')
    last_message_date = data.get('lastMessage', {}).get('utcDhMessage')
    is_me = data.get('lastMessage', {}).get('sender', {}).get('isMe')
    return Chat(
        id=chat_id,
        last_message_date=last_message_date,
        is_me=is_me
    )