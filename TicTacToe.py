# Tic Tac Toe 
import pandas as pd
import numpy as np
#from pynput import keyboard
    

class TicTacToe ():
    def __init__(self):
        self.playerSymbol = "o"
        self.playerScore = 1
        self.AISymbol = "x"
        self.AIScore = -1
        self.moveNo = 0
        self.roundNo = 1
        self.gameOver = False
        self.winner = "Draw"

        # Pandas Dataframes:
        self.validCells = pd.DataFrame([['A1', 'B1', 'C1'], ['A2', 'B2', 'C2'], ['A3', 'B3', 'C3']], columns=["A", "B", "C"])
        self.validCells.index = range(1, len(self.validCells) + 1)

        self.gameScoresMatrix = pd.DataFrame([[0, 0, 0], [0, 0, 0], [0, 0, 0]], columns=["A", "B", "C"])
        self.gameScoresMatrix.index = range(1, len(self.gameScoresMatrix) + 1)

        self.gameBoardMatrix = pd.DataFrame([["_", "_", "_"], ["_", "_", "_"], ["_", "_", "_"]], columns=["A", "B", "C"])
        self.gameBoardMatrix.index = range(1, len(self.gameBoardMatrix) + 1)
        

    def gameInit(self):
        print("Welcome to Tic Tac Toe Challenge!")
        print(" ")


        # Chosing player symbol
        symbolChoice = input("Press 'x' or 'o' to choose your side: ")
        while symbolChoice.lower() not in ("x", "o"):  
            symbolChoice = input("Please choose between 'x' or 'o': ")

        if symbolChoice == "x":
            self.playerSymbol = "x"
            self.AISymbol = "o"

        # Chosing a starting player
        anyKey = input("Great! Now press any key to initiate a draw for starting player.")
        print(" ")
        randomInt = np.random.randint(1, 100)

        if randomInt > 50:
            self.startingPlayer = "Player"
            print("You start the game!")
        else:    
            self.startingPlayer = "AI"
            print("I start the game!")
        
        print(" ")
        print("LET THE GAME BEGIN!")
        
        # Start games
        self.startGame()

        # End game
        self.endGame()
        
        
    # Game End
    def endGame(self):
        print(" ")
        print("=========================")
        print(" ")
        print("GAME OVER!")
        print(" ")
        self.displayGameBoard() 
        print(" ")

        if self.winner == "Surrender":
            print("You surrendered!")
        if self.winner == "Draw":
            print("Game ended with a draw!")
        if self.winner == "Player":
            print("Congratulations!! You won!")
        if self.winner == "AI":
            print("I WON!! Thank you for the game. More luck next time!")     

    
     # Print current game board situation
    def displayGameBoard(self):
        print("Game Board:")
        print(" ")
        print(self.gameBoardMatrix)
        #print(self.gameScoresMatrix)
        print(" ")
        


    # MAIN game loop
    def startGame(self):
        
        # Check if game over condition is met (move 10 or victory)
        def _checkGameOver(lastPlayer):

            #print(self.moveNo)
            #print(lastPlayer)
            # Check turn number
            def _checkFinalMove():
                if self.moveNo == 9:
                    self.gameOver = True
            
            # Check if victory condition is met
            def _checkVictory(lastPlayer):
                rowsSums = self.gameScoresMatrix.sum(axis=1).tolist()
                columnsSums = self.gameScoresMatrix.sum(axis=0).tolist()
                diagonal1Sum = np.trace(self.gameScoresMatrix.values)
                diagonal2Sum = self.gameScoresMatrix.at[1, "C"] + self.gameScoresMatrix.at[2, "B"] + self.gameScoresMatrix.at[3, "A"]
                
                if (any(x in rowsSums for x in [3, -3])
                    or any(x in columnsSums for x in [3, -3])
                    or (diagonal1Sum == 3 or diagonal1Sum == -3)
                    or (diagonal2Sum == 3 or diagonal2Sum == -3)):
                    
                    self.gameOver = True
                    self.winner = lastPlayer
            
            if self.gameOver:
                self.winner = "Surrender"
            else:
                _checkFinalMove()
                _checkVictory(lastPlayer)

        # insert move onto a game board
        def _insertMove(move, symbol, score):
            rowNo = int(move[-1])
            colNo = move[0]
            self.gameBoardMatrix.at[rowNo, colNo] = symbol
            self.gameScoresMatrix.at[rowNo, colNo] = score


        # Player's move logic
        def _playerMove():
            def _checkPlayerMoveIsValid(playerMove):
                moveValid = False

                validCell = playerMove in self.validCells.values.flatten()
                if validCell:
                    rowNo = int(playerMove[-1])
                    colNo = playerMove[0]
                    if self.gameBoardMatrix.at[rowNo, colNo] == "_":
                        moveValid = True

                return moveValid
            
            # play if game didn't end with last AI's move
            if not self.gameOver:
                self.moveNo += 1
                
                playerMove = input("Choose you move (e.g. B3) or x to end game: ").strip().upper()
                
                if playerMove == "X":
                    self.gameOver = True
                else:
                    while not _checkPlayerMoveIsValid(playerMove):
                        playerMove = input("Please choose valid and free option: ").strip().upper()

                    _insertMove(move=playerMove, symbol=self.playerSymbol, score=self.playerScore)
        
        # AI's move logic
        def _AIMove():
            
            # check if:
            # itteration 1: AI can win - Win!
            # itteration 2: player can win - Block move!
            def _AI_checkCriticalMove(scoreInt):
                _AIMove = 0
                _moveDone = False

                def _checkPotentialAIMove(listScoreIs2):
                    for rowIndex, row in listScoreIs2.iterrows():
                        for colIndex, value in row.items():
                            if value == 0:
                                return colIndex, rowIndex
                                

                rowsSums = self.gameScoresMatrix.sum(axis=1)
                rowsSums_ScoreIs2 = self.gameScoresMatrix[rowsSums == scoreInt]
                
                 
                index1, index2 = _checkPotentialAIMove(rowsSums_ScoreIs2) or (0, 0)
                if index1 != 0:
                    _AIMove = index1 + str(index2)
                    _moveDone = True

                if not _moveDone:
                    colsSums = self.gameScoresMatrix.sum(axis=0)
                    colsSums_ScoreIs2 = self.gameScoresMatrix.loc[:, colsSums == scoreInt]

                    index1, index2 = _checkPotentialAIMove(colsSums_ScoreIs2) or (0, 0)
                    if index1 != 0:
                        _AIMove = index1 + str(index2)
                        _moveDone = True

                
                return _moveDone, _AIMove
        

            # do random valid move
            def _AI_moveRandom():
                freeCells = self.gameScoresMatrix[self.gameScoresMatrix == 0]
                linear_list = freeCells.to_numpy().flatten().tolist()

                randomInt = np.random.randint(0, 8)
                while not linear_list[randomInt] == 0.0:
                    randomInt = np.random.randint(0, 8)
               
                validCells = self.validCells.to_numpy().flatten().tolist()
                _AIMove = validCells[randomInt]   
                _moveDone = True
                return _moveDone, _AIMove
                
                
            
            # play if game didn't end with last player's move
            if not self.gameOver:
                moveDone = False
                AIMove = 0

                self.moveNo += 1

                if not moveDone:
                    moveDone, AIMove = _AI_checkCriticalMove(-2) or (False, "x")

                if not moveDone:
                    moveDone, AIMove = _AI_checkCriticalMove(2) or (False, "x")

                if not moveDone:
                    moveDone, AIMove = _AI_moveRandom() or (False, "x")


                if moveDone:
                    _insertMove(move=AIMove, symbol=self.AISymbol, score=self.AIScore)
                else:
                    print("AI move error!!")

                self.displayGameBoard()
        
        
        # Game Loop - player moves
        while not self.gameOver:
            print("---")
            print(f"""Round number: {self.roundNo}""")
            print(" ")
            self.displayGameBoard() 
            print(" ")
            
            if self.startingPlayer == "Player":
                _checkGameOver(lastPlayer="AI")    
                _playerMove()
                _checkGameOver(lastPlayer="Player")
                _AIMove()
            else:
                _checkGameOver(lastPlayer="Player")    
                _AIMove()
                _checkGameOver(lastPlayer="AI")
                _playerMove()

            self.roundNo += 1
            

if __name__=="__main__":
    game = TicTacToe()
    game.gameInit()

