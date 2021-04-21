# Display Board
def display_board():
    print("\nThis is your board:")
    print(board[1].rjust(10)+'|'+board[2]+'|'+board[3])
    print("-------".rjust(15))
    print(board[4].rjust(10)+'|'+board[5]+'|'+board[6])
    print("-------".rjust(15))
    print(board[7].rjust(10)+'|'+board[8]+'|'+board[9])

# Take player input - names and marker choice
def player_names():
    player1_name=input('\nPlayer-1, please enter your name: ')
    player2_name=input('\nPlayer-2, please enter your name: ')
    return player1_name.upper(),player2_name.upper()

def marker_choice(player1):
    acceptable_choice=['X','O']
    valid=False
    while not valid:
        choice=input('\n'+player1 + ', please choose X or O as your marker: ')
        if choice.upper() in acceptable_choice:
            valid=True
        else:
            print("Only X or O allowed. Choose again\n")
    if choice.upper()=='X':
        return ('X','O')
    return ('O','X')

# PLace input on board
def position_choice(board,player_marker):
    invalid=True
    while invalid:
        position=input('Where do you want to place your marker? (1-9): ')
        if position.isdigit() and int(position) in range(1,10):
            position=int(position)
            if board[position] != ' ':
                print('Spot already taken. Please choose another position.')
            else:
                invalid=False
        else:
            print('Unacceptable input!')
    board[position]=player_marker
    return board

#Check game won, tied or ongoing
def game_check(board,player_markers,names):
    #WIN conditions
    win_seq_indexes=[[1,2,3],[4,5,6],[7,8,9],[1,4,7],[2,5,8],[3,6,9],[1,5,9],[3,5,7]]
    for iter1 in win_seq_indexes:
        p1_win=0
        p2_win=0
        for iter2 in iter1:
            if board[iter2]==player_markers[0]:
                p1_win+=1
            elif board[iter2]==player_markers[1]:
                p2_win+=1
        if p1_win==3:
            print('\n'+names[0]+' wins!')
            display_board()
            sleep(5)
            return True
        elif p2_win==3:
            print('\n'+names[1]+' wins!')
            display_board()
            sleep(5)
            return True
    if ' ' not in board:
        print('\nThe game is tied - no winner')
        display_board()
        sleep(5)
        return True
    return False

#Ask if players want to play again
def replay_game():
    invalid=True
    while invalid:
        replay=input('Do you want to play again? (Y or N): ')
        if replay.upper() not in ('Y','N'):
            print('Incorrect selection')
        else:
            invalid=False
    if replay.upper()=='Y':
        print('Wonderful! Let us play again.....')
        sleep(3)
        return True
    else:
        print('Thank you for playing!')
        sleep(3)
        return False

# Main program
from os import system
from time import sleep

play_again=True
while play_again:
    board=['#']+[' ']*9
    game_over=False
    names=player_names()
    player_markers=marker_choice(names[0])
    sleep(0.5)
    system('clear')
    player_turn=0
    while not game_over:
        display_board()
        if player_turn%2==0:
            print("\n*** "+names[0]+" ***")
            board=position_choice(board,player_markers[0])
        else:
            print("\n*** "+names[1]+" ***")
            board=position_choice(board,player_markers[1])
        sleep(0.5)
        player_turn+=1
        game_over=game_check(board,player_markers,names)
        system('clear')
    play_again=replay_game()
    system('clear')
exit()
