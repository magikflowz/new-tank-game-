import turtle
import math
import random

class screensetup:
    screen = turtle.Screen()
    screen.title("Cup Battle")
    screen.setup(500,500)
    screen.setworldcoordinates(0,0,200.0,200.0)
    screen.tracer(0)  
    turtle.speed(0) 
    turtle.hideturtle()

class Grid:
    def __init__(self, size, cell_size):
        self.size = size
        self.cell_size = cell_size
        self.grid = [[False for _ in range(size)] for _ in range(size)]  # Initialize grid with no obstacles
        self.visible = True  # Initially, grid is visible
        self.screen = turtle.Screen()
        self.screen.setup(size * cell_size + 100, size * cell_size + 100)
        self.screen.tracer(0)
        self.pen = turtle.Turtle()
        self.pen.penup()
        self.pen.speed(0)
        self.screen.onclick(self.toggle_obstacle)
        self.screen.onkeypress(self.toggle_grid, "g")
        self.screen.onkeypress(self.increase_size, "+")
        self.screen.onkeypress(self.decrease_size, "-")
        self.screen.listen()
        self.draw()

    def toggle_obstacle(self, x, y):
        col = int((x + self.size * self.cell_size / 2) // self.cell_size)
        row = int((-y + self.size * self.cell_size / 2) // self.cell_size)
        if 0 <= row < self.size and 0 <= col < self.size:
            self.grid[row][col] = not self.grid[row][col]  # Toggle obstacle presence
            self.draw()

    def toggle_grid(self):
        self.visible = not self.visible
        self.draw()  # Call draw to update grid visibility

    def increase_size(self):
        self.size += 1
        self.reset_grid()

    def decrease_size(self):
        if self.size > 2:
            self.size -= 1
            self.reset_grid()

    def reset_grid(self):
        self.grid = [[False for _ in range(self.size)] for _ in range(self.size)]
        self.draw()

    def draw(self):
        self.pen.clear()
        self.pen.goto(-self.size * self.cell_size / 2, self.size * self.cell_size / 2)

        if self.visible:
            for row in range(self.size):
                for col in range(self.size):
                    if self.grid[row][col]:
                        self.pen.fillcolor("black")
                    else:
                        self.pen.fillcolor("white")
                    self.pen.begin_fill()
                    for _ in range(4):
                        self.pen.forward(self.cell_size)
                        self.pen.right(90)
                    self.pen.end_fill()
                    self.pen.forward(self.cell_size)
                self.pen.backward(self.size * self.cell_size)
                self.pen.right(90)
                self.pen.forward(self.cell_size)
                self.pen.left(90)

        self.screen.update()

# Example usage:
grid_size = 5  # Initial grid size
cell_size = 20
grid = Grid(grid_size, cell_size)

class Bullet:
    def __init__(self, x, y, angle, speed):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed

    def move(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

    def draw(self):
        turtle.pu()
        turtle.goto(self.x, self.y)
        turtle.pd()
        turtle.dot(5)  # Example representation, adjust as needed

class tanks:
    def __init__(self,x,y,angle,size,v,health,color,targetx,targety,rotate):
        self.x=x
        self.y=y
        self.size=size
        self.angle=angle
        self.v=v/2
        self.health=health
        self.color=color
        self.targetx=targetx
        self.targety=targety
        self.rotate=rotate

    def fire_bullet(self):
        bullet_speed = 5  # Adjust as needed
        # Create a bullet object based on tank's position and angle
        bullet = Bullet(self.x, self.y, self.angle, bullet_speed)
        return bullet
    
    def draw(self):
        turtle.color(self.color)
        turtle.pu()
        turtle.goto(self.x,self.y-self.size)
        turtle.pd()
        turtle.setheading(0)
        turtle.circle(self.size)
        turtle.pu()
        turtle.goto(self.x,self.y)
        turtle.pd()
        turtle.goto(self.x+math.cos(self.angle)*self.size * 1.5,self.y+math.sin(self.angle)*self.size *1.5)
               
    def move(self, tanks):
        self.allowmovement = True #Sets to True
        tempX = self.x + math.cos(self.angle)*self.v # Get current X coordinate
        tempY = self.y + math.sin(self.angle)*self.v # Get current Y coordinate

        # Check for collisions with tanks
        for tank in tanks:
            if tank is not self:
                distance = math.sqrt((tempX-tank.x)**2 + (tempY-tank.y)**2)
                if distance < (self.size + tank.size):
                    # Collision occurred - stop the tanks
                    self.allowmovement = False #moveing no longer allowed due to collision
                    return

        # Check for collisions with walls
        if (tempX > 0.0 and tempX < 200.0) and (tempY > 0.0 and tempY < 200.0) and self.allowmovement is True:
            self.x = tempX
            self.y = tempY
            self.angle += self.rotate
        else:
            # Collision occurred - stop the tank in the direction of the wall
            if tempX <= 0.0 or tempX >= 200.0:
                self.rotate = -self.rotate
            if tempY <= 0.0 or tempY >= 200.0:
                self.rotate = -self.rotate
            self.v = 0

    def target(self, x,y):
        self.targetx=x
        self.targety=y

    def ai(self):
        self.angle = math.atan2(self.targety - self.y, self.targetx - self.x) #takes current x,y cords and subtracts it from the player to find what angle the AI needs to face

    def controlrotation(self,rotate):
        self.rotate=rotate

    def controlvelocity(self,velocity):
        self.v=velocity    

class keyboard:
    def __init__(self,tank):
        keyboard.tank = tank
        keyboard.end = False
        screensetup.screen.listen()
        screensetup.screen.onkeypress(self.kmove, "Up")
        screensetup.screen.onkeyrelease(self.kstop, "Up")
        screensetup.screen.onkeypress(self.kleft, "Left")
        screensetup.screen.onkeyrelease(self.kleftstop, "Left")
        screensetup.screen.onkeypress(self.kright, "Right")
        screensetup.screen.onkeyrelease(self.krightstop, "Right")
        screensetup.screen.onkeypress(self.kfire, "space")  # Bind kfire to space bar event
        screensetup.screen.onkeypress(self.kend, "Escape")

    global bullets

    bullets = []

    def kfire(self):
        bullet = keyboard.tank.fire_bullet()
        bullets.append(bullet)
                       
    def kmove(self):  
        keyboard.tank.controlvelocity(.2)
    def kstop(self):
        keyboard.tank.controlvelocity(0)
    def kleft(self):
        keyboard.tank.controlrotation(.02)
    def kleftstop(self):
        keyboard.tank.controlrotation(0)
    def kright(self):
        keyboard.tank.controlrotation(-.02)
    def krightstop(self):
        keyboard.tank.controlrotation(0)
    def kend(self):
        keyboard.end=1

def calculate_distance(tank1, tank2):
    return math.sqrt((tank1.x - tank2.x)**2 + (tank1.y - tank2.y)**2)

def sort_tanks_by_distance(user, enemy):
    distances = []
    for i, tank in enumerate(enemy):
        distance = calculate_distance(user, tank)
        distances.append((i, distance))  # Storing tank index and its distance

    distances.sort(key=lambda x: x[1])  # Sort based on distance
    return distances

user=tanks(10,10,0,5,0,10,"blue",0,0,0)
keyboard(user)

numtanks= 4
enemy = [] 
for i in range(numtanks):    
    enemy+=[tanks(random.randint(5,195),random.randint(5,195),random.randint(0,360),5,0.15,10,"red",0,0,0)]

while not keyboard.end: 
    turtle.clear()

    for bullet in bullets:
        bullet.move()
        bullet.draw()
    
    for bullet in bullets:
        # Check for collisions with walls
        if bullet.x < 0 or bullet.x > 200 or bullet.y < 0 or bullet.y > 200:
            bullets.remove(bullet)
            continue
    
    # Check for collisions with tanks
        for tank in enemy:
            distance = math.sqrt((bullet.x - tank.x)**2 + (bullet.y - tank.y)**2)
            if distance < tank.size:
                bullets.remove(bullet)
                # Handle tank hit, e.g., reduce health
                tank.health -= 1
                if tank.health <= 0:
                    enemy.remove(tank)
                break

    sorted_distances = sort_tanks_by_distance(user, enemy)

    # Move and draw enemy tanks; allows each enemy tank to check for collisions 
    # with all the other tanks in the game, including the user tank
    for i in sorted_distances:
        tank_index = i[0]  # Index of the tank
        tank = enemy[tank_index]
        tank.target(user.x,user.y)
        tank.move(enemy+[user])
        tank.ai()
        tank.draw()
        print("Tank: 1", "Distance:", i[0:0],"\r", "\n", "Tank: 2", "Distance:", i[0:1],"\r", "\n", "Tank: 3", "Distance:", i[0:2],"\r", "\n","Tank: 4", "Distance:", i[0:3],end = "\r")


    # Move and draw user tank; allows the user tank to check for collisions 
    # with all the enemy tanks, in addition to checking for collisions with the walls.
    user.move(enemy+[user])
    user.draw()

    screensetup.screen.update()
