from utils import *
import pygame
from random import choice, randint as rand

pygame.init()

WIDTH, HEIGHT = 800, 800
FRAMERATE = 75
TILE_SIZE = 20

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Wave function collapse")
clock = pygame.time.Clock()


class WaveFunctionCollapse:
    def __init__(self):
        self.w = int(WIDTH/TILE_SIZE)
        self.h = int(HEIGHT/TILE_SIZE)
        self.tiles: dict[tuple[int, int], int] = {}
        self.texture_mappings = {
            0: "left.png",
            1: "down.png",
            2: "right.png",
            3: "up.png",
            4: "nub_left.png",
            5: "nub_down.png",
            6: "nub_right.png",
            7: "nub_up.png",
            8: "plus.png",
            9: "bridge_vert.png",
            10: "bridge_horiz.png",
            11: "corner_bl.png",
            12: "corner_br.png",
            13: "corner_tr.png",
            14: "corner_tl.png",
            15: "blank.png"
        }
        self.dir_map = {
            0: (True, True, False, True),
            1: (True, True, True, False),
            2: (False, True, True, True),
            3: (True, False, True, True),
            4: (True, False, False, False),
            5: (False, True, False, False),
            6: (False, False, True, False),
            7: (False, False, False, True),
            8: (True, True, True, True),
            9: (False, True, False, True),
            10: (True, False, True, False),
            11: (True, True, False, False),
            12: (False, True, True, False),
            13: (False, False, True, True),
            14: (True, False, False, True),
            15: (False, False, False, False)
        }

    def draw(self, which=None):
        if which is None:
            for tile in self.tiles:
                screen.blit(
                    fetch_texture(self.texture_mappings[self.tiles[tile]]), (tile[0]*TILE_SIZE, tile[1]*TILE_SIZE)
                )
        else:
            screen.blit(
                fetch_texture(self.texture_mappings[self.tiles[which]]), (which[0]*TILE_SIZE, which[1]*TILE_SIZE)
            )

    def possibilities(self, pos: tuple[int, int]):
        check_positions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        prob_reqs = []
        for index, c_position in enumerate(check_positions):
            mod_pos = c_position[0]+pos[0], c_position[1]+pos[1]
            if self.tiles.get(mod_pos, None) is not None:
                compare_tile = self.dir_map[self.tiles[mod_pos]]
                prob_reqs.append(compare_tile[divmod(index+2, 4)[1]])
            else:
                prob_reqs.append(None)
        prob_reqs = tuple(prob_reqs)
        possibilities = []
        for possible_dir in self.dir_map:
            for index, direction in enumerate(prob_reqs):
                if direction is None:
                    continue
                if direction != self.dir_map[possible_dir][index]:
                    break
            else:
                possibilities.append(possible_dir)
        return possibilities


def reveal_tile(m_pos, replace=False):
    possible = collapser.possibilities(m_pos)
    if len(possible):
        if (collapser.tiles.get(m_pos, None) is None) or replace:
            collapser.tiles[m_pos] = choice(possible)
    else:
        print("Not possible!")


def hover_position(re_mul=True):
    m_pos = pygame.mouse.get_pos()
    if re_mul:
        return int(m_pos[0]/TILE_SIZE)*TILE_SIZE, int(m_pos[1]/TILE_SIZE)*TILE_SIZE
    else:
        return int(m_pos[0]/TILE_SIZE), int(m_pos[1]/TILE_SIZE)


collapser = WaveFunctionCollapse()

running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                collapser.tiles = {}
                for y in range(collapser.h):
                    for x in range(collapser.w):
                        reveal_tile((x, y))

    collapser.draw()

    if pygame.mouse.get_pressed(3)[2]:
        reveal_tile(hover_position(False), True)

    pygame.display.flip()
    clock.tick(FRAMERATE)
pygame.quit()
