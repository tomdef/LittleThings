MOVE_TOP = (-1, 0)
MOVE_BOTTOM = (1, 0)
MOVE_LEFT = (0, -1)
MOVE_RIGHT = (0, 1)


def get_angle(mirrors_list: list[tuple[int, int, int]], check_row: int, check_col: int) -> int:
    for r, c, ma in mirrors_list:
        if c == check_col and r == check_row:
            return ma
    return 0


def check_if_mirrors_works(mirrors_positions: list[tuple[int, int, int]], start_from: tuple[int,int], vector:int):
    current_position = start_from
    prev_position = (current_position[0] - vector, current_position[1])
    prev_row = prev_position[0]
    prev_col = prev_position[1]
    move = (1, 0)
    visited_fields_between_last_mirror_and_border = set()
    visited_mirrors = set()

    while True:
        row, col = current_position
        if not ((0 <= row < garden_size) and (0 <= col < garden_size)):
            return visited_fields_between_last_mirror_and_border, visited_mirrors

        current_angle: int = get_angle(mirrors_positions, row, col)

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

        if current_angle != 0:
            visited_mirrors.add((row, col))
            visited_fields_between_last_mirror_and_border = set()
        else:
            visited_fields_between_last_mirror_and_border.add((row, col))

        prev_row, prev_col = row, col
        current_position = (row + move[0], col + move[1])


if __name__ == '__main__':

    input_garden = input().strip()
    garden_size = int(input_garden.split(' ')[0])
    number_of_mirrors = int(input_garden.split(' ')[1])

    mirrors: list[tuple[int, int, int]] = []

    for i in range(number_of_mirrors):
        mirror_info = input()
        x, y, angle = map(int, mirror_info.split(' '))
        mirrors.append((x, y, angle))

    start_position = (0, 0)
    meta_position = (garden_size -1, garden_size - 1)

    visited_fields_1, visited_mirrors_1 = check_if_mirrors_works(mirrors, start_position, 1)
    visited_fields_2, visited_mirrors_2 = check_if_mirrors_works(mirrors, meta_position, -1)

    all_visited_mirrors = visited_mirrors_1.union(visited_mirrors_2)
    unused_mirror = None

    if visited_fields_1 and visited_fields_2 and all_visited_mirrors:
        for mirror in mirrors:
            if mirror not in all_visited_mirrors:
                unused_mirror = mirror
                break

        field_to_move_mirror = visited_fields_1.intersection(visited_fields_2)
        if len(field_to_move_mirror) == 1:
            (from_x, from_y, _) = unused_mirror
            (to_x, to_y) = next(iter(field_to_move_mirror))
            print(f'{from_x} {from_y}')
            print(f'{to_x} {to_y}')
