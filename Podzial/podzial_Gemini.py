def minimum_divide(S_cyfr):
    N = len(S_cyfr)
    # Ustawienie nieskończoności
    INF = float('inf')

    # DP[i] = minimalna liczba kawałków dla prefiksu S[0...i-1]
    DP = [INF] * (N + 1)
    DP[0] = 0  # 0 kawałków dla pustego prefiksu

    # Utworzenie napisu z ciągu cyfr dla łatwiejszego wycinania podciągów
    S = "".join(map(str, S_cyfr))

    # ITERACJA: Obliczanie DP[i] dla i od 1 do N
    for i in range(1, N + 1):
        # Sprawdzamy wszystkie możliwe punkty przecięcia j
        # j jest początkiem ostatniego kawałka S[j...i-1]
        for j in range(i):

            # Wymóg: Jeśli nie udało się podzielić prefiksu S[0...j-1],
            # nie możemy kontynuować od tego miejsca
            if DP[j] == INF:
                continue

            # Kawałek do sprawdzenia: podciąg S[j...i-1]
            kawalek_str = S[j:i]

            # 1. Sprawdź warunek unikalności cyfr
            if not is_unique(kawalek_str):
                continue

            # 2. Utwórz liczbę i sprawdź warunek pierwszości
            try:
                liczba = int(kawalek_str)
                # Ograniczenie: Liczba nie może zaczynać się od zera (chyba że jest to 0, ale 0 nie jest pierwsza)
                if len(kawalek_str) > 1 and kawalek_str[0] == '0':
                    continue

            except ValueError:
                continue  # Błąd konwersji (nie powinien wystąpić)

            # Użycie sita do sprawdzenia pierwszości
            if is_prime(liczba):
                # Jeśli S[j...i-1] jest prawidłowym kawałkiem, możemy uaktualnić DP[i]
                DP[i] = min(DP[i], DP[j] + 1)
                print(f'DP[{i}] = {DP[i]}|{liczba}|kawalek={kawalek_str}')

    # WYNIK KOŃCOWY
    min_kawalek = DP[N]

    # Wymóg: Podział musi być na co najmniej dwa kawałki (min_kawalek >= 2)
    if min_kawalek >= 2 and min_kawalek != INF:
        return min_kawalek
    else:
        return "BRAK"


"""
check if all digits in string are unique
"""
def is_unique(value: int) -> bool:
    value_str = str(value)
    for char in value_str:
        if value_str.count(char) > 1:
            return False
    return True

"""
check if number is prime
"""
def is_prime(value: int) -> bool:
    if value < 2:
        return False
    for i in range(2, int(value**0.5) + 1):
        if value % i == 0:
            return False
    return True

"""
check if input data is valid
    1) length between 9 and 99
    2) all signs are digits
"""
def validate_row(row_value: str) -> bool:
    if len(row_value) < 2 or len(row_value) > 99:
        return False
    else:
        for i, current in enumerate(row_value):
            if not current.isdigit():
                return False
        return True

"""
main program
"""
if __name__ == "__main__":

    row: str = '1374121319'
    if validate_row(row):
        print(minimum_divide(row))
    else:
        print("Ciąg wejściowy nie spełnia wymagań")