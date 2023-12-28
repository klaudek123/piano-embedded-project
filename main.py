import time
import tkinter as tk

import numpy as np
import pygame
import sounddevice as sd

import sqlite3
import datetime

# Tworzymy lub łączymy się z bazą danych
# Tworzymy tabelę w bazie danych

# Funkcja zapisująca sekwencję do bazy danych SQLite
def zapisz_do_bazy(nazwa_utworu, klawisz_lista, czas_lista):
    print("lista klawiszy:")
    print(klawisz_lista)
    print("czas dla kawiszy: ")
    print(czas_lista)
    conn = sqlite3.connect('sekwencje_pianina.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Utwory (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       nazwa_utworu TEXT,
                       data_utworu TIMESTAMP)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Sekwencje (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_utworu NUMBER,
                    klawisz TEXT,
                    czas_nacisniecia REAL)''')

    # Dodanie utworu do tabeli Utwory
    cursor.execute('''INSERT INTO Utwory (nazwa_utworu, data_utworu) VALUES (?, ?)''', (nazwa_utworu, datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S")))

    # Pobranie ID dodanego utworu
    id_utworu = cursor.lastrowid

    for i in range(len(klawisz_lista)):
        cursor.execute('''INSERT INTO Sekwencje (id_utworu, klawisz, czas_nacisniecia)
                        VALUES (?, ?, ?)''', (id_utworu, klawisz_lista[i], czas_lista[i]))
    conn.commit()
    print("Sekwencje: ")
    for row in cursor.execute("SELECT * FROM Sekwencje"):
        print(row)

    print("Utworki:")
    for row in cursor.execute("SELECT * FROM Utwory"):
        print(row)


# Częstotliwości dźwięków klawiszy
frequencies = {
    'C4': 261.63,
    'C#4': 277.18,
    'D4': 293.66,
    'D#4': 311.13,
    'E4': 329.63,
    'F4': 349.23,
    'F#4': 369.99,
    'G4': 392.00,
    'G#4': 415.30,
    'A4': 440.00,
    'A#4': 466.16,
    'H4': 493.88,
    'C5': 523.25,
    'C#5': 554.37,
    'D5': 587.33,
    'D#5': 622.25,
    'E5': 659.25,
    'F5': 698.46,
    'F#5': 739.99,
    'G5': 783.99,
    'G#5': 830.61,
    'A5': 880.00,
    'A#5': 932.33,
    'H5': 987.77
}

# Lista klawiszy pianina
klawisze_pianina = ['C4', 'C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4', 'G4', 'G#4', 'A4', 'A#4', 'H4', 'C5', 'C#5', 'D5',
                    'D#5', 'E5', 'F5', 'F#5', 'G5', 'G#5', 'A5', 'A#5', 'H5']

# Tutaj funkcja odtwarzająca dźwięk dla danego klawisza
def zagraj_dzwiek(klawisz):
    # Implementacja odtwarzania dźwięku dla danego klawisza
    sample_rate = 44100
    duration = 0.2  # 0.2 second
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    note = np.sin(frequencies[klawisz] * t * 2 * np.pi)
    # Odtworzenie dźwięku
    sd.play(note, sample_rate)


# Funkcja obsługująca kliknięcie klawisza na interfejsie
def klikniecie_klawisza(klawisz):
    zagraj_dzwiek(klawisz)

    if nagrywanie == True:
        czas_lista.append(time.time() - czas_nacisniecia)
        klawisz_lista.append(klawisz)


nagrywanie = False

czas_lista = []
klawisz_lista = []
czas_nacisniecia = time.time()


# def nagrywaj_sekwencje():
#     def zapisz_sekwencje():
#
#         nonlocal nagrywanie, czas_start, sekwencja
#         if not nagrywanie:
#             return
#
#         for idx, klawisz in enumerate(klawisze_pianina):
#             if pygame.key.get_pressed()[pygame.K_SPACE]:  # Przykładowy klawisz do zatrzymania nagrywania (spacja)
#                 nagrywanie = False
#                 break  # Przerwij pętlę gdy nagrywanie zostanie zatrzymane
#
#             if pygame.key.get_pressed()[idx]:
#                 czas_naciśnięcia = time.time() - czas_start
#
#                 sekwencja.append((klawisz, czas_naciśnięcia))
#
#         if czas_naciśnięcia >= 20:  # Przykładowy czas nagrywania [s]
#             nagrywanie = False
#
#         if nagrywanie:
#             root.after(10, zapisz_sekwencje)  # Kontynuuj nagrywanie co 10 ms
#
#
#     nagrywanie = True
#     czas_start = time.time()
#     sekwencja = []
#     zapisz_sekwencje()  # Rozpocznij nagrywanie


# Inicjalizacja Pygame (do obsługi dźwięków)
pygame.init()

# Tworzenie okna głównego
root = tk.Tk()
root.title("Wirtualne pianino")
root.geometry("1280x400")

def nagrywanie_fun():
    global nagrywanie
    global klawisz_lista
    global czas_lista
    global czas_nacisniecia

    nagrywanie = not nagrywanie

    czas_nacisniecia = time.time()


    if nagrywanie == False:
        #TODO MARTA INPUT DO NAZWY

        zapisz_do_bazy("utworek123", klawisz_lista, czas_lista)

        klawisz_lista = []
        czas_lista = []


def stworz_przycisk_nagrywania():
    return tk.Button(root, text="Nagrywaj sekwencję", command=lambda: nagrywanie_fun())

przycisk_nagrywania = stworz_przycisk_nagrywania()
przycisk_nagrywania.pack()


# Funkcja tworząca przyciski dla klawiszy pianina
# def stworz_klawisz(klawisz):
#     return tk.Button(root, width=4, height=8, bg='white', fg='grey', font=("arial", 18, "bold"), text=klawisz,
#                      command=lambda: klikniecie_klawisza(klawisz))
#
# def stworz_klawisz_czarny(klawisz):
#     return tk.Button(root, width=3, height=5, bg='black', fg='white', font=("arial", 12, "bold"), text=klawisz,
#                      command=lambda: klikniecie_klawisza(klawisz))

def stworz_klawisz(klawisz, czarny=False):
    if czarny:
        return tk.Button(root, width=3, height=5, bg='black', fg='white', font=("arial", 12, "bold"), text=klawisz,
                         command=lambda: klikniecie_klawisza(klawisz))
    else:
        return tk.Button(root, width=4, height=8, bg='white', fg='grey', font=("arial", 18, "bold"), text=klawisz,
                         command=lambda: klikniecie_klawisza(klawisz))

# Dodanie klawiszy do interfejsu na zmianę
for i in range(len(klawisze_pianina)):
    if '#' in klawisze_pianina[i]:
        przycisk_czarny = stworz_klawisz(klawisze_pianina[i], True)
        przycisk_czarny.pack(side=tk.LEFT)
    else:
        przycisk_bialy = stworz_klawisz(klawisze_pianina[i])
        przycisk_bialy.pack(side=tk.LEFT)

# Rozpoczęcie głównej pętli programu
root.mainloop()
