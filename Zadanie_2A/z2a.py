DIR_RIGHT = (0, 1)
DIR_LEFT = (0, -1)
DIR_UP = (-1, 0)
DIR_DOWN = (1, 0)

ROTATION_MAP = {
    45: {
        DIR_RIGHT: DIR_UP,
        DIR_DOWN: DIR_LEFT,
        DIR_LEFT: DIR_DOWN,
        DIR_UP: DIR_RIGHT
    },
    135: {
        DIR_RIGHT: DIR_DOWN,
        DIR_DOWN: DIR_RIGHT,
        DIR_LEFT: DIR_UP,
        DIR_UP: DIR_LEFT
    }
}

"""
Simple garden fields drawer with mirrors, current position and visited fields.
"""
def draw(map_size: tuple[int,int], 
         mirrors:dict[(int,int)], 
         current_position: tuple[int,int] = None, 
         visited:set[int,int] = None):

    print('[S]' + ('---' * (map_size - 1)))
    for row_index in range(map_size):
        txt: str = ''
        for col_index in range(map_size):
            angle = mirrors.get((row_index, col_index), 0)
            cur_prefix = '['
            cur_suffix = ']'
            cur_item = ' '

            if current_position and current_position[0] == row_index and current_position[1] == col_index:
                cur_item = '.'
                if angle != 0:
                    cur_prefix = '('
                    cur_suffix = ')'
                else:
                    cur_item = 'o'
            elif visited and (row_index, col_index) in visited and angle == 0:
                cur_item = '.'

            if angle == 45:
                cur_item = '/'
            elif angle == 135:
                cur_item = '\\'

            txt += f'{cur_prefix}{cur_item}{cur_suffix}'

        print(txt)
    print(('---' * (map_size - 1)) + '[M]')


"""

"""
def walk(map_size: int, 
         mirrors:dict[(int,int)], 
         current_position: tuple[int,int],
         current_direction: tuple[int,int],
         visited:set[int,int] = None) -> bool:

    if not ((0 <= current_position[0] < map_size) and (0 <= current_position[1] < map_size)):
        return False

    draw(map_size, mirrors, current_position, visited)

    if visited is not None:
        visited.add((current_position[0], current_position[1]))

    current_angle: int =  mirrors.get((current_position[0], current_position[1]), 0)
    current_direction = ROTATION_MAP.get(current_angle, {}).get(current_direction, current_direction)
    current_position = (current_position[0] + current_direction[0], current_position[1] + current_direction[1])

    return walk(map_size, mirrors, current_position, current_direction, visited)


if __name__ == '__main__':

    #input_garden = input().strip()
    #garden_size = int(input_garden.split(' ')[0])

    g_size = 5
    # m_lenght = 6
    
    mirrors = {}
    mirrors[(1, 3)] = 135
    mirrors[(1, 1)] = 45
    mirrors[(3, 0)] = 135
    mirrors[(3, 3)] = 45
    mirrors[(4, 1)] = 135
    mirrors[(4, 4)] = 135
     

    # for i in range(m_lenght):
    #     mirror_info = input()
    #     x, y, angle = map(int, mirror_info.split(' '))
    #     mirrors[(x, y)] = angle

    visited = set()

    draw(g_size, mirrors, (3, 3), visited)
   
    walk(g_size, mirrors, (0,0), (1,0), visited)

    print(visited)