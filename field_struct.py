from enum import Enum

class ValueTypes(Enum):
    UNVISITED, OPEN, CLOSED, START, GOAL, PATH, OBSTACLE = range(7)

class Coords:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def add(self, x_offset, y_offset):
        res_x = self.x + x_offset
        res_y = self.y + y_offset
        return Coords(res_x, res_y)

    def __eq__(self, other):
        if isinstance(other, Coords):
            return self.x == other.x and self.y == other.y
        else:
            return False

class Node:
    def __init__(self):
        self.gcost = None
        self.fcost = None
        self.value = ValueTypes.UNVISITED
        self.coords = None
        self.parent = None

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.fcost == other.fcost and self.gcost == other.gcost
        else:
            return False 

    def __ne__(self, other):
        if isinstance(other, Node):
            return not(self.fcost == other.fcost and self.gcost == other.gcost)
        else:
            return True 
    
    def __lt__(self, other):
        if isinstance(other, Node):
            return (self.fcost < other.fcost) or (self.fcost == other.fcost and self.gcost > other.gcost)
    
    def set_gcost(self, cost):
        self.gcost = cost

    def get_gcost(self):
        return self.gcost

    def set_fcost(self, cost):
        self.fcost = cost

    def get_fcost(self):
        return self.fcost

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value
    
    def set_coords(self, coords):
        self.coords = coords
    
    def get_coords(self):
        return self.coords

    def set_parent(self, parent):
        self.parent = parent

    def get_parent(self):
        return self.parent

    def toggle_obstacle(self):
        if self.value == ValueTypes.UNVISITED:
            self.value = ValueTypes.OBSTACLE
        elif self.value == ValueTypes.OBSTACLE:
            self.value = ValueTypes.UNVISITED

    # calculates the distance to the other node as 14 * diagonal_moves + 10 * vertical/horizontal_moves
    def get_distance(self, other):
        x_diff = abs(self.coords.x - other.coords.x)
        y_diff = abs(self.coords.y - other.coords.y)
        return (10 * abs(x_diff - y_diff) + 14 * (x_diff if (x_diff < y_diff) else y_diff))

class PlayingField:
    def __init__(self, x, y):
        self.size = Coords(x, y)
        self.field = [[Node() for i in range(x)] for j in range(y)]
        for i in range(x):
            for j in range(y):
                self.field[i][j].set_coords(Coords(i, j))
        self.start = None
        self.goal = None

    def set_start(self, coords):
        if self.start == None or self.start != coords:
            if self.start != None:
                self.field[self.start.x][self.start.y].set_value(ValueTypes.UNVISITED)
            self.start = coords
            self.field[self.start.x][self.start.y].set_value(ValueTypes.START)

    def get_size(self):
        return self.size

    def get_start(self):
        if self.start != None:
            return self.field[self.start.x][self.start.y]
        return None
        
    def set_goal(self, coords):
        if self.goal == None or self.goal != coords:
            if self.goal != None:
                self.field[self.goal.x][self.goal.y].set_value(ValueTypes.UNVISITED)
            self.goal = coords
            self.field[self.goal.x][self.goal.y].set_value(ValueTypes.GOAL)

    def get_goal(self):
        if self.goal != None:
            return self.field[self.goal.x][self.goal.y]
        return None

    def set_value(self, coords, value):
        if (value == ValueTypes.UNVISITED or value == ValueTypes.OPEN or value == ValueTypes.CLOSED):
            self.field[coords.x][coords.y].set_value(value)
            return True
        return False

    def get_value(self, coords):
        return self.field[coords.x][coords.y].get_value()

    def get_node(self, coords):
        return self.field[coords.x][coords.y]

    def toggle_obstacle(self, coords):
        self.field[coords.x][coords.y].toggle_obstacle()