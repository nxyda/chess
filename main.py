import pygame
import sys
#fwugqyuwegfuweyg
#fijhwgufwguwefyg
pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
dark_green = (0, 100, 0)

screen_width = 800
screen_heigth = 800
rows = 8
cols = 8
square_size = screen_width // cols


pieces = {
    "bb": pygame.image.load("pieces/black/bishop_black.png"),
    "kb": pygame.image.load("pieces/black/king_black.png"),
    "lb": pygame.image.load("pieces/black/knight_black.png"),
    "pb": pygame.image.load("pieces/black/pawn_black.png"),
    "qb": pygame.image.load("pieces/black/queen_black.png"),
    "rb": pygame.image.load("pieces/black/rook_black.png"),
    "bw": pygame.image.load("pieces/white/bishop_white.png"),
    "kw": pygame.image.load("pieces/white/king_white.png"),
    "lw": pygame.image.load("pieces/white/knight_white.png"),
    "pw": pygame.image.load("pieces/white/pawn_white.png"),
    "qw": pygame.image.load("pieces/white/queen_white.png"),
    "rw": pygame.image.load("pieces/white/rook_white.png"),
}   
    
screen = pygame.display.set_mode((screen_width, screen_heigth))
pygame.display.set_caption("Chess")

def draw_board(screen):
    screen.fill(white)
    for row in range(rows):
        for col in range(cols):
            if (row + col) % 2 == 0:
                color = dark_green
            else:
                color = green
            pygame.draw.rect(screen, color, (col * square_size, row * square_size, square_size, square_size))


def draw_pieces(screen, board):
    for row in range(rows):
        for col in range(cols):
            piece = board[row][col]
            if piece != " ":
                screen.blit(pieces[piece], (col * square_size, row * square_size))

def create_board():
    board = [["rb", "lb", "bb", "qb", "kb", "bb", "lb", "rb"],
             ["pb", "pb", "pb", "pb", "pb", "pb", "pb", "pb"],
             [" ", " ", " ", " ", " ", " ", " ", " "],
             [" ", " ", " ", " ", " ", " ", " ", " "],
             [" ", " ", " ", " ", " ", " ", " ", " "],
             [" ", " ", " ", " ", " ", " ", " ", " "],
             ["pw", "pw", "pw", "pw", "pw", "pw", "pw", "pw"],
             ["rw", "lw", "bw", "qw", "kw", "bw", "lw", "rw"]]
    return board

def main():
    board = create_board()
    running = True
    while running:
        draw_board(screen)
        draw_pieces(screen, board)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()