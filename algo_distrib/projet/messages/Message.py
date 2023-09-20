import uuid


class Message():

    def __init__(self, sender, content=None, type="ASYNC"):
        self.sender = sender
        self.content = content
        self.clock = 0
        self.type = type
        self.id = uuid.uuid4()

    def getId(self):
        return self.id

    def getContent(self):
        return self.content

    def getSender(self):
        return self.sender

    def isFromMe(self, me):
        return self.sender == me

    def getClock(self):
        return self.clock

    def setClock(self, clock):
        self.clock = clock

    def isAcknowledged(self):
        return self.acknowledged

    def markAcknowledged(self):
        self.acknowledged = True

    def __str__(self) -> str:
        return f"Message(sender={self.sender}, content={self.content}, clock={self.clock})"
