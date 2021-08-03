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

def makeFlagged(col, row):
    code = list(board[col][row])
    code[3] = "1"
    board[col][row] = str("".join(code))

def makeDiscovered(col, row):
    code = list(board[col][row])
    code[1] = "1"
    board[col][row] = str("".join(code))

def isDiscovered(col, row):
    if list(board[col][row])[1] == "1":
        return True
    return False

def getNeighbours(col, row):
    if ( 0 <= col < colNum) and ( 0 <= row < rowNum):
        return list(board[col][row])[2]
    return None

def isMine(col, row):
    if ( 0 <= col < colNum) and ( 0 <= row < rowNum):
        if board[col][row][0] == "1":
            return 1
    return 0

def updateNeighbours(board):
    for row in range(colNum):
        for col in range(rowNum):
            neighbours = 0

            for i in range(-1, 2, 1):
                for j in range(-1, 2, 1):
                    neighbours += isMine(col+j, row+i)
            
            code = list(board[col][row])
            code[2] = str(neighbours)
            board[col][row] = str("".join(code))

def createBoard():
    board = [["" for i in range(rowNum)]for i in range(colNum)]
    global numOfMines
    numOfMines = 0

    for row in range(rowNum):
        for col in range(colNum):
            code = "" # see ln 40 for explanation
            
            if random.randint(1, chanceOfMine) == 1:
                code += "1" # ismine
            else:
                code += "0" #ismine

            code += "0" # is discovered
            code += "0" # neighbours
            code += "0" # is flagged

            board[col][row] = code

    return board

def drawBoxes(board, rowWidth, colHeight):
    for row in range(rowNum):
        for col in range(colNum):
            colour = (200,200,200)
            node = str(board[col][row])

            mine, discovered, neighbours, flagged = node[0] == "1", node[1] == "1", node[2], node[3] == "1"

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
            
            if flagged:
                flagImage = pygame.image.load('flag.png')
                flagImage = pygame.transform.scale(flagImage, (round(rowWidth*.7), round(colHeight*.7)))
                WIN.blit(flagImage, (row*rowWidth+(round(rowWidth*.15)), col*colHeight+(round(colHeight*.15)))) 

def RenderBoard(board):
    updateNeighbours(board)

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
            colHeight, rowWidth = (HEIGHT // rowNum), (WIDTH // colNum)

            WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if isMine(clickedCol, clickedRow):
                    exit() ## TODO add end screen
                makeDiscovered(clickedCol, clickedRow)
        
            elif event.button == 3:
                makeFlagged(clickedCol, clickedRow)

    RenderBoard(board)
    
    clock.tick(30)
    pygame.display.update()