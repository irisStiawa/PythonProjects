import pygame
from math import degrees, atan

class Ball(object):
    def __init__(self,img,d=10,center=(5,5)):
        self.img = img
        self.d = d
        self.center = center
        self.pos = (center[0]-d/2,center[1]-d/2)
        self.speed = [0,0]
        self.R = 0
        
class Linie(object):
    def __init__(self,start,end,width=1,color=(255,255,255)):
        self.start = start
        self.end = end
        self.width = width
        self.color = color
        # Berechnen der Erzeugerfunktion "y = kx + d" für die Linie
        # y = kx+d --> d = y-kx
        self.k = ((self.end[1]-self.start[1])/(self.end[0]-self.start[0]))
        self.d = self.start[1] - self.k * self.start[0]
    
def blitRotateCenter(surf, image, topleft, angle):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    surf.blit(rotated_image, new_rect.topleft)
    
def reflexion(linie,objekt,P):   
    # Einfallsvektor A-->P = aktuelle Geschwindigkeit des Balls, Ausgangspunkt A = aktuelle Position - Bewegung
    A = (P[0]-objekt.speed[0],P[1]-objekt.speed[1])
    
    # Normale: y = -x/k + d_normal (Gerade: y = kx --> Normale Gerade: y = -1/k * x = -x/k)
    # Einsetzen von P zur Ermittlung von d_normal
    d_normal = P[1] + P[0]/linie.k
    
    # Parallele: y = kx + d_parallel - Einsetzen von A zur Ermittlung von d_parallel
    d_parallel = A[1] - linie.k * A[0]
    # Schnittpunkt S von Normale und Parallele
    S = ((d_normal - d_parallel)/(linie.k+1/linie.k),(-(d_normal - d_parallel)/(linie.k+1/linie.k))/linie.k + d_normal)
    # Endpunkt E (Spiegelpunkt) = S + A->S
    E = (S[0]+S[0]-A[0],S[1]+S[1]-A[1])
    # Ausfallsvektor = neue Geschwindigkeit = P->E
    Ausfallsvektor = [E[0]-P[0],E[1]-P[1]]
    
    return Ausfallsvektor

def checkcollision(linie,objekt):
    # Kollisionsabfrage - jeder Punkt der Linie wird gegen die Grenzen des Balls geprüft
    for x in range(linie.start[0],linie.end[0]):
        if objekt.pos[0] < x < objekt.pos[0] + objekt.d:
            y = linie.k * x + linie.d
            if objekt.pos[1] < y < objekt.pos[1] + objekt.d:
                return reflexion(linie,objekt,(x,y))
    return False


def main():
    pygame.init()
    b,h = 1000, 1000
    screen = pygame.display.set_mode((b,h))
    
    img = pygame.image.load('BB2.png').convert()
    img.set_colorkey((0,0,0))
    Ballliste = [[40,(111,111)],
                 [50,(222,222)],
                 [60,(333,333)],
                 [70,(444,444)]]
    Bälle = []
    Linienliste = [[(150,450),(450,150),11],
          [(550,150),(850,450),11],
          [(150,550),(450,850),11],
          [(550,850),(850,550),11]]
    Linien = []
    
    for elem in Ballliste:
        BO = Ball(img,elem[0],elem[1])
        BO.img = pygame.transform.scale(BO.img,(BO.d,BO.d))
        Bälle.append(BO)
    
    for elem in Linienliste:
        L = Linie(elem[0],elem[1],elem[2])
        Linien.append(L)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONUP:
                mpos = pygame.mouse.get_pos()
                for B in Bälle:
                    if B.pos[0] < mpos[0] < B.pos[0] + B.d:
                        if B.pos[1] < mpos[1] < B.pos[1] + B.d:
                            B.center = (B.pos[0]+B.d/2,B.pos[1]+B.d/2)
                            B.speed = [(B.center[0]-mpos[0])/5,(B.center[1]-mpos[1])/5]
                mpos = None
        
        screen.fill((55,55,255))
        
        for L in Linien:            
            pygame.draw.line(screen, L.color, L.start,L.end,width=L.width)
                     
        for B in Bälle:
            blitRotateCenter(screen, B.img, B.pos, B.R)
            #if B.pos[1] < h-B.d: B.speed[1]+=0.005
            B.speed[0] = B.speed[0]*0.999
            B.speed[1] = B.speed[1]*0.999      
            B.R = B.R + (degrees(atan(B.speed[1]/B.speed[0])))*(((B.speed[0]**2+B.speed[1]**2)**1/2)/60) if B.speed[0] != 0 else B.R
            
            B.pos = (B.pos[0] + B.speed[0], B.pos[1] + B.speed[1])   
            if B.pos[0] < 0 or B.pos[0] > b-B.d: B.speed[0] = -B.speed[0]
            if B.pos[1] < 0 or B.pos[1] > h-B.d: B.speed[1] = -B.speed[1]
            
        
            for L in Linien:
                Reflexion = checkcollision(L,B)
                if Reflexion:
                    B.speed = Reflexion
                    
        pygame.display.flip()
        
if __name__=="__main__":
    main()