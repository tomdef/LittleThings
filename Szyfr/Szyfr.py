
# pobiera wszystkie unikalne litery z listy równań
def get_all_unique_letters(equations):
    letters = []
    for eq in equations:
        for ch in eq:
            if ch.isalpha():
                if (letters.__contains__(ch)) == False:
                    letters.append(ch)
    return sorted(letters)

# sprawdza czy równanie zwraca prawidłowy wynik dla konkretnego przypisania liter
def calculate(equation, current_mapping):
    
    print("Oblicz dla:")
    print(" Wzór: {}".format(equation))
    print(" Kolejne wartości liter: {}".format(current_mapping))
    
    letter_mapping = {}
    
    for i in range(0, len(current_mapping) - 1):
        letter = chr(ord('A') + i)
        letter_mapping[letter] = current_mapping[i]

    print(" Mapowanie liter: {}".format(letter_mapping))

    for m in letter_mapping:
        equation = equation.replace(m, str(letter_mapping[m]))

    left, right = equation.replace(" ","").split('=')
    left_parts = left.split('+')
    
    left_sum = sum(int(part) for part in left_parts)
    right_value = int(right)

    is_valid = left_sum == right_value
    print(" Wzór do obliczenia: {} | {} = {} | {}".format(equation, left_sum, right_value, is_valid))

    return is_valid

# zwraca przykładowe dane
def example_data():
    n = 3
    equations = ["ABC+DEF=EGH", "BCF+FBH=IFE", "AAA+BBB=CCC"]
    return n, equations

# program główny
if __name__ == "__main__":

    n = 0
    equations = []

    x = input("Czy użyć gotowego przykładu? (t/n):").strip().lower()
    if x == 't':
        n, equations = example_data()
    else:
        n = int(input("Podaj ilość:").strip())        
        for i in range(n):
            equations.append(input("Podaj wzór {}/{}:".format(i+1,n)).strip())
    
    unique_letters = get_all_unique_letters(equations)

    print("Wzory: {}".format(equations))
    print("Unikalne litery: {}".format(unique_letters))

    calculate(equations[0], [1,2,3,4,5,6,7,8,9] );
    calculate(equations[0], [1,2,3,4,5,6,7,9,8] );