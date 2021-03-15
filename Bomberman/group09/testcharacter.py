# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
from queue import PriorityQueue
from math import copysign

class TestCharacter(CharacterEntity):

    
    def __init__(self, name, avatar, x, y, varient):
        CharacterEntity.__init__(self, name, avatar, x, y)
        self.varient = varient
        self.path = []
        # (x,y) tuple for location of the exit
        self.goal = None
        self.bombs = []


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
        elif self.varient == 2:
            self.minimax()
        elif self.varient >= 3:
            self.expectimax()
        pass


    def astar(self, wrld):
        if len(self.path) > 0:
            self.smart_follow(wrld)
        else:
            print("Need to find a new path")
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
            # if len(self.path) > 1 and (self.path[0] != "bomb" and self.path[1] != "bomb"):
            #     old_dx = self.path[1][0] - self.path[0][0]
            #     cur_dx = self.path[0][0] - next[0]
            #     print(old_dx, cur_dx)
            #     if old_dx != cur_dx:
            #         self.path.insert(0,"bomb")
        

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
        self.update_bombs()
        next = self.path[0]
        if next == "bomb":
            self.follow_path(wrld)
            return
        look_for_bombs = True
        dx = next[0] - self.x
        dy = next[1] - self.y
        monster = self.check_for_monsters(next[0], next[1], wrld)
        print(monster)
        if monster:
            # look_for_bombs = False
            # self.path.clear()
            # # There is a monster too close to where I want to go
            # # look 1 around where I currently am for the spot closest to the exit
            # # that is at least 3 from the monster, and isn't a wall or out of bounds
            # closest = sys.maxsize
            # direction = (int(copysign(1,self.x - monster[0])),int(copysign(1,self.y-monster[1])))
            # for i in range(-1,2):
            #     if 0 <= self.x + i < wrld.width():
            #         for j in range(-1, 2):
            #             if 0 <= self.y + j < wrld.height() and not wrld.wall_at(self.x + i, self.y + j) and \
            #                     not self.check_bombs((self.x+i, self.y+j), wrld):
            #                 new_dist = self.diag_dist(wrld, (self.x + i, self.y + j))
            #                 dist_to_monster = max(abs(self.x - monster[0]), abs(self.y - monster[1]))
            #                 print("Dist to Monster:", dist_to_monster)
            #                 print("Dist to exit:", new_dist)
            #                 if dist_to_monster >= 4 and new_dist < closest:
            #                     direction = (i,j)
            if self.y - monster[1] != 0:
                dx = int(copysign(1,3.5-self.x))
            else:
                dx = int(copysign(1,self.x - monster[0]))
            dy = int(copysign(1,self.y - monster[1]))
            # Make sure we are moving and not just pushing against a wall
            if self.x + dx < 0 or self.x + dx >= wrld.width():
                dx = 0
            if self.y + dy < 0 or self.y + dy >= wrld.height():
                dx = int(copysign(1, self.x - monster[0]))
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
            self.bomb(wrld)
            self.path.clear()
            self.move(dx, dy)

            return
        if self.check_bombs(next, wrld) and look_for_bombs:
            for i in range(-1,2):
                for j in range(-1,2):
                    check_x = self.x + i
                    check_y = self.y + j
                    if check_x >= 0 and check_x < wrld.width() and check_y >= 0 and check_y < wrld.height() and \
                            not wrld.wall_at(check_x, check_y):
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

    def check_for_monsters(self, x, y, wrld):
        for i in range(-3, 4):
            for j in range(-3, 4):
                check_x = x + i
                check_y = y + j
                if wrld.monsters_at(check_x, check_y):
                    return check_x,check_y
        return None

    def minimax(self):
        pass

    def expectimax(self):
        pass


