from messages.BroadcastMessage import BroadcastMessage


class ConnectConfirmation(BroadcastMessage):

    def __init__(self, sender, idTable):
        super().__init__(sender, content=idTable)

    def getSender(self):
        return self.sender

    def __str__(self) -> str:
        return f"ConnectConfirmation(sender={self.sender}, idTable={self.content})"
