def playmove(board,column,player):
    temp_column=board[column]
    move_played=False
    for index, space in enumerate(temp_column):
        if space != 0:
            if index == 0:
                break # no valid moves
            else:
                # print("move is valid")
                move_played=True
                temp_column[index-1]=player
                break
        elif index == len(temp_column)-1:
            # print("move is valid")
            move_played=True
            temp_column[index]=player
            break
            
    board[column]=temp_column
    return board, move_played

def detectsame(list):
    return len(set(list)) == 1

def detectwin(board, win_length=4):
    win_length_s=win_length-1
    #vertical
    for column in board:
        for index in range(len(column)-win_length_s):
            if detectsame([column[index+a] for a in range(win_length)]) and column[index] != 0:
                return True, column[index]
                # continue # disable after testing
    
    #horizontal
    for row_index in range(len(board[0])):
        for column_index in range(len(board)-win_length_s):
            if detectsame([board[column_index+a][row_index] for a in range(win_length)]) and board[column_index][row_index] != 0:
                return True, board[column_index][row_index]
                # continue # disable after testing
    
    #diagonal
    for row in range(len(board)-win_length):
        for column in range(win_length_s,len(board[0])):
            # print(column,row)
            if detectsame([board[column-a][row+a] for a in range(win_length)]) and board[column][row] != 0:
                return True, board[column][row]
    
    for j in range(win_length_s,len(board)-1):
        for i in range(win_length_s,len(board[0])):
            if detectsame([board[i-a][j-a] for a in range(win_length)]) and board[i][j] != 0:
                return True, board[i][j]
    
    # detecting draw:
    drawed=True
    for column in board:
        if 0 in column:
            drawed=False
    
    return drawed, 0

def printboard(board):
    c=""
    for y in range(len(board[0])):
        for x in range(len(board)):
            c+=str(board[x][y])+" | "
        c+="\n"
    c+="---------------------------\n1 | 2 | 3 | 4 | 5 | 6 | 7 |"
    print(c)

if __name__ == "__main__":
    board=[[0 for _ in range(6)] for _ in range(7)]
    turn=0
    while not detectwin(board):
        printboard(board)
        print("Turn:",turn+1)
        choice=int(input("what space? "))-1
        temp_board, valid = playmove(board,choice,turn+1)
        if valid:
            board=temp_board
            turn=1-turn
    printboard(board)
    print(detectwin(board)[1],"Wins!")