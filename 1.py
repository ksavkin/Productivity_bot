from audioop import reverse


class car1():
    def __init__(self, x, r, w, name):
        self.x = x
        self.r = r
        self.w = w
        self.name = name
classik1 = car1(3, 2, 3, "car1")
class car2():
    def __init__(self, x, r, w, name):
        self.x = x
        self.r = r
        self.w = w
        self.name = name
classik2 = car2(4, 2, 3, "car2")

class car3():
    def __init__(self, x, r, w, name):
        self.x = x
        self.r = r
        self.w = w
        self.name = name
classik3 = car3(5, 2, 3, "car3")
sp = [classik1, classik2, classik3]

sp.sort(key=lambda x: x.x, reverse=True)

print(sp[0].name)