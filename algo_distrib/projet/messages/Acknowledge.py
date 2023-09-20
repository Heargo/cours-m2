from messages.TargetMessage import TargetMessage


class Acknowledge(TargetMessage):

    def __init__(self, sender, target, id):
        super().__init__(sender, target, content=id)

    def __str__(self) -> str:
        return f"Acknowledge(sender={self.sender}, target={self.target}, msgId={self.content})"
