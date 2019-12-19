
class Moon:
    def __init__(self, x,y,z):
        self.x = x
        self.y = y
        self.z = z
        self.vx = 0
        self.vy = 0
        self.vz = 0

    @staticmethod
    def _dv(self_v, moon_v):
        if self_v == moon_v:
            return 0
        elif self_v > moon_v:
            return -1
        else:
            return 1
        
    def calc_v(self, moons):
        self.vx += sum(self._dv(self.x, moon.x) for moon in moons)
        self.vy += sum(self._dv(self.y, moon.y) for moon in moons)
        self.vz += sum(self._dv(self.z, moon.z) for moon in moons)

    def step(self):
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz


    
    def print(self):
        print(f"{self.x:>3}  {self.y:>3}  {self.z:>3}        -     "
              f"{self.vx:>3}  {self.vy:>3}  {self.vz:>3}")

    def energy(self):
        pot = [self.x, self.y, self.z]
        kin = [self.vx, self.vy, self.vz]
        return sum(map(abs, pot)) * sum(map(abs, kin))
        

m0 = Moon(x=6, y=10, z=10)
m1 = Moon(x=-9, y=3, z=17)
m2 = Moon(x=9, y=-4, z=14)
m3 = Moon(x=4, y=14, z=4)

steps = 1000

m0 = Moon(x=-1, y=0, z=2)
m1 = Moon(x=2, y=-10, z=-7)
m2 = Moon(x=4, y=-8, z=8)
m3 = Moon(x=3, y=5, z=-1)

steps = 10


m0 = Moon(x=-8, y=-10, z=0)
m1 = Moon(x=5, y=5, z=10)
m2 = Moon(x=2, y=-7, z=3)
m3 = Moon(x=9, y=-8, z=-3)

steps = 100



moons = [m0, m1, m2, m3]


def move(moons):
    for moon in moons:
        moon.calc_v(moons)

    for moon in moons:
        moon.step() 
        moon.print()
    print()


for moon in moons:
    moon.print()
print()

for i in range(steps):
    move(moons)

print(sum(moon.energy() for moon in moons))
