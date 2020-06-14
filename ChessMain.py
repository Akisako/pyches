import pygame as p
import ChessEngine


WIDTH = HEIGHT = 512
DIMENSION = 8 #dimension d'un échiquier 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15#pour les animations
IMAGES = {}

'''
Créé un dico global d'images
'''
def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ', ]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("asset/" + piece +".png"), (SQ_SIZE, SQ_SIZE))
    #l'on peut mtn accéder à une image en l'appelant ex: IMAGES['wp']
    
    '''
    code principal : s'occupe des input de l'utilisateur and update les graphismes
    '''

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("White"))
    gs = ChessEngine.GameState()
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #souris
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #(x,y) position de la souris
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col): #l'utilisateur clique sur le même carré deux fois
                    sqSelected = () #déselectionne la case
                    playerClicks = [] #efface/enlève le click du joueur 
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2: #après le deuxième click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    gs.makeMove(move)
                    sqSelected = () #reset le click
                    playerClicks = []
            #clavier
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #annule le coup quand w(w = z en qwerty) est pressé
                    gs.undoMove()
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


'''
s'occupe des graphismes
'''
def drawGameState(screen, gs):
    drawBoard(screen) #dessine les carrés sur le plateau
    drawPieces(screen, gs.board) #dessine les pièces

'''
dessines les carrés
'''
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))



'''
dessine les pièces, utilise GameState.board'''
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": #"--" = carré vide, donc si, pièce n'est pas un carré vide, alors...
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()
