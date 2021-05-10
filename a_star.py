import field_struct as fs

class AStar:
    def __init__(self, field):
        self.field = field
        self.open = [field.get_start()]
        self.field.get_start().set_gcost(0)
        self.field.get_start().set_fcost(self.field.get_start().get_distance(self.field.get_goal()))
        self.closed = []
        self.current = None

    def is_node_open(self, node):
        for i in self.open:
            if i.get_coords() == node.get_coords():
                return True
        return False
        
    def calculate_costs(self, neighbour):
        temp_gcost = self.current.get_gcost() + self.current.get_distance(neighbour)
        if (neighbour.get_value() == fs.ValueTypes.UNVISITED or neighbour.get_value() == fs.ValueTypes.OPEN or neighbour.get_value() == fs.ValueTypes.GOAL):
            if (neighbour.get_gcost() == None or temp_gcost < neighbour.get_gcost()):
                neighbour.set_parent(self.current)
                neighbour.set_gcost(temp_gcost)
                neighbour.set_fcost(neighbour.get_gcost() + neighbour.get_distance(self.field.get_goal()))
                if (neighbour.get_value() != fs.ValueTypes.OPEN):
                    self.open.append(neighbour)
                if (neighbour.get_value() == fs.ValueTypes.UNVISITED):
                    neighbour.set_value(fs.ValueTypes.OPEN)
            
    def reconstruct_path(self):
        parent = self.field.get_goal().get_parent()
        while (parent.coords != self.field.get_start().coords):
            parent.set_value(fs.ValueTypes.PATH)
            parent = parent.get_parent()
        
    def calculate_surrounding_costs(self):
        for i in range (-1, 2):
            for j in range (-1, 2):
                if (i != 0 or j != 0):
                    neighbour_coords = self.current.get_coords().add(i, j)
                    if (neighbour_coords.x >= 0 and neighbour_coords.y >= 0 and neighbour_coords.x < self.field.get_size().x and neighbour_coords.y < self.field.get_size().y):
                        self.calculate_costs(self.field.get_node(neighbour_coords))

    def make_step(self):
        if (len(self.open) != 0) and (self.field.get_start() != None) and (self.field.get_goal() != None):
            self.current = self.open.pop(0)
            if ((self.current != None) and (self.current.get_coords() == self.field.get_goal().get_coords())):
                self.reconstruct_path()
                return False
            if (self.current.get_value() == fs.ValueTypes.OPEN):
                self.current.set_value(fs.ValueTypes.CLOSED)
            self.calculate_surrounding_costs()
            self.open.sort()
            return True
        return False