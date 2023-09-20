from messages.Message import Message


class Connect(Message):

    def __init__(self, sender, id):
        super().__init__(sender, content=id)

    def getSender(self):
        return self.sender

    def __str__(self) -> str:
        return f"Connect(sender={self.sender}, wantedId={self.content})"
