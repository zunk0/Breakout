# import pygame
# import random
# import sys

# # Inicializácia
# pygame.init()

# # Rozmery obrazovky
# width, height = 690, 600
# screen = pygame.display.set_mode((width, height))
# pygame.display.set_caption("Pohyb kruhu šípkami")

# # Farby
# biela = (255, 255, 255)
# cierna = (0, 0, 0)

# # Počiatočná pozícia kruhu
# x = width // 2 - 50
# y = height * 0.8
# sirka = 100
# vyska = 25
# rychlost = 0.2

# sirka1 = 90
# vyska1 = 40
# cervena = (255, 0, 0)
# f = [(0, 0, 255), (255, 0, 0), (255, 255, 0), (0, 255, 0)] # Modrá Červená Žltá Zelená

# # Herný cyklus
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # Získanie stlačených kláves
#     keys = pygame.key.get_pressed()

#     # Pohyb podľa šípok
#     if keys[pygame.K_LEFT]:
#         x -= rychlost
#     if keys[pygame.K_RIGHT]:
#         x += rychlost

#     # Vyčistenie obrazovky
#     screen.fill(biela)

#     # Kreslenie obdĺžnikov
#     x1 = 0
#     y1 = 0
#     ff = 0
#     for i in range(28):  # Presne 28 obdĺžnikov
#         pygame.draw.rect(screen, f[ff], [x1, y1, sirka1, vyska1], border_radius=10)
#         x1 += 100  # Posun na ďalší stĺpec
#         if (i + 1) % 7 == 0:  # Po každom 7. obdĺžniku
#             x1 = 0  # Začiatok nového riadku
#             y1 += 50  # Posun na ďalší riadok
#             ff = (ff + 1) % len(f)  # Zmena farby (cyklicky)

#     # Kreslenie kruhu na novej pozícii
#     pygame.draw.rect(screen, cierna, [x, y, sirka, vyska], border_radius=10)

#     # Aktualizácia obrazovky
#     pygame.display.flip()

# # Ukončenie
# pygame.quit()
# sys.exit()










import pygame
import random
import sys

# Inicializácia
pygame.init()

# Rozmery obrazovky
width, height = 690, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pohyb kruhu šípkami")

# Farby
biela = (255, 255, 255)
cierna = (0, 0, 0)

# Počiatočná pozícia kruhu
x = width // 2 - 50
y = height * 0.8
sirka = 100
vyska = 25
rychlost = 0.2

sirka1 = 90
vyska1 = 40
cervena = (255, 0, 0)
f = [(0, 0, 255), (255, 0, 0), (255, 255, 0), (0, 255, 0)]  # Modrá Červená Žltá Zelená

# Počiatočné nastavenia guľôčky
ball_x = width // 2
ball_y = height // 2
ball_radius = 10
ball_speed_x = random.choice([-0.1, 0.1])  # Náhodný smer (doľava alebo doprava)
ball_speed_y = 0.1
ball_color = (0, 0, 255)  # Modrá

# Zoznam obdĺžnikov (pozície a farby)
rectangles = []
x1 = 0
y1 = 0
ff = 0
for i in range(28):  # Presne 28 obdĺžnikov
    rectangles.append([x1, y1, sirka1, vyska1, f[ff]])  # Pridanie obdĺžnika do zoznamu
    x1 += 100
    if (i + 1) % 7 == 0:
        x1 = 0
        y1 += 50
        ff = (ff + 1) % len(f)

# Herný cyklus
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Získanie stlačených kláves
    keys = pygame.key.get_pressed()

    # Pohyb podľa šípok (zabránime, aby čierny obdĺžnik vyšiel z hracej plochy)
    if keys[pygame.K_LEFT] and x > 0:
        x -= rychlost
    if keys[pygame.K_RIGHT] and x + sirka < width:
        x += rychlost

    # Vyčistenie obrazovky
    screen.fill(biela)

    # Kreslenie obdĺžnikov
    for rect in rectangles:
        pygame.draw.rect(screen, rect[4], rect[:4], border_radius=10)

    # Kreslenie čierneho obdĺžnika
    pygame.draw.rect(screen, cierna, [x, y, sirka, vyska], border_radius=10)

    # Pohyb guľôčky
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Detekcia kolízie so stenami
    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= width:
        ball_speed_x *= -1  # Odrážanie od ľavej a pravej steny
    if ball_y - ball_radius <= 0:
        ball_speed_y *= -1  # Odrážanie od hornej steny

    # Detekcia kolízie s čiernym obdĺžnikom
    if (x < ball_x < x + sirka) and (y - ball_radius <= ball_y <= y):
        # Ak sa guľôčka dotkne hornej hrany čierneho obdĺžnika, odrazí sa
        ball_speed_y *= -1

    # Ak guľôčka klesne pod čierny obdĺžnik, spawne sa nová
    if ball_y - ball_radius > y + vyska:
        ball_x = width // 2
        ball_y = height // 2
        ball_speed_x = random.choice([-0.1, 0.1])  # Náhodný smer
        ball_speed_y = 0.1

    # Detekcia kolízie s farebnými obdĺžnikmi
    for rect in rectangles[:]:
        rect_x, rect_y, rect_width, rect_height, rect_color = rect
        if (rect_x < ball_x < rect_x + rect_width) and (rect_y < ball_y < rect_y + rect_height):
            rectangles.remove(rect)  # Odstránenie obdĺžnika
            ball_speed_y *= -1  # Odrážanie guľôčky

    # Kreslenie guľôčky
    pygame.draw.circle(screen, ball_color, (int(ball_x), int(ball_y)), ball_radius)

    # Aktualizácia obrazovky
    pygame.display.flip()

# Ukončenie
pygame.quit()
sys.exit()