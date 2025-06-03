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
f = [(0, 0, 255), (255, 0, 0), (255, 255, 0), (0, 255, 0)] # Modrá Červená Žltá Zelená

# Herný cyklus
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Získanie stlačených kláves
    keys = pygame.key.get_pressed()

    # Pohyb podľa šípok
    if keys[pygame.K_LEFT]:
        x -= rychlost
    if keys[pygame.K_RIGHT]:
        x += rychlost

    # Vyčistenie obrazovky
    screen.fill(biela)

    # Kreslenie kruhu na novej pozícii
    pygame.draw.rect(screen, cierna, [x, y, sirka, vyska], border_radius=10)

    # Kreslenie červených obdĺžnikov
    x1 = 0
    y1 = 0
    ff = 0
    for i in range(0, 31):
        pygame.draw.rect(screen, f[ff], [x1, y1, sirka1, vyska1], border_radius=10)
        if x1 > width:
            x1 = 0
            y1 += 50
            ff += 1
        else:
            x1 += 100
    
    # x1 = 0
    # y1 = 0
    # ff = 0
    # for i in range(28):  # Presne 28 obdĺžnikov
    #     pygame.draw.rect(screen, f[ff], [x1, y1, sirka1, vyska1], border_radius=10)
    #     x1 += 100  # Posun na ďalší stĺpec
    #     if (i + 1) % 7 == 0:  # Po každom 7. obdĺžniku
    #         x1 = 0  # Začiatok nového riadku
    #         y1 += 50  # Posun na ďalší riadok
    #         ff = (ff + 1) % len(f)  # Zmena farby (cyklicky)
    #     pygame.display.flip()

# Ukončenie
pygame.quit()
sys.exit()