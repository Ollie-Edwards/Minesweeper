from re import split
import pygame
import random

from pygame import color

BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)

WIDTH = 500
HEIGHT = 500
gapWidth = 1

pygame.init()
clock = pygame.time.Clock()
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Sorting Visualiser")
PoppinsFont = pygame.font.Font('Fonts\Poppins-Light.ttf', 14)

rowNum = 20
colNum = 20
rowWidth = WIDTH // colNum
colHeight = HEIGHT // rowNum

lineColor = (0,0,0)

board = [["011" for i in range(rowNum)]for i in range(colNum)]

chanceOfMine = 5 # 1/chance of mine

#
# the first number represents whether the box contains a mine or not
# the second number represents whether the the node has been discovered
# the third number represents the number of mines around the current node
#
# eg. 003 represents a box with no mine, that has not been discovered but has 3 mines next to it 
# and. 100 represents a bo0x with a mine, that has not been discovered and has not mines next to it
# 

def drawLines(board, rowWidth, colHeight):
    for row in range(rowNum):
        pygame.draw.line(WIN, lineColor, (row*rowWidth, 0), (row*rowWidth, colNum*colHeight), gapWidth) # sureface colour start end width    
    for col in range(colNum):
        pygame.draw.line(WIN, lineColor, (0, col*colHeight), (rowNum*rowWidth, col*colHeight), gapWidth) # sureface colour start end width

# def drawLines(board, rowWidth, colHeight):
#     for col in range(colNum):
#         for row in range(rowNum):
#             pygame.draw.line(WIN, lineColor, (0, row*rowWidth), (rowWidth, row*rowWidth), gapWidth)
#             #pygame.draw.line(WIN, lineColor, (col*widthOfBox, 0), (col*widthOfBox, width), gapWidth)

def updateneighbours(board):
    for row in range(rowNum):
        for col in range(colNum):
            neighbours = 0

            # TODO make this more concise

            row, col = col, row

            if ( 0 <= col+1 < colNum) and ( 0 <= row+1 < rowNum):
                if board[col+1][row+1][0] == "1":
                    neighbours += 1

            if ( 0 <= col < colNum) and ( 0 <= row+1 < rowNum):
                if board[col][row+1][0] == "1":
                    neighbours += 1

            if ( 0 <= col-1 < colNum) and ( 0 <= row+1 < rowNum):
                if board[col-1][row+1][0] == "1":
                    neighbours += 1   

            if ( 0 <= col-1 < colNum) and ( 0 <= row < rowNum):
                if board[col-1][row][0] == "1":
                    neighbours += 1 

            if ( 0 <= col-1 < colNum) and ( 0 <= row-1 < rowNum):
                if board[col-1][row-1][0] == "1":
                    neighbours += 1   

            if ( 0 <= col < colNum) and ( 0 <= row-1 < rowNum):
                if board[col][row-1][0] == "1":
                    neighbours += 1   

            if ( 0 <= col+1 < colNum) and ( 0 <= row-1 < rowNum):
                if board[col+1][row-1][0] == "1":
                    neighbours += 1   

            if ( 0 <= col+1 < colNum) and ( 0 <= row < rowNum):

                if board[col+1][row][0] == "1":
                    neighbours += 1

            code = list(board[row][col])
            code[2] = str(neighbours)
            board[row][col] = str("".join(code))

def createBoard():
    board = [["" for i in range(rowNum)]for i in range(colNum)]
    global numOfMines
    numOfMines = 0

    for row in range(rowNum):
        for col in range(colNum):
            code = "" # see ln 40 for explanation
            
            if random.randint(0, chanceOfMine) == 0:
                code += "1"
            else:
                code += "0"

            code += "0"

            code += "2"

            board[col][row] = code

    return board

def drawBoxes(board, rowWidth, colHeight):
    for row in range(rowNum):
        for col in range(colNum):
            colour = (200,200,200)
            node = str(board[col][row])

            mine, discovered, neighbours = (node[0] == "1", node[1] == "1", node[2])

            if mine == True:
                colour = (100, 10, 10)      

            if discovered:
                colour = (0,0,255)   
            
            rect = pygame.Rect(row*rowWidth, col*colHeight, rowWidth, colHeight) #left, top, width, height 
            pygame.draw.rect(WIN, colour, rect)

            if discovered:
                # render text
                textSurfaceObj = PoppinsFont.render(neighbours, True, (255,10,18), None)
                textRectObj = textSurfaceObj.get_rect()
                textRectObj.center  = ((row*rowWidth)+rowWidth//2, (col*colHeight)+colHeight//2)
                WIN.blit(textSurfaceObj, textRectObj)

def RenderBoard(board):
    rowWidth = WIDTH // colNum
    colHeight = HEIGHT // rowNum

    updateneighbours(board)

    drawBoxes(board, rowWidth, colHeight)
    drawLines(board, rowWidth, colHeight)

board = createBoard()

run = True
while run:
    WIN.fill(WHITE)

    mousex, mousey = pygame.mouse.get_pos()
    clickedRow = mousex//rowWidth
    clickedCol = mousey//colHeight

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.VIDEORESIZE:
            w, h = (event.dict['size'])
            WIDTH, HEIGHT = w, h
            
            WIDTH = (WIDTH // colNum)*colNum
            HEIGHT = (HEIGHT // rowNum)*rowNum

            WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

        if event.type == pygame.MOUSEBUTTONDOWN: # begining of a drag
            code = list(board[clickedCol][clickedRow])
            code[1] = "1"
            board[clickedCol][clickedRow] = str("".join(code))

    RenderBoard(board)
    
    clock.tick(30)
    pygame.display.update()