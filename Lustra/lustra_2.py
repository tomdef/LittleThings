def parse_input(input_g, input_m):
    g = int(input_g.split(' ')[0])
    m = []
    for line in input_m:
        m.append(tuple(map(int, line.split())))
    return g, m

'''
Metoda sprawdzająca czy bieżąca konfiguracja luster w ogrodzie spełnia warunek widoczności we->wy
'''
def check_if_mirrors_works(garden_to_check: list[list[int]], number_of_mirrors: int) -> bool:
    is_valid: bool = True
    max_size: int = len(garden_to_check)
    # pozycja startowa
    current_position = (0, 0)
    # poprzednia pozycja potrzebna do ustalenia kierunku ruchu
    prev_position = (-1, 0) # init position outside garden
    # ilość odwiedzonych luster - światło musi się odbić od wszystkich luster
    number_of_visited_mirrors = 0
    # rodzaj ruchu
    move = (1, 0) # first move
    move_top = (-1, 0)
    move_bottom = (1, 0)
    move_left = (0, -1)
    move_right = (0, 1)
    meta = (max_size - 1, max_size - 1)

    while is_valid:
        current_angle: int = garden_to_check[current_position[0]][current_position[1]]
        number_of_visited_mirrors += 1 if current_angle != 0 else 0
        # wyznaczenie kierynku ruchu po odbiciu od lustra
        # ten kod można by jeszcze uprościć
        if current_angle == 45:
            if prev_position[0] == current_position[0]:
                # ruch pionowy
                move = move_top if prev_position[1] < current_position[1] else move_bottom
            else:
                # ruch poziomy
                move = move_left if prev_position[0] < current_position[0] else move_right
        elif current_angle == 135:
            if prev_position[0] == current_position[0]:
                # ruch pionowy
                move = move_bottom if prev_position[1] < current_position[1] else move_top
            else:
                # ruch poziomy
                move = move_right if prev_position[0] < current_position[0] else move_left

        # sprawdzam czy osiągnięto metę i odwiedzono wszystkie lustra
        if current_position[0] == meta[0] and current_position[1] == meta[1] and number_of_visited_mirrors == number_of_mirrors:
            return True

        # zapamiętuję poprzednią pozycję żeby ustalić kierunek ruchu przy odbiciu od lustra
        prev_position = current_position
        # ustalam nową pozycję
        current_position = (current_position[0] + move[0], current_position[1] + move[1])
        # sprawczam czy nowa pozycja mieści się w granicach ogrodu
        is_valid = ((0 <= current_position[0] < max_size)
                    and (0 <= current_position[1] < max_size))
    return  False


'''
Metoda tworząca tablicę opisująca ogród z lustrami
Komórka z wartością 0 - puste pole, 45 - lustro, 135 - lustro
'''
def create_garden_with_mirrors(garden_size:int, m_positions:list[tuple[int, int, int]]):
    garden_fields = [[0 for x in range(garden_size)] for y in range(garden_size)]
    for item in m_positions:
        (x,y,angle) = item
        garden_fields[x][y] = angle
    return garden_fields


'''
Metoda przesunięcia lustra na nową pozycję, z możliwościa jego obrócenia
'''
def move_mirror(current_garden, move_from, move_to, change_angle_to:int = -1):
    angle = current_garden[move_from[0]][move_from[1]]
    row = current_garden[move_from[0]]
    row[move_from[1]] = 0
    if change_angle_to > -1:
        angle = change_angle_to
    row = current_garden[move_to[0]]
    row[move_to[1]] = angle


'''
Metoda zwraca listę pustych pól - to na te pola można przestawiać lustra
'''
def get_empty_fields(garden_to_check):
    empty_fields: list[tuple[int, int]] = []
    for row_index in range(len(garden_to_check)):
        row = garden_to_check[row_index]
        for col_index in range(len(row)):
            if row[col_index] == 0:
                empty_fields.append((col_index, row_index))
    return empty_fields

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
    garden_original = [row[:] for row in garden]
    empty_fields = get_empty_fields(garden)

    # pętla po wszystkich lustrach i wszystkich miejscach do których te lustra można przesunąć
    # testuję poprawny przebieg światła dla kąta 45 i 135 stopni
    for mirror in mirrors:
        mirror_orig_position: tuple[int,int] = (mirror[0], mirror[1])
        mirror_orig_angle = mirror[2]
        for empty_field in empty_fields:
            for angle in [45, 135]:
                move_mirror(garden, mirror_orig_position, empty_field, angle)
                is_meta = check_if_mirrors_works(garden, len(mirrors))

                # sprawdzam czy ta zmiana położenia lustra daje poprawny przebieg światła
                if is_meta:
                    print (f'{mirror_orig_position[0]} {mirror_orig_position[1]}')
                    print(f'{empty_field[0]} {empty_field[1]}')
                    exit(0)
                else:
                    # jeżeli nie jest to prawidłowe położenie lustra - przywracam oryginalny układ ogrodu
                    garden = [row[:] for row in garden_original]