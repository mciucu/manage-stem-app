from establishment.errors.models import get_error
from establishment.errors.errors import ErrorList


class MyErrorList(ErrorList):
    INVALID_MESSAGE_CONTENT = get_error(message="Invalid message content")
    MESSAGE_NOT_EDITABLE = get_error(message="Message not editable")
    MESSAGE_LIMIT_EXCEEDED = get_error(message="Message limit exceeded")
    NEW_PRIVATE_CHAT_LIMIT_EXCEEDED = get_error(message="Too many private chats initiated")
