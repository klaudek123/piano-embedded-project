import tkinter as tk
import pygame
import numpy as np
import sounddevice as sd

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

# Inicjalizacja Pygame (do obsługi dźwięków)
pygame.init()

# Tworzenie okna głównego
root = tk.Tk()
root.title("Wirtualne pianino")
root.geometry("1280x400")
# Lista klawiszy pianina
klawisze_pianina = ['C4','C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4', 'G4', 'G#4', 'A4', 'A#4', 'H4', 'C5', 'C#5', 'D5', 'D#5', 'E5', 'F5', 'F#5', 'G5', 'G#5', 'A5', 'A#5', 'H5']

# Funkcja tworząca przyciski dla klawiszy pianina
def stworz_klawisz(klawisz):
    return tk.Button(root, width=4, height=8, bg='white', fg='grey', font=("arial", 18, "bold"), text=klawisz ,command=lambda: klikniecie_klawisza(klawisz))

def stworz_klawisz_czarny(klawisz):
    return tk.Button(root, width=3, height=5, bg='black', fg='white', font=("arial", 12, "bold"), text=klawisz, command=lambda: klikniecie_klawisza(klawisz))

def stworz_klawisz(klawisz, czarny=False):
    if czarny:
        return tk.Button(root, width=3, height=5, bg='black', fg='white', font=("arial", 12, "bold"), text=klawisz, command=lambda: klikniecie_klawisza(klawisz))
    else:
        return tk.Button(root, width=4, height=8, bg='white', fg='grey', font=("arial", 18, "bold"), text=klawisz, command=lambda: klikniecie_klawisza(klawisz))

# Dodanie klawiszy do interfejsu na zmianę
for i in range(len(klawisze_pianina)):
    #przycisk_bialy = stworz_klawisz(klawisze_pianina[i])
    # przycisk_bialy.pack(side=tk.LEFT)
    #
    # # Sprawdzenie, czy są jeszcze klawisze czarne do dodania
    # if i < len(klawisze_czarne):
    #     przycisk_czarny = stworz_klawisz(klawisze_czarne[i], czarny=True)
    #     przycisk_czarny.pack(side=tk.LEFT, padx=(0, 10))  # Dodanie odstępu między klawiszami czarnymi
    if( '#' in klawisze_pianina[i]):
        przycisk_czarny = stworz_klawisz(klawisze_pianina[i], True)
        przycisk_czarny.pack(side=tk.LEFT)
    else:
        przycisk_bialy = stworz_klawisz(klawisze_pianina[i])
        przycisk_bialy.pack(side=tk.LEFT)

# Rozpoczęcie głównej pętli programu
root.mainloop()


