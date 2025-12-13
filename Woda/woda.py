import heapq

'''
    Least Common Multiple (LCM)
'''
def lcm_list(numbers: list[int]) -> int:
    res = numbers[0]
    for x in numbers[1:]:
        while x != 0:
            res, x = x, res % x
    return res

if __name__ == "__main__":

    N = int(input())
    buckets = list(map(int, input().split()))

    # utworzenie stanu pocz¹tkowego (np. [20, 0, 0, 0]))
    start_state = tuple([buckets[0]] + [0] * (N - 1))

    if (lcm_list(buckets) != 1):
         print("BRAK")
         exit(0)

    MAX_STEPS: int = 8
    all_states = [(0, 0, start_state)]

    state_with_minimum_cost = {}
    state_with_minimum_cost[start_state] = {0: 0}

    final_min_cost = float('inf')
    final_state = None

    while all_states:

        # wyci¹gniêcie z listy stanów ostatniego stanu
        (cost, steps, state) = heapq.heappop(all_states)

        # jeœli wyci¹gniêty koszt jest wiêkszy ni¿ znaleziony optymalny dla tej samej liczby kroków
        if cost > state_with_minimum_cost.get(state, {}).get(steps, float('inf')):
             continue

        # Osi¹gniêto stan oczekiwane, tj. w jednym z pojemników jest 1 litr
        if 1 in state:
            if cost < final_min_cost:
                #print(f"Cost={cost}|Steps={steps}|State={state}")
                final_min_cost = cost
                final_state = state
            continue

        # Ograniczenie liczby kroków
        next_steps = steps + 1
        if next_steps > MAX_STEPS:
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
                new_state = tuple(new_state)
                
                # koszt (ilosc przelanej wody) osiagniacia nowego stanu
                new_cost = cost + water_to_transfer
                
                # pobieram minimalny koszt osi¹gniêcia new_state w next_steps
                min_cost_at_next_steps = state_with_minimum_cost.get(new_state, {}).get(next_steps, float('inf'))

                if new_cost < min_cost_at_next_steps:
                    
                    # Aktualizacja kosztu dla tego stanu i kroku
                    if new_state not in state_with_minimum_cost:
                        state_with_minimum_cost[new_state] = {}
                        
                    state_with_minimum_cost[new_state][next_steps] = new_cost
                    heapq.heappush(all_states, (new_cost, next_steps, new_state))


    if final_min_cost is not None and final_state is not None:
        print(final_min_cost)
    else:
        print("BRAK")