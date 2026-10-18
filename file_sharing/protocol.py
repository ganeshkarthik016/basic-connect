
def parse_message(raw_message):
    if "|" not in raw_message:
        raise ValueError("Invalid message format")

    message_type, content = raw_message.split("|", 1)

    if not message_type:
        raise ValueError("Message type cannot be empty")

    return message_type, content
