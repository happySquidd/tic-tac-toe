thing = [3, 5, 4, 2]

class bleh():
    def __init__(self):
        lol = 5
        self.whatever()
        print(thing)

    def change_thing(self):
        for i in range(len(thing)):
            thing[i] = i

    def whatever(self):
        self.change_thing()
b = bleh()
print(thing)