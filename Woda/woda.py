import heapq

'''
    Least Common Multiple (LCM)
'''
def lcm(a: int, b: int)-> int:
    while b != 0:
        a, b = b, a % b
    return a

def lcm_list(numbers: list[int]) -> int:
    res = numbers[0]
    for x in numbers[1:]:
        res = lcm(res, x)
    return res

if __name__ == "__main__":

    N = int(input())
    buckets = list(map(int, input().split()))

    # utworzenie stanu pocz¹tkowego (np. [20, 0, 0, 0]))
    start_state: list[int] = [buckets[0]] + [0] * (N - 1)

    if (lcm_list(buckets) != 1):
         print("BRAK")
         exit(0)
    
    N = len(buckets)

    all_states = [(0, start_state)]
    state_with_minimum_cost = {tuple(start_state):0}

    while all_states:

        # wyci¹gniêcie z listy stanów ostatniego stanu
        (cost, state) = heapq.heappop(all_states)
        
        if 1 in state:
            print(cost)
            exit(0)

        # Przetwarzaj tylko, jesli obecny koszt jest faktycznie najlepszy
        # jeœli element nie istnieje - zwraca nieskoñczonoœæ czyli float('inf')
        if cost > state_with_minimum_cost.get(tuple(state), float('inf')):
            continue

        # dla wszystkich pojemników...
        for i in range(N):            
            # jeœli pojemnik jest pusty - pomiñ
            if state[i] == 0:
                continue
                
            # ustalenie stanu pojemnika Ÿród³owego
            state_src = state[i]

            # szukamy pojemnika docelowego
            for j in range(N):
                # oczywiœcie pomijamy ten sam pojemnik
                if i == j:
                    continue

                # ustalenie stanu i pojemnoœci pojemnika docelowego
                state_dest = state[j]
                capacity_dest = buckets[j]

                # Ustalenia maksymalnej ilosci wody, ktora mozna przelac
                free_space_dest = capacity_dest - state_dest
                water_to_transfer = min(state_src, free_space_dest)
                
                # pomijamy jeœli nic nie mo¿na przelaæ
                if water_to_transfer == 0:
                    continue
               
                # kopia bie¿¹cego stanu do modyfikacji
                new_state = list(state) 

                # przelanie wody
                new_state[i] = state_src - water_to_transfer
                new_state[j] = state_dest + water_to_transfer
                
                # koszt (ilosc przelanej wody) osiagniacia nowego stanu
                new_cost = cost + water_to_transfer
                
                # Relaksacja Dijkstry
                if new_cost < state_with_minimum_cost.get(tuple(new_state), float('inf')):
                    state_with_minimum_cost[tuple(new_state)] = new_cost
                    heapq.heappush(all_states, (new_cost, new_state))