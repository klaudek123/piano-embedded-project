import time
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from ttkthemes import ThemedTk
from datetime import datetime, timedelta

import numpy as np
import pygame
import sounddevice as sd

import sqlite3
import datetime


aktualny_klawisz_sekwencji = None
start_time = None
nagrywanie = False

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

def odtworz_wybrany_utwor(id_utworu):
    conn = sqlite3.connect('sekwencje_pianina.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Sekwencje WHERE id_utworu=?", (id_utworu,))
    sekwencja = cursor.fetchall()

    # Odtwarzanie sekwencji utworu
    for row in sekwencja:
        klawisz = row[2]
        czas_nacisniecia = row[3]

        zagraj_dzwiek(klawisz)
        time.sleep(czas_nacisniecia)  # Poczekaj przed odtworzeniem kolejnego dźwięku

    conn.close()


def zagraj_dzwiek(klawisz):
    # Implementacja odtwarzania dźwięku dla danego klawisza
    sample_rate = 44100
    duration = 0.1  # 0.1 second
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    note = np.sin(frequencies[klawisz] * t * 2 * np.pi)
    # Odtworzenie dźwięku
    sd.play(note, sample_rate)

def zmiana_koloru(klawisz):
    global klawisze_buttons
    for button in klawisze_buttons:
        if button['text'] == klawisz:
            button.config(bg="yellow")
            button.update_idletasks()  # Wymuszenie odświeżenia interfejsu

def reset_koloru(klawisz):
    global klawisze_buttons
    for button in klawisze_buttons:
        if button['text'] == klawisz:
            button.config(bg="white" if '#' not in klawisz else "black")
            button.update_idletasks()  # Wymuszenie odświeżenia interfejsu

def odtworz_wybrany_utwor_z_tutorialem(id_utworu):
    conn = sqlite3.connect('sekwencje_pianina.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Sekwencje WHERE id_utworu=?", (id_utworu,))
    sekwencja = cursor.fetchall()
    conn.close()

    # Odtwarzanie sekwencji utworu z podświetlaniem klawiszy
    for row in sekwencja:
        klawisz = row[2]
        czas_nacisniecia = row[3]

        zmiana_koloru(klawisz)
        zagraj_dzwiek(klawisz)
        time.sleep(czas_nacisniecia)

        # Resetowanie koloru po odtworzeniu dźwięku
        reset_koloru(klawisz)
        time.sleep(0.05)  # Dodatkowy czas, aby kolor mógł się zresetować

    conn.close()




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
kolor_tymczasowy = ""

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

# --------------------------------GUI------------------------------------
# Tutaj funkcja tworząca listę utworów:
# tryb - nagrania lub tutoriale
# where - zakładka, gdzie będzie umieszczona lista 
def lista_utworow_z_bazy(tryb, where):
    conn = sqlite3.connect('sekwencje_pianina.db')
    cursor = conn.cursor()

    # Pobieranie wszystkich utworów z tabeli Utwory
    cursor.execute("SELECT * FROM Utwory")
    utwory = cursor.fetchall()

    # Tworzenie przycisków do odtwarzania utworów
    for utwor in utwory:
        nazwa_utworu = utwor[1]
        id_utworu = utwor[0]
        if tryb == 0:
            button = tk.Button(where, text=nazwa_utworu, command=lambda id_utworu=id_utworu: odtworz_wybrany_utwor(id_utworu))
        elif tryb == 1:

            button = tk.Button(where, text=nazwa_utworu,
                               command=lambda id_utworu=id_utworu: odtworz_wybrany_utwor_z_tutorialem(id_utworu))
        button.pack()

    conn.close()

def update_timer(timer_label):
    if nagrywanie:
        elapsed_time = time.time() - start_time
        formatted_time = time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
        timer_label.config(text=formatted_time)
        timer_label.after(1000, lambda: update_timer(timer_label))

def nagrywanie_fun(przycisk_nagrywania, icons, timer_label):
    global nagrywanie
    global klawisz_lista
    global czas_lista
    global czas_nacisniecia
    global start_time

    nagrywanie = not nagrywanie

    if nagrywanie:
        przycisk_nagrywania.config(image=icons[1])
        start_time = time.time()
        update_timer(timer_label)
    else:
        przycisk_nagrywania.config(image=icons[0])
        timer_label.config(text="00:00:00")


    czas_nacisniecia = time.time()


    if nagrywanie == False:
        #TODO MARTA INPUT DO NAZWY

        zapisz_do_bazy("utworek123", klawisz_lista, czas_lista)

        klawisz_lista = []
        czas_lista = []



klawisze_buttons = []
def stworz_klawisz(where, klawisz, x, czarny=False):
    if czarny:
        button = tk.Button(where, width=6, height=12, bg='black', fg='white', text=klawisz,
                           command=lambda: klikniecie_klawisza(klawisz))
        button.place(x=x, y=100)
    else:
        button = tk.Button(where, width=12, height=20, bg='white', fg='black', text=klawisz,
                           command=lambda: klikniecie_klawisza(klawisz))
        button.place(x=x, y=100)
    klawisze_buttons.append(button)
    return button




def guiApp():
    root = ThemedTk(theme="adapta") 
    root.title("Wirtualne pianino")
    root.geometry("1024x600")

    ico = Image.open('icon22.png')
    photo = ImageTk.PhotoImage(ico)
    root.wm_iconphoto(False, photo)
    
    style = ttk.Style()
    style.configure('Custom.TButton', bordercolor='blue', background='lightgray')

    # style = Style()
 
    # This will be adding style, and 
    # naming that style variable as 
    # W.Tbutton (TButton is used for ttk.Button).
    style.configure('W.TButton', font =
               ('calibri', 10, 'bold', 'underline'),
                foreground = 'red')

    # main notebook of app
    app = ttk.Notebook(root)
    app.pack(side='top', fill='both', expand=True)

    # Pianino frame
    pianinoFrame = ttk.Frame(app)
    pianinoFrame.pack(fill='both', expand=True)


    # Buttons frame
    buttonsFrame = ttk.Frame(pianinoFrame)
    buttonsFrame.pack(side='top', fill='x', padx=10, pady=10)

    # Recordings frame
    recordingsFrame = ttk.Frame(app)
    recordingsFrame.pack(fill='both', expand=True)

    # Tutorials frame
    tutorialsFrame = ttk.Frame(app)
    tutorialsFrame.pack(fill='both', expand=True)

    # Adding tabs to the app notebook
    app.add(pianinoFrame, text='Pianino')
    app.add(recordingsFrame, text='Nagrane nagrania')
    app.add(tutorialsFrame, text='Tutorial')

    # dodanie przycisku do nagrywania sekwencji
    # skalowanie 1 ikony to przycku
    rec_icon_1_path = './rec-off.png'
    image1 = Image.open(rec_icon_1_path)
    image1 = image1.resize((50, 50), Image.LANCZOS)
    rec_icon_1 = ImageTk.PhotoImage(image1)

    # skalowanie 1 ikony to przycku
    rec_icon_2_path = './rec-on.png'
    image2 = Image.open(rec_icon_2_path)
    image2 = image2.resize((50, 50), Image.LANCZOS)
    rec_icon_2 = ImageTk.PhotoImage(image2)

    # przycisk nagrywania
    przycisk_nagrywania = ttk.Button(
        buttonsFrame, 
        image=rec_icon_1, 
        style='Custom.TButton', 
        command=lambda: nagrywanie_fun(przycisk_nagrywania, [rec_icon_1, rec_icon_2], timer_label)
    )
    przycisk_nagrywania.pack(side='left', padx=5)
    
    #czas nagrywania
    timer_label = ttk.Label(buttonsFrame, text="00:00:00", font=('Helvetica', '16'))
    timer_label.pack(side=tk.LEFT, padx=20, pady=20)

    

    # guzik_odtworz = tk.Button(buttonsFrame, text="Odtwórz utwór", command=lambda: odtworz_utwor_z_bazy(0))
    # guzik_odtworz.pack(side='left', padx=5)

    # guzik_odtworz_z_tutorialem = tk.Button(buttonsFrame, text="Odtwórz utwór z tutorialem", command=lambda: odtworz_utwor_z_bazy(1))
    # guzik_odtworz_z_tutorialem.pack(side='left', padx=5)
    

    # Adding piano keys to the pianino_frame
    x_coordinate = 0

    # white keys
    for i in range(len(klawisze_pianina)):
        if '#' not in klawisze_pianina[i]:
            przycisk_bialy = stworz_klawisz(pianinoFrame, klawisze_pianina[i], x_coordinate)
            x_coordinate += przycisk_bialy.winfo_reqwidth()

    black_key_offsets = {'C#4': 1, 'D#4': 2, 'F#4': 4, 'G#4': 5, 'A#4': 6, 'C#5':8, 'D#5':9, 'F#5':11, 'G#5':12, 'A#5':13}

    for i in range(len(klawisze_pianina)):
        if '#' in klawisze_pianina[i]:
            white_key_width = przycisk_bialy.winfo_reqwidth()
            black_key_offset = black_key_offsets[klawisze_pianina[i]]
            black_key_x = (black_key_offset * white_key_width) - (white_key_width // 3.65)

            stworz_klawisz(pianinoFrame, klawisze_pianina[i], black_key_x, czarny=True)
    
    # dodanie listy utworów w zakladce "nagrania"
    lista_utworow_z_bazy(0, recordingsFrame)

    # dodanie listy tutoriali w zakładce "tutoriale"
    lista_utworow_z_bazy(1, tutorialsFrame)

    root.mainloop()

guiApp()