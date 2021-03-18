# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
from queue import PriorityQueue
import math
from math import copysign

STATE_SNEAK = 0
STATE_ESCAPE = 1
STATE_WALL_WAIT = 2
STATE_WALL_BREAK = 3
STATE_SURVIVE = 4

class TestCharacter(CharacterEntity):

    
    def __init__(self, name, avatar, x, y, varient = 1):
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


    """ Finds the exit of the board and returns it as a tuple"""
    def find_exit(self, wrld):
        for i in range(wrld.width()):
            for j in range(wrld.height()):
                if wrld.exit_at(i,j):
                    return (i,j)

    """ Takes the turn of the character. Uses the specified method with varient"""
    def do(self, wrld):
        # Your code here
        if self.goal is None:
            self.goal = self.find_exit(wrld)
        if self.varient == 1:
            self.astar(wrld)
        else:
            self.state_machine(wrld)
        pass

    """ Will find the path to the exit using astar. If the path has already been found it will just follow it. """
    def astar(self, wrld):
        # Path already found, follow it
        if len(self.path) > 0:
            self.smart_follow(wrld)
        # Path hasn't been found, or was erased due to smart_follow, find it
        # Truely is a basic boring A*
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
                                if next not in cost_so_far.keys() or new_cost < cost_so_far[next]:
                                    cost_so_far[next] = new_cost
                                    priority = new_cost + self.diag_dist(wrld, next)
                                    frontier.put((priority, (next[0], next[1])))
                                    came_from[next] = current
            # We got to the exit, make a path from the current location to the exit and follow it
            if reached_goal:
                self.create_path(came_from)
                self.smart_follow(wrld)
            # Didn't get to the exit (walls blocking). Make and follow a path to the location closest to the exit and then place a bomb
            else:
                closest = self.closest_reached(came_from, wrld)
                self.create_path_dest(came_from,(self.x,self.y),closest)
                self.path.append("bomb")
                self.smart_follow(wrld)


    # Finds the diagonal distance from loc (tuple (x,y) of next location) to the exit
    def diag_dist(self, wrld, loc):
        return max(abs(loc[0]-wrld.width()-1), abs(loc[1]-wrld.height()-1))

    
    """ Creates a path for the character to follow to the exit.  Uses the came_from dictionary from astar """
    def create_path(self, came_from):
        next = self.goal
        # Continue making path backwards until we get to current location
        while next != (self.x, self.y):
            # Starting with exit and working to current location, so we need to insert at the front of the list
            self.path.insert(0,next)
            next = came_from[next]
                    
    """ Follows the path self.path by taking the first element in the list as the next location to goto and remove it from the list """
    def follow_path(self, wrld):
        if len(self.path) > 0:
            next = self.path[0]
            self.path.remove(next)
            # Next thing in the list is a location, go there
            if next != "bomb":
                self.move(next[0]-self.x, next[1]-self.y)
            elif len(self.bombs) == 0:
                # Going to place bomb, want to move out of blast zone
                # Need to stay out for bomb_time + expl_duration + 1 because wall is removed as expl ends
                for i in range(wrld.bomb_time + wrld.expl_duration + 2):
                   if(self.x != 0):
                        self.path.append((self.x-1, self.y-1))
                   else:
                       self.path.append((self.x+1, self.y-1))
                self.bomb(wrld)

    """ Finds the location (x,y) that is closest to the exit. """
    def closest_reached(self, came_from, wrld):
        visited = came_from.keys()
        closest = None
        dist = sys.maxsize
        for loc in visited:
            nextDist = self.diag_dist(wrld, loc)
            if nextDist <= dist:
                dist = nextDist
                closest = loc
        return closest

    
    """ Creates a path from start to end using came_from dictionary created in astar """
    def create_path_dest(self, came_from, start, end):
        next = end
        while next != start:
            self.path.insert(0,next)
            next = came_from[next]

    
    """ Takes the next location in the path, it will look around for monsters and explosions 
        and act in a way that will prevent it from dying.  If there is nothing wrong with where we want to go then
        we will follow it like the board were empty using follow_path() above.  If the next step is to place 
        a bomb one is place where the character is and it then checks its surroundings to see if its 
        current location is safe to stay at. """
    def smart_follow(self, wrld):
        self.update_bombs()
        next = self.path[0]
        # Next thing to do is place a bomb, do it
        if next == "bomb":
            self.path.remove(next)
            self.bomb(wrld)
            next = (self.x, self.y)
        look_for_bombs = True
        dx = next[0] - self.x
        dy = next[1] - self.y
        # Find any monsters around the location we want to move to
        monster = self.check_for_monsters(next[0], next[1], wrld)
        # If there is one we need to find a different place to go
        if monster:
            # The best place to go. If it doesn't exist stay here and excpet fait
            next = self.find_good_cell(monster, wrld)
            if not next:
                look_for_bombs = True
                next = (self.x, self.y)
            # we will drop a bomb to try and kill monster and move to the spot found
            else:
                self.bomb(wrld)
                self.path.clear()
                self.move(next[0]-self.x, next[1]-self.y)
                return
        # If there isn't a monster near we need to check for explosions in our next location
        if look_for_bombs and (self.check_bombs(next, wrld) or (wrld.wall_at(next[0], next[1]) and self.check_bombs((self.x, self.y), wrld))):
            for i in range(-1,2):
                for j in range(-1,2):
                    check_x = self.x + i
                    check_y = self.y + j
                    # Check to see if (check_x, check_y) is on the board
                    if check_x >= 0 and check_x < wrld.width() and check_y >= 0 and check_y < wrld.height() and \
                            not wrld.wall_at(check_x, check_y):
                        # If the location (check_x, check_y) is not in an explosion go there
                        if not self.check_bombs((check_x, check_y), wrld):
                            self.path.clear()
                            self.move(i,j)
                            return
        # We didn't find any problems with our next location so follow our initial path
        self.follow_path(wrld)

    # Places a bomb and adds it to the list of bombs
    def bomb(self, wrld):
        if len(self.bombs) == 0:
            self.bombs.append((self.x, self.y, wrld.bomb_time))
            self.place_bomb()

    # Updates the counter on all of the bombs in the bomb list
    def update_bombs(self):
        if len(self.bombs) > 0:
            old_bomb = self.bombs[0]
            self.bombs[0] = (old_bomb[0], old_bomb[1], old_bomb[2]-1)
            if self.bombs[0][2] < -3:
                self.bombs.clear()

    """ Checks the location next to see if it will be where a bomb is going to or is currently exploding """
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

    """ Checks for monsters within 4 cells of the loction (x,y).  If there is one it returns the tuple location of that monster
        if there isn't a monster return null """
    def check_for_monsters(self, x, y, wrld):
        monster = None
        for i in range(-4, 5):
            for j in range(-4, 5):
                check_x = x + i
                check_y = y + j
                if wrld.monsters_at(check_x, check_y):
                    monster = check_x,check_y
        return monster

    """ Finds the best cell to move to if there is a monster near by.  Does so by finding the cell that is the furthest from the monster
        and closest to the middle.  We go as far from the monster as possible because the worst thing that can happen is we die, 
        we go to the middle because there will be less of a chance that we get caught in a corner."""
    def find_good_cell(self, monster, wrld):
        furthest_dist_monster = max(abs(self.x - monster[0]), abs(self.y - monster[1]))
        viable = []
        for dx in range(-1,2):
            x = self.x + dx
            if 0 <= x < wrld.width():
                for dy in range(-1, 2):
                    y = self.y + dy
                    if 0 <= y < wrld.height() and not wrld.wall_at(x,y) and not self.check_bombs((x,y),wrld):
                        cur_dist_monster = max(abs(x-monster[0]), abs(y-monster[1]))
                        if cur_dist_monster > furthest_dist_monster:
                            viable.clear()
                            furthest_dist_monster = cur_dist_monster
                            viable.append((x,y))
                        elif cur_dist_monster == furthest_dist_monster:
                            viable.append((x,y))
        best = None
        for loc in viable:
            if not best:
                best = loc
            else:
                if abs(loc[0] - 3.5) < abs(best[0] - 3.5):
                    best = loc
        return best

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
