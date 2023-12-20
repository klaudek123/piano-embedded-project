import tkinter as tk
import pygame

# Tutaj funkcja odtwarzająca dźwięk dla danego klawisza
def zagraj_dzwiek(klawisz):
    # Implementacja odtwarzania dźwięku dla danego klawisza
    print(f"Odtwarzam dźwięk dla klawisza {klawisz}")

# Funkcja obsługująca kliknięcie klawisza na interfejsie
def klikniecie_klawisza(klawisz):
    zagraj_dzwiek(klawisz)

# Inicjalizacja Pygame (do obsługi dźwięków)
pygame.init()

# Tworzenie okna głównego
root = tk.Tk()
root.title("Wirtualne pianino")

# Lista klawiszy pianina
klawisze_pianina = ['C', 'D', 'E', 'F', 'G', 'A', 'B']

# Funkcja tworząca przyciski dla klawiszy pianina
def stworz_klawisz(klawisz):
    return tk.Button(root, text=klawisz, command=lambda: klikniecie_klawisza(klawisz))

# Dodanie klawiszy do interfejsu
for klawisz in klawisze_pianina:
    przycisk = stworz_klawisz(klawisz)
    przycisk.pack(side=tk.LEFT)

# Rozpoczęcie głównej pętli programu
root.mainloop()


