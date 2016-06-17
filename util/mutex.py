class Mutex(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __ne__(self, check):
        return not self.__eq__()

    def __eq__(self, check):
        if (self.x == check.x) & (self.y == check.y):
            return True
        if (self.y == check.x) & (self.x == check.y):
            return True
        return False

    def __str__(self):
        return "Mutex("+self.x.nombre+", "+self.y.nombre+")"


