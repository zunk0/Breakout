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
BALL_SPEED = 0.8
PADDLE_SPEED = 0.8
COLORS = [(0, 0, 255), (255, 0, 0), (255, 255, 0), (0, 255, 0)]  # Modrá Červená Žltá Zelená
BROWN = (139, 69, 19)
LIGHT_BROWN = (205, 133, 63)

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
    rectangles.append([x1, y1, 90, 40, color, has_plus, is_brown, has_shrink])
    x1 += 100
    if (i + 1) % 7 == 0:
        x1 = 0
        y1 += 50

# Vytvorenie zoznamu guľôčok
balls = [Ball(width // 2, height // 2, 0, BALL_SPEED)]  # Začína padáť kolmo dole

# Herný cyklus
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Kontrola času zmenšenia
    if is_shrunk and time.time() - shrink_start_time >= 5:
        is_shrunk = False
        sirka = original_sirka

    # Pohyb čierneho obdĺžnika
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and x > 0:
        x -= rychlost
    if keys[pygame.K_RIGHT] and x + sirka < width:
        x += rychlost

    # Vykreslenie
    screen.fill((255, 255, 255))
    
    # Kreslenie obdĺžnikov
    for rect in rectangles:
        pygame.draw.rect(screen, rect[4], rect[:4], border_radius=10)
        if rect[5]:  # plus
            text = pygame.font.Font(None, 36).render("+", True, (0, 0, 0))
            screen.blit(text, (rect[0] + (rect[2] - text.get_width()) // 2,
                             rect[1] + (rect[3] - text.get_height()) // 2))
        elif rect[7]:  # shrink
            text = pygame.font.Font(None, 36).render("><", True, (0, 0, 0))
            screen.blit(text, (rect[0] + (rect[2] - text.get_width()) // 2,
                             rect[1] + (rect[3] - text.get_height()) // 2))

    pygame.draw.rect(screen, (0, 0, 0), [x, y, sirka, vyska], border_radius=10)

    # Aktualizácia guľôčok
    for ball in balls[:]:
        ball.x += ball.speed_x
        ball.y += ball.speed_y

        # Kolízie so stenami
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

        # Kolízia s čiernym obdĺžnikom
        if (ball.y + ball.radius >= y and ball.y - ball.radius <= y + vyska and
            ball.x + ball.radius >= x and ball.x - ball.radius <= x + sirka):
            bounce_angle = ((ball.x - x) / sirka - 0.5) * 2
            ball.speed_x = bounce_angle * BALL_SPEED
            ball.speed_y = -BALL_SPEED

        # Odstránenie guľôčky ak padne pod čierny obdĺžnik
        if ball.y - ball.radius > y + vyska:
            balls.remove(ball)
            continue

        # Kolízie s farebnými obdĺžnikmi
        for rect in rectangles[:]:
            if (rect[0] < ball.x < rect[0] + rect[2] and 
                rect[1] < ball.y < rect[1] + rect[3]):
                dx = (ball.x - (rect[0] + rect[2]/2)) / (rect[2]/2)
                dy = (ball.y - (rect[1] + rect[3]/2)) / (rect[3]/2)
                
                if abs(dx) > abs(dy):
                    ball.speed_x *= -1
                else:
                    ball.speed_y *= -1
                ball.speed_x, ball.speed_y = normalize_speed(ball.speed_x, ball.speed_y, BALL_SPEED)

                if rect[6]:  # brown
                    if rect[4] == BROWN:
                        rect[4] = LIGHT_BROWN
                    else:
                        rectangles.remove(rect)
                else:
                    if rect[5]:  # plus
                        new_speed_x, new_speed_y = normalize_speed(-ball.speed_x, ball.speed_y, BALL_SPEED)
                        balls.append(Ball(ball.x, ball.y, new_speed_x, new_speed_y))
                    elif rect[7]:  # shrink
                        is_shrunk = True
                        shrink_start_time = time.time()
                        sirka = shrunken_sirka
                    rectangles.remove(rect)

        pygame.draw.circle(screen, ball.color, (int(ball.x), int(ball.y)), ball.radius)

    # Vytvorenie novej guľôčky ak nie sú žiadne
    if not balls:
        balls.append(Ball(width // 2, height // 2, 0, BALL_SPEED))  # Začína padáť kolmo dole

    pygame.display.flip()

pygame.quit()
sys.exit()