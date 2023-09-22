from messages.Message import Message


class Heartbit(Message):

    def __init__(self, sender):
        super().__init__(sender)

    def __str__(self) -> str:
        return f"Hearbit(sender={self.sender})"
