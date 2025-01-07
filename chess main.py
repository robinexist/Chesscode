import pygame as p
import chessEngine

WIDTH = 512
HEIGHT = 512
DIMENSION = 8
SQSIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def LoadImages():
    pieces = ["wp","wn","wb" ,"wr","wq","wk", "bp","bn","br","bb","bq","bk"]
    
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(piece +".png"),(SQSIZE, SQSIZE))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chessEngine.gamestate()
    validMoves = gs.getValidMoves()
    moveMade = False
    LoadImages()
    running= True
    sqSelected = ()
    playerClicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SQSIZE
                row = location[1]//SQSIZE
                if sqSelected == (row,col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:
                    move = chessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gs.makeMove(move)
                            moveMade = True
                            sqSelected = ()
                            playerClicks = []
                    if not moveMade:
                        playerClicks = [sqSelected]
            elif e.type ==p.KEYDOWN:
                if e.key ==p.K_z:
                    gs.undoMove()
                    moveMade = True
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen,gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    colours = [p.Color("white"),p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            colour = colours[((r+c)%2)]
            p.draw.rect(screen, colour, p.Rect(c*SQSIZE, r*SQSIZE, SQSIZE, SQSIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board [c][r]
            if piece != "--":
                screen.blit(IMAGES[piece],p.Rect(r*SQSIZE, c*SQSIZE,SQSIZE,SQSIZE))

if __name__ == "__main__":
    main()
