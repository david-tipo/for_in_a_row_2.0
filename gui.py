import pygame
import math
WIDTH = 800
HEIGHT = 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
BG = pygame.image.load("backround.jpg")
FPS = 60
RED_PIECE = pygame.image.load("red ball.png")
YELLOW_PIECE = pygame.image.load("yellow.png")
PLAY_AGAIN = pygame.image.load("play again button.png")

# button variables
buttons = []
NUMBERS = 7
RADIUS = 25
GAP = 46
startX = round((WIDTH - (RADIUS * 2 + GAP) * NUMBERS) / 2)
Y = 30


BORDER_COLOR = (0, 0, 0)
NUMBERS_COLOR = (200, 0, 0)

# fonts
pygame.font.init()
NUMBER_FONT = pygame.font.SysFont('comicsans', 50)
PlAYER_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 150)
TIE_FONT = pygame.font.SysFont('comicsans', 300)

for i in range(NUMBERS):
    x = startX + GAP + (RADIUS * 2 + GAP) * i
    num = i + 1
    buttons.append((x, Y, num))

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 33, 182)
# pieces variables
PIECE_X_RADIUS = 40
PIECE_X_GAP = 17
PIECE_START_X = 13 + PIECE_X_GAP + PIECE_X_RADIUS

PIECE_Y_RADIUS = 38
PIECE_Y_GAP = 10
PIECE_START_Y = 35 + PIECE_Y_GAP + PIECE_Y_RADIUS

# play again button variables
PLAY_AGAIN_WIDTH = PLAY_AGAIN.get_width()
PLAY_AGAIN_HEIGHT = PLAY_AGAIN.get_height()
PLAY_AGAIN_X = (WIDTH - PLAY_AGAIN.get_width()) / 2
PLAY_AGAIN_Y = 400


class Gui:

    # general drawing functions
    def draw(self):
        """draws the background and the buttons"""
        win.blit(BG, (0, 0))
        self.__draw_buttons()
        pygame.display.update()

    def __draw_buttons(self):
        for button in buttons:
            x, y, num = button
            pygame.draw.circle(win, BORDER_COLOR, (x, y), RADIUS, 3)
            text = NUMBER_FONT.render(str(num), True, NUMBERS_COLOR)
            textX = x - text.get_width() / 2
            textY = y - text.get_height() / 2
            win.blit(text, (textX, textY))

    def draw_current_player(self, player):
        """draws given player to the screen. top left"""
        BG_COLOR = (4, 91, 184)
        if player == 'red':
            color = (200, 0, 0)
            text = PlAYER_FONT.render("yellow", True, BG_COLOR)
            win.blit(text, (0, 0))
        else:
            color = (255, 242, 0)
            text = PlAYER_FONT.render("red", True, BG_COLOR)
            win.blit(text, (0, 0))
        text = PlAYER_FONT.render(player, True, color)
        win.blit(text, (0, 0))
        pygame.display.update()

    def draw_piece(self, color, row, column):
        """draws new given piece-color, column and row. and draw the piece in this place"""
        x = PIECE_START_X + (PIECE_X_RADIUS * 2 + PIECE_X_GAP) * row
        y = PIECE_START_Y + (PIECE_Y_RADIUS * 2 + PIECE_Y_GAP) * column
        if color.lower() == 'red':
            win.blit(RED_PIECE, (x, y))
        elif color.lower() == 'yellow':
            win.blit(YELLOW_PIECE, (x, y))
        pygame.display.update()

    # win/tie drawing
    def draw_winner(self, winner):
        """draws given winner to the screen"""
        text = WINNER_FONT.render(winner + " won", True, BLUE)
        x = (WIDTH - text.get_width()) / 2
        win.blit(text, (x, 200))
        pygame.display.update()

    def draw_tie(self):
        """draws TIE title"""
        text = TIE_FONT.render("TIE!", True, BLUE)
        x = (WIDTH - text.get_width()) / 2
        win.blit(text, (x, 200))
        pygame.display.update()

    # after game drawing

    def draw_play_again(self):
        """draws the play_again button"""
        win.blit(PLAY_AGAIN, (PLAY_AGAIN_X, PLAY_AGAIN_Y))
        pygame.display.update()

    # input functions
    def __get_number_pressed(self):
        """returns the number pressed. if no number was pressed returns None"""
        mouseX, mouseY = pygame.mouse.get_pos()
        for button in buttons:
            x, y, num = button
            dis = math.sqrt((x - mouseX) ** 2 + (y - mouseY) ** 2)
            if dis < RADIUS:
                return num

    def get_player_input(self):
        """returns the player input or contact with the game"""
        run = True
        while run:
            pygame.time.delay(FPS)
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    return 'quit'

                if event.type == pygame.MOUSEBUTTONDOWN:
                    column_number = self.__get_number_pressed()
                    if column_number != None:
                        return column_number

    def expect(self, *args):
        """gets a string of what to expect, and returns only if the input as expected"""
        run = True
        while run:
            pygame.time.delay(FPS)
            for event in pygame.event.get():

                if event.type == pygame.QUIT and 'quit' in args:
                    return 'quit'

                if event.type == pygame.MOUSEBUTTONDOWN and 'column' in args:
                    column_number = self.__get_number_pressed()
                    if column_number != None:
                        return column_number

                if event.type == pygame.MOUSEBUTTONDOWN and 'play again' in args:
                    mouseX, mouseY = pygame.mouse.get_pos()
                    maxX = PLAY_AGAIN_X + PLAY_AGAIN_WIDTH
                    maxY = PLAY_AGAIN_Y + PLAY_AGAIN_HEIGHT
                    good_x = mouseX > PLAY_AGAIN_X and mouseX < maxX
                    good_y = mouseY > PLAY_AGAIN_Y and mouseY < maxY
                    if good_x and good_y:
                        return 'play again'

    def end(self):
        """ends the drawing. quit pygame"""
        pygame.quit()

# boot buttons
# TODO: add Documentation to each methoed

