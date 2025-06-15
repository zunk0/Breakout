# Import potrebných knižníc
import tkinter as tk  # Importuje Tkinter pre vytvorenie grafického rozhrania
import random  # Importuje random pre generovanie náhodných čísel
import math  # Importuje math pre matematické operácie
import time  # Importuje time pre prácu s časom

class Lopta:  # Definuje triedu pre hernú guličku
    def __init__(self, x, y, rychlost_x, rychlost_y):  # Konštruktor triedy Lopta
        self.x = x  # Nastaví X-ovú súradnicu guličky
        self.y = y  # Nastaví Y-ovú súradnicu guličky
        self.polomer = 10  # Nastaví polomer guličky na 10 pixelov
        self.rychlost_x = rychlost_x  # Nastaví rýchlosť guličky v X smere
        self.rychlost_y = rychlost_y  # Nastaví rýchlosť guličky v Y smere
        self.farba = "white"  # Nastaví farbu guličky na bielu

class BreakoutHra:  # Definuje hlavnú triedu hry
    def __init__(self, root):  # Konštruktor triedy BreakoutHra
        self.root = root  # Uloží referenciu na hlavné okno
        self.root.title("Breakout Hra")  # Nastaví názov okna
        
        # Definícia konštánt hry
        self.SIRKA = 690  # Nastaví šírku herného okna na 690 pixelov
        self.VYSKA = 600  # Nastaví výšku herného okna na 600 pixelov
        self.RYCHLOST_LOPTY = 5  # Nastaví základnú rýchlosť guličky na 5 pixelov za frame
        self.RYCHLOST_PALICKY = 30  # Nastaví rýchlosť pohybu paličky na 30 pixelov za stlačenie
        self.FARBY = ["#5078FF", "#FF5050", "#FFDC50", "#50DC78"]  # Definuje farby blokov (modrá, červená, žltá, zelená)
        self.HNEDA = "#78643C"  # Definuje farbu kamenných blokov
        self.SVETLA_HNEDA = "#B48C50"  # Definuje farbu poškodených kamenných blokov
        self.POZADIE = "#181420"  # Definuje farbu pozadia
        self.BIELA = "#FFFFFF"  # Definuje bielu farbu
        self.TMAVE_FARBY = ["#283C80", "#802828", "#806E28", "#286E3C"]  # Definuje tmavé farby pre text

        # Vytvorenie herného plátna
        self.platno = tk.Canvas(root, width=self.SIRKA, height=self.VYSKA, bg=self.POZADIE)  # Vytvorí plátno s danými rozmermi a farbou pozadia
        self.platno.pack()  # Umiestni plátno do okna

        # Inicializácia herných premenných
        self.palicka_x = self.SIRKA // 2 - 50  # Nastaví počiatočnú X pozíciu paličky na stred mínus polovica šírky
        self.palicka_y = self.VYSKA * 0.8  # Nastaví Y pozíciu paličky na 80% výšky okna
        self.palicka_sirka = 100  # Nastaví šírku paličky na 100 pixelov
        self.palicka_vyska = 25  # Nastaví výšku paličky na 25 pixelov
        
        # Premenné pre zmenšenie paličky
        self.cas_zmeny = 0  # Inicializuje čas poslednej zmeny veľkosti paličky
        self.je_zmensena = False  # Flag indikujúci či je palička zmenšená
        self.povodna_sirka = self.palicka_sirka  # Uloží pôvodnú šírku paličky
        self.znizena_sirka = 50  # Definuje zmenšenú šírku paličky
        
        # Nastavenie životov
        self.zivoty = 3  # Nastaví počiatočný počet životov na 3
        self.polomer_zivota = 14  # Nastaví veľkosť ikony života
        self.medzera_zivotov = 10  # Nastaví medzeru medzi ikonami životov
        self.zivot_y = self.VYSKA - 30  # Nastaví Y pozíciu ikon životov
        self.zivot_x_start = 30  # Nastaví počiatočnú X pozíciu ikon životov

        # Herný stav
        self.lopty = [Lopta(self.SIRKA // 2, self.VYSKA // 2, 0, self.RYCHLOST_LOPTY)]  # Vytvorí počiatočnú guličku v strede
        self.casovac = None  # Inicializuje časovač pre respawn guličky
        self.vyhra = False  # Flag indikujúci výhru
        self.koniec = False  # Flag indikujúci koniec hry
        self.start_cas = time.time()  # Uloží čas začiatku hry
        self.konecny_cas = None  # Inicializuje čas konca hry

        # Vytvorenie blokov
        self.vytvor_bloky()  # Zavolá metódu na vytvorenie blokov

        # Nastavenie ovládania
        self.root.bind("<Left>", self.pohyb_vlavo)  # Váže klávesu vľavo na pohyb paličky vľavo
        self.root.bind("<Right>", self.pohyb_vpravo)  # Váže klávesu vpravo na pohyb paličky vpravo
        self.root.bind("<Button-1>", self.kontrola_restartu)  # Váže kliknutie myšou na kontrolu restartu

        # Spustenie hernej slučky
        self.aktualizuj()  # Zavolá metódu aktualizácie hry

    def vytvor_bloky(self):  # Metóda na vytvorenie herných blokov
        self.bloky = []  # Vytvorí prázdny zoznam blokov
        vsetky_pozicie = list(range(28))  # Vytvorí zoznam všetkých možných pozícií (28 blokov)
        plus_pozicie = random.sample(vsetky_pozicie, 5)  # Náhodne vyberie 5 pozícií pre plus bloky
        zvysne_pozicie = [pos for pos in vsetky_pozicie if pos not in plus_pozicie]  # Vytvorí zoznam zostávajúcich pozícií
        hnede_pozicie = random.sample(zvysne_pozicie, 5)  # Náhodne vyberie 5 pozícií pre kamenné bloky
        zvysne_pozicie = [pos for pos in zvysne_pozicie if pos not in hnede_pozicie]  # Aktualizuje zoznam zostávajúcich pozícií
        zmensenie_pozicie = random.sample(zvysne_pozicie, 3)  # Náhodne vyberie 3 pozície pre zmenšujúce bloky

        # Vytvorenie blokov v mriežke
        x1, y1 = 0, 0  # Inicializuje počiatočné súradnice
        for i in range(28):  # Pre každý blok
            ma_plus = i in plus_pozicie  # Kontroluje či blok má plus
            je_hneda = i in hnede_pozicie  # Kontroluje či je blok kamenný
            ma_zmensenie = i in zmensenie_pozicie  # Kontroluje či blok zmenšuje
            farba = self.HNEDA if je_hneda else self.FARBY[i // 7]  # Vyberie farbu bloku
            pocet_zasahov = 0  # Inicializuje počítadlo zásahov
            self.bloky.append([x1, y1, 90, 40, farba, ma_plus, je_hneda, ma_zmensenie, pocet_zasahov])  # Pridá blok do zoznamu
            x1 += 100  # Posunie sa na ďalšiu pozíciu v riadku
            if (i + 1) % 7 == 0:  # Ak je koniec riadku
                x1 = 0  # Resetuje X pozíciu
                y1 += 50  # Posunie sa na ďalší riadok

    def normalizuj_rychlost(self, rychlost_x, rychlost_y, cielova_rychlost):  # Metóda na normalizáciu rýchlosti
        aktualna_rychlost = (rychlost_x ** 2 + rychlost_y ** 2) ** 0.5  # Vypočíta aktuálnu rýchlosť
        if aktualna_rychlost > 0:  # Ak je rýchlosť väčšia ako 0
            return (rychlost_x / aktualna_rychlost) * cielova_rychlost, (rychlost_y / aktualna_rychlost) * cielova_rychlost  # Vráti normalizovanú rýchlosť
        return rychlost_x, rychlost_y  # Vráti pôvodnú rýchlosť ak je 0

    def pohyb_vlavo(self, event):  # Metóda pre pohyb paličky vľavo
        if not self.koniec and not self.vyhra:  # Ak hra nie je ukončená
            if self.palicka_x > 0:  # Ak palička nie je na ľavom okraji
                self.palicka_x -= self.RYCHLOST_PALICKY  # Posunie paličku vľavo

    def pohyb_vpravo(self, event):  # Metóda pre pohyb paličky vpravo
        if not self.koniec and not self.vyhra:  # Ak hra nie je ukončená
            if self.palicka_x + self.palicka_sirka < self.SIRKA:  # Ak palička nie je na pravom okraji
                self.palicka_x += self.RYCHLOST_PALICKY  # Posunie paličku vpravo

    def kontrola_restartu(self, event):  # Metóda pre kontrolu restartu
        if (self.koniec or self.vyhra) and self.restart_obdlznik:  # Ak je hra ukončená a je možné restartovať
            x, y = event.x, event.y  # Získa pozíciu kliknutia
            tlacidlo_x = self.SIRKA // 2  # Nastaví X pozíciu tlačidla
            tlacidlo_y = self.VYSKA // 2 + 60  # Nastaví Y pozíciu tlačidla
            tlacidlo_sirka = 100  # Nastaví šírku tlačidla
            tlacidlo_vyska = 40  # Nastaví výšku tlačidla
            
            if (tlacidlo_x - tlacidlo_sirka//2 <= x <= tlacidlo_x + tlacidlo_sirka//2 and  # Kontroluje či kliknutie bolo na tlačidle
                tlacidlo_y - tlacidlo_vyska//2 <= y <= tlacidlo_y + tlacidlo_vyska//2):
                self.reset_hry()  # Restartuje hru

    def reset_hry(self):  # Metóda pre reset hry
        self.palicka_x = self.SIRKA // 2 - 50  # Resetuje pozíciu paličky
        self.palicka_y = self.VYSKA * 0.8  # Resetuje Y pozíciu paličky
        self.palicka_sirka = 100  # Resetuje šírku paličky
        self.palicka_vyska = 25  # Resetuje výšku paličky
        self.zivoty = 3  # Resetuje počet životov
        self.lopty = [Lopta(self.SIRKA // 2, self.VYSKA // 2, 0, self.RYCHLOST_LOPTY)]  # Vytvorí novú guličku
        self.casovac = None  # Resetuje časovač
        self.vyhra = False  # Resetuje flag výhry
        self.koniec = False  # Resetuje flag konca
        self.vytvor_bloky()  # Vytvorí nové bloky
        self.start_cas = time.time()  # Resetuje čas začiatku

    def aktualizuj(self):  # Hlavná herná slučka
        self.platno.delete("all")  # Vymaže celé plátno

        # Kontrola zmenšenia paličky
        if self.je_zmensena and time.time() - self.cas_zmeny >= 5:  # Ak je palička zmenšená a uplynulo 5 sekúnd
            self.je_zmensena = False  # Resetuje flag zmenšenia
            delta = (self.povodna_sirka - self.palicka_sirka) // 2  # Vypočíta rozdiel šírky
            self.palicka_x -= delta  # Upraví X pozíciu
            self.palicka_sirka = self.povodna_sirka  # Obnoví pôvodnú šírku

        # Kreslenie životov
        for i in range(3):  # Pre každý život
            stred_x = self.zivot_x_start + i * (self.polomer_zivota * 2 + self.medzera_zivotov)  # Vypočíta X pozíciu
            if i < self.zivoty:  # Ak má hráč tento život
                self.platno.create_oval(  # Vykreslí plný kruh
                    stred_x - self.polomer_zivota, self.zivot_y - self.polomer_zivota,
                    stred_x + self.polomer_zivota, self.zivot_y + self.polomer_zivota,
                    fill=self.BIELA
                )
            self.platno.create_oval(  # Vykreslí prázdny kruh
                stred_x - self.polomer_zivota, self.zivot_y - self.polomer_zivota,
                stred_x + self.polomer_zivota, self.zivot_y + self.polomer_zivota,
                outline=self.BIELA, width=2
            )

        # Kreslenie času
        if not self.koniec and not self.vyhra:  # Ak hra prebieha
            uplynuly_cas = int(time.time() - self.start_cas)  # Vypočíta uplynulý čas
            self.platno.create_text(  # Vykreslí čas
                self.SIRKA - 50, self.VYSKA - 60,
                text=f"{uplynuly_cas}s",
                fill=self.BIELA,
                font=("Arial", 18)
            )

        # Kreslenie blokov
        for blok in self.bloky:  # Pre každý blok
            self.platno.create_rectangle(  # Vykreslí blok
                blok[0], blok[1],
                blok[0] + blok[2], blok[1] + blok[3],
                fill=blok[4], outline=blok[4]
            )
            if blok[5]:  # Ak má blok plus
                self.platno.create_text(  # Vykreslí plus
                    blok[0] + blok[2] // 2, blok[1] + blok[3] // 2,
                    text="+", fill=self.TMAVE_FARBY[self.FARBY.index(blok[4]) if blok[4] in self.FARBY else 0],
                    font=("Arial", 22)
                )
            elif blok[6]:  # Ak je blok kamenný
                self.platno.create_text(  # Vykreslí text STONE
                    blok[0] + blok[2] // 2, blok[1] + blok[3] // 2,
                    text="STONE", fill=self.TMAVE_FARBY[0],
                    font=("Arial", 16)
                )
            elif blok[7]:  # Ak blok zmenšuje
                self.platno.create_text(  # Vykreslí symbol zmenšenia
                    blok[0] + blok[2] // 2, blok[1] + blok[3] // 2,
                    text="><", fill=self.TMAVE_FARBY[self.FARBY.index(blok[4]) if blok[4] in self.FARBY else 0],
                    font=("Arial", 22)
                )

        # Kreslenie paličky
        self.platno.create_rectangle(  # Vykreslí paličku
            self.palicka_x, self.palicka_y,
            self.palicka_x + self.palicka_sirka, self.palicka_y + self.palicka_vyska,
            fill=self.BIELA, outline=self.BIELA
        )

        if not self.koniec and not self.vyhra:  # Ak hra prebieha
            for lopta in self.lopty[:]:  # Pre každú guličku
                lopta.x += lopta.rychlost_x  # Aktualizuje X pozíciu
                lopta.y += lopta.rychlost_y  # Aktualizuje Y pozíciu

                # Kolízie so stenami
                if lopta.x - lopta.polomer <= 0:  # Kolízia s ľavou stenou
                    lopta.x = lopta.polomer + 1  # Opraví pozíciu
                    lopta.rychlost_x *= -1  # Obráti rýchlosť
                elif lopta.x + lopta.polomer >= self.SIRKA:  # Kolízia s pravou stenou
                    lopta.x = self.SIRKA - lopta.polomer - 1  # Opraví pozíciu
                    lopta.rychlost_x *= -1  # Obráti rýchlosť
                if lopta.y - lopta.polomer <= 0:  # Kolízia s hornou stenou
                    lopta.y = lopta.polomer + 1  # Opraví pozíciu
                    lopta.rychlost_y *= -1  # Obráti rýchlosť

                # Kolízia s paličkou
                if (lopta.y + lopta.polomer >= self.palicka_y and lopta.y - lopta.polomer <= self.palicka_y + self.palicka_vyska and
                    lopta.x + lopta.polomer >= self.palicka_x and lopta.x - lopta.polomer <= self.palicka_x + self.palicka_sirka):
                    uhol_odrazu = ((lopta.x - self.palicka_x) / self.palicka_sirka - 0.5) * 2  # Vypočíta uhol odrazu
                    lopta.rychlost_x = uhol_odrazu * self.RYCHLOST_LOPTY  # Nastaví X rýchlosť
                    lopta.rychlost_y = -self.RYCHLOST_LOPTY  # Nastaví Y rýchlosť

                # Stratená lopta
                if lopta.y - lopta.polomer > self.palicka_y + self.palicka_vyska:  # Ak gulička prešla pod paličku
                    self.lopty.remove(lopta)  # Odstráni guličku
                    continue  # Pokračuje na ďalšiu guličku

                # Kolízie s blokmi
                for blok in self.bloky[:]:  # Pre každý blok
                    if (blok[0] < lopta.x < blok[0] + blok[2] and  # Kontrola kolízie
                        blok[1] < lopta.y < blok[1] + blok[3]):
                        lopta.rychlost_y *= -1  # Obráti Y rýchlosť
                        
                        if blok[6]:  # Ak je blok kamenný
                            blok[8] += 1  # Zvýši počítadlo zásahov
                            if blok[8] == 1:  # Po prvom zásahu
                                blok[4] = self.SVETLA_HNEDA  # Zmení farbu na svetlú hnedú
                            elif blok[8] >= 2:  # Po druhom zásahu
                                self.bloky.remove(blok)  # Odstráni blok
                        else:  # Ak nie je kamenný
                            if blok[5]:  # Ak má plus
                                uhol = random.uniform(0, 2 * math.pi)  # Náhodný uhol
                                nova_rychlost_x = self.RYCHLOST_LOPTY * math.cos(uhol)  # Vypočíta X rýchlosť
                                nova_rychlost_y = self.RYCHLOST_LOPTY * math.sin(uhol)  # Vypočíta Y rýchlosť
                                nova_lopta = Lopta(lopta.x, lopta.y, nova_rychlost_x, nova_rychlost_y)  # Vytvorí novú guličku
                                self.lopty.append(nova_lopta)  # Pridá guličku do zoznamu
                            elif blok[7]:  # Ak zmenšuje
                                self.je_zmensena = True  # Nastaví flag zmenšenia
                                self.cas_zmeny = time.time()  # Uloží čas zmeny
                                delta = (self.palicka_sirka - self.znizena_sirka) // 2  # Vypočíta rozdiel šírky
                                self.palicka_x += delta  # Upraví X pozíciu
                                self.palicka_sirka = self.znizena_sirka  # Zmenší paličku
                            self.bloky.remove(blok)  # Odstráni blok

                # Kreslenie lopty
                self.platno.create_oval(  # Vykreslí guličku
                    lopta.x - lopta.polomer, lopta.y - lopta.polomer,
                    lopta.x + lopta.polomer, lopta.y + lopta.polomer,
                    fill=lopta.farba, outline=""
                )

        # Kontrola herného stavu
        if not self.koniec and not self.vyhra:  # Ak hra prebieha
            if not self.lopty:  # Ak nie sú žiadne guličky
                if self.zivoty > 0:  # Ak má hráč životy
                    if self.casovac is None:  # Ak nie je aktívny časovač
                        self.zivoty -= 1  # Zníži počet životov
                        self.casovac = time.time()  # Spustí časovač
                    elif time.time() - self.casovac >= 2:  # Ak uplynuli 2 sekundy
                        self.lopty.append(Lopta(self.SIRKA // 2, self.VYSKA // 2, 0, self.RYCHLOST_LOPTY))  # Vytvorí novú guličku
                        self.casovac = None  # Resetuje časovač
                else:  # Ak nemá životy
                    self.koniec = True  # Nastaví koniec hry
                    self.konecny_cas = int(time.time() - self.start_cas)  # Uloží konečný čas
            if not self.bloky:  # Ak nie sú žiadne bloky
                self.vyhra = True  # Nastaví výhru
                self.konecny_cas = int(time.time() - self.start_cas)  # Uloží konečný čas

        # Obrazovka konca hry
        if self.koniec:  # Ak je koniec hry
            self.platno.create_text(  # Vykreslí text KONIEC HRY
                self.SIRKA // 2, self.VYSKA // 2,
                text="KONIEC HRY",
                fill="#FF3C3C",
                font=("Arial", 40)
            )
            self.platno.create_text(  # Vykreslí tlačidlo RESTART
                self.SIRKA // 2, self.VYSKA // 2 + 60,
                text="RESTART",
                fill=self.BIELA,
                font=("Arial", 20)
            )
            self.restart_obdlznik = True  # Nastaví flag pre restart

        # Obrazovka výhry
        if self.vyhra:  # Ak je výhra
            self.platno.create_text(  # Vykreslí čas
                self.SIRKA // 2, self.VYSKA // 2 - 60,
                text=f"{self.konecny_cas}s",
                fill=self.BIELA,
                font=("Arial", 18)
            )
            self.platno.create_text(  # Vykreslí text VÝHRA
                self.SIRKA // 2, self.VYSKA // 2,
                text="VÝHRA",
                fill="#50FF50",
                font=("Arial", 40)
            )
            self.platno.create_text(  # Vykreslí tlačidlo RESTART
                self.SIRKA // 2, self.VYSKA // 2 + 60,
                text="RESTART",
                fill=self.BIELA,
                font=("Arial", 20)
            )
            self.restart_obdlznik = True  # Nastaví flag pre restart

        # Naplánovanie ďalšej aktualizácie
        self.root.after(16, self.aktualizuj)  # Naplánuje ďalšiu aktualizáciu za 16ms (60 FPS)

# Spustenie hry
root = tk.Tk()  # Vytvorí hlavné okno
hra = BreakoutHra(root)  # Vytvorí inštanciu hry
root.mainloop()  # Spustí hlavnú slučku
