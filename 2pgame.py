import sys
 
import pygame
from pygame.locals import *

from game import detectwin, playmove

def drawtext(text,pos,color=(0,0,0)):
    surface=sans.render(text,False,color)
    screen.blit(surface,pos)

board=[[0 for _ in range(6)] for _ in range(7)]
# organized SIDEWAYS

pygame.init()
pygame.font.init()

sans = pygame.font.SysFont('Comic Sans MS', 30)

fps = 10
fpsClock = pygame.time.Clock()

width, height = 600, 500
screen = pygame.display.set_mode((width, height))

board_width, board_height = width-60, height-70
board_rect=pygame.rect.Rect(30,30,board_width, board_height+10)

#create rects for each column
rects=[]
for x in range(len(board)):
    rects.append(pygame.rect.Rect(30 + ((board_width*x)/len(board)), 0, board_width/len(board),height))

turn=0

won=False

while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if won:
                board=[[0 for _ in range(6)] for _ in range(7)]
            else:
                x, y = pygame.mouse.get_pos() # Get click position
                for index, collision in enumerate(rects):
                    if collision.collidepoint(x,y):
                        print("Click collides with",index)
                        temp_board, valid = playmove(board,index,turn+1)
                        if valid:
                            print("Move is valid")
                            board=temp_board
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

    won, winner = detectwin(board)
    if won:
        drawtext(f"{winner} Wins!!!!",(width/2,height/2))

    pygame.display.flip()
    fpsClock.tick(fps)