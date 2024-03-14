from random import randint
from game import playmove, detectwin

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
                    test_board,_ = playmove(board,column_index+empty_index,3-number)
                    detecting_win, whowon=detectwin(test_board)
                    if detecting_win and whowon == 3-number:
                        return True, column_index+empty_index
        
        return False, 0
    
    def getmove(self, board):
        print("getting move")
        detected, index = self.detect_three(board,self.number)
        if detected:
            print("win detected")
            return index
        
        detected, index = self.detect_three(board,3-self.number)
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
        print("getting move")
        detected, index = self.detect_three(board,self.number)
        if detected:
            print("win detected")
            return index
        
        detected, index = self.detect_three(board,3-self.number)
        if detected:
            print("blocking move")
            return index
        
        print("no 3 found")
        
        print("looking for twos")
        detected, index = self.detect_two(board,self.number)
        if detected:
            print("2 for me detected")
            return index
        
        detected, index = self.detect_two(board,3-self.number)
        if detected:
            print("2 for enemy detected")
            return index
        
        print("no two found")
        return randint(0,len(board)-1)