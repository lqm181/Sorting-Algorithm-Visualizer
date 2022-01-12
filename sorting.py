import math
import random
import pygame
pygame.init()

SIDE_PAD = 100
TOP_PAD = 150
class DisplayInfo:
    BLUE = 0, 255, 255
    RED = 255, 0, 0
    GREEN = 0, 255, 0
    WHITE = 255, 255, 255
    BLACK = 0, 0, 0
    BG_COLOR = WHITE

    GREYS = [(192, 192, 192),
             (160, 160, 160),
             (128, 128, 128)]

    #Small Font for Controls
    SMALL_FONT = pygame.font.SysFont("comicsans", 30)

    #Large Font for the heading
    LARGE_FONT = pygame.font.SysFont("comicsans", 40)
    def __init__(self, caption, width, height, lst):
        self.width = width
        self.height = height

        pygame.display.set_caption(caption)
        self.win = pygame.display.set_mode((width, height))
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min = min(lst)
        self.max= max(lst)

        self.bar_width = (self.width - SIDE_PAD) / len(lst)
        self.bar_height = math.floor((self.height - TOP_PAD) / (self.max - self.min))

def create_list(n, low, high):
    lst = []

    for _ in range(n):
        lst.append(random.randint(low, high))

    return lst

def draw(display_info, algo_name, ascending):
    display_info.win.fill(display_info.BG_COLOR)

    draw_control(display_info)
    draw_header(display_info, algo_name, ascending)
    draw_list(display_info)
    
    pygame.display.update()

def draw_control(info):
    controls = info.SMALL_FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, info.BLACK)
    info.win.blit(controls, (info.width/2 - controls.get_width()/2, 45))

    sorting = info.SMALL_FONT.render("B - Bubble Sort | I - Insetion Sort | S - Selection Sort", 1, info.BLACK)
    info.win.blit(sorting, (info.width/2 - sorting.get_width()/2, 75))

def draw_header(info, algo_name, ascending):
    header = info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, info.GREEN)
    info.win.blit(header, (info.width/2 - header.get_width()/2, 5))

def draw_list(info, color_pos= {}, clear_bg= False):   
    def rect_pos(i, val):
        rect_height = (val - info.min + 1) * info.bar_height
        rect_x = SIDE_PAD // 2 + i * info.bar_width
        rect_y = info.height - rect_height

        return rect_x, rect_y, info.bar_width, rect_height


    if clear_bg:
        clear_rect = (SIDE_PAD // 2, TOP_PAD, info.width - SIDE_PAD, info.height - TOP_PAD)
        pygame.draw.rect(info.win, info.BG_COLOR, clear_rect)

    for i,val in enumerate(info.lst):
        color = info.GREYS[i % 3]

        if i in color_pos:
            color = color_pos[i]

        pygame.draw.rect(info.win, color, rect_pos(i,val))

    if clear_bg:
        pygame.display.update()
    
    

def bubble_sort(info, ascending= True):
    lst = info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            if (ascending and lst[j] > lst[j+1]) or (not ascending and lst[j] < lst[j+1]):
                lst[j], lst[j+1] = lst[j+1], lst[j]
                draw_list(info, {j: info.RED, j+1: info.BLUE}, True)
                yield True

    return lst

def insertion_sort(info, ascending= True):
    lst = info.lst

    for i in range(1, len(lst)):
        j = i

        while j > 0: 
            if (ascending and lst[j] < lst[j-1]) or (not ascending and lst[j] > lst[j-1]):
                lst[j], lst[j-1] = lst[j-1], lst[j]
                draw_list(info, {j: info.RED, j-1: info.BLUE}, True)
                j -= 1
                yield True
            else:
                break

    return lst

def selection_sort(info, ascending= True):
    lst = info.lst

    for i in range(len(lst) - 1):
        for j in range(i, len(lst)):
            ascending_sort = ascending and lst[i] > lst[j]
            descending_sort = not ascending and lst[i] < lst[j]

            if ascending_sort or descending_sort:
                # Swap if the two number are not sorted
                lst[i],lst[j] = lst[j], lst[i]
                draw_list(info, {j: info.RED, i: info.BLUE}, True)
                yield True

    return lst

def main(n, low, high):
    lst = create_list(n, low, high)
    info = DisplayInfo("Visualizer", 800, 600, lst)

    running = True
    clock = pygame.time.Clock()

    sorting = False
    ascending = True 
    is_sorted = False
    need_sort = True

    sort_algo = bubble_sort
    sort_algo_name = "Bubble Sort"
    sort_generator = None

    while running:
        clock.tick(60)

        if sorting and need_sort:
            try:
                next(sort_generator)
            except StopIteration:
                sorting = False
                is_sorted = True
                need_sort = False
        else:
            draw(info, sort_algo_name, ascending)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            
            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r and not sorting:
                #Reset
                lst = create_list(n, low, high)
                info.set_list(lst)

                sorting = False
                is_sorted = False
                need_sort = True

                # ascending = True 
                # sort_algo = bubble_sort
                # sort_algo_name = "Bubble Sort"
                # sort_generator = None

            if event.key == pygame.K_SPACE and not sorting and need_sort:
                sorting = True
                sort_generator = sort_algo(info, ascending)

            if event.key == pygame.K_a and not sorting:
                if not ascending:
                    ascending = True

                    if is_sorted:
                        if not need_sort:
                            need_sort = True
                        else:
                            need_sort = False


            if event.key == pygame.K_d and not sorting:
                if ascending:
                    ascending = False

                    if is_sorted:
                        if not need_sort:
                            need_sort = True
                        else:
                            need_sort = False

            if event.key == pygame.K_b and not sorting:
                sort_algo = bubble_sort
                sort_algo_name = "Bubble Sort"

            if event.key == pygame.K_i and not sorting:
                sort_algo = insertion_sort
                sort_algo_name = "Insertion Sort"

            if event.key == pygame.K_s and not sorting:
                sort_algo = selection_sort
                sort_algo_name = "Selection Sort"

if __name__ == "__main__":
    main(50, 1, 100)