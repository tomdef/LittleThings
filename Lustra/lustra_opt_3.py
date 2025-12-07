MOVE_TOP = (-1, 0)
MOVE_BOTTOM = (1, 0)
MOVE_LEFT = (0, -1)
MOVE_RIGHT = (0, 1)


def get_angle(check_row: int, check_col: int, mirror_orig_pos: tuple[int,int,int], mirror_new_pos: tuple[int,int,int]) -> int:

    if check_row == mirror_new_pos[0] and check_col == mirror_new_pos[1] :
        return mirror_new_pos[2]
    elif check_row == mirror_orig_pos[0] and check_col == mirror_orig_pos[1]:
        return 0
    else:
        for r, c, ma in mirrors:
            if c == check_col and r == check_row:
                return ma
    return 0


def get_empty_fields() -> list[tuple[int, int]]:
    mirrors_positions = {(row, col) for row, col, _ in mirrors}
    result = []
    for row in range(garden_size):
        for col in range(garden_size):
            field = (row, col)
            if field not in mirrors_positions:
                result.append(field)
    return result


def check_if_mirrors_works(mirror_orig_position, mirror_new_position) -> bool:
    current_position = (0, 0)
    prev_row = -1
    prev_col = 0
    number_of_visited_mirrors = 0
    move = (1, 0)

    while True:
        row, col = current_position
        if not ((0 <= row < garden_size) and (0 <= col < garden_size)):
            return False

        current_angle: int = get_angle(row, col, mirror_orig_position, mirror_new_position)
        number_of_visited_mirrors += 1 if current_angle != 0 else 0

        if current_position == meta_position:
            return number_of_visited_mirrors == number_of_mirrors

        if current_angle == 45:
            if prev_row == row:
                move = MOVE_TOP if prev_col < col else MOVE_BOTTOM
            else:
                move = MOVE_LEFT if prev_row < row else MOVE_RIGHT
        elif current_angle == 135:
            if prev_row == current_position[0]:
                move = MOVE_BOTTOM if prev_col < col else MOVE_TOP
            else:
                move = MOVE_RIGHT if prev_row < row else MOVE_LEFT

        prev_row = current_position[0]
        prev_col = current_position[1]
        current_position = (row + move[0], col + move[1])

'''
Program glowny
'''
if __name__ == '__main__':

    input_garden = input().strip()
    garden_size = int(input_garden.split(' ')[0])
    number_of_mirrors = int(input_garden.split(' ')[1])

    mirrors: list[tuple[int, int, int]] = []

    for i in range(number_of_mirrors):
        mirror_info = input()
        x, y, angle = map(int, mirror_info.split(' '))
        mirrors.append((x, y, angle))

    # example data:
    #input_garden = '5 6'
    #input_mirrors = ['0 4 45', '1 1 45', '3 0 135', '3 3 45', '4 1 135', '4 4 135']

    meta_position = (garden_size -1, garden_size - 1)
    empty_fields = get_empty_fields()

    for mirror in mirrors:
        for (empty_field_row, empty_field_col) in empty_fields:
            for angle in [45, 135]:
                new_mirror_position = (empty_field_row, empty_field_col, angle)
                if check_if_mirrors_works(mirror, new_mirror_position):
                    print(f'{mirror[0]} {mirror[1]}')
                    print(f'{new_mirror_position[0]} {new_mirror_position[1]} ')
                    exit(0)