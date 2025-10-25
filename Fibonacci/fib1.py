def fib_sequence(limit):
    """Generuje ciąg Fibonacciego do momentu, aż suma przekroczy limit."""
    fib = [0, 1]
    while fib[-1] <= limit:
        fib.append(fib[-1] + fib[-2])
    return fib

def exists_contiguous_subsequence_with_sum(fib, target):
    """Sprawdza, czy istnieje spójny podciąg o zadanej sumie."""
    left = 0
    current_sum = 0

    for right in range(len(fib)):
        current_sum += fib[right]

        # Ograniczamy sumę z lewej strony
        while current_sum > target and left <= right:
            current_sum -= fib[left]
            left += 1

        if current_sum == target:
            print(f"Znaleziono podciąg: {fib[left:right+1]}")
            return True

    return False


if __name__ == "__main__":
    target = int(input("Podaj sumę, której szukasz: "))
    fib = fib_sequence(target)
    print("Ciąg Fibonacciego:", fib)

    if not exists_contiguous_subsequence_with_sum(fib, target):
        print("Nie istnieje spójny podciąg o tej sumie.")
