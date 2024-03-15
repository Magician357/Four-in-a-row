from random import randint, shuffle
from game import playmove, detectwin, printboard

class random_ai:
    def __init__(self,number):
        self.number=number
        
    def getmove(self,board):
        print("generating random move")
        return randint(0,len(board)-1)

class win_and_block_ai(random_ai):
    def __init__(self, number):
        super().__init__(number)
    
    def detect_three(self,board,number):
        #vertical
        for cn, column in enumerate(board):
            for index in range(len(column)-3):
                if column[index] == 0 and column[index+1] == number and column[index+2] == number and column[index+3] == number:
                    return True, cn
        
        #horizontal
        for row_index in range(len(board[0])):
            for column_index in range(len(board)-3):
                cur_slize=[board[column_index+a][row_index] for a in range(4)]
                count=0
                empty_index = None
                for i, slot in enumerate(cur_slize):
                    if slot == number:
                        count+=1
                    elif slot == 0:
                        empty_index = i
                if count == 3 and empty_index != None:
                    print("3 found at",column_index+empty_index,"for",number)
                    print("Testing if valid")
                    test_board, _ = playmove(board,column_index+empty_index,number)
                    printboard(test_board)
                    detecting_win, whowon=detectwin(test_board)
                    if detecting_win and whowon == number:
                        return True, column_index+empty_index
        
        return False, 0
    
    def getmove(self, board):
        board_copy=list(board)
        print("getting move")
        detected, index = self.detect_three(board_copy,self.number)
        if detected:
            print("win detected")
            return index
        
        detected, index = self.detect_three(board_copy,3-self.number)
        if detected:
            print("blocking move")
            return index

        print("no 3 found")
        return randint(0,len(board)-1)
    

class block_two_ai(win_and_block_ai):
    def __init__(self, number):
        super().__init__(number)
        
    
    def detect_three(self, board, number):
        return super().detect_three(board, number)
    
    def detect_two(self,board,number):
            #vertical
            for cn, column in enumerate(board):
                for index in range(len(column)-2):
                    if column[index] == 0 and column[index+1] == number and column[index+2] == number:
                        return True, cn
            
            #horizontal
            for row_index in range(len(board[0])):
                for column_index in range(len(board)-2):
                    cur_slize=[board[column_index+a][row_index] for a in range(3)]
                    count=0
                    empty_index = None
                    for i, slot in enumerate(cur_slize):
                        if slot == number:
                            count+=1
                        elif slot == 0:
                            empty_index = i
                    if count == 3 and empty_index != None:
                        return True, column_index+empty_index
                    
            
            return False, 0
    
    def getmove(self, board):
        board_copy=list(board)
        print("getting move")
        detected, index = self.detect_three(board_copy,self.number)
        if detected:
            print("win detected")
            return index
        
        detected, index = self.detect_three(board_copy,3-self.number)
        if detected:
            print("blocking move")
            return index
        
        print("no 3 found")
        
        print("looking for twos")
        detected, index = self.detect_two(board_copy,self.number)
        if detected:
            print("2 for me detected")
            return index
        
        detected, index = self.detect_two(board_copy,3-self.number)
        if detected:
            print("2 for enemy detected")
            return index
        
        print("no two found")
        return randint(0,len(board)-1)
    
class brute_force_single(random_ai):
    def __init__(self, number):
        super().__init__(number)
    
    def brute_force_from_point(self,board):
        board_copy=list(board) # just in case
        printboard(board_copy)
        #play all possible moves
        columns=[n for n in range(7)]
        for turn in [self.number,3-self.number]:
            print("\nBrute forcing for",turn)
            shuffle(columns) # shuffle for more variety
            for column in columns:
                print("Checking column",column)
                temp_board, valid = playmove(board_copy,column,turn)
                if not valid:
                    print("invalid move")
                    continue
                printboard(temp_board)
                won, winner = detectwin(temp_board)
                if won and winner == turn:
                    print("win detected")
                    return True, column, turn
        return False, 0, 0
    
    def getmove(self, board):
        found, result, _ = self.brute_force_from_point(board)
        
        return result if found else super().getmove(board)

class brute_force_better_random(brute_force_single):
    def __init__(self, number):
        super().__init__(number)
    
    def brute_force_from_point(self, board):
        return super().brute_force_from_point(board)
    
    def getmove(self, board):
        board_copy=list(board)
        found, result, winner = self.brute_force_from_point(board_copy)
        if not found:
            print("win not found, going deeper")
            columns=[n for n in range(7)]
            shuffle(columns)
            for column in columns:
                # test if move gives opponent win
                temp_board, valid = playmove(board_copy,column,3-self.number)
                
                new_found, new_result, new_winner = self.brute_force_from_point(temp_board)
        
        return result