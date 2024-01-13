import time
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from ttkthemes import ThemedTk
from datetime import datetime
import threading
import pygame
import sqlite3
import datetime
import pygame.mixer

# Inicjalizacja modułu mixer
pygame.mixer.init()


aktualny_klawisz_sekwencji = None
start_time = None
nagrywanie = False

# Funkcja zapisująca sekwencję do bazy danych SQLite
def zapisz_do_bazy(nazwa_utworu, klawisz_lista, czas_lista):
    print("lista klawiszy:")
    print(klawisz_lista)
    print("czas dla kawiszy: ")
    print(czas_lista)
    # Połączenie z bazą danych SQLite
    conn = sqlite3.connect('sekwencje_pianina.db')
    cursor = conn.cursor()
    # Stworzenie tabeli Utwory, jeśli nie istnieje
    cursor.execute('''CREATE TABLE IF NOT EXISTS Utwory (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       nazwa_utworu TEXT,
                       data_utworu TIMESTAMP)''')
    # Stworzenie tabeli Sekwencje, jeśli nie istnieje
    cursor.execute('''CREATE TABLE IF NOT EXISTS Sekwencje (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_utworu INTEGER,
                    klawisz TEXT,
                    czas_nacisniecia REAL)''')
    # Dodanie utworu do tabeli Utwory
    cursor.execute('''INSERT INTO Utwory (nazwa_utworu, data_utworu) VALUES (?, ?)''', (nazwa_utworu, datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S")))

    # Pobranie ID dodanego utworu
    id_utworu = cursor.lastrowid

    # Dodanie sekwencji do tabeli Sekwencje
    for i in range(len(klawisz_lista)):
        cursor.execute('''INSERT INTO Sekwencje (id_utworu, klawisz, czas_nacisniecia)
                        VALUES (?, ?, ?)''', (id_utworu, klawisz_lista[i], czas_lista[i]))
    # Zapisanie zmian w bazie danych
    conn.commit()


def show_list_tutorials():
    conn = sqlite3.connect('sekwencje_pianina.db')
    cursor = conn.cursor()

    # Pobieranie wszystkich utworów z tabeli Utwory
    cursor.execute("SELECT * FROM Utwory")
    utwory = cursor.fetchall()

    # Przygotowanie interfejsu wyboru utworu do odtworzenia
    top = tk.Toplevel()
    top.title("Odtwarzanie utworu")

    # Zablokowanie możliwości zmiany rozmiaru okna
    top.resizable(False, False)

    # Dodanie przewijania do interfejsu
    canvas = tk.Canvas(top)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(top, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)

    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor=tk.NW)

    def play_tutorial_and_close(id_utworu, window):
        window.destroy()
        odtworz_wybrany_utwor_z_tutorialem(id_utworu)

    # Tworzenie przycisków do odtwarzania utworów
    for utwor in utwory:
        nazwa_utworu = utwor[1]
        id_utworu = utwor[0]

        button = tk.Button(frame, text=nazwa_utworu,
                           command=lambda id_utworu=id_utworu: play_tutorial_and_close(id_utworu, top))
        button.pack()

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox('all'))

    frame.bind('<Configure>', on_configure)

    conn.close()
def show_list():
    # Połączenie z bazą danych SQLite
    conn = sqlite3.connect('sekwencje_pianina.db')
    cursor = conn.cursor()

    # Pobieranie wszystkich utworów z tabeli Utwory
    cursor.execute("SELECT * FROM Utwory")
    utwory = cursor.fetchall()

    # Przygotowanie interfejsu wyboru utworu do odtworzenia
    top = tk.Toplevel()
    top.title("Odtwarzanie utworu")

    # Zablokowanie możliwości zmiany rozmiaru okna
    top.resizable(False, False)


    # Dodanie przewijania do interfejsu
    canvas = tk.Canvas(top)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(top, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)

    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor=tk.NW)

    def play_tutorial_and_close(id_utworu, window):
        window.destroy()
        odtworz_wybrany_utwor_z_tutorialem(id_utworu)

    # Tworzenie przycisków do odtwarzania utworów
    for utwor in utwory:
        nazwa_utworu = utwor[1]
        id_utworu = utwor[0]

        # Przycisk do odtwarzania wybranego utworu
        button = tk.Button(frame, text=nazwa_utworu, command=lambda id_utworu=id_utworu: play_tutorial_and_close(id_utworu, top))
        button.pack()

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox('all'))

    frame.bind('<Configure>', on_configure)

    # Zamknięcie połączenia z bazą danych
    conn.close()
def odtworz_wybrany_utwor(id_utworu):
    # Połączenie z bazą danych SQLite
    conn = sqlite3.connect('sekwencje_pianina.db')
    cursor = conn.cursor()

    # Pobranie sekwencji dla wybranego utworu
    cursor.execute("SELECT * FROM Sekwencje WHERE id_utworu=?", (id_utworu,))
    sekwencja = cursor.fetchall()

    # Zamknięcie połączenia z bazą danych
    conn.close()

    czas_nacisniecia_tmp = 0
    # Odtwarzanie sekwencji utworu z podświetlaniem klawiszy
    for row in sekwencja:
        klawisz = row[2]
        czas_nacisniecia = row[3]

        # Odtworzenie dźwięku
        zagraj_dzwiek(klawisz)

        # Poczekanie przed odtworzeniem kolejnego dźwięku
        time.sleep(czas_nacisniecia - czas_nacisniecia_tmp)

        czas_nacisniecia_tmp = czas_nacisniecia


def odtworz_wybrany_utwor_z_tutorialem(id_utworu):
    # Połączenie z bazą danych SQLite
    conn = sqlite3.connect('sekwencje_pianina.db')
    cursor = conn.cursor()

    # Pobranie sekwencji dla wybranego utworu
    cursor.execute("SELECT * FROM Sekwencje WHERE id_utworu=?", (id_utworu,))
    sekwencja = cursor.fetchall()

    # Zamknięcie połączenia z bazą danych
    conn.close()

    czas_nacisniecia_tmp = 0
    # Odtwarzanie sekwencji utworu z podświetlaniem klawiszy
    for row in sekwencja:
        klawisz = row[2]
        czas_nacisniecia = row[3]

        # Podświetlenie klawisza
        zmiana_koloru(klawisz)

        # Odtworzenie dźwięku
        zagraj_dzwiek(klawisz)

        # Poczekanie przed odtworzeniem kolejnego dźwięku
        time.sleep(czas_nacisniecia - czas_nacisniecia_tmp)

        czas_nacisniecia_tmp = czas_nacisniecia

        # Resetowanie koloru po odtworzeniu dźwięku
        reset_koloru(klawisz)

def zagraj_dzwiek(klawisz):
    # Załadowanie i odtworzenie dźwięku dla danego klawisza
    pygame.mixer.music.load(frequencies[klawisz])
    pygame.mixer.music.play()

def zmiana_koloru(klawisz):
    global klawisze_buttons
    # Zmiana koloru przycisku odpowiadającego danemu klawiszowi na żółty
    for button in klawisze_buttons:
        if button['text'] == klawisz:
            button.config(bg="yellow")
            button.update_idletasks()  # Wymuszenie odświeżenia interfejsu

def reset_koloru(klawisz):
    global klawisze_buttons
    # Zresetowanie koloru przycisku odpowiadającego danemu klawiszowi na biały (biały dla białych klawiszy, czarny dla czarnych)
    for button in klawisze_buttons:
        if button['text'] == klawisz:
            button.config(bg="white" if '#' not in klawisz else "black")
            button.update_idletasks()  # Wymuszenie odświeżenia interfejsu


# Częstotliwości dźwięków klawiszy
frequencies = {
    'C4': "24-piano-keys/key01.mp3",
    'C#4': "24-piano-keys/key02.mp3",
    'D4': "24-piano-keys/key03.mp3",
    'D#4': "24-piano-keys/key04.mp3",
    'E4': "24-piano-keys/key05.mp3",
    'F4': "24-piano-keys/key06.mp3",
    'F#4': "24-piano-keys/key07.mp3",
    'G4': "24-piano-keys/key08.mp3",
    'G#4': "24-piano-keys/key09.mp3",
    'A4': "24-piano-keys/key10.mp3",
    'A#4': "24-piano-keys/key11.mp3",
    'H4': "24-piano-keys/key12.mp3",
    'C5': "24-piano-keys/key13.mp3",
    'C#5': "24-piano-keys/key14.mp3",
    'D5': "24-piano-keys/key15.mp3",
    'D#5': "24-piano-keys/key16.mp3",
    'E5': "24-piano-keys/key17.mp3",
    'F5': "24-piano-keys/key18.mp3",
    'F#5': "24-piano-keys/key19.mp3",
    'G5': "24-piano-keys/key20.mp3",
    'G#5': "24-piano-keys/key21.mp3",
    'A5': "24-piano-keys/key22.mp3",
    'A#5': "24-piano-keys/key23.mp3",
    'H5': "24-piano-keys/key24.mp3"
}

# Lista klawiszy pianina
klawisze_pianina = ['C4', 'C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4', 'G4', 'G#4', 'A4', 'A#4', 'H4', 'C5', 'C#5', 'D5',
                    'D#5', 'E5', 'F5', 'F#5', 'G5', 'G#5', 'A5', 'A#5', 'H5']

# Utworzenie słownika dźwięków, gdzie klucz to klawisz pianina, a wartość to obiekt dźwięku stworzony z odpowiedniej częstotliwości
sounds = {klawisz: pygame.mixer.Sound(frequencies[klawisz]) for klawisz in klawisze_pianina}

# Funkcja obsługująca kliknięcie klawisza na interfejsie
def klikniecie_klawisza(klawisz):
    # Uruchomienie funkcji zagraj_dzwiek w osobnym wątku
    t = threading.Thread(target=zagraj_dzwiek, args=(klawisz,))
    t.start()

    if nagrywanie == True:
        czas_lista.append(time.time() - czas_nacisniecia)
        klawisz_lista.append(klawisz)

# Obsługa wielu naciśnięć klawiszy jednocześnie
def obsluga_wielu_klawiszy(event):
    for klawisz in event.keysym.split('+'):
        if klawisz in klawisze_pianina:
            klikniecie_klawisza(klawisz)

# Inicjalizacja zmiennych globalnych do obsługi nagrywania sekwencji
nagrywanie = False  # Flaga określająca, czy trwa nagrywanie sekwencji
czas_lista = []  # Lista przechowująca czasy naciśnięć klawiszy podczas nagrywania
klawisz_lista = []  # Lista przechowująca naciśnięte klawisze podczas nagrywania
czas_nacisniecia = time.time()  # Czas naciśnięcia pierwszego klawisza
kolor_tymczasowy = ""  # Zmienna przechowująca tymczasowy kolor (do podświetlenia klawisza)
# Uwaga: Wartości te są używane w funkcjach obsługujących interakcję z interfejsem graficznym i nagrywanie sekwencji.
# Nagrywanie sekwencji odbywa się poprzez zapisywanie czasu naciśnięcia klawisza oraz identyfikatora klawisza.


# Inicjalizacja Pygame (do obsługi dźwięków)
pygame.init()


# Funkcja wyświetlająca ostatni utwór z bazy danych w danym miejscu (where)
def ostatni_utwor_z_bazy(where):
    conn = sqlite3.connect('sekwencje_pianina.db')
    cursor = conn.cursor()

    # Pobieranie wszystkich utworów z tabeli Utwory
    cursor.execute("SELECT * FROM Utwory")
    utwory = cursor.fetchall()


    # Tworzenie przycisków do odtwarzania utworów
    for utwor in utwory:
        nazwa_utworu = utwor[1]
        id_utworu = utwor[0]
        if id_utworu == utwory[-1][0]:
            button = tk.Button(where, text=nazwa_utworu,
                                   command=lambda id_utworu=id_utworu: odtworz_wybrany_utwor_z_tutorialem(id_utworu))
            button.pack()
    # Rysowanie klawiszy pianina w danym miejscu (where)
    x_coordinate = 80
    for i in range(len(klawisze_pianina)):
        if '#' not in klawisze_pianina[i]:
            przycisk_bialy = stworz_klawisz(tutorialsFrame, klawisze_pianina[i], x_coordinate, 250)
            x_coordinate += przycisk_bialy.winfo_reqwidth()

    # Rysowanie czarnych klawiszy w danym miejscu (where)
    black_key_offsets = {'C#4': 1, 'D#4': 2, 'F#4': 4, 'G#4': 5, 'A#4': 6, 'C#5': 8, 'D#5': 9, 'F#5': 11, 'G#5': 12,
                         'A#5': 13}
    # Rysowanie czarnych klawiszy w pianinoFrame
    for i in range(len(klawisze_pianina)):
        if '#' in klawisze_pianina[i]:
            white_key_width = przycisk_bialy.winfo_reqwidth()
            black_key_offset = black_key_offsets[klawisze_pianina[i]]
            black_key_x = (black_key_offset * white_key_width) - (white_key_width // 3.1) + 100

            stworz_klawisz(tutorialsFrame, klawisze_pianina[i], black_key_x, 250, czarny=True)

    conn.close()

# Funkcja wyświetlająca listę utworów z bazy danych w danym miejscu (where)
def lista_utworow_z_bazy(where):
    conn = sqlite3.connect('sekwencje_pianina.db')
    cursor = conn.cursor()

    # Pobieranie wszystkich utworów z tabeli Utwory
    cursor.execute("SELECT * FROM Utwory")
    utwory = cursor.fetchall()

    # Tworzenie przycisków do odtwarzania utworów
    for utwor in utwory:
        nazwa_utworu = utwor[1]
        id_utworu = utwor[0]

        button = tk.Button(where, text=nazwa_utworu,
                               command=lambda id_utworu=id_utworu: odtworz_wybrany_utwor_z_tutorialem(id_utworu))
        button.pack()

    # Rysowanie klawiszy pianina w danym miejscu (where)
    x_coordinate = 80
    for i in range(len(klawisze_pianina)):
        if '#' not in klawisze_pianina[i]:
            przycisk_bialy = stworz_klawisz(tutorialsFrame, klawisze_pianina[i], x_coordinate, 250)
            x_coordinate += przycisk_bialy.winfo_reqwidth()

    # Rysowanie czarnych klawiszy w danym miejscu (where)
    black_key_offsets = {'C#4': 1, 'D#4': 2, 'F#4': 4, 'G#4': 5, 'A#4': 6, 'C#5': 8, 'D#5': 9, 'F#5': 11, 'G#5': 12,
                         'A#5': 13}
    # Rysowanie czarnych klawiszy w pianinoFrame
    for i in range(len(klawisze_pianina)):
        if '#' in klawisze_pianina[i]:
            white_key_width = przycisk_bialy.winfo_reqwidth()
            black_key_offset = black_key_offsets[klawisze_pianina[i]]
            black_key_x = (black_key_offset * white_key_width) - (white_key_width // 3.1) + 100

            stworz_klawisz(tutorialsFrame, klawisze_pianina[i], black_key_x, 250, czarny=True)

    conn.close()

# Funkcja aktualizująca timer w danym labelu
def update_timer(timer_label):
    if nagrywanie:
        elapsed_time = time.time() - start_time
        formatted_time = time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
        timer_label.config(text=formatted_time)
        timer_label.after(1000, lambda: update_timer(timer_label))

nazwa_utworu = ""

# Funkcja obsługująca nagrywanie sekwencji po naciśnięciu przycisku nagrywania
def nagrywanie_fun(przycisk_nagrywania, icons, timer_label):
    # Zmienne globalne
    global nagrywanie
    global klawisz_lista
    global czas_lista
    global czas_nacisniecia
    global start_time
    # Zmiana stanu nagrywania (rozpoczęcie lub zakończenie)
    nagrywanie = not nagrywanie

    if nagrywanie:
        przycisk_nagrywania.config(image=icons[1])
        start_time = time.time()
        update_timer(timer_label)
    else:
        przycisk_nagrywania.config(image=icons[0])
        timer_label.config(text="00:00:00")


    czas_nacisniecia = time.time()
    # Jeśli nagrywanie zakończone, przechodzi do zapisu sekwencji do bazy danych
    if nagrywanie == False:
        # Utwórz nowe okno top-level do wprowadzenia nazwy utworu
        entry_window = tk.Toplevel()
        entry_window.title("Podaj nazwę utworu")

        # Funkcja obsługująca zamknięcie okna
        global nazwa_utworu


        # Funkcja obsługująca zamknięcie okna
        def on_close():
            global nazwa_utworu
            nazwa_utworu = entry.get()
            entry_window.destroy()

        # Entry do wprowadzenia nazwy utworu
        entry = tk.Entry(entry_window)
        entry.pack(padx=10, pady=10)

        # Przycisk do potwierdzenia wprowadzonej nazwy
        confirm_button = tk.Button(entry_window, text="Potwierdź", command=on_close)
        confirm_button.pack(pady=10)

        # Czekaj na zamknięcie okna
        entry_window.wait_window()
        # Sprawdź, czy użytkownik nie anulował wprowadzania nazwy
        if not nazwa_utworu:
            return

        # Zapisz sekwencję do bazy danych
        zapisz_do_bazy(nazwa_utworu, klawisz_lista, czas_lista)

        # dodanie listy tutoriali w zakładce "tutoriale"
        #ostatni_utwor_z_bazy(scrollableTutorialsFrame)
        # Zresetowanie list nagrywania
        klawisz_lista = []
        czas_lista = []

# Lista przycisków klawiszy
klawisze_buttons = []
# Funkcja tworząca przycisk klawisza w danym miejscu
def stworz_klawisz(where, klawisz, x, y, czarny=False):
    if czarny:
        button = tk.Button(where, width=4, height=12, bg='black', fg='white', text=klawisz,
                           command=lambda: klikniecie_klawisza(klawisz))
        button.place(x=x, y=y)
    else:
        button = tk.Button(where, width=8, height=18, bg='white', fg='black', text=klawisz,
                           command=lambda: klikniecie_klawisza(klawisz))
        button.place(x=x, y=y)
    klawisze_buttons.append(button)
    return button
# Inicjalizacja zmiennych dla zakładki "tutoriale"
tutorialsFrame = None
scrollableTutorialsFrame = None

# Funkcja tworząca interfejs graficzny
def guiApp():
    global tutorialsFrame
    # Inicjalizacja głównego okna
    root = ThemedTk(theme="adapta")
    root.title("Wirtualne pianino")
    root.geometry("1024x600")
    root.attributes('-fullscreen', True)
    # Ustawienie ikony aplikacji
    ico = Image.open('icon22.png')
    photo = ImageTk.PhotoImage(ico)
    root.wm_iconphoto(False, photo)

    # Konfiguracja stylów przycisków
    style = ttk.Style()
    style.configure('Custom.TButton', bordercolor='blue', background='lightgray')
    style.configure('W.TButton', font=('calibri', 10, 'bold', 'underline'), foreground='red')

    # Inicjalizacja zakładek
    app = ttk.Notebook(root)
    app.pack(side='top', fill='both', expand=True)

    pianinoFrame = ttk.Frame(app)
    pianinoFrame.pack(fill='both', expand=True)

    buttonsFrame = ttk.Frame(pianinoFrame)
    buttonsFrame.pack(side='top', fill='x', padx=0, pady=0)

    tutorialsFrame = ttk.Frame(app) #1
    tutorialsFrame.pack(fill='both', expand=True)

    app.add(pianinoFrame, text='Pianino')
    app.add(tutorialsFrame, text='Tutorial')

    # Ikony przycisku nagrywania
    rec_icon_1_path = './rec-off.png'
    image1 = Image.open(rec_icon_1_path)
    image1 = image1.resize((50, 50), Image.LANCZOS)
    rec_icon_1 = ImageTk.PhotoImage(image1)

    rec_icon_2_path = './rec-on.png'
    image2 = Image.open(rec_icon_2_path)
    image2 = image2.resize((50, 50), Image.LANCZOS)
    rec_icon_2 = ImageTk.PhotoImage(image2)

    # Przycisk nagrywania
    przycisk_nagrywania = ttk.Button(
        buttonsFrame,
        image=rec_icon_1,
        style='Custom.TButton',
        command=lambda: nagrywanie_fun(przycisk_nagrywania, [rec_icon_1, rec_icon_2], timer_label)
    )
    przycisk_nagrywania.pack(side='left', padx=5)

    # Przycisk otwierający listę tutoriali
    przycisk_tutorialu = ttk.Button(
        buttonsFrame,
        text="UTWORY",
        style='Custom.TButton',
        command=lambda: show_list()
    )
    przycisk_tutorialu.pack(side='left', padx=5)

    # Etykieta wyświetlająca czas nagrania
    timer_label = ttk.Label(buttonsFrame, text="00:00:00", font=('Helvetica', '16'))
    timer_label.pack(side=tk.LEFT, padx=5, pady=5)

    # Tworzenie białych klawiszy w pianinoFrame
    x_coordinate = 0
    for i in range(len(klawisze_pianina)):
        if '#' not in klawisze_pianina[i]:
            przycisk_bialy = stworz_klawisz(pianinoFrame, klawisze_pianina[i], x_coordinate, 64)
            x_coordinate += przycisk_bialy.winfo_reqwidth()

    black_key_offsets = {'C#4': 1, 'D#4': 2, 'F#4': 4, 'G#4': 5, 'A#4': 6, 'C#5': 8, 'D#5': 9, 'F#5': 11, 'G#5': 12, 'A#5': 13}
    # Rysowanie czarnych klawiszy w pianinoFrame
    for i in range(len(klawisze_pianina)):
        if '#' in klawisze_pianina[i]:
            white_key_width = przycisk_bialy.winfo_reqwidth()
            black_key_offset = black_key_offsets[klawisze_pianina[i]]
            black_key_x = (black_key_offset * white_key_width) - (white_key_width // 3.1)

            stworz_klawisz(pianinoFrame, klawisze_pianina[i], black_key_x, 64, czarny=True)

    # Przycisk otwierający listę tutoriali
    przycisk_tutorialu = ttk.Button(
        tutorialsFrame,
        text="UTWORY",
        style='Custom.TButton',
        command=lambda: show_list_tutorials()
    )
    przycisk_tutorialu.pack(side='left', padx=5)

    # Tworzenie białych klawiszy w tutorialsFrame
    x_coordinate = 80
    for i in range(len(klawisze_pianina)):
        if '#' not in klawisze_pianina[i]:
            przycisk_bialy = stworz_klawisz(tutorialsFrame, klawisze_pianina[i], x_coordinate, 250)
            x_coordinate += przycisk_bialy.winfo_reqwidth()

    black_key_offsets = {'C#4': 1, 'D#4': 2, 'F#4': 4, 'G#4': 5, 'A#4': 6, 'C#5': 8, 'D#5': 9, 'F#5': 11, 'G#5': 12,
                         'A#5': 13}
    # Rysowanie czarnych klawiszy w pianinoFrame
    for i in range(len(klawisze_pianina)):
        if '#' in klawisze_pianina[i]:
            white_key_width = przycisk_bialy.winfo_reqwidth()
            black_key_offset = black_key_offsets[klawisze_pianina[i]]
            black_key_x = (black_key_offset * white_key_width) - (white_key_width // 3.1) + 100

            stworz_klawisz(tutorialsFrame, klawisze_pianina[i], black_key_x, 250, czarny=True)

    # Przypisanie funkcji do zdarzeń klawiatury
    root.bind("<KeyPress>", obsluga_wielu_klawiszy)
    root.bind("<KeyRelease>", obsluga_wielu_klawiszy)

    # Rozpoczęcie pętli głównej
    root.mainloop()

# Uruchomienie głównej funkcji interfejsu graficznego
guiApp()