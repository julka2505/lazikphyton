
import math
import random
import turtle


# =========================
# FUNKCJE POMOCNICZE
# =========================

def pobierz_int(komunikat, minimum=None, maksimum=None, domyslna=None):
    while True:
        wartosc = input(komunikat)

        if wartosc == "" and domyslna is not None:
            return domyslna

        try:
            liczba = int(wartosc)

            if minimum is not None and liczba < minimum:
                print(f"Podaj wartość >= {minimum}")
                continue

            if maksimum is not None and liczba > maksimum:
                print(f"Podaj wartość <= {maksimum}")
                continue

            return liczba

        except ValueError:
            print("Błąd! Podaj poprawną liczbę całkowitą.")


def ogranicz_wspolrzedne(x, y, granica):
    x = max(-granica, min(granica, x))
    y = max(-granica, min(granica, y))
    return x, y


# =========================
# WIZUALIZACJA TURTLE
# =========================

def rysuj_trase(trasa, granica, cel):
    ekran = turtle.Screen()
    ekran.title("Symulator wyprawy - trasa łazika")

    rysownik = turtle.Turtle()
    rysownik.speed(0)
    rysownik.pensize(2)

    # Rysowanie granic świata
    granice = turtle.Turtle()
    granice.hideturtle()
    granice.speed(0)

    granice.penup()
    granice.goto(-granica, -granica)
    granice.pendown()

    for _ in range(4):
        granice.forward(granica * 2)
        granice.left(90)

    # Punkt celu
    cel_turtle = turtle.Turtle()
    cel_turtle.hideturtle()
    cel_turtle.penup()
    cel_turtle.goto(cel[0], cel[1])
    cel_turtle.dot(15, "red")
    cel_turtle.write(" CEL", font=("Arial", 10, "bold"))

    # Punkt startowy
    start_x, start_y = trasa[0]

    rysownik.penup()
    rysownik.goto(start_x, start_y)
    rysownik.dot(12, "green")
    rysownik.write(" START", font=("Arial", 10, "bold"))
    rysownik.pendown()

    # Rysowanie trasy
    for punkt in trasa[1:]:
        rysownik.goto(punkt[0], punkt[1])

    # Punkt końcowy
    koniec_x, koniec_y = trasa[-1]

    koniec = turtle.Turtle()
    koniec.hideturtle()
    koniec.penup()
    koniec.goto(koniec_x, koniec_y)
    koniec.dot(12, "blue")
    koniec.write(" KONIEC", font=("Arial", 10, "bold"))

    turtle.done()


# =========================
# GŁÓWNA SYMULACJA
# =========================

def uruchom_symulacje():

    print("\n==============================")
    print(" SYMULATOR WYPRAWY ŁAZIKA")
    print("==============================\n")

    print("Podaj parametry wyprawy.")
    print("Jeśli chcesz użyć wartości domyślnej, naciśnij ENTER.\n")

    nazwa = input("Nazwa łazika: ")
    if nazwa.strip() == "":
        nazwa = "Explorer"

    x = pobierz_int("Pozycja startowa X (-100 do 100): ", -100, 100, 0)
    y = pobierz_int("Pozycja startowa Y (-100 do 100): ", -100, 100, 0)

    kat = pobierz_int("Kąt startowy (0-359): ", 0, 359, 0)

    energia = pobierz_int(
        "Początkowa energia (10-200): ",
        10,
        200,
        100
    )

    trudnosc = pobierz_int(
        "Poziom trudności 1-3: ",
        1,
        3,
        1
    )

    granica_swiata = 100
    limit_krokow = 20 + (10 - trudnosc * 2)

    cel = (
        random.randint(-80, 80),
        random.randint(-80, 80)
    )

    # Historia wyprawy
    trasa = [(x, y)]
    wydarzenia = []

    krok = 0
    sukces = False
    przyczyna_konca = ""

    print("\n==============================")
    print(" START WYPRAWY")
    print("==============================")
    print(f"Nazwa łazika: {nazwa}")
    print(f"Pozycja startowa: ({x}, {y})")
    print(f"Kąt startowy: {kat}°")
    print(f"Energia początkowa: {energia}")
    print("Granice świata: od -100 do 100")
    print(f"Cel wyprawy: dotrzeć do punktu {cel}")
    print(f"Limit kroków: {limit_krokow}")
    print("==============================\n")

    # =========================
    # PĘTLA SYMULACJI
    # =========================

    while True:

        krok += 1

        if krok > limit_krokow:
            przyczyna_konca = "Przekroczono limit kroków."
            break

        if energia <= 0:
            przyczyna_konca = "Łazikowi zabrakło energii."
            break

        print(f"\n----- KROK {krok} -----")

        stara_x = x
        stara_y = y
        stara_energia = energia

        # Losowa zmiana kierunku
        zmiana_kata = random.randint(-45, 45)
        kat += zmiana_kata
        kat %= 360

        # Ruch
        dystans = random.randint(5, 15)

        nowy_x = x + int(math.cos(math.radians(kat)) * dystans)
        nowy_y = y + int(math.sin(math.radians(kat)) * dystans)

        # Sprawdzenie granic
        if (
            nowy_x < -granica_swiata
            or nowy_x > granica_swiata
            or nowy_y < -granica_swiata
            or nowy_y > granica_swiata
        ):
            print("Łazik próbował opuścić świat!")
            energia -= 10

            nowy_x, nowy_y = ogranicz_wspolrzedne(
                nowy_x,
                nowy_y,
                granica_swiata
            )

            wydarzenia.append("Uderzenie w granicę świata")

        # Zużycie energii
        energia -= dystans

        # Aktualizacja pozycji
        x = nowy_x
        y = nowy_y

        print(f"Ruch o dystans: {dystans}")
        print(f"Zmiana kąta: {zmiana_kata}°")
        print(f"Pozycja przed ruchem: ({stara_x}, {stara_y})")
        print(f"Pozycja po ruchu: ({x}, {y})")

        print(f"Energia przed krokiem: {stara_energia}")
        print(f"Energia po ruchu: {energia}")

        # =========================
        # ELEMENTY ŚWIATA
        # =========================

        typ_pola = random.choice([
            "spokojne",
            "burza",
            "stacja",
            "krater"
        ])

        if typ_pola == "burza":
            strata = random.randint(5, 20)
            energia -= strata

            print("Zdarzenie: Burza piaskowa!")
            print(f"Łazik stracił {strata} energii.")

            wydarzenia.append("Burza piaskowa")

        elif typ_pola == "stacja":
            bonus = random.randint(10, 25)
            energia += bonus

            print("Zdarzenie: Stacja ładowania!")
            print(f"Łazik odzyskał {bonus} energii.")

            wydarzenia.append("Stacja ładowania")

        elif typ_pola == "krater":
            przesuniecie_x = random.randint(-10, 10)
            przesuniecie_y = random.randint(-10, 10)

            x += przesuniecie_x
            y += przesuniecie_y

            x, y = ogranicz_wspolrzedne(
                x,
                y,
                granica_swiata
            )

            print("Zdarzenie: Krater!")
            print(
                f"Łazik został przesunięty o "
                f"({przesuniecie_x}, {przesuniecie_y})"
            )

            wydarzenia.append("Krater")

        else:
            print("Spokojny teren. Nic się nie wydarzyło.")

        # =========================
        # LOSOWE ZDARZENIA
        # =========================

        losowe = random.randint(1, 100)

        # Znalezisko
        if losowe <= 15:
            energia += 15

            print("Losowe zdarzenie: znaleziono zapasowe baterie!")
            print("Energia +15")

            wydarzenia.append("Zapasowe baterie")

        # Awaria
        elif losowe >= 90:
            energia -= 20

            print("Losowe zdarzenie: awaria silnika!")
            print("Energia -20")

            wydarzenia.append("Awaria silnika")

        print(f"Stan energii po zdarzeniach: {energia}")

        trasa.append((x, y))

        # =========================
        # WARUNEK SUKCESU
        # =========================

        odleglosc = math.sqrt((x - cel[0]) ** 2 + (y - cel[1]) ** 2)

        if odleglosc <= 10:
            sukces = True
            przyczyna_konca = "Łazik dotarł do celu!"
            break

    # =========================
    # RAPORT KOŃCOWY
    # =========================

    print("\n==============================")
    print(" RAPORT KOŃCOWY")
    print("==============================")

    print(f"Nazwa łazika: {nazwa}")
    print(f"Pozycja startowa: ({trasa[0][0]}, {trasa[0][1]})")
    print(f"Końcowa pozycja: ({x}, {y})")
    print(f"Liczba kroków: {krok}")
    print(f"Pozostała energia: {energia}")
    print(f"Cel wyprawy: {cel}")

    print("\nNajważniejsze wydarzenia:")

    if len(wydarzenia) == 0:
        print("- Brak specjalnych wydarzeń")
    else:
        for wydarzenie in set(wydarzenia):
            print(f"- {wydarzenie}")

    print(f"\nPrzyczyna zakończenia: {przyczyna_konca}")

    # Wynik końcowy
    wynik = energia + max(0, (100 - krok * 2))

    if sukces:
        print("\nWYNIK: SUKCES")
        wynik += 100
    elif energia > 0:
        print("\nWYNIK: CZĘŚCIOWY SUKCES")
    else:
        print("\nWYNIK: PORAŻKA")

    print(f"Końcowy wynik punktowy: {wynik}")

    print("==============================\n")

    # Wizualizacja
    rysuj_trase(trasa, granica_swiata, cel)


# =========================
# PROGRAM GŁÓWNY
# =========================

while True:

    uruchom_symulacje()

    ponownie = input(
        "\nCzy chcesz uruchomić nową symulację? (t/n): "
    ).lower()

    if ponownie != "t":
        print("Koniec programu.")
        break
