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

selection = pygame.image.load("circle.png")
selection = pygame.transform.scale(selection, (square_size, square_size))

pieces = {
    "b": pygame.image.load("pieces/black/bishop_black.png"),
    "k": pygame.image.load("pieces/black/king_black.png"),
    "l": pygame.image.load("pieces/black/knight_black.png"),
    "p": pygame.image.load("pieces/black/pawn_black.png"),
    "q": pygame.image.load("pieces/black/queen_black.png"),
    "r": pygame.image.load("pieces/black/rook_black.png"),
    "B": pygame.image.load("pieces/white/bishop_white.png"),
    "K": pygame.image.load("pieces/white/king_white.png"),
    "L": pygame.image.load("pieces/white/knight_white.png"),
    "P": pygame.image.load("pieces/white/pawn_white.png"),
    "Q": pygame.image.load("pieces/white/queen_white.png"),
    "R": pygame.image.load("pieces/white/rook_white.png"),
}

screen = pygame.display.set_mode((screen_width, screen_heigth))
pygame.display.set_caption("Chess")


def draw_board(screen, rows, cols, square_size, selected_pos, selection_image):
    white = (255, 255, 255)
    dark_green = (0, 100, 0)
    green = (0, 128, 0)
    screen.fill(white)

    for row in range(rows):
        for col in range(cols):
            if (row + col) % 2 == 0:
                color = dark_green
            else:
                color = green
            pygame.draw.rect(screen, color,
                             (col * square_size, row * square_size,
                              square_size, square_size))

    if selected_pos:
        x, y = selected_pos[0] * square_size, selected_pos[1] * square_size
        screen.blit(selection_image, (x, y))


def draw_pieces(screen, board):
    for row in range(rows):
        for col in range(cols):
            piece = board[row][col]
            if piece != " ":
                screen.blit(pieces[piece],
                            (col * square_size, row * square_size))


def create_board():
    board = [["r", "l", "b", "q", "k", "b", "l", "r"],
             ["p", "p", "p", "p", "p", "p", "p", "p"],
             [" ", " ", " ", " ", " ", " ", " ", " "],
             [" ", " ", " ", " ", " ", " ", " ", " "],
             [" ", " ", " ", " ", " ", " ", " ", " "],
             [" ", " ", " ", " ", " ", " ", " ", " "],
             ["P", "P", "P", "P", "P", "P", "P", "P"],
             ["R", "L", "B", "Q", "K", "B", "L", "R"]]
    return board


def move(board, start, end, piece):
    start_x, start_y = start
    end_x, end_y = end
    if start_x == end_x and start_y == end_y:
        return False

    move_x, move_y = end_x - start_x, end_y - start_y
    abs_move_x, abs_move_y = abs(move_x), abs(move_y)

    if piece.lower() == 'p':
        direction = -1 if piece.isupper() else 1
        start_row = 6 if piece.isupper() else 1
        # Ruch do przodu o 1
        if (move_y == direction and move_x == 0
                and board[end_y][end_x] == " "):
            return True
        elif (move_y == 2 * direction and move_x == 0 and start_y == start_row
              and board[start_y + direction][start_x] == " "
              and board[end_y][end_x] == " "):
            return True
        elif (abs_move_x == 1 and move_y == direction
              and board[end_y][end_x] != " "
              and board[end_y][end_x].islower() != piece.islower()):
            return True
        return False

    elif piece.lower() == 'r':
        if move_x != 0 and move_y != 0:
            return False
        steps = max(abs_move_x, abs_move_y)
        step_x = move_x // steps if move_x != 0 else 0
        step_y = move_y // steps if move_y != 0 else 0
        for i in range(1, steps):
            if board[start_y + i * step_y][start_x + i * step_x] != " ":
                return False
        return board[end_y][end_x] == " " or board[end_y][end_x].islower(
        ) != piece.islower()

    elif piece.lower() == 'l':
        return (abs_move_x == 1 and abs_move_y == 2 or abs_move_x == 2 and abs_move_y == 1) and \
               (board[end_y][end_x] == " " or board[end_y][end_x].islower() != piece.islower())

    elif piece.lower() == 'b':
        if abs_move_x != abs_move_y:
            return False
        steps = abs_move_x
        step_x = move_x // steps
        step_y = move_y // steps
        for i in range(1, steps):
            if board[start_y + i * step_y][start_x + i * step_x] != " ":
                return False
        return board[end_y][end_x] == " " or board[end_y][end_x].islower(
        ) != piece.islower()

    elif piece.lower() == 'q':
        if abs_move_x != abs_move_y and move_x != 0 and move_y != 0:
            return False
        steps = max(abs_move_x, abs_move_y)
        step_x = move_x // steps if move_x != 0 else 0
        step_y = move_y // steps if move_y != 0 else 0
        for i in range(1, steps):
            if board[start_y + i * step_y][start_x + i * step_x] != " ":
                return False
        return board[end_y][end_x] == " " or board[end_y][end_x].islower(
        ) != piece.islower()

    elif piece.lower() == 'k':
        return abs_move_x <= 1 and abs_move_y <= 1 and \
               (board[end_y][end_x] == " " or board[end_y][end_x].islower() != piece.islower())

    return False


def is_check(board, king_pos, king_color):
    enemy_pieces = {
        "w": ["P", "R", "L", "B", "Q", "K"],
        "b": ["p", "r", "l", "b", "q", "k"]
    }
    if king_color == "b":
        enemy_color = "w"
    else:
        enemy_color = "b"
    for i in range(8):
        for j in range(8):
            if board[i][j] in enemy_pieces[enemy_color] and move(
                    board, (j, i), king_pos, board[i][j]):
                return True
    return False


def is_checkmate(board, king_pos, king_color):
    if not is_check(board, king_pos, king_color):
        return False
    for i in range(8):
        for j in range(8):
            if board[i][j].lower() == king_color and move(
                    board, king_pos, (j, i), board[i][j]):
                new_board = [row[:] for row in board]
                new_board[king_pos[1]][king_pos[0]] = " "
                new_board[i][j] = king_color.upper()
                if not is_check(new_board, (j, i), king_color):
                    return False
    return True


def main():
    board = create_board()
    running = True
    selected_piece = None
    selected_pos = None
    current_player = 1

    white_king_pos = (7, 4)
    black_king_pos = (0, 4)

    selection_image = selection

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                col = pos[0] // square_size
                row = pos[1] // square_size
                if selected_piece:
                    if move(board, selected_pos, (col, row), board[selected_pos[1]][selected_pos[0]]) and \
                       ((current_player == 1 and board[selected_pos[1]][selected_pos[0]].isupper()) or
                        (current_player == -1 and board[selected_pos[1]][selected_pos[0]].islower())):
                        board[row][col] = board[selected_pos[1]][
                            selected_pos[0]]
                        board[selected_pos[1]][selected_pos[0]] = " "
                        selected_piece = None
                        selected_pos = None
                        current_player *= -1
                    else:
                        print("Nielegalny ruch")
                        selected_piece = None
                        selected_pos = None
                else:
                    if board[row][col] != " " and \
                       ((current_player == 1 and board[row][col].isupper()) or
                        (current_player == -1 and board[row][col].islower())):
                        selected_piece = board[row][col]
                        selected_pos = (col, row)

        draw_board(screen, rows, cols, square_size, selected_pos,
                   selection_image)
        draw_pieces(screen, board)
        pygame.display.update()

        if selected_pos is None:
            if is_checkmate(board,  white_king_pos, 'k'):
                print("Białe wygrały!")
                running = False
            elif is_checkmate(board, black_king_pos, 'K'):
                print("Czarne wygrały!")
                running = False

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
