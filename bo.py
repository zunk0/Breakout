# Import potrebných knižníc
import tkinter as tk  # Importuje Tkinter pre vytvorenie grafického rozhrania
import random  # Importuje random pre generovanie náhodných čísel
import math  # Importuje math pre matematické operácie
import time  # Importuje time pre prácu s časom

class Lopta:
    def __init__(self, x, y, rychlost_x, rychlost_y):
        # Inicializácia lopty s jej pozíciou a rýchlosťou
        self.x = x  # X-ová súradnica lopty
        self.y = y  # Y-ová súradnica lopty
        self.polomer = 10  # Polomer lopty v pixeloch
        self.rychlost_x = rychlost_x  # Rýchlosť lopty v X smere
        self.rychlost_y = rychlost_y  # Rýchlosť lopty v Y smere
        self.farba = "white"  # Farba lopty

class BreakoutHra:
    def __init__(self, root):
        # Inicializácia hlavnej hry
        self.root = root  # Uloží hlavné okno
        self.root.title("Breakout Hra")  # Nastaví názov okna
        
        # Definícia konštánt hry
        self.SIRKA = 690  # Šírka herného okna
        self.VYSKA = 600  # Výška herného okna
        self.RYCHLOST_LOPTY = 5  # Základná rýchlosť lopty
        self.RYCHLOST_PALICKY = 30  # Rýchlosť pohybu paličky
        self.FARBY = ["#5078FF", "#FF5050", "#FFDC50", "#50DC78"]  # Farby blokov (modrá, červená, žltá, zelená)
        self.HNEDA = "#78643C"  # Farba kamenných blokov
        self.SVETLA_HNEDA = "#B48C50"  # Farba poškodených kamenných blokov
        self.POZADIE = "#181420"  # Farba pozadia
        self.BIELA = "#FFFFFF"  # Biela farba
        self.TMAVE_FARBY = ["#283C80", "#802828", "#806E28", "#286E3C"]  # Tmavé farby pre text

        # Vytvorenie herného plátna
        self.platno = tk.Canvas(root, width=self.SIRKA, height=self.VYSKA, bg=self.POZADIE)
        self.platno.pack()

        # Inicializácia herných premenných
        self.palicka_x = self.SIRKA // 2 - 50  # Počiatočná X pozícia paličky
        self.palicka_y = self.VYSKA * 0.8  # Y pozícia paličky
        self.palicka_sirka = 100  # Šírka paličky
        self.palicka_vyska = 25  # Výška paličky
        
        # Premenné pre zmenšenie paličky
        self.cas_zmeny = 0  # Čas poslednej zmeny veľkosti paličky
        self.je_zmensena = False  # Flag pre zmenšenú paličku
        self.povodna_sirka = self.palicka_sirka  # Pôvodná šírka paličky
        self.znizena_sirka = 50  # Zmenšená šírka paličky
        
        # Nastavenie životov
        self.zivoty = 3  # Počet životov
        self.polomer_zivota = 14  # Veľkosť ikony života
        self.medzera_zivotov = 10  # Medzera medzi ikonami životov
        self.zivot_y = self.VYSKA - 30  # Y pozícia ikon životov
        self.zivot_x_start = 30  # Počiatočná X pozícia ikon životov

        # Herný stav
        self.lopty = [Lopta(self.SIRKA // 2, self.VYSKA // 2, 0, self.RYCHLOST_LOPTY)]  # Zoznam loptičiek
        self.casovac = None  # Časovač pre respawn lopty
        self.vyhra = False  # Flag pre výhru
        self.koniec = False  # Flag pre koniec hry
        self.start_cas = time.time()  # Čas začiatku hry
        self.konecny_cas = None  # Čas konca hry

        # Vytvorenie blokov
        self.vytvor_bloky()

        # Nastavenie ovládania
        self.root.bind("<Left>", self.pohyb_vlavo)  # Viazanie klávesy vľavo
        self.root.bind("<Right>", self.pohyb_vpravo)  # Viazanie klávesy vpravo
        self.root.bind("<Button-1>", self.kontrola_restartu)  # Viazanie kliknutia myšou

        # Spustenie hernej slučky
        self.aktualizuj()

    def vytvor_bloky(self):
        # Vytvorenie herných blokov
        self.bloky = []  # Prázdny zoznam blokov
        vsetky_pozicie = list(range(28))  # Všetky možné pozície blokov
        plus_pozicie = random.sample(vsetky_pozicie, 5)  # Náhodný výber 5 pozícií pre plus bloky
        zvysne_pozicie = [pos for pos in vsetky_pozicie if pos not in plus_pozicie]  # Zostávajúce pozície
        hnede_pozicie = random.sample(zvysne_pozicie, 5)  # Náhodný výber 5 pozícií pre kamenné bloky
        zvysne_pozicie = [pos for pos in zvysne_pozicie if pos not in hnede_pozicie]  # Zostávajúce pozície
        zmensenie_pozicie = random.sample(zvysne_pozicie, 3)  # Náhodný výber 3 pozícií pre zmenšujúce bloky

        # Vytvorenie blokov v mriežke
        x1, y1 = 0, 0
        for i in range(28):
            ma_plus = i in plus_pozicie  # Kontrola či blok má plus
            je_hneda = i in hnede_pozicie  # Kontrola či je blok kamenný
            ma_zmensenie = i in zmensenie_pozicie  # Kontrola či blok zmenšuje
            farba = self.HNEDA if je_hneda else self.FARBY[i // 7]  # Výber farby bloku
            pocet_zasahov = 0  # Počítadlo zásahov pre kamenné bloky
            self.bloky.append([x1, y1, 90, 40, farba, ma_plus, je_hneda, ma_zmensenie, pocet_zasahov])
            x1 += 100  # Posun na ďalší blok v riadku
            if (i + 1) % 7 == 0:  # Ak je koniec riadku
                x1 = 0  # Reset X pozície
                y1 += 50  # Posun na ďalší riadok

    def normalizuj_rychlost(self, rychlost_x, rychlost_y, cielova_rychlost):
        # Normalizácia rýchlosti lopty na konštantnú hodnotu
        aktualna_rychlost = (rychlost_x ** 2 + rychlost_y ** 2) ** 0.5  # Výpočet aktuálnej rýchlosti
        if aktualna_rychlost > 0:
            return (rychlost_x / aktualna_rychlost) * cielova_rychlost, (rychlost_y / aktualna_rychlost) * cielova_rychlost
        return rychlost_x, rychlost_y

    def pohyb_vlavo(self, event):
        # Ovládanie pohybu paličky vľavo
        if not self.koniec and not self.vyhra:
            if self.palicka_x > 0:
                self.palicka_x -= self.RYCHLOST_PALICKY

    def pohyb_vpravo(self, event):
        # Ovládanie pohybu paličky vpravo
        if not self.koniec and not self.vyhra:
            if self.palicka_x + self.palicka_sirka < self.SIRKA:
                self.palicka_x += self.RYCHLOST_PALICKY

    def kontrola_restartu(self, event):
        # Kontrola kliknutia na tlačidlo restart
        if (self.koniec or self.vyhra) and self.restart_obdlznik:
            x, y = event.x, event.y
            tlacidlo_x = self.SIRKA // 2
            tlacidlo_y = self.VYSKA // 2 + 60
            tlacidlo_sirka = 100
            tlacidlo_vyska = 40
            
            if (tlacidlo_x - tlacidlo_sirka//2 <= x <= tlacidlo_x + tlacidlo_sirka//2 and
                tlacidlo_y - tlacidlo_vyska//2 <= y <= tlacidlo_y + tlacidlo_vyska//2):
                self.reset_hry()

    def reset_hry(self):
        # Reset hry na počiatočný stav
        self.palicka_x = self.SIRKA // 2 - 50
        self.palicka_y = self.VYSKA * 0.8
        self.palicka_sirka = 100
        self.palicka_vyska = 25
        self.zivoty = 3
        self.lopty = [Lopta(self.SIRKA // 2, self.VYSKA // 2, 0, self.RYCHLOST_LOPTY)]
        self.casovac = None
        self.vyhra = False
        self.koniec = False
        self.vytvor_bloky()
        self.start_cas = time.time()

    def aktualizuj(self):
        # Hlavná herná slučka - aktualizácia a vykreslenie
        self.platno.delete("all")  # Vymazanie celého plátna

        # Kontrola zmenšenia paličky
        if self.je_zmensena and time.time() - self.cas_zmeny >= 5:
            self.je_zmensena = False
            delta = (self.povodna_sirka - self.palicka_sirka) // 2
            self.palicka_x -= delta
            self.palicka_sirka = self.povodna_sirka

        # Kreslenie životov
        for i in range(3):
            stred_x = self.zivot_x_start + i * (self.polomer_zivota * 2 + self.medzera_zivotov)
            if i < self.zivoty:
                self.platno.create_oval(
                    stred_x - self.polomer_zivota, self.zivot_y - self.polomer_zivota,
                    stred_x + self.polomer_zivota, self.zivot_y + self.polomer_zivota,
                    fill=self.BIELA
                )
            self.platno.create_oval(
                stred_x - self.polomer_zivota, self.zivot_y - self.polomer_zivota,
                stred_x + self.polomer_zivota, self.zivot_y + self.polomer_zivota,
                outline=self.BIELA, width=2
            )

        # Kreslenie času
        if not self.koniec and not self.vyhra:
            uplynuly_cas = int(time.time() - self.start_cas)
            self.platno.create_text(
                self.SIRKA - 50, self.VYSKA - 60,
                text=f"{uplynuly_cas}s",
                fill=self.BIELA,
                font=("Arial", 18)
            )

        # Kreslenie blokov
        for blok in self.bloky:
            self.platno.create_rectangle(
                blok[0], blok[1],
                blok[0] + blok[2], blok[1] + blok[3],
                fill=blok[4], outline=blok[4]
            )
            if blok[5]:  # plus
                self.platno.create_text(
                    blok[0] + blok[2] // 2, blok[1] + blok[3] // 2,
                    text="+", fill=self.TMAVE_FARBY[self.FARBY.index(blok[4]) if blok[4] in self.FARBY else 0],
                    font=("Arial", 22)
                )
            elif blok[6]:  # hnedá
                self.platno.create_text(
                    blok[0] + blok[2] // 2, blok[1] + blok[3] // 2,
                    text="STONE", fill=self.TMAVE_FARBY[0],
                    font=("Arial", 16)
                )
            elif blok[7]:  # zmenšenie
                self.platno.create_text(
                    blok[0] + blok[2] // 2, blok[1] + blok[3] // 2,
                    text="><", fill=self.TMAVE_FARBY[self.FARBY.index(blok[4]) if blok[4] in self.FARBY else 0],
                    font=("Arial", 22)
                )

        # Kreslenie paličky
        self.platno.create_rectangle(
            self.palicka_x, self.palicka_y,
            self.palicka_x + self.palicka_sirka, self.palicka_y + self.palicka_vyska,
            fill=self.BIELA, outline=self.BIELA
        )

        if not self.koniec and not self.vyhra:
            for lopta in self.lopty[:]:
                lopta.x += lopta.rychlost_x
                lopta.y += lopta.rychlost_y

                # Kolízie so stenami
                if lopta.x - lopta.polomer <= 0:
                    lopta.x = lopta.polomer + 1
                    lopta.rychlost_x *= -1
                elif lopta.x + lopta.polomer >= self.SIRKA:
                    lopta.x = self.SIRKA - lopta.polomer - 1
                    lopta.rychlost_x *= -1
                if lopta.y - lopta.polomer <= 0:
                    lopta.y = lopta.polomer + 1
                    lopta.rychlost_y *= -1

                # Kolízia s paličkou
                if (lopta.y + lopta.polomer >= self.palicka_y and lopta.y - lopta.polomer <= self.palicka_y + self.palicka_vyska and
                    lopta.x + lopta.polomer >= self.palicka_x and lopta.x - lopta.polomer <= self.palicka_x + self.palicka_sirka):
                    uhol_odrazu = ((lopta.x - self.palicka_x) / self.palicka_sirka - 0.5) * 2
                    lopta.rychlost_x = uhol_odrazu * self.RYCHLOST_LOPTY
                    lopta.rychlost_y = -self.RYCHLOST_LOPTY

                # Stratená lopta
                if lopta.y - lopta.polomer > self.palicka_y + self.palicka_vyska:
                    self.lopty.remove(lopta)
                    continue

                # Kolízie s blokmi
                for blok in self.bloky[:]:
                    if (blok[0] < lopta.x < blok[0] + blok[2] and 
                        blok[1] < lopta.y < blok[1] + blok[3]):
                        lopta.rychlost_y *= -1
                        
                        if blok[6]:  # hnedá
                            blok[8] += 1
                            if blok[8] == 1:
                                blok[4] = self.SVETLA_HNEDA
                            elif blok[8] >= 2:
                                self.bloky.remove(blok)
                        else:
                            if blok[5]:  # plus
                                uhol = random.uniform(0, 2 * math.pi)
                                nova_rychlost_x = self.RYCHLOST_LOPTY * math.cos(uhol)
                                nova_rychlost_y = self.RYCHLOST_LOPTY * math.sin(uhol)
                                nova_lopta = Lopta(lopta.x, lopta.y, nova_rychlost_x, nova_rychlost_y)
                                self.lopty.append(nova_lopta)
                            elif blok[7]:  # zmenšenie
                                self.je_zmensena = True
                                self.cas_zmeny = time.time()
                                delta = (self.palicka_sirka - self.znizena_sirka) // 2
                                self.palicka_x += delta
                                self.palicka_sirka = self.znizena_sirka
                            self.bloky.remove(blok)

                # Kreslenie lopty
                self.platno.create_oval(
                    lopta.x - lopta.polomer, lopta.y - lopta.polomer,
                    lopta.x + lopta.polomer, lopta.y + lopta.polomer,
                    fill=lopta.farba, outline=""
                )

        # Kontrola herného stavu
        if not self.koniec and not self.vyhra:
            if not self.lopty:
                if self.zivoty > 0:
                    if self.casovac is None:
                        self.zivoty -= 1
                        self.casovac = time.time()
                    elif time.time() - self.casovac >= 2:
                        self.lopty.append(Lopta(self.SIRKA // 2, self.VYSKA // 2, 0, self.RYCHLOST_LOPTY))
                        self.casovac = None
                else:
                    self.koniec = True
                    self.konecny_cas = int(time.time() - self.start_cas)
            if not self.bloky:
                self.vyhra = True
                self.konecny_cas = int(time.time() - self.start_cas)

        # Obrazovka konca hry
        if self.koniec:
            self.platno.create_text(
                self.SIRKA // 2, self.VYSKA // 2,
                text="KONIEC HRY",
                fill="#FF3C3C",
                font=("Arial", 40)
            )
            self.platno.create_text(
                self.SIRKA // 2, self.VYSKA // 2 + 60,
                text="RESTART",
                fill=self.BIELA,
                font=("Arial", 20)
            )
            self.restart_obdlznik = True

        # Obrazovka výhry
        if self.vyhra:
            self.platno.create_text(
                self.SIRKA // 2, self.VYSKA // 2 - 60,
                text=f"{self.konecny_cas}s",
                fill=self.BIELA,
                font=("Arial", 18)
            )
            self.platno.create_text(
                self.SIRKA // 2, self.VYSKA // 2,
                text="VÝHRA",
                fill="#50FF50",
                font=("Arial", 40)
            )
            self.platno.create_text(
                self.SIRKA // 2, self.VYSKA // 2 + 60,
                text="RESTART",
                fill=self.BIELA,
                font=("Arial", 20)
            )
            self.restart_obdlznik = True

        # Naplánovanie ďalšej aktualizácie (60 FPS)
        self.root.after(16, self.aktualizuj)

# Spustenie hry
root = tk.Tk()  # Vytvorenie hlavného okna
hra = BreakoutHra(root)  # Vytvorenie inštancie hry
root.mainloop()  # Spustenie hlavnej slučky
