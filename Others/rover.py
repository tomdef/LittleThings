def draw(map_size: tuple[int,int], mirrors:list[tuple[int,int,int]], current_position: tuple[int,int]):
    (map_width,map_height) = map_size
    start_pos = (0, 0)
    meta_pos = (map_width - 1, map_height - 1)

    print('[S]' + ('---' * (map_width - 1)))

    for row_index in range(map_height):
        txt: str = ''
        for col_index in range(map_width):
            mirror = mirrors[row_index]
            print(mirror)

        #print(txt)
    print(('---' * (map_width - 1)) + '[M]')


if __name__ == '__main__':
    s: tuple[int,int] = (5, 5)
    m: list[tuple[int,int,int]] = [(0,4,45), (1,1,45), (3,0,135), (3,3,45), (4,1,135), (4,4,135)]

    draw(s, m, (0, 0))