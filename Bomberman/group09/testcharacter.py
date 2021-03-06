# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
from queue import PriorityQueue

class TestCharacter(CharacterEntity):

    
    def __init__(self, name, avatar, x, y, varient):
        CharacterEntity.__init__(self, name, avatar, x, y)
        self.varient = varient
        self.path = []
        # (x,y) tuple for location of the exit
        self.goal = None


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
        if self.path:
            self.follow_path(wrld)
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
                                if next not in cost_so_far.keys()  or new_cost < cost_so_far[next]:
                                    cost_so_far[next] = new_cost
                                    priority = new_cost + self.diag_dist(wrld, next)
                                    frontier.put((priority, (next[0], next[1])))
                                    came_from[next] = current

            if reached_goal:
                self.create_path(came_from)
                self.follow_path(wrld)
            else:
                closest = self.closest_reached(came_from, wrld)
                self.create_path_dest(came_from,(self.x,self.y),closest)
                self.path.append("bomb")
                self.follow_path(wrld)


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
            self.place_bomb()


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


    def minimax(self):
        pass

    def expectimax(self):
        pass


