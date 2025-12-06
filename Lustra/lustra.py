import copy


def parse_input(input_g, input_m):
    g = int(input_g.split(' ')[0])
    m = []
    for line in input_m:
        m.append(tuple(map(int, line.split())))
    return g, m

def get_move_name(move):
    if move == (-1,0):
        return '[▲]top'
    elif move == (1,0):
        return '[▼]bottom'
    elif move == (0,-1):
        return '[◀]left'
    else:
        return '[▶]right'


def check_if_mirrors_works(garden_to_check: list[list[int]], draw_each_step: bool = False) -> bool:
    is_valid: bool = True
    max_size: int = len(garden_to_check)
    current_position = (0, 0) # init position inside garden
    prev_position = (-1, 0) # init position outside garden
    move = (1, 0) # first move
    move_top = (-1, 0)
    move_bottom = (1, 0)
    move_left = (0, -1)
    move_right = (0, 1)
    meta = (max_size - 1, max_size - 1)
    step: int = 0
    while is_valid:
        step += 1
        current_angle: int = garden_to_check[current_position[0]][current_position[1]]
        print(f'Step: {step} | move: {get_move_name(move)} | current position: {current_position} | current angle: {current_angle}')

        if draw_each_step:
            draw_garden(garden_to_check, current_position)


        if current_angle == 45:
            if prev_position[0] == current_position[0]:
                # vertical move
                move = move_top if prev_position[1] < current_position[1] else move_bottom
            else:
                # horizontal move
                move = move_left if prev_position[0] < current_position[0] else move_right
        elif current_angle == 135:
            if prev_position[0] == current_position[0]:
                # vertical move
                move = move_bottom if prev_position[1] < current_position[1] else move_top
            else:
                # horizontal move
                move = move_right if prev_position[0] < current_position[0] else move_left

        if current_position[0] == meta[0] and current_position[1] == meta[1]:
            print('Meta!')
            return True

        prev_position = current_position

        current_position = (current_position[0] + move[0], current_position[1] + move[1])

        is_valid = (0 <= current_position[0] < max_size and
                    0 <= current_position[1] < max_size)
        if not is_valid:
            print(f'Next move {get_move_name(move)} is outside of the garden')

    return  False


def draw_garden(garden_to_draw: list[list[int]], current_position: tuple = (-1,-1)):
    s = len(garden_to_draw)
    print('[▼]' + ('---' * (s - 1)))
    for row_index in range(len(garden_to_draw)):
        row = garden_to_draw[row_index]
        txt: str = ''
        for col_index in range(len(row)):
            angle = row[col_index]
            cur_prefix = '['
            cur_suffix = ']'

            if current_position[0] == row_index and current_position[1] == col_index:
                cur_item = '●'
                if angle != 0:
                    cur_prefix = '{'
                    cur_suffix = '}'
            else:
                cur_item = ' '

            if angle == 45:
                cur_item = '/'
            elif angle == 135:
                cur_item = '\\'

            txt += cur_prefix + cur_item + cur_suffix
        print(txt)
    print(('---' * (s - 1)) + '[▼]')


def create_garden_with_mirrors(garden_size:int, m_positions:list[tuple[int, int, int]]):
    garden_fields = [[0 for x in range(garden_size)] for y in range(garden_size)]
    for item in m_positions:
        (x,y,angle) = item
        garden_fields[x][y] = angle
    return garden_fields


def move_mirror(current_garden, move_from, move_to, change_angle_to:int = -1):
    angle = current_garden[move_from[0]][move_from[1]]
    row = current_garden[move_from[0]]
    row[move_from[1]] = 0
    if change_angle_to > -1:
        angle = change_angle_to
    row = current_garden[move_to[0]]
    row[move_to[1]] = angle


def get_empty_fields(garden_to_check):
    empty_fields: list[tuple[int, int]] = []
    for row_index in range(len(garden_to_check)):
        row = garden_to_check[row_index]
        for col_index in range(len(row)):
            if row[col_index] == 0:
                empty_fields.append((col_index, row_index))

    return empty_fields


if __name__ == '__main__':

    # example data:
    input_garden = '5 6'
    input_mirrors = ['0 4 45', '1 1 45', '3 0 135', '3 3 45', '4 1 135', '4 4 135']

    # parse
    garden_size, mirrors  = parse_input(input_garden, input_mirrors)
    garden = create_garden_with_mirrors(garden_size, mirrors)
    original_garden = copy.deepcopy(garden)

    print('-------------------------------------')
    print(f'Mirrors:{mirrors}')
    print('-------------------------------------')
    empty_fields = get_empty_fields(garden)
    print(f'Empty fields:{empty_fields}')
    print('-------------------------------------')
    print('Original garden:')
    draw_garden(garden)

    attempts = 0

    for mirror in mirrors:
        attempts += 1
        print('====================================================')
        print(f'Attempt(s): {attempts} | Check move mirror:{mirror}')
        print('====================================================')
        mirror_orig_position: tuple[int,int] = (mirror[0], mirror[1])
        mirror_orig_angle = mirror[2]
        for empty_field in empty_fields:
            for angle in [45, 135]:
                print(f'\nMove mirror from {mirror_orig_position} to {empty_field} with angle {angle}')
                garden = copy.deepcopy(original_garden) # restore original garden configuration
                move_mirror(garden, mirror_orig_position, empty_field, angle)
                is_meta = check_if_mirrors_works(garden, True)

                if is_meta:
                    print('----------------------------------------------')
                    print('| Meta is  reachable in this configuration !!!')
                    print(f'| You need to move mirror from {mirror_orig_position} to {empty_field}')
                    print('----------------------------------------------')
                    exit(0)

    print('------------------------------------')
    print('Finish')