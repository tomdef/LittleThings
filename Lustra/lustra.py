
def parse_input(input_g, input_m):
    g = int(input_g.split(' ')[0])
    m = []
    for line in input_m:
        m.append(tuple(map(int, line.split())))
    return g, m

def check_if_mirrors_works(garden_to_check: list[list[int]]) -> bool:
    is_valid: bool = True
    max_size: int = len(garden_to_check)
    current_position = (0,0)
    prev_position = (0, 0)
    move = (1, 0)
    meta = (max_size - 1, max_size - 1)
    step: int = 0
    while is_valid:
        step += 1
        print(f"step: {step}|move: {move}|current_position: {current_position}")
        draw_garden(garden_to_check, current_position)
        current_angle: int = garden_to_check[current_position[0]][current_position[1]]
        if current_angle == 45:
            if prev_position[0] == current_position[0]:
                # ruch pionowo
                if prev_position[1] < current_position[1]:
                    move = (-1, 0)
                else:
                    move = (1, 0)
            else:
                # ruch poziomo
                if prev_position[0] < current_position[0]:
                    move = (-1, 0)
                else:
                    move = (1, 0)
        elif current_angle == 135:
            if prev_position[0] == current_position[0]:
                # ruch pionowo
                if prev_position[1] < current_position[1]:
                    move = (1, 0)
                else:
                    move = (-1, 0)
            else:
                # ruch poziomo
                if prev_position[0] < current_position[0]:
                    move = (0, 1)
                else:
                    move = (0, -1)

        prev_position = current_position

        if current_position[0] == meta[0] and current_position[1] == meta[1]:
            return True

        current_position = (current_position[0] + move[0], current_position[1] + move[1])

        is_valid = (0 <= current_position[0] < max_size and
                    0 <= current_position[1] < max_size)

    #return current_position[0] == meta[0] and current_position[1] == meta[1]
    return  False

def draw_garden(garden_to_draw: list[list[int]], current_position: tuple = (-1,-1)):
    s = len(garden_to_draw)
    print(f"--- Garden [{s}x{s}] ---")
    for row_index in range(len(garden_to_draw)):
        row = garden_to_draw[row_index]
        txt: str = ""
        for col_index in range(len(row)):
            angle = row[col_index]

            cur_prefix = '['
            cur_suffix = ']'

            if current_position[0] == row_index and current_position[1] == col_index:
                cur_item = '*'
                if angle != 0:
                    cur_prefix = '{'
                    cur_suffix = '}'
            else:
                cur_item = ' '

            if angle == 45:
                cur_item = '⋰'
            elif angle == 135:
                cur_item = '⋱'

            txt += cur_prefix + cur_item + cur_suffix
        print(txt)
    print("--------------------")


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

if __name__ == "__main__":

    # example data:
    input_garden = "5 6"
    input_mirrors = ["0 4 45", "1 1 45", "3 0 135", "3 3 45", "4 1 135", "4 4 135"]

    # parse
    garden_size, mirrors  = parse_input(input_garden, input_mirrors)
    garden = create_garden_with_mirrors(garden_size, mirrors)

    is_meta = check_if_mirrors_works(garden)
    print(f"Czy meta: {is_meta}")

    move_mirror(garden,(0,4), (1,3), 135)
    is_meta = check_if_mirrors_works(garden)
    print(f"Czy meta: {is_meta}")
