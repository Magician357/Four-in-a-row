import sys

import pygame
from pygame.locals import *

from game import detectwin, playmove
from ai import random_ai, win_and_block_ai, block_two_ai, brute_force_single

def drawtext(text,pos,color=(0,0,0)):
    surface=sans.render(text,False,color)
    screen.blit(surface,pos)

board=[[0 for _ in range(6)] for _ in range(7)]
# organized SIDEWAYS

pygame.init()
pygame.font.init()

sans = pygame.font.SysFont('Comic Sans MS', 30)

fps = 48
fpsClock = pygame.time.Clock()

width, height = 600, 700
screen = pygame.display.set_mode((width, height))

board_width, board_height = 540, 430
board_rect=pygame.rect.Rect(30,30,board_width, board_height+10)

#create rects for each column
rects=[]
for x in range(len(board)):
    rects.append(pygame.rect.Rect(30 + ((board_width*x)/len(board)), 0, board_width/len(board),height))

# 1 is player, 1< is ai
players=[1,1]
random=random_ai(2)
win_and_block=win_and_block_ai(2)
block_two=block_two_ai(2)
brute_force=brute_force_single(2)

turn=0

won=True
wins=[0,0,0]

moves=0

stop_between=False

while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            wins[winner]+=1
            print(f"Draws: {wins[0]}\nPlayer 1: {wins[1]}\nPlayer 2: {wins[2]}")
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if won:
                wins[winner]+=1
                board=[[0 for _ in range(6)] for _ in range(7)]
            elif players[turn] == 1:
                x, y = pygame.mouse.get_pos() # Get click position
                print("")
                for index, collision in enumerate(rects):
                    if collision.collidepoint(x,y):
                        moves=0
                        print("Click collides with",index)
                        temp_board, valid = playmove(board,index,turn+1)
                        if valid:
                            print("Move is valid")
                            board=temp_board
                            turn=1-turn
    
    cur_player=players[turn]
    if cur_player == 2 and not won:
        win_and_block.number=turn+1
        moves+=1
        print("")
        print("Ai 1 running")
        ai_move=win_and_block.getmove(board)
        temp_board, valid=playmove(board,ai_move,turn+1)
        while not valid:
            print("not valid")
            ai_move=random.getmove(board)
            temp_board, valid = playmove(board,ai_move,turn+1)
        print("AI's move:",ai_move)
        board=temp_board
        turn=1-turn
        
    elif cur_player == 3 and not won:
        block_two.number=turn+1
        moves+=1
        print("")
        print("Ai 2 running")
        ai_move=block_two.getmove(board)
        temp_board, valid=playmove(board,ai_move,turn+1)
        while not valid:
            print("not valid")
            ai_move=random.getmove(board)
            temp_board, valid = playmove(board,ai_move,turn+1)
        print("AI's move:",ai_move)
        board=temp_board
        turn=1-turn
    
    elif cur_player == 4 and not won:
        brute_force.number=turn+1
        moves+=1
        print("")
        print("Ai 3 running")
        ai_move=brute_force.getmove(board)
        board, _ = playmove(board,ai_move,turn+1)
        print("AI's move:",ai_move)
        turn=1-turn
        
    # Draw background
    screen.fill((0,0,0))
    pygame.draw.rect(screen,(0,0,255),board_rect)

    # Draw spaces
    for n, column in enumerate(board):
        cur_x=30 + ((board_width*n)/len(board)) + (board_width/(len(board)*2))
        for i, space in enumerate(column):
            cur_y=30 + ((board_height*i)/len(column)) + (board_height/(len(column)*2))
            # print(cur_x,cur_y)
            if space == 1:
                cur_color=(255,0,0)
            elif space == 2:
                cur_color=(255,255,0)
            else:
                cur_color=(255,255,255)
            pygame.draw.circle(screen,cur_color,(cur_x,cur_y),30)

    #display debug
    # drawtext(f"AI moves in a row: {moves}",(100,100))

    won, winner = detectwin(board)
    if won:
        drawtext(f"{winner} Wins!!!!",(230,500),(255,255,255))
        if not stop_between:
            wins[winner]+=1
            board=[[0 for _ in range(6)] for _ in range(7)]

    drawtext("Turn:",(50,600),(255,255,255))
    pygame.draw.circle(screen,(255,255 if turn == 1 else 0, 0),(160,625),30)
    drawtext(str(turn+1),(150,600))

    pygame.display.flip()
    fpsClock.tick(fps)