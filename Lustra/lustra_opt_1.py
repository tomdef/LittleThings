def parse_input(input_g, input_m):
    g = int(input_g.split(' ')[0])
    m = []
    for line in input_m:
        m.append(tuple(map(int, line.split())))
    return g, m

MOVE_TOP = (-1, 0)
MOVE_BOTTOM = (1, 0)
MOVE_LEFT = (0, -1)
MOVE_RIGHT = (0, 1)

'''
Metoda sprawdzająca czy bieżąca konfiguracja luster w ogrodzie spełnia warunek widoczności we->wy
'''
def check_if_mirrors_works(garden_to_check: list[list[int]], meta_position: tuple[int,int], number_of_mirrors: int) -> bool:
    # pozycja startowa
    current_position = (0, 0)
    # poprzednia pozycja potrzebna do ustalenia kierunku ruchu
    prev_position = (-1, 0) # init position outside garden
    # ilość odwiedzonych luster - światło musi się odbić od wszystkich luster
    number_of_visited_mirrors = 0
    # rodzaj ruchu
    move = (1, 0) # first move

    while True:
        # Sprawdzanie, czy promień jest nadal w ogrodzie
        col, row  = current_position
        if not ((0 <= row < garden_size) and (0 <= col < garden_size)):
            return False

        current_angle: int = garden_to_check[col][row]
        number_of_visited_mirrors += 1 if current_angle != 0 else 0

        # Osiągnięcie mety przy poprawnej liczbie odbić
        if current_position == meta_position:
            return number_of_visited_mirrors == number_of_mirrors

        if current_angle == 45:
            if prev_position[0] == current_position[0]:
                # ruch pionowy
                move = MOVE_TOP if prev_position[1] < current_position[1] else MOVE_BOTTOM
            else:
                # ruch poziomy
                move = MOVE_LEFT if prev_position[0] < current_position[0] else MOVE_RIGHT
        elif current_angle == 135:
            if prev_position[0] == current_position[0]:
                # ruch pionowy
                move = MOVE_BOTTOM if prev_position[1] < current_position[1] else MOVE_TOP
            else:
                # ruch poziomy
                move = MOVE_RIGHT if prev_position[0] < current_position[0] else MOVE_LEFT

        prev_position = current_position
        current_position = (col + move[0], row + move[1])


'''
Metoda tworząca tablicę opisująca ogród z lustrami
Komórka z wartością 0 - puste pole, 45 - lustro, 135 - lustro
'''
def create_garden_with_mirrors(g_size:int, m_positions:list[tuple[int, int, int]]):
    garden_fields = [[0 for _ in range(g_size)] for _ in range(g_size)]
    for item in m_positions:
        (x,y,a) = item
        garden_fields[x][y] = a
    return garden_fields


'''
Metoda zwraca listę pustych pól - to na te pola można przestawiać lustra
'''
def get_empty_fields(garden_to_check: list[list[int]]) -> list[tuple[int,int]]:
    e_fields: list[tuple[int, int]] = []
    for row in range(len(garden_to_check)):
        for col in range(len(garden_to_check[row])):
            if garden_to_check[col][row] == 0:
                e_fields.append((col, row))
    return e_fields


'''
Program główny
'''
if __name__ == '__main__':

    # example data:
    input_garden = '5 6'
    input_mirrors = ['0 4 45', '1 1 45', '3 0 135', '3 3 45', '4 1 135', '4 4 135']

    # parsuję rozmiar ogrodu i ilość luster
    garden_size, mirrors  = parse_input(input_garden, input_mirrors)
    garden = create_garden_with_mirrors(garden_size, mirrors)
    empty_fields = get_empty_fields(garden)
    mirror_count = len(mirrors)
    meta = (garden_size -1, garden_size - 1)

    # pętla po wszystkich lustrach i wszystkich miejscach do których te lustra można przesunąć
    # testuję poprawny przebieg światła dla kąta 45 i 135 stopni
    for mirror in mirrors:
        orig_col, orig_row, orig_angle = mirror[0], mirror[1], mirror[2]
        # usuwam lustro z oryginalnej pozycji
        garden[orig_col][orig_row] = 0
        for (empty_field_col, empty_field_row) in empty_fields:
            for angle in [45, 135]:
                garden[empty_field_col][empty_field_row] = angle

                # sprawdzam czy ta zmiana położenia lustra daje poprawny przebieg światła
                if check_if_mirrors_works(garden, meta, mirror_count):
                    print(f'{orig_col} {orig_row}')
                    print(f'{empty_field_col} {empty_field_row} ')
                    exit(0)
                garden[empty_field_col][empty_field_row] = 0
        garden[orig_col][orig_row] = orig_angle