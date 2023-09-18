from messages.Message import Message


class TargetMessage(Message):

    def __init__(self, sender, target, content=None, type="ASYNC"):
        super().__init__(sender, content, type)
        self.target = target

    def getTarget(self):
        return self.target

    def isForMe(self, me):
        return self.target == me

    def __str__(self) -> str:
        return f"TargetMessage(sender={self.sender}, target={self.target}, content={self.content}, clock={self.clock})"
