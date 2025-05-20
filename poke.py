import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
TILE_SIZE = 32
PLAYER_SPEED = 3

# Color Palette (Pokemon Red GB palette)
COLORS = {
    'black': (15, 15, 15),
    'white': (155, 188, 15),
    'light': (139, 172, 15),
    'dark': (48, 98, 48),
    'red': (172, 50, 50),
    'blue': (50, 50, 172),
    'skin': (172, 132, 85)
}

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pokemon Red Engine")
font = pygame.font.Font(None, 24)
clock = pygame.time.Clock()

# Game State
show_welcome = True
current_dialog = None

# Pallet Town Map (ASCII representation)
MAP_DATA = [
    "BBBBBBBBBBBBBBBB",
    "B..............B",
    "B..P.......P...B",
    "B..............B",
    "B.......B......B",
    "B..............B",
    "BBBBBBBBBBBBBBBB",
]

class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.direction = 'down'
        self.speed = PLAYER_SPEED
        self.frame = 0

    def move(self, dx, dy):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        # Convert position to grid coordinates
        grid_x = int(new_x // TILE_SIZE)
        grid_y = int(new_y // TILE_SIZE)
        
        # Check collision with buildings
        if MAP_DATA[grid_y][grid_x] != 'B':
            self.x = new_x
            self.y = new_y
            self.frame = (self.frame + 1) % 10

    def draw(self, surface):
        # Simple character using rectangles
        pygame.draw.rect(surface, COLORS['blue'], 
                        (self.x, self.y, TILE_SIZE//2, TILE_SIZE))
        pygame.draw.rect(surface, COLORS['skin'], 
                        (self.x+4, self.y+8, TILE_SIZE//2-8, TILE_SIZE//2))

class NPC:
    def __init__(self, x, y, dialog):
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.dialog = dialog

    def draw(self, surface):
        pygame.draw.rect(surface, COLORS['red'], 
                        (self.x, self.y, TILE_SIZE, TILE_SIZE))

def draw_map():
    for y, row in enumerate(MAP_DATA):
        for x, tile in enumerate(row):
            rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if tile == 'B':
                pygame.draw.rect(screen, COLORS['dark'], rect)
            elif tile == 'P':
                pygame.draw.rect(screen, COLORS['white'], rect)
            else:
                pygame.draw.rect(screen, COLORS['light'], rect)

def show_text(text):
    global current_dialog
    current_dialog = text

# Game Objects
player = Player()
npcs = [
    NPC(5, 3, "Welcome to the world of POKEMON!"),
    NPC(10, 3, "This is PALLET TOWN.")
]

# Main Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z and current_dialog:
                current_dialog = None
            elif event.key == pygame.K_x and show_welcome:
                show_welcome = False

    # Player Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(-1, 0)
        player.direction = 'left'
    elif keys[pygame.K_RIGHT]:
        player.move(1, 0)
        player.direction = 'right'
    elif keys[pygame.K_UP]:
        player.move(0, -1)
        player.direction = 'up'
    elif keys[pygame.K_DOWN]:
        player.move(0, 1)
        player.direction = 'down'

    # Drawing
    screen.fill(COLORS['black'])
    draw_map()
    
    for npc in npcs:
        npc.draw(screen)
    
    player.draw(screen)

    # Show welcome message
    if show_welcome:
        welcome_text = font.render("Welcome to the world of POKEMON!", 
                                 True, COLORS['white'])
        screen.blit(welcome_text, (50, SCREEN_HEIGHT - 50))

    # Show NPC dialog
    if current_dialog:
        dialog_box = pygame.Surface((SCREEN_WIDTH - 20, 60))
        dialog_box.fill(COLORS['white'])
        text = font.render(current_dialog, True, COLORS['black'])
        dialog_box.blit(text, (10, 10))
        screen.blit(dialog_box, (10, SCREEN_HEIGHT - 70))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
