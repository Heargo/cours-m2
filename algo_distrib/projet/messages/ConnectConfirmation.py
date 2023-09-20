from messages.TargetMessage import TargetMessage


class ConnectConfirmation(TargetMessage):

    def __init__(self, sender, target, id):
        super().__init__(sender, target, content=id)

    def getSender(self):
        return self.sender

    def __str__(self) -> str:
        return f"ConnectConfirmation(sender={self.sender}, wantedId={self.content})"
