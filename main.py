import pygame
import random
import sys
import time

# Inicializácia
pygame.init()
width, height = 690, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pohyb kruhu šípkami")

# Konštanty
BALL_SPEED = 2
PADDLE_SPEED = 2
COLORS = [(80, 120, 255), (255, 80, 80), (255, 220, 80), (80, 220, 120)]  # blue, red, yellow, green (podobné obrázku)
BROWN = (120, 100, 60)
LIGHT_BROWN = (180, 140, 80)
BG_COLOR = (24, 20, 32)
WHITE = (255, 255, 255)
LIFE_COLOR = (255, 255, 255)
GAME_OVER_COLOR = (255, 60, 60)
WIN_COLOR = (80, 255, 80)  # zelená pre YOU WON
DARK_COLORS = [(40, 60, 128), (128, 40, 40), (128, 110, 40), (40, 110, 60)]  # tmavšie odtiene pre symboly
STONE_COLOR = (80, 60, 30)  # tmavohnedá

# Počiatočné nastavenia
x = width // 2 - 50
y = height * 0.8
sirka = 100
vyska = 25
rychlost = PADDLE_SPEED

# Premenné pre zmenšenie obdĺžnika
shrink_start_time = 0
is_shrunk = False
original_sirka = sirka
shrunken_sirka = 50

# Životy
lives = 3
life_radius = 14
life_margin = 10
life_y = height - 30
life_x_start = 30

class Ball:
    def __init__(self, x, y, speed_x, speed_y):
        self.x = x
        self.y = y
        self.radius = 10
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.color = (0, 0, 0)

def normalize_speed(speed_x, speed_y, target_speed):
    current_speed = (speed_x ** 2 + speed_y ** 2) ** 0.5
    if current_speed > 0:
        return (speed_x / current_speed) * target_speed, (speed_y / current_speed) * target_speed
    return speed_x, speed_y

# Vytvorenie obdĺžnikov
rectangles = []
all_positions = list(range(28))
plus_positions = random.sample(all_positions, 5)
remaining_positions = [pos for pos in all_positions if pos not in plus_positions]
brown_positions = random.sample(remaining_positions, 5)
remaining_positions = [pos for pos in remaining_positions if pos not in brown_positions]
shrink_positions = random.sample(remaining_positions, 3)

x1, y1 = 0, 0
for i in range(28):
    has_plus = i in plus_positions
    is_brown = i in brown_positions
    has_shrink = i in shrink_positions
    color = BROWN if is_brown else COLORS[i // 7]
    hits = 0
    rectangles.append([x1, y1, 90, 40, color, has_plus, is_brown, has_shrink, hits])
    x1 += 100
    if (i + 1) % 7 == 0:
        x1 = 0
        y1 += 50

# Herný cyklus
balls = [Ball(width // 2, height // 2, 0, BALL_SPEED)]
spawn_timer = None
font_big = pygame.font.Font(None, 80)
font_life = pygame.font.Font(None, 32)
font_restart = pygame.font.Font(None, 40)
won = False
game_over = False
restart_rect = None
start_time = time.time()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if is_shrunk and time.time() - shrink_start_time >= 5:
        is_shrunk = False
        # Obnov pôvodnú šírku a vycentruj späť
        delta = (original_sirka - sirka) // 2
        x -= delta
        sirka = original_sirka

    if not game_over and not won:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and x > 0:
            x -= rychlost
        if keys[pygame.K_RIGHT] and x + sirka < width:
            x += rychlost

    screen.fill(BG_COLOR)

    # Životy vľavo dole
    for i in range(3):
        center = (life_x_start + i * (life_radius * 2 + life_margin), life_y)
        if i < lives:
            pygame.draw.circle(screen, LIFE_COLOR, center, life_radius, 0)  # plná gulička
        pygame.draw.circle(screen, LIFE_COLOR, center, life_radius, 2)      # obvod vždy svieti

    # Časovač vpravo dole
    elapsed = int(time.time() - start_time)
    time_text = pygame.font.Font(None, 36).render(f"{elapsed}s", True, WHITE)
    screen.blit(time_text, (width - time_text.get_width() - 10, height - 60))

    for rect in rectangles:
        pygame.draw.rect(screen, rect[4], rect[:4], border_radius=10)
        base_color = rect[4]
        # urč index farby pre tmavší odtieň
        color_index = None
        for idx, c in enumerate(COLORS):
            if not rect[6] and c == base_color:
                color_index = idx
        if rect[5]:  # plus
            plus_color = DARK_COLORS[color_index] if color_index is not None else (60, 60, 60)
            text = pygame.font.Font(None, 44).render("+", True, plus_color)
            screen.blit(text, (rect[0] + (rect[2] - text.get_width()) // 2,
                              rect[1] + (rect[3] - text.get_height()) // 2))
        elif rect[6]:  # brown
            stone_font = pygame.font.Font(None, 24)
            stone_text = stone_font.render("STONE", True, STONE_COLOR)
            screen.blit(stone_text, (rect[0] + (rect[2] - stone_text.get_width()) // 2,
                                    rect[1] + (rect[3] - stone_text.get_height()) // 2))
        elif rect[7]:  # shrink
            shrink_color = DARK_COLORS[color_index] if color_index is not None else (60, 60, 60)
            text = pygame.font.Font(None, 44).render("><", True, shrink_color)
            screen.blit(text, (rect[0] + (rect[2] - text.get_width()) // 2,
                              rect[1] + (rect[3] - text.get_height()) // 2))

    pygame.draw.rect(screen, (255, 255, 255), [x, y, sirka, vyska], border_radius=10)

    if not game_over and not won:
        for ball in balls[:]:
            ball.x += ball.speed_x
            ball.y += ball.speed_y

            if ball.x - ball.radius <= 0:
                ball.x = ball.radius + 1
                ball.speed_x *= -1
                ball.speed_x, ball.speed_y = normalize_speed(ball.speed_x, ball.speed_y, BALL_SPEED)
            elif ball.x + ball.radius >= width:
                ball.x = width - ball.radius - 1
                ball.speed_x *= -1
                ball.speed_x, ball.speed_y = normalize_speed(ball.speed_x, ball.speed_y, BALL_SPEED)
            if ball.y - ball.radius <= 0:
                ball.y = ball.radius + 1
                ball.speed_y *= -1
                ball.speed_x, ball.speed_y = normalize_speed(ball.speed_x, ball.speed_y, BALL_SPEED)

            if (ball.y + ball.radius >= y and ball.y - ball.radius <= y + vyska and
                ball.x + ball.radius >= x and ball.x - ball.radius <= x + sirka):
                bounce_angle = ((ball.x - x) / sirka - 0.5) * 2
                ball.speed_x = bounce_angle * BALL_SPEED
                ball.speed_y = -BALL_SPEED
                ball.speed_x, ball.speed_y = normalize_speed(ball.speed_x, ball.speed_y, BALL_SPEED)

            if ball.y - ball.radius > y + vyska:
                balls.remove(ball)
                continue

            for rect in rectangles[:]:
                if (rect[0] < ball.x < rect[0] + rect[2] and 
                    rect[1] < ball.y < rect[1] + rect[3]):
                    dx = (ball.x - (rect[0] + rect[2]/2)) / (rect[2]/2)
                    dy = (ball.y - (rect[1] + rect[3]/2)) / (rect[3]/2)
                    ball.speed_x, ball.speed_y = normalize_speed(ball.speed_x, ball.speed_y, BALL_SPEED)
                    if abs(dx) > abs(dy):
                        ball.speed_x *= -1
                    else:
                        ball.speed_y *= -1
                    ball.speed_x, ball.speed_y = normalize_speed(ball.speed_x, ball.speed_y, BALL_SPEED)
                    if rect[6]:  # brown
                        rect[8] += 1  # zvýš počet zásahov
                        if rect[8] == 1:
                            rect[4] = LIGHT_BROWN
                        elif rect[8] >= 2:
                            rectangles.remove(rect)
                    else:
                        if rect[5]:  # plus
                            new_speed_x = -BALL_SPEED if ball.speed_x > 0 else BALL_SPEED
                            new_speed_y = ball.speed_y
                            new_ball = Ball(ball.x, ball.y, new_speed_x, new_speed_y)
                            balls.append(new_ball)
                            ball.speed_x, ball.speed_y = normalize_speed(ball.speed_x, ball.speed_y, BALL_SPEED)
                        elif rect[7]:  # shrink
                            ball.speed_x, ball.speed_y = normalize_speed(ball.speed_x, ball.speed_y, BALL_SPEED)
                            is_shrunk = True
                            shrink_start_time = time.time()
                            # Zmenši z oboch strán a vycentruj
                            delta = (sirka - shrunken_sirka) // 2
                            x += delta
                            sirka = shrunken_sirka
                        rectangles.remove(rect)
            ball.speed_x, ball.speed_y = normalize_speed(ball.speed_x, ball.speed_y, BALL_SPEED)
            pygame.draw.circle(screen, WHITE, (int(ball.x), int(ball.y)), ball.radius)

    # Kontrola konca hry
    if not game_over and not won:
        if not balls:
            if lives > 0:
                if spawn_timer is None:
                    lives -= 1
                    spawn_timer = time.time()
                elif time.time() - spawn_timer >= 2:
                    balls.append(Ball(width // 2, height // 2, 0, BALL_SPEED))
                    spawn_timer = None
            else:
                game_over = True
        if not rectangles:
            won = True

    # GAME OVER
    if game_over:
        elapsed = int(time.time() - start_time)
        time_text = font_life.render(f"{elapsed}s", True, WHITE)
        screen.blit(time_text, ((width - time_text.get_width()) // 2, (height - font_big.get_height()) // 2 - 60))
        text = font_big.render("GAME OVER", True, GAME_OVER_COLOR)
        screen.blit(text, ((width - text.get_width()) // 2, (height - text.get_height()) // 2))
        restart_text = font_restart.render("RESTART", True, WHITE)
        restart_rect = restart_text.get_rect(center=(width // 2, (height + text.get_height()) // 2 + 40))
        screen.blit(restart_text, restart_rect)
    # YOU WON
    if won:
        elapsed = int(time.time() - start_time)
        time_text = font_life.render(f"{elapsed}s", True, WHITE)
        screen.blit(time_text, ((width - time_text.get_width()) // 2, (height - font_big.get_height()) // 2 - 60))
        text = font_big.render("YOU WON", True, WIN_COLOR)
        screen.blit(text, ((width - text.get_width()) // 2, (height - text.get_height()) // 2))
        restart_text = font_restart.render("RESTART", True, WHITE)
        restart_rect = restart_text.get_rect(center=(width // 2, (height + text.get_height()) // 2 + 40))
        screen.blit(restart_text, restart_rect)

    pygame.display.flip()

    # Kliknutie na RESTART
    if (game_over or won) and restart_rect:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    # Reset všetkých premenných
                    x = width // 2 - 50
                    y = height * 0.8
                    sirka = 100
                    vyska = 25
                    rychlost = PADDLE_SPEED
                    shrink_start_time = 0
                    is_shrunk = False
                    original_sirka = sirka
                    shrunken_sirka = 50
                    lives = 3
                    balls = [Ball(width // 2, height // 2, 0, BALL_SPEED)]
                    spawn_timer = None
                    won = False
                    game_over = False
                    # Vytvorenie obdĺžnikov nanovo
                    rectangles.clear()
                    all_positions = list(range(28))
                    plus_positions = random.sample(all_positions, 5)
                    remaining_positions = [pos for pos in all_positions if pos not in plus_positions]
                    brown_positions = random.sample(remaining_positions, 5)
                    remaining_positions = [pos for pos in remaining_positions if pos not in brown_positions]
                    shrink_positions = random.sample(remaining_positions, 3)
                    x1, y1 = 0, 0
                    for i in range(28):
                        has_plus = i in plus_positions
                        is_brown = i in brown_positions
                        has_shrink = i in shrink_positions
                        color = BROWN if is_brown else COLORS[i // 7]
                        hits = 0
                        rectangles.append([x1, y1, 90, 40, color, has_plus, is_brown, has_shrink, hits])
                        x1 += 100
                        if (i + 1) % 7 == 0:
                            x1 = 0
                            y1 += 50
                    start_time = time.time()
                    break

pygame.quit()
sys.exit()