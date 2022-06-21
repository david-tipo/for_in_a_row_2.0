import gui
from bot import EasyBot
from game import Game
from time import sleep




#main loop
game = Game()
bot = EasyBot(game)
run = True
while run:
    gui1 = gui.Gui()
    gui1.draw()
    while True:
        gui1.draw_current_player(game.player)
        input = gui1.get_player_input()
        while (type(input) == int) and (game.available_slot(input - 1) == None):
            input = gui1.get_player_input()

        if input == 'quit':
            run = False
            break

        column = input - 1
        row = game.available_slot(column)
        game.place(game.player, row, column, gui1)
        if game.who_won():
            gui1.draw_winner(game.who_won())
            print(game.who_won(), 'won!!!!!')
            break
        if game.tie_check():
            gui1.draw_tie()
            print('tie!!')
            break
        game.switch_players()
        bot.do_turn(game, gui1)
        if game.who_won():
            gui1.draw_winner(game.who_won())
            print(game.who_won(), 'won!!!!!')
            print(game.who_won(), 'won!!!!!')
            print(game.who_won(), 'won!!!!!')
            print(game.who_won(), 'won!!!!!')
            break
        if game.tie_check():
            gui1.draw_tie()
            print('tie!!')
            break
        game.switch_players()
        game.print_board()
    if run == False:
        break
    sleep(1)
    gui1.draw_play_again()
    input = gui1.expect('quit', 'play again')
    if input == 'quit':
        run = False
        break
    if input == 'play again':
        game.reset_board()
        bot.reset_bot()
        game.print_board()
