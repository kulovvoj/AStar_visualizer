import a_star
import field_struct as fs
import pygame
import sys

TILE_SIZE = 15
GAP_SIZE = 2
TILES_X = 50
TILES_Y = 50
VISUALIZATION_SPEED = 20

class Display:
    def __init__(self):
        # General setup
        self.clock = pygame.time.Clock()
        # Set up main window
        self.field = fs.PlayingField(TILES_X, TILES_Y)
        self.screen = pygame.display.set_mode((GAP_SIZE + (GAP_SIZE + TILE_SIZE) * TILES_X, GAP_SIZE + (GAP_SIZE + TILE_SIZE) * TILES_Y))
        pygame.display.set_caption('A* visualization')

    def get_color(self, x, y):
        if (self.field.get_node(fs.Coords(x, y)).get_value() == fs.ValueTypes.UNVISITED):
            return (143, 196, 214)
        elif (self.field.get_node(fs.Coords(x, y)).get_value() == fs.ValueTypes.OPEN):
            return (52, 210, 53)
        elif (self.field.get_node(fs.Coords(x, y)).get_value() == fs.ValueTypes.CLOSED):
            return (231, 63, 55)
        elif (self.field.get_node(fs.Coords(x, y)).get_value() == fs.ValueTypes.START):
            return (96, 40, 140)
        elif (self.field.get_node(fs.Coords(x, y)).get_value() == fs.ValueTypes.GOAL):
            return (140, 40, 96)
        elif (self.field.get_node(fs.Coords(x, y)).get_value() == fs.ValueTypes.PATH):
            return (162, 80, 162)
        elif (self.field.get_node(fs.Coords(x, y)).get_value() == fs.ValueTypes.OBSTACLE):
            return (80, 80, 80)
        return (0, 0, 0)

    def draw_screen(self):
        for i in range(TILES_X):
            for j in range(TILES_Y):
                pygame.draw.rect(self.screen, self.get_color(i, j), (GAP_SIZE + (GAP_SIZE + TILE_SIZE) * i, GAP_SIZE + (GAP_SIZE + TILE_SIZE) * j, TILE_SIZE, TILE_SIZE))
        pygame.display.update()

    def setup_loop(self):
        pressed_o = False
        coords = None
        while True:
            # Handling input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.QUIT
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    (x, y) = pygame.mouse.get_pos()
                    # Set start at mouse pos.
                    if event.key == pygame.K_s:
                        (x, y) = pygame.mouse.get_pos()
                        self.field.set_start(fs.Coords(int((x - GAP_SIZE) / (TILE_SIZE + GAP_SIZE)), int((y - GAP_SIZE) / (TILE_SIZE + GAP_SIZE))))
                    # Set goal at mouse pos.
                    if event.key == pygame.K_g:
                        (x, y) = pygame.mouse.get_pos()
                        self.field.set_goal(fs.Coords(int((x - GAP_SIZE) / (TILE_SIZE + GAP_SIZE)), int((y - GAP_SIZE) / (TILE_SIZE + GAP_SIZE))))
                    # Toggle obstacle at mouse pos.
                    if event.key == pygame.K_o:
                        pressed_o = True
                    # Start the simulation
                    if event.key == pygame.K_SPACE:
                        if (self.field.get_start() != None and self.field.get_goal() != None):
                            return
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_o:
                        pressed_o = False
                        coords = None
            if pressed_o:
                (x, y) = pygame.mouse.get_pos()
                old_coords = coords
                coords = fs.Coords(int((x - GAP_SIZE) / (TILE_SIZE + GAP_SIZE)), int((y - GAP_SIZE) / (TILE_SIZE + GAP_SIZE)))
                if (coords != old_coords):
                    self.field.toggle_obstacle(coords)
            self.draw_screen()
            self.clock.tick(60)   
            
    def visualize_loop(self):
        visualizer = a_star.AStar(self.field)
        while visualizer.make_step():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.QUIT
                    sys.exit()
            self.draw_screen()
            self.clock.tick(VISUALIZATION_SPEED)
        self.draw_screen()

    def reset_loop(self):
        while(True):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.QUIT
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    # Reset the simulation
                    if event.key == pygame.K_SPACE:
                        self.field = fs.PlayingField(TILES_X, TILES_Y)
                        return

    def main_loop(self):
        while(True):
            self.setup_loop()
            self.visualize_loop()
            self.reset_loop()


Display().main_loop()
