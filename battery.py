class Battery:
    LOW_LEVEL = 20

    def __init__(self, level=100):
        self.level = level

    def drain(self, amount):
        self.level -=amount
        if self.level < 0:
            self.level = 0

    def is_low(self):
        return self.level <= self.LOW_LEVEL

    def charge(self, amount):
        self.level +=amount
        if self.level > 100:
            self.level = 100