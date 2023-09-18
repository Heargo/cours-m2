from messages.Message import Message


class BroadcastMessage(Message):

    def __init__(self, sender, content=None, type="ASYNC"):
        super().__init__(sender, content, type)

    def __str__(self) -> str:
        return f"BroadcastMessage(sender={self.sender}, content={self.content}, clock={self.clock})"
