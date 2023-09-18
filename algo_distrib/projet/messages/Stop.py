from messages.Message import Message


class Stop(Message):

    def __init__(self, sender):
        super().__init__(sender)

    def getSender(self):
        return self.sender

    def __str__(self) -> str:
        return f"Stop(sender={self.sender})"
