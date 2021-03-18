# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
from queue import PriorityQueue
from math import copysign

STATE_SNEAK = 0
STATE_ESCAPE = 1
STATE_WALL_WAIT = 2
STATE_WALL_BREAK = 3
STATE_SURVIVE = 4

class TestCharacter(CharacterEntity):

    def __init__(self, name, avatar, x, y, varient):
        CharacterEntity.__init__(self, name, avatar, x, y)
        self.varient = varient
        self.path = []
        # (x,y) tuple for location of the exit
        self.goal = None
        self.bombs = []
        self.toBomb = (4, 2)
        self.newbomb_flag = 0
        self.old_state = None
        self.timer = -1
        self.state = STATE_SNEAK


    def find_exit(self, wrld):
        for i in range(wrld.width()):
            for j in range(wrld.height()):
                if wrld.exit_at(i,j):
                    return (i,j)


    def do(self, wrld):
        # Your code here
        if self.goal is None:
            self.goal = self.find_exit(wrld)
        if self.varient == 1:
            self.astar(wrld)
        else:
            self.state_machine(wrld)
        pass



    def state_machine(self, wrld):
        self.timer = self.timer -1
        self.state = self.find_new_state(wrld)

        print("Current State: " + str(self.state))
        print("Timer: " + str(self.timer))
        print("Char Pos: (" + str(self.x) + ", " + str(self.y) + ")")
        if self.state == STATE_ESCAPE:
            self.activate_escape(wrld)
        if self.state == STATE_SURVIVE:
            self.activate_survive(wrld)
        if self.state == STATE_SNEAK:
            self.activate_sneak(wrld)
        if self.state == STATE_WALL_BREAK:
            self.activate_break(wrld)
        if self.state == STATE_WALL_WAIT:
            self.activate_wait(wrld)

    def activate_escape(self, world):
        self.astar(world)

    def activate_survive(self, world):
        for dx in [-1, 0, 1]:
            if (self.x + dx >= 0) and (self.x + dx < world.width()):
                for dy in [-1, 0, 1]:
                    if (self.y + dy >= 0) and (self.y + dy < world.height()):
                        if (not world.wall_at(self.x + dx, self.y + dy)) and (not world.monsters_at(self.x + dx, self.y+dy)):
                            if self.timer <= 5 and self.timer >= -1:
                                if (self.x + dx != self.toBomb[0]) and (self.y + dy != self.toBomb[1]):
                                    self.move(dx, dy)
                            else:
                                self.move(dx, dy)

    def activate_sneak(self, world):
        if self.toBomb is None:
            dx = 0
            x = 0
            y = self.y
            while y < world.height():
                x = 0
                while x < world.width():
                    if not world.wall_at(x, y):
                        dy = 1
                        j = 1
                        while j < 4:
                            if world.wall_at(x, y + j*dy):
                                self.toBomb = (x, y)
                                print("New Bomb will be placed at (" + str(x) + ", " + str(y) + ")")
                                if x > self.x:
                                    dx = 1
                                elif x == self.x:
                                    dx = 0
                                else:
                                    dx = -1
                                if y < self.y:
                                    dy = -1
                                elif y == self.y:
                                    dy = 0
                                else:
                                    dy = 1
                                self.move(dx, dy)
                                return
                            j= j+1
                    x = x + 1
                y = y + 1
        else:
            x = self.toBomb[0]
            y = self.toBomb[1]
            print("Bomb at (" + str(x) + ", " + str(y) + ")")
            dx = 0
            dy = 0
            if x > self.x:
                dx = 1
            elif x == self.x:
                dx = 0
            else:
                dx = -1
            if y < self.y:
                dy = -1
            elif y == self.y:
                dy = 0
            else:
                dy = 1
            self.move(dx, dy)
            return


    def activate_break(self, world):
        self.toBomb = (self.x, self.y)
        self.place_bomb()
        self.newbomb_flag = 1
        self.activate_wait(world)
        self.state = STATE_WALL_WAIT

    def activate_wait(self, world):
        if self.newbomb_flag:
            self.timer = 14
            self.newbomb_flag = 0
        # modified from sample code on github. Link: https://github.com/eahatton/CS4341/tree/master/Bomberman
        for dx in [-1, 0, 1]:
            # Avoid out-of-bound indexing
            if (self.x + dx >= 0) and (self.x + dx < world.width()):
                # Loop through delta y
                for dy in [-1, 0, 1]:
                    # Avoid out-of-bound indexing
                    if (self.y + dy >= 0) and (self.y + dy < world.height()):
                        # No need to check impossible moves
                        if not world.wall_at(self.x + dx, self.y + dy):
                            if self.timer < 6 and self.timer >= 0:
                                if ((self.x + dx != self.toBomb[0]) and (self.y + dy != self.toBomb[1])):
                                    # Set move in wrld
                                    self.move(dx, dy)
                            else:
                                self.move(dx, dy)
        if self.timer == 0:
            self.toBomb = None

    def find_new_state(self, wrld):
        current = self.state
        if current == STATE_ESCAPE or self.canEscape(wrld):
            return STATE_ESCAPE
        if not self.isSafe(wrld):
            if self.state != STATE_SURVIVE:
                self.old_state = self.state
            return STATE_SURVIVE
        if current == STATE_SURVIVE:
            return self.old_state
        if current == STATE_WALL_BREAK:
            return STATE_WALL_WAIT
        if current == STATE_WALL_WAIT and self.timer < 0:
            return STATE_SNEAK
        elif current == STATE_WALL_WAIT:
            return STATE_WALL_WAIT
        if current == STATE_SNEAK and self.toBomb is None:
            return STATE_SNEAK
        if current == STATE_SNEAK and self.x == self.toBomb[0] and self.y == self.toBomb[1]:
            return STATE_WALL_BREAK
        else:
            return STATE_SNEAK



    def isSafe(self, world):
        y = self.y - 2
        while y < self.y + 2:
            x = self.x - 2
            while x < self.x + 2:
                if world.monsters_at(x, y):
                    return False
                x = x + 1
            y = y + 1
        return True


    def canEscape(self, world):
        x = 0
        y = 0
        num = 0
        while x < world.width():
            y = 0
            while y < world.height():
                if world.monsters_at(x, y):
                    if self.y - y <= 1:
                        num = num + 1
                y = y + 1
            x = x + 1
        if num == 0:
            return True
        else:
            return False

    def astar(self, wrld):
        if self.path:
            self.smart_follow(wrld)
        else:
            frontier = PriorityQueue()
            # priority queue will be (priority,(x,y))
            frontier.put((0,(self.x,self.y)))
            came_from = dict()
            cost_so_far = dict()
            came_from[(self.x,self.y)] = None
            cost_so_far[(self.x,self.y)] = 0
            reached_goal = False

            while not frontier.empty():
                # current is tuple (x,y)
                cur = frontier.get()[1]
                current = (cur[0], cur[1])

                if wrld.exit_at(current[0], current[1]):
                    reached_goal = True
                    break

                for dx in range(-1,2):
                    if (current[0] + dx) < wrld.width() and (current[0] + dx) >= 0:
                        for dy in range(-1,2):
                            # dont bother if we are out of bounds, at a wall, or the same as current
                            if (current[1] + dy) < wrld.height() and (current[1] + dy) >= 0 and (not wrld.wall_at(current[0]+dx,current[1]+dy)) and not (dx == 0 and dy == 0):
                                next = (current[0]+dx, current[1]+dy)
                                # Cost to move one square is always 1
                                new_cost = cost_so_far[current] + 1
                                if next not in cost_so_far.keys()  or new_cost <= cost_so_far[next]:
                                    cost_so_far[next] = new_cost
                                    priority = new_cost + self.diag_dist(wrld, next)
                                    frontier.put((priority, (next[0], next[1])))
                                    came_from[next] = current

            if reached_goal:
                self.create_path(came_from)
                self.smart_follow(wrld)
            else:
                closest = self.closest_reached(came_from, wrld)
                self.create_path_dest(came_from,(self.x,self.y),closest)
                self.path.append("bomb")
                self.smart_follow(wrld)


    # Finds the diagonal distance from loc (tuple (x,y) of next location) to the exit
    def diag_dist(self, wrld, loc):
        return max(abs(loc[0]-wrld.width()-1), abs(loc[1]-wrld.height()-1))


    def create_path(self, came_from):
        next = self.goal
        while next != (self.x, self.y):
            self.path.insert(0,next)
            next = came_from[next]
        

    def follow_path(self, wrld):
        next = self.path[0]
        self.path.remove(next)
        if next != "bomb":
            self.move(next[0]-self.x, next[1]-self.y)
        else:
            # Going to place bomb, want to move out of blast zone
            # Need to stay out for bomb_time + expl_duration + 1 because wall is removed as expl ends
            for i in range(wrld.bomb_time + wrld.expl_duration + 2):
               if(self.x != 0):
                    self.path.append((self.x-1, self.y-1))
               else:
                   self.path.append((self.x+1, self.y-1))
            self.bomb(wrld)


    def closest_reached(self, came_from, wrld):
        visited = came_from.keys()
        closest = None
        dist = sys.maxsize
        for loc in visited:
            nextDist = self.diag_dist(wrld, loc)
            if nextDist < dist:
                dist = nextDist
                closest = loc
        return closest


    def create_path_dest(self, came_from, start, end):
        next = end
        while next != start:
            self.path.insert(0,next)
            next = came_from[next]


    def smart_follow(self, wrld):
        print(self.path)
        self.update_bombs()
        next = self.path[0]
        if next == "bomb":
            self.follow_path(wrld)
            return
        dx = next[0] - self.x
        dy = next[1] - self.y
        for i in range(-2, 3):
            for j in range(-2, 3):
                check_x = next[0] + i
                check_y = next[1] + j
                if wrld.monsters_at(check_x, check_y):
                    self.path.clear()
                    if j != 0:
                        dx = int(copysign(1,3.5-self.x))
                    else:
                        dx = int(copysign(1,-i))
                    dy = int(copysign(1,-j))
                    # Make sure we are moving and not just pushing against a wall
                    if self.x + dx < 0 or self.x + dx >= wrld.width():
                        dx = 0
                    if self.y + dy < 0 or self.y + dy >= wrld.height():
                        dx = int(copysign(1,-i))
                        dy = 0

                    # Check if monster is pushing you into an explosion
                    if self.check_bombs((self.x + dx, self.y + dy), wrld):
                        if not self.check_bombs((self.x, self.y + dy), wrld):
                            dx = 0
                        elif not self.check_bombs((self.x + dx, self.y), wrld):
                            dy = 0
                        else:
                            dx = 0
                            dy = 0
                        if self.x + dx < 0 or self.x + dx >= wrld.width() and self.check_bombs((self.x, self.y), wrld):
                            dx = -dx
                        if self.y + dy < 0 or self.y + dy >= wrld.height() and self.check_bombs((self.x, self.y), wrld):
                            dy = -dy
                    if self.x + dx < 0 or self.x + dx >= wrld.width():
                        dx = 0
                    if self.y + dy < 0 or self.y + dy >= wrld.height():
                        dy = 0
                    if wrld.wall_at(self.x + dx, self.y + dy):
                        if not wrld.wall_at(self.x, self.y + dy):
                            dx = 0
                        elif not wrld.wall_at(self.x + dx, self.y):
                            dy = 0

                    self.path.clear()
                    self.move(dx, dy)
                    self.bomb(wrld)
                    return
        if self.check_bombs(next, wrld):
            for i in range(-1,2):
                for j in range(-1,2):
                    check_x = self.x + i
                    check_y = self.y + j
                    if check_x >= 0 and check_x < wrld.width() and check_y >= 0 and check_y < wrld.height() and not wrld.wall_at(check_x, check_y):
                        if not self.check_bombs((check_x, check_y), wrld):
                            self.path.clear()
                            self.move(i,j)
                            return
        self.follow_path(wrld)

    def bomb(self, wrld):
        if len(self.bombs) == 0:
            self.bombs.append((self.x, self.y, wrld.bomb_time))
            self.place_bomb()

    def update_bombs(self):
        if len(self.bombs) > 0:
            old_bomb = self.bombs[0]
            self.bombs[0] = (old_bomb[0], old_bomb[1], old_bomb[2]-1)
            if self.bombs[0][2] < -3:
                self.bombs.clear()

    def check_bombs(self, next, wrld):
        if not (len(self.bombs) > 0):
            return False
        bomb_x = self.bombs[0][0]
        bomb_y = self.bombs[0][1]
        if next[0] == bomb_x and bomb_y - wrld.expl_range <= next[1] and bomb_y + wrld.expl_range >= next[1] and self.bombs[0][2] <= 0:
            return True
        if next[1] == bomb_y and bomb_x - wrld.expl_range <= next[0] and bomb_x + wrld.expl_range >= next[0] and self.bombs[0][2] <= 0:
            return True
        return False


    def state_machine(self, wrld):
        self.timer = self.timer -1
        self.state = self.find_new_state(wrld)

        print("Current State: " + str(self.state))
        print("Timer: " + str(self.timer))
        print("Char Pos: (" + str(self.x) + ", " + str(self.y) + ")")
        if self.state == STATE_ESCAPE:
            self.activate_escape(wrld)
        if self.state == STATE_SURVIVE:
            self.activate_survive(wrld)
        if self.state == STATE_SNEAK:
            self.activate_sneak(wrld)
        if self.state == STATE_WALL_BREAK:
            self.activate_break(wrld)
        if self.state == STATE_WALL_WAIT:
            self.activate_wait(wrld)

    def activate_escape(self, world):
        self.astar(world)

    def activate_survive(self, world):
        for dx in [-1, 0, 1]:
            if (self.x + dx >= 0) and (self.x + dx < world.width()):
                for dy in [-1, 0, 1]:
                    if (self.y + dy >= 0) and (self.y + dy < world.height()):
                        if (not world.wall_at(self.x + dx, self.y + dy)) and (not world.monsters_at(self.x + dx, self.y+dy)):
                            if self.timer <= 5 and self.timer >= -1:
                                if (self.x + dx != self.toBomb[0]) and (self.y + dy != self.toBomb[1]):
                                    self.move(dx, dy)
                            else:
                                self.move(dx, dy)

    def activate_sneak(self, world):
        if self.toBomb is None:
            dx = 0
            x = 0
            y = self.y
            while y < world.height():
                x = 0
                while x < world.width():
                    if not world.wall_at(x, y):
                        dy = 1
                        j = 1
                        while j < 4:
                            if world.wall_at(x, y + j*dy):
                                self.toBomb = (x, y)
                                print("New Bomb will be placed at (" + str(x) + ", " + str(y) + ")")
                                if x > self.x:
                                    dx = 1
                                elif x == self.x:
                                    dx = 0
                                else:
                                    dx = -1
                                if y < self.y:
                                    dy = -1
                                elif y == self.y:
                                    dy = 0
                                else:
                                    dy = 1
                                self.move(dx, dy)
                                return
                            j= j+1
                    x = x + 1
                y = y + 1
        else:
            x = self.toBomb[0]
            y = self.toBomb[1]
            print("Bomb at (" + str(x) + ", " + str(y) + ")")
            dx = 0
            dy = 0
            if x > self.x:
                dx = 1
            elif x == self.x:
                dx = 0
            else:
                dx = -1
            if y < self.y:
                dy = -1
            elif y == self.y:
                dy = 0
            else:
                dy = 1
            self.move(dx, dy)
            return


    def activate_break(self, world):
        self.toBomb = (self.x, self.y)
        self.place_bomb()
        self.newbomb_flag = 1
        self.activate_wait(world)
        self.state = STATE_WALL_WAIT

    def activate_wait(self, world):
        if self.newbomb_flag:
            self.timer = 14
            self.newbomb_flag = 0
        # modified from sample code on github. Link: https://github.com/eahatton/CS4341/tree/master/Bomberman
        for dx in [-1, 0, 1]:
            # Avoid out-of-bound indexing
            if (self.x + dx >= 0) and (self.x + dx < world.width()):
                # Loop through delta y
                for dy in [-1, 0, 1]:
                    # Avoid out-of-bound indexing
                    if (self.y + dy >= 0) and (self.y + dy < world.height()):
                        # No need to check impossible moves
                        if not world.wall_at(self.x + dx, self.y + dy):
                            if self.timer < 6 and self.timer >= 0:
                                if ((self.x + dx != self.toBomb[0]) and (self.y + dy != self.toBomb[1])):
                                    # Set move in wrld
                                    self.move(dx, dy)
                            else:
                                self.move(dx, dy)
        if self.timer == 0:
            self.toBomb = None

    def find_new_state(self, wrld):
        current = self.state
        if current == STATE_ESCAPE or self.canEscape(wrld):
            return STATE_ESCAPE
        if not self.isSafe(wrld):
            if self.state != STATE_SURVIVE:
                self.old_state = self.state
            return STATE_SURVIVE
        if current == STATE_SURVIVE:
            return self.old_state
        if current == STATE_WALL_BREAK:
            return STATE_WALL_WAIT
        if current == STATE_WALL_WAIT and self.timer < 0:
            return STATE_SNEAK
        elif current == STATE_WALL_WAIT:
            return STATE_WALL_WAIT
        if current == STATE_SNEAK and self.toBomb is None:
            return STATE_SNEAK
        if current == STATE_SNEAK and self.x == self.toBomb[0] and self.y == self.toBomb[1]:
            return STATE_WALL_BREAK
        else:
            return STATE_SNEAK



    def isSafe(self, world):
        y = self.y - 2
        while y < self.y + 2:
            x = self.x - 2
            while x < self.x + 2:
                if world.monsters_at(x, y):
                    return False
                x = x + 1
            y = y + 1
        return True


    def canEscape(self, world):
        x = 0
        y = 0
        num = 0
        while x < world.width():
            y = 0
            while y < world.height():
                if world.monsters_at(x, y):
                    if self.y - y <= 1:
                        num = num + 1
                y = y + 1
            x = x + 1
        if num == 0:
            return True
        else:
            return False
