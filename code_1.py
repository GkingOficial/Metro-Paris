import pygame
import heapq

pygame.init()
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Metro de Paris - Algoritmo A*")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)

RADIUS = 12

NUM_ESTACOES = 14

station_coords = [
    (36, 221), (197, 270), (327, 320), (435, 344), (620, 418),
    (642, 456), (590, 444), (461, 149), (327, 175), (154, 308),
    (221, 25), (460, 50), (392, 504), (368, 578)
]

distancias_diretas = [
    [0, 10, 18.5, 24.8, 36.4, 38.8, 35.8, 25.4, 17.6, 9.1, 16.7, 27.3, 27.6, 29.8],
    [10, 0, 8.5, 14.8, 26.6, 29.1, 26.1, 17.3, 10, 3.5, 15.5, 20.9, 19.1, 21.8],
    [18.5, 8.5, 0, 6.3, 18.2, 20.6, 17.6, 13.6, 9.4, 10.3, 19.5, 19.1, 12.1, 16.6],
    [24.8, 14.8, 6.3, 0, 12, 14.4, 11.5, 12.4, 12.6, 16.7, 23.6, 18.6, 10.6, 15.4],
    [36.4, 26.6, 18.2, 12, 0, 3, 2.4, 19.4, 23.3, 28.2, 34.2, 24.8, 14.5, 17.9],
    [38.8, 29.1, 20.6, 14.4, 3, 0, 3.3, 22.3, 25.7, 30.3, 36.7, 27.6, 15.2, 18.2],
    [35.8, 26.1, 17.6, 11.5, 2.4, 3.3, 0, 20, 23, 27.3, 34.2, 25.7, 12.4, 15.6],
    [25.4, 17.3, 13.6, 12.4, 19.4, 22.3, 20, 0, 8.2, 20.3, 16.1, 6.4, 22.7, 27.6],
    [17.6, 10, 9.4, 12.6, 23.3, 25.7, 23, 8.2, 0, 13.5, 11.2, 10.9, 21.2, 26.6],
    [9.1, 3.5, 10.3, 16.7, 28.2, 30.3, 27.3, 20.3, 13.5, 0, 17.6, 24.2, 18.7, 21.2],
    [16.7, 15.5, 19.5, 23.6, 34.2, 36.7, 34.2, 16.1, 11.2, 17.6, 0, 14.2, 31.5, 35.5],
    [27.3, 20.9, 19.1, 18.6, 24.8, 27.6, 25.7, 6.4, 10.9, 24.2, 14.2, 0, 28.8, 33.6],
    [27.6, 19.1, 12.1, 10.6, 14.5, 15.2, 12.4, 22.7, 21.2, 18.7, 31.5, 28.8, 0, 5.1],
    [29.8, 21.8, 16.6, 15.4, 17.9, 18.2, 15.6, 27.6, 26.6, 21.2, 35.5, 33.6, 5.1, 0]
]

distancias_reais = [
    [0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [10, 0, 8.5, 0, 0, 0, 0, 0, 10, 3.5, 0, 0, 0, 0],
    [0, 8.5, 0, 6.3, 0, 0, 0, 0, 9.4, 0, 0, 0, 18.7, 0],
    [0, 0, 6.3, 0, 13, 0, 0, 15.3, 0, 0, 0, 0, 12.8, 0],
    [0, 0, 0, 13, 0, 3, 2.4, 30, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2.4, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 15.3, 30, 0, 0, 0, 9.6, 0, 0, 6.4, 0, 0],
    [0, 10, 9.4, 0, 0, 0, 0, 9.6, 0, 0, 12.2, 0, 0, 0],
    [0, 3.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 12.2, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 6.4, 0, 0, 0, 0, 0, 0],
    [0, 0, 18.7, 12.8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5.1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5.1, 0]
]

lines = [
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0],
    [0, 0, 1, 0, 1, 0, 0, 4, 0, 0, 0, 0, 4, 0],
    [0, 0, 0, 1, 0, 1, 2, 2, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 4, 2, 0, 0, 0, 2, 0, 0, 4, 0, 0],
    [0, 2, 3, 0, 0, 0, 0, 2, 0, 0, 3, 0, 0, 0],
    [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0]
]

def heuristic(atual, destino):
    return distancias_diretas[atual][destino]

def a_star(origem, destino):
    g = {i: float('inf') for i in range(NUM_ESTACOES)}
    f = {i: float('inf') for i in range(NUM_ESTACOES)}

    g[origem] = 0
    f[origem] = g[origem]

    open_queue = []
    heapq.heappush(open_queue, (f[origem], origem))
    came_from = {}
    
    while open_queue:
        _, current = heapq.heappop(open_queue)
        if current == destino:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(origem)
            path.reverse()
            return path
        
        for neighbor in range(len(station_coords)):
            if distancias_reais[current][neighbor] != 0:
                g_score = g[current] + distancias_reais[current][neighbor]
                
                if g_score < g[neighbor]:
                    came_from[neighbor] = current
                    g[neighbor] = g_score
                    f[neighbor] = g[neighbor] + heuristic(current, neighbor)
                    heapq.heappush(open_queue, (f[neighbor], neighbor))
    
    return []

def calculate_total_time(path):
    total_time = 0
    num_swaps = 0

    swap = lines[path[0]][path[1]]

    for i in range(len(path) - 1):
        if(swap != lines[path[i]][path[i + 1]]):
            num_swaps += 1
        swap = lines[path[i]][path[i + 1]]

        total_time += (distancias_reais[path[i]][path[i + 1]] * 60) / 30

    total_time += (num_swaps * 4)
    return total_time, num_swaps

def draw_stations(win, station_coords, path, origem, destino):
    for i, (x, y) in enumerate(station_coords):
        if i == destino:
            color = RED
        elif i == origem:
            color = YELLOW
        elif i in path:
            color = GREEN
        else:
            color = BLUE
        pygame.draw.circle(win, color, (x, y), RADIUS)
        pygame.draw.circle(win, BLACK, (x, y), RADIUS, 1)

def draw_path(win, station_coords, path):
    for i in range(len(path) - 1):
        x1, y1 = station_coords[path[i]]
        x2, y2 = station_coords[path[i+1]]
        pygame.draw.line(win, RED, (x1, y1), (x2, y2), 8)

def draw_button(win, x, y, width, height, text):
    pygame.draw.rect(win, GRAY, (x, y, width, height))
    pygame.draw.rect(win, BLACK, (x, y, width, height), 2)
    font = pygame.font.SysFont(None, 36)
    text_surface = font.render(text, True, BLACK)
    win.blit(text_surface, (x + (width - text_surface.get_width()) // 2, y + (height - text_surface.get_height()) // 2))

def draw_info_bar(win, text):
    font = pygame.font.SysFont(None, 20)
    swaps_text = font.render(text[0], True, BLACK)
    time_text = font.render(text[1], True, BLACK)
    pygame.draw.rect(win, WHITE, (WIDTH - 202, 2, 200, 120))
    pygame.draw.rect(win, BLACK, (WIDTH - 202, 2, 200, 120), 2)
    win.blit(swaps_text, (WIDTH - 190, 80))
    win.blit(time_text, (WIDTH - 190, 102))

def main():
    origem = None
    destino = None
    run = True
    path = []
    text = ["", ""]
    
    background = pygame.image.load('mapa.png')
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    background.set_alpha(120)

    while run:
        WIN.fill(WHITE)
        WIN.blit(background, (0, 0))

        draw_info_bar(WIN, text)

        draw_button(WIN, 630, 20, 150, 40, "Reiniciar")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 630 <= mouse_x <= 780 and 20 <= mouse_y <= 60:
                    origem = None
                    destino = None
                    path = []
                    text = ["", ""]
                else:
                    for i, (x, y) in enumerate(station_coords):
                        if (x - mouse_x) ** 2 + (y - mouse_y) ** 2 <= RADIUS ** 2:
                            if origem is None:
                                origem = i
                            elif destino is None:
                                destino = i
                            break
                    if origem is not None and destino is not None:
                        path = a_star(origem, destino)

                        total_time, num_swaps= calculate_total_time(path)
                        if num_swaps:
                            text[0] = f"Houve {num_swaps} troca(s) de linha!"
                        else:
                            text[0] = f"Não houve troca(s) de linha!"

                        text[1] = f"Tempo total: {total_time:.2f} minutos"
        
        draw_stations(WIN, station_coords, path, origem, destino)
        if path:
            draw_path(WIN, station_coords, path)
        
        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()
