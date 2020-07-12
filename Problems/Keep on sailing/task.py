# our class Ship
class Ship:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity
        self.cargo = 0

    # the old sail method that you need to rewrite
    def sail(self, where):
        print(f"The {self.name} has sailed for {where}!")


black_pearl = Ship("Black Pearl", 800)
where = input()
black_pearl.sail(where)
