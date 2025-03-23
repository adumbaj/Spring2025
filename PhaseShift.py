import pygame

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
RED = (255, 50, 50)
GREEN = (50, 200, 50)
BLACK = (0, 0, 0)
GRAVITY = 0.5
JUMP_STRENGTH = -10
BOUNDARY_X = WIDTH // 2
GROUND_Y = HEIGHT - 50
PLAYER_SPEED = 5

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Phase Shift Platformer")
title_font = pygame.font.Font(None, 72)
font = pygame.font.Font(None, 36)

# Function to display menu
def show_menu():
    menu_running = True
    while menu_running:
        screen.fill(WHITE)
        title = title_font.render("Phase Shift", True, BLACK)
        instructions1 = font.render("Use A and D to move left and right", True, BLACK)
        instructions2 = font.render("Spacebar to jump", True, BLACK)
        instructions3 = font.render("Reach the green square at the end", True, BLACK)
        quit_text = font.render("Press Q to quit", True, BLACK)
        start_text = font.render("Press Enter to Start", True, BLACK)
        
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
        screen.blit(instructions1, (WIDTH // 2 - instructions1.get_width() // 2, 200))
        screen.blit(instructions2, (WIDTH // 2 - instructions2.get_width() // 2, 250))
        screen.blit(instructions3, (WIDTH // 2 - instructions3.get_width() // 2, 300))
        screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, 350))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, 400))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu_running = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()

show_menu()

# Function to display win screen
def show_win_screen():
    win_running = True
    while win_running:
        screen.fill(WHITE)
        win_text = title_font.render("You Win!", True, GREEN)
        restart_text = font.render("Press Enter to Play Again", True, BLACK)
        quit_text = font.render("Press Q to Quit", True, BLACK)
        
        screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, 200))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 300))
        screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, 350))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return  # Restart game
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()

# Player setup
player = pygame.Rect(100, HEIGHT - 100, 40, 40)
velocity_y = 0
flipped_gravity = False
can_jump = False

# Platforms
platforms = [
    pygame.Rect(150, 450, 100, 20),
    pygame.Rect(350, 350, 100, 20),
    pygame.Rect(550, 250, 100, 20),
    pygame.Rect(650, 100, 100, 20)
]

# Ground
ground = pygame.Rect(0, GROUND_Y, WIDTH, 50)

# Goal
goal = pygame.Rect(700, 50, 40, 40)

# Initialize Pygame Mixer
pygame.mixer.init()

# Load sound effects
jump_sound = pygame.mixer.Sound("jump.wav")
#land_sound = pygame.mixer.Sound("land.wav")
#win_sound = pygame.mixer.Sound("win.wav")


# Game loop
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(WHITE)
    
    # Draw boundary line
    pygame.draw.line(screen, RED, (BOUNDARY_X, 0), (BOUNDARY_X, HEIGHT), 5)
    
    # Draw platforms
    for platform in platforms:
        pygame.draw.rect(screen, BLUE, platform)
    
    # Draw ground
    pygame.draw.rect(screen, BLUE, ground)
    
    # Draw goal
    pygame.draw.rect(screen, GREEN, goal)
    
    # Draw player
    pygame.draw.rect(screen, BLACK, player)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Get keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        running = False
    if keys[pygame.K_a] and player.x > 0:
        player.x -= PLAYER_SPEED
    if keys[pygame.K_d] and player.x < WIDTH - player.width:
        player.x += PLAYER_SPEED
    if keys[pygame.K_SPACE] and can_jump:
        velocity_y = JUMP_STRENGTH if not flipped_gravity else -JUMP_STRENGTH
        can_jump = False  
        jump_sound.play() # Prevent multiple jumps
    
    # Check boundary crossing
    if player.x > BOUNDARY_X and not flipped_gravity:
        flipped_gravity = True
    elif player.x <= BOUNDARY_X and flipped_gravity:
        flipped_gravity = False
    
    # Apply gravity
    velocity_y += -GRAVITY if flipped_gravity else GRAVITY
    player.y += velocity_y
    
    # Collision with platforms
    can_jump = False
    for platform in platforms:
        if player.colliderect(platform):
            if velocity_y > 0 and not flipped_gravity:
                player.bottom = platform.top
                velocity_y = 0
                can_jump = True
            elif velocity_y < 0 and flipped_gravity:
                player.top = platform.bottom
                velocity_y = 0
                can_jump = True
    
    # Collision with ground
    if player.bottom >= GROUND_Y and not flipped_gravity:
        player.bottom = GROUND_Y
        velocity_y = 0
        can_jump = True
    
    # Prevent flying through ceiling
    if player.top <= 0 and flipped_gravity:
        player.top = 0
        velocity_y = 0
    
    # Check win condition
    if player.colliderect(goal):
        show_win_screen()
        show_menu()
        player.x, player.y = 100, HEIGHT - 100  # Reset player position
        flipped_gravity = False
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
