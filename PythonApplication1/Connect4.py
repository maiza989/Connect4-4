import numpy as np
import pygame 
import sys
import math

# defining rows and column size for the board
Rows= 6
Columns= 7

# defining the color used in the game GUI
Blue = (0,0,255)
Black = (0,0,0)
Red = (255,0,0)
Yellow = (255,255,0)


# creating the board size and return it
def create_board():
    board = np.zeros((Rows, Columns))
    return board


def drop_piece(board,row,col,piece):
    board[row][col] = piece

# a function that check a valid play. if the location selected is occupied or not
def is_valid_play(board,col):
    return board[Rows-1][col] == 0

# checks the rows of the board
def check_next_open_row(board,col):
    for r in range(Rows):
        if board[r][col] == 0:
            return r

# print the board
def display_board(board):
    print(np.flip(board,0))

# defining what is a winning move, horizontal win, vertical win, positive diagonal slop win, negative diagonal slop win.
def win_move(board, piece):
    
    # for loop that check a win in a horizontal fashion '-'
    for c in range(Columns - 3):
        for r in range(Rows):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    # for loop that check a win in vertical fashion '|'
    for c in range(Columns):
        for r in range(Rows - 3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    # for loop that check a win in a positively diagonal slop '/'
    for c in range(Columns - 3):
        for r in range(Rows - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    # for loop that check a win in a nevatively diagonal slop '\'
    for c in range(Columns - 3):
        for r in range(3, Rows):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True



#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# building a GUI for the game 
   #drawing a rectangle/squre for the board and a circle to give it a coin shape the connect 4 uses
   #also drawing the player 1 coin and player 2 coin
def draw_board(board):
    # for loop that draws the shaphes of the board that the coin drops into
    for c in range(Columns):
        for r in range(Rows):
            pygame.draw.rect(screen, Blue, 
                             (c*squareSize, r*squareSize+squareSize, squareSize, squareSize))
            pygame.draw.circle(screen, Black,
                               (int(c*squareSize+squareSize/2),
                               int(r*squareSize+squareSize+squareSize/2)),
                               radius)

    # for loop that check whos turn it us and show red coin for player one and yellow coin for player two
    for c in range(Columns):
        for r in range(Rows):
            if board[r][c] == 1:
                pygame.draw.circle(screen, Red, (int(c*squareSize+squareSize/2),height-int(r*squareSize+squareSize/2)), radius)
                                   
            elif board[r][c] == 2:
                pygame.draw.circle(screen, Yellow, (int(c*squareSize+squareSize/2), height-int(r*squareSize+squareSize/2)), radius)
    pygame.display.update()
        
# initalize the board 
board = create_board()
# call display_board to print the board
display_board(board)
# Setting the game over to be false
game_over = False 
# set the inital turn to be 0 
turn = 0
# initializing the game/starting
pygame.init()

squareSize = 100
width = Columns * squareSize
height = (Rows+1) * squareSize
size = (width,height)
radius = int(squareSize/2-5)
# display the game to the screen
screen = pygame.display.set_mode(size)

#Calling fuction draw_board and update our screen again
draw_board(board)
pygame.display.update()
# setting the font of the game
myFont = pygame.font.SysFont("monospace", 75)

# a while loop to check whos turn to go 
while not game_over:
    
    # for loop to get all the registered event from user and put them in an event queue
    # an if statement to check if the user click windows's "X" button or when the system 'asks' for the process to quit if so exit the application
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # if statemnet that check if there is a movment with mouse on the screen draw a rectangle
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, Black, (0,0, width, squareSize))
            posx = event.pos[0]
            #if statment to check of if the trun is 0 draw a coin for player one as 'Red' or for player two as 'Yellow' and update the game as so
            if turn == 0:
                pygame.draw.circle(screen, Red, (posx, int(squareSize/2)), radius)
            else: 
                pygame.draw.circle(screen, Yellow, (posx, int(squareSize/2)), radius)
        pygame.display.update()
 
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, Black, (0,0, width, squareSize))

           # asking for playing one to play/input
            if turn == 0:
                # set the player coin position as the mouse cursor position
                posx = event.pos[0]
                # round a column down to the nearest integer of mouse position divided by the squaresize
                col = int(math.floor(posx/squareSize))
                # if statement that check if the player one is making a valid move
                if is_valid_play(board, col):
                    row = check_next_open_row(board, col)
                    drop_piece(board, row, col, 1)
                    # if statement check if the played made a winning move and display that player 1 won the game and end the game.
                    if win_move(board, 1):
                        label = myFont.render("Player 1 wins!!", 1, Red)
                        screen.blit(label, (40,10))
                        game_over = True
 
 
            # # Ask for Player 2 Input
            else:               
                posx = event.pos[0]
                col = int(math.floor(posx/squareSize))
                # if statement that check if the player two is making a valid move
                if is_valid_play(board, col):
                    row = check_next_open_row(board, col)
                    drop_piece(board, row, col, 2)
                    # if statement check if the played made a winning move and display that player 2 won the game and end the game.
                    if win_move(board, 2):
                        label = myFont.render("Player 2 wins!!", 1, Yellow)
                        screen.blit(label, (40,10))
                        game_over = True
 
            display_board(board)
            draw_board(board)
            
            # increase the turn with each move
            turn += 1
            # switch the turn between players
            turn = turn % 2
 
            if game_over:
               pygame.time.wait(3000)
               
        

    

    