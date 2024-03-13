from random import randint

class random_ai:
    def __init__(self,number):
        self.number=number
        
    def getmove(self,board):
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
        return super().getmove(board)