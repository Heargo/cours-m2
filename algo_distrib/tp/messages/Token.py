from messages.TargetMessage import TargetMessage


class Token(TargetMessage):

    def __init__(self, sender, target):
        super().__init__(sender, target)

    def __str__(self) -> str:
        return f"TokenMessage(sender={self.sender}, target={self.target})"
