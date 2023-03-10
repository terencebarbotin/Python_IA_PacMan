import random
import tkinter as tk
from tkinter import font  as tkfont
import numpy as np
import sys

##########################################################################
#
#   Partie I : variables du jeu  -  placez votre code dans cette section
#
#########################################################################
 
 
# Plan du labyrinthe

# 0 vide
# 1 mur
# 2 maison des fantomes (ils peuvent circuler mais pas pacman)
# 3 Super-PacGum

ScorePlayer = 0

# 0 En cours
# 1 Perdu
# 2 Gagné
GameState = 0

GameStateMsg = "En cours"

Super = False
SuperCount = 16

# transforme une liste de liste Python en TBL numpy équivalent à un tableau 2D en C
def CreateArray(L):
   T = np.array(L,dtype=np.int64)
   T = T.transpose()  ## ainsi, on peut écrire TBL[x][y]
   return T

TBL = CreateArray([
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,3,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,3,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,0,1,1,0,1,1,2,2,1,1,0,1,1,0,1,0,1],
        [1,0,0,0,0,0,0,1,2,2,2,2,1,0,0,0,0,0,0,1],
        [1,0,1,0,1,1,0,1,1,1,1,1,1,0,1,1,0,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,3,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,3,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] ]);
# attention, on utilise TBL[x][y] 
        
HAUTEUR = TBL.shape [1]      
LARGEUR = TBL.shape [0]  

I = 1000
M = HAUTEUR * LARGEUR

# On définit une valeur G pour représenter les cases où il y a encore des gommes 
O = 0 

# On créé une nouvelle grille correspondant à la taille de la grille du jeu. 
# La maison des fantômes est considérée comme des murs car inaccessible pour Pacman 



# placements des pacgums et des fantomes

def PlacementsGUM():  # placements des pacgums
   GUM = np.zeros(TBL.shape,dtype=np.int64)
   
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( TBL[x][y] == 0):
            GUM[x][y] = 1
         # Super PacGums
         if(TBL[x][y] == 3):
            GUM[x][y] = 2
   return GUM
            
GUM = PlacementsGUM()   

PacManPos = [5,5]

def IsGum():
   IsGum = False

   if(GUM[PacManPos[0]][PacManPos[1]] == 1 ):
      IsGum = True

   return IsGum

def IsSuperGum():
   return GUM[PacManPos[0]][PacManPos[1]] == 2

   
Ghosts  = []
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "pink", '']   )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "orange", ''] )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "cyan", '']   )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "red", ''   ]     )         

     

##############################################################################
#
#  Debug : ne pas toucher (affichage des valeurs autours dans les cases

LTBL = 100
TBL1 = [["" for i in range(LTBL)] for j in range(LTBL)]
TBL2 = [["" for i in range(LTBL)] for j in range(LTBL)]


# info peut etre une valeur / un string vide / un string...
def SetInfo1(x,y,info):
   info = str(info)
   if x < 0 : return
   if y < 0 : return
   if x >= LTBL : return
   if y >= LTBL : return
   TBL1[x][y] = info
   
def SetInfo2(x,y,info):
   info = str(info)
   if x < 0 : return
   if y < 0 : return
   if x >= LTBL : return
   if y >= LTBL : return
   TBL2[x][y] = info
   


##############################################################################
#
#   Partie II :  AFFICHAGE -- NE PAS MODIFIER  jusqu'à la prochaine section
#
##############################################################################

 

ZOOM = 40   # taille d'une case en pixels
EPAISS = 8  # epaisseur des murs bleus en pixels

screeenWidth = (LARGEUR+1) * ZOOM  
screenHeight = (HAUTEUR+2) * ZOOM

Window = tk.Tk()
Window.geometry(str(screeenWidth)+"x"+str(screenHeight))   # taille de la fenetre
Window.title("ESIEE - PACMAN")

# gestion de la pause

PAUSE_FLAG = False 

def keydown(e):
   global PAUSE_FLAG
   if e.char == ' ' : 
      PAUSE_FLAG = not PAUSE_FLAG 
 
Window.bind("<KeyPress>", keydown)
 

# création de la frame principale stockant plusieurs pages

F = tk.Frame(Window)
F.pack(side="top", fill="both", expand=True)
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)


# gestion des différentes pages

ListePages  = {}
PageActive = 0

def CreerUnePage(id):
    Frame = tk.Frame(F)
    ListePages[id] = Frame
    Frame.grid(row=0, column=0, sticky="nsew")
    return Frame

def AfficherPage(id):
    global PageActive
    PageActive = id
    ListePages[id].tkraise()
    
    
def WindowAnim():
    PlayOneTurn()
    Window.after(333,WindowAnim)
    
def AffichageScore():
   global ScorePlayer
   canvas.create_text(30, screenHeight- 20 , text = ScorePlayer, fill ="yellow", font = PoliceTexte)

Window.after(100,WindowAnim)

# Ressources

PoliceTexte = tkfont.Font(family='Arial', size=22, weight="bold", slant="italic")

# création de la zone de dessin

Frame1 = CreerUnePage(0)

canvas = tk.Canvas( Frame1, width = screeenWidth, height = screenHeight )
canvas.place(x=0,y=0)
canvas.configure(background='black')
 
 
#  FNT AFFICHAGE


def To(coord):
   return coord * ZOOM + ZOOM 
   
# dessine l'ensemble des éléments du jeu par dessus le décor

anim_bouche = 0
animPacman = [ 5,10,15,10,5]


def Affiche(PacmanColor,message):
   global anim_bouche
   
   def CreateCircle(x,y,r,coul):
      canvas.create_oval(x-r,y-r,x+r,y+r, fill=coul, width  = 0)
   
   canvas.delete("all")
      
      
   # murs
   
   for x in range(LARGEUR-1):
      for y in range(HAUTEUR):
         if ( TBL[x][y] == 1 and TBL[x+1][y] == 1 ):
            xx = To(x)
            xxx = To(x+1)
            yy = To(y)
            canvas.create_line(xx,yy,xxx,yy,width = EPAISS,fill="blue")

   for x in range(LARGEUR):
      for y in range(HAUTEUR-1):
         if ( TBL[x][y] == 1 and TBL[x][y+1] == 1 ):
            xx = To(x) 
            yy = To(y)
            yyy = To(y+1)
            canvas.create_line(xx,yy,xx,yyy,width = EPAISS,fill="blue")
            
   # pacgum
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( GUM[x][y] == 1):
            xx = To(x) 
            yy = To(y)
            e = 5
            canvas.create_oval(xx-e,yy-e,xx+e,yy+e,fill="orange")
         if ( GUM[x][y] == 2):
            xx = To(x) 
            yy = To(y)
            e = 10
            canvas.create_oval(xx-e,yy-e,xx+e,yy+e,fill="orange")
            
   #extra info
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         xx = To(x) 
         yy = To(y) - 11
         txt = TBL1[x][y]
         canvas.create_text(xx,yy, text = txt, fill ="white", font=("Purisa", 8)) 
         
   #extra info 2
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         xx = To(x) + 10
         yy = To(y) 
         txt = TBL2[x][y]
         canvas.create_text(xx,yy, text = txt, fill ="yellow", font=("Purisa", 8)) 
         
  
   # dessine pacman
   xx = To(PacManPos[0]) 
   yy = To(PacManPos[1])
   e = 20
   anim_bouche = (anim_bouche+1)%len(animPacman)
   ouv_bouche = animPacman[anim_bouche] 
   tour = 360 - 2 * ouv_bouche
   canvas.create_oval(xx-e,yy-e, xx+e,yy+e, fill = PacmanColor)
   canvas.create_polygon(xx,yy,xx+e,yy+ouv_bouche,xx+e,yy-ouv_bouche, fill="black")  # bouche
   
  
   #dessine les fantomes
   dec = -3
   for P in Ghosts:
      xx = To(P[0]) 
      yy = To(P[1])
      e = 16
      
      coul = P[2]
      # corps du fantome
      CreateCircle(dec+xx,dec+yy-e+6,e,coul)
      canvas.create_rectangle(dec+xx-e,dec+yy-e,dec+xx+e+1,dec+yy+e, fill=coul, width  = 0)
      
      # oeil gauche
      CreateCircle(dec+xx-7,dec+yy-8,5,"white")
      CreateCircle(dec+xx-7,dec+yy-8,3,"black")
       
      # oeil droit
      CreateCircle(dec+xx+7,dec+yy-8,5,"white")
      CreateCircle(dec+xx+7,dec+yy-8,3,"black")
      
      dec += 3
      
   # texte  
   
   canvas.create_text(screeenWidth // 2, screenHeight- 50 , text = "PAUSE : PRESS SPACE", fill ="yellow", font = PoliceTexte)
   canvas.create_text(screeenWidth // 2, screenHeight- 20 , text = message, fill ="yellow", font = PoliceTexte)
   
   # Affiche le score du Player à l'écran
   AffichageScore()
 
AfficherPage(0)
            
#########################################################################
#
#  Partie III :   Gestion de partie   -   placez votre code dans cette section
#
#########################################################################

      
def PacManPossibleMove(TBL_IA, TBL_Ghost_IA):
   L = ()
   x,y = PacManPos
   # Mode Normal
   if(not Super):
      max = -1000
      # Mode chasse aux pacgums
      # on cherche la case adjacente avec la plus courte distante vers la pacgum
      # et on la choisit comme solution
      if(TBL_Ghost_IA[x][y] > 3):
         min = TBL_IA[x][y-1]
         L = (0,-1)
         # if (min > TBL_IA[x  ][y-1]):
         #    min = TBL_IA[x][y-1]
         #    L = (0,-1)
         if (min > TBL_IA[x  ][y+1]):
            min = TBL_IA[x][y+1]
            L = (0, 1)
         if (min > TBL_IA[x+1][y  ] ):
            min = TBL_IA[x+1][y]
            L = (1,0)
         if (min > TBL_IA[x-1][y ]):
            min = TBL_IA[x-1][y]
            L = (-1,0)
      # Mode fuite (mode tapette en fait)
      if(TBL_Ghost_IA[x][y] <= 3):
         if max < TBL_Ghost_IA[x-1][y] and TBL_Ghost_IA[x-1][y] < 999 :
            max = TBL_Ghost_IA[x-1][y]
            L = (-1,0)
         if max < TBL_Ghost_IA[x+1][y] and TBL_Ghost_IA[x+1][y] < 999 :
            max = TBL_Ghost_IA[x+1][y]
            L = (1,0)
         if max < TBL_Ghost_IA[x][y-1] and TBL_Ghost_IA[x][y-1] < 999 :
            max = TBL_Ghost_IA[x][y-1]
            L = (0,-1)
         if max < TBL_Ghost_IA[x][y+1] and TBL_Ghost_IA[x][y+1] < 999 :
            max = TBL_Ghost_IA[x][y+1]
            L = (0,1)
   # Mode super = Chasse aux fantômes
   else:
      min = 1000
      if min > TBL_Ghost_IA[x-1][y] and TBL_IA[x-1][y] != 999:
         min = TBL_Ghost_IA[x-1][y]
         L = (-1,0)
      if min > TBL_Ghost_IA[x+1][y] and TBL_IA[x+1][y] != 999:
         min = TBL_Ghost_IA[x+1][y]
         L = (1,0)
      if min > TBL_Ghost_IA[x][y-1] and TBL_IA[x][y-1] != 999:
         min = TBL_Ghost_IA[x][y-1]
         L = (0,-1)
      if min > TBL_Ghost_IA[x][y+1] and TBL_IA[x][y+1] != 999:
         min = TBL_Ghost_IA[x][y+1]
         L = (0,1)

   return L
   
def GhostsPossibleMove(x,y,move):
   L = []
   # On vérifie si le ghost se trouve dans un couloir
   # couloir horizontal
   if (TBL[x][y+1] == 1 and TBL[x][y-1] == 1 and TBL[x+1][y] in [2,0] and TBL[x-1][y] in [2,0]):
      L.append(move)
   # couloir vertical
   elif (TBL[x-1][y] == 1 and TBL[x+1][y] == 1 and TBL[x][y-1] in [2,0] and TBL[x][y+1] in [2,0]):
      L.append(move)
   # tournant ou croisement
   else:
      # on vérifie si la case possible n'est pas un mur
      if ( TBL[x  ][y-1] in [2,0] ): L.append((0,-1))
      if ( TBL[x  ][y+1] in [2,0] ): L.append((0, 1))
      if ( TBL[x+1][y  ] in [2,0] ): L.append(( 1,0))
      if ( TBL[x-1][y  ] in [2,0] ): L.append((-1,0))

   return L
   
def IAPacman():
   global PacManPos, Ghosts
   
   # On initialise un tableau où toutes les cases du parcours sont initialisés à M.
   TBL_IA = CreateArray([
      [I,I,I,I,I,I,I,I,I,I,I,I,I,I,I,I,I,I,I,I],
      [I,M,M,M,M,I,M,M,M,M,M,M,M,M,I,M,M,M,M,I],
      [I,M,I,I,M,I,M,I,I,I,I,I,I,M,I,M,I,I,M,I],
      [I,M,I,M,M,M,M,M,M,M,M,M,M,M,M,M,M,I,M,I],
      [I,M,I,M,I,I,M,I,I,I,I,I,I,M,I,I,M,I,M,I],
      [I,M,M,M,M,M,M,I,I,I,I,I,I,M,M,M,M,M,M,I],
      [I,M,I,M,I,I,M,I,I,I,I,I,I,M,I,I,M,I,M,I],
      [I,M,I,M,M,M,M,M,M,M,M,M,M,M,M,M,M,I,M,I],
      [I,M,I,I,M,I,M,I,I,I,I,I,I,M,I,M,I,I,M,I],
      [I,M,M,M,M,I,M,M,M,M,M,M,M,M,I,M,M,M,M,I],
      [I,I,I,I,I,I,I,I,I,I,I,I,I,I,I,I,I,I,I,I]
   ]);
   # On remplace toutes les cases du parcours par des "0" si la case correspondante contient une pacgum
   TBL_IA = np.where(((GUM == 1) | (GUM == 2)), 0, TBL_IA)
   
   # On initialise un tableau où toutes les cases du parcours sont initialisés à M.
   TBL_Ghost_IA = CreateArray([
      [I,I,I,I,I,I,I,I,I,I,I,I,I,I,I,I,I,I,I,I],
      [I,M,M,M,M,I,M,M,M,M,M,M,M,M,I,M,M,M,M,I],
      [I,M,I,I,M,I,M,I,I,I,I,I,I,M,I,M,I,I,M,I],
      [I,M,I,M,M,M,M,M,M,M,M,M,M,M,M,M,M,I,M,I],
      [I,M,I,M,I,I,M,I,I,I,I,I,I,M,I,I,M,I,M,I],
      [I,M,M,M,M,M,M,I,I,I,I,I,I,M,M,M,M,M,M,I],
      [I,M,I,M,I,I,M,I,I,I,I,I,I,M,I,I,M,I,M,I],
      [I,M,I,M,M,M,M,M,M,M,M,M,M,M,M,M,M,I,M,I],
      [I,M,I,I,M,I,M,I,I,I,I,I,I,M,I,M,I,I,M,I],
      [I,M,M,M,M,I,M,M,M,M,M,M,M,M,I,M,M,M,M,I],
      [I,I,I,I,I,I,I,I,I,I,I,I,I,I,I,I,I,I,I,I]
   ]);
   # On créé un tableau similaire à GUM où chaque case égale à 1 contient un fantôme
   GHOST = np.zeros(TBL.shape,dtype=np.int64)
   # On met à jour le tableau à chaque tour
   for F in Ghosts:
      GHOST[F[0]][F[1]] = 1
   # On remplace toutes les cases du parcours par des "0" si la case correspondante contient une pacgum
   # On ne prend pas en compte les Ghosts présents dans la base
   TBL_Ghost_IA = np.where((GHOST == 1) & (TBL == 0), 0, TBL_Ghost_IA)
   
   # Carte des distance fantômes 
   # On initialise à True au début pour commencer la boucle
   updated = True
   while(updated):
      # On remet à false, comme ça il repasse à true uniquement si mise à jour il y a
      updated = False
      # On parcourt chaque case du tableau, dénué de ses murs
      for j in range(1,HAUTEUR-1):
         for i in range(1,LARGEUR-1):
            # On stocke les valeurs de la case et de ses cases adjacentes
            case = TBL_Ghost_IA[i][j]
            case_haut = TBL_Ghost_IA[i][j + 1]
            case_bas = TBL_Ghost_IA[i][j - 1]
            case_gauche = TBL_Ghost_IA[i - 1][j]
            case_droite = TBL_Ghost_IA[i + 1][j]
            # On mémorise le minimum des trois et on lui ajoute un
            # on obtient la longueur du meilleur chemin possible en empruntant une de ces 4 cases
            min_case = min(case_haut, case_bas,  case_gauche, case_droite) + 1
            # # Si la valeur calculée est meilleure que la valeur de la case courante
            # # on la met à jour
            if(min_case < TBL_Ghost_IA[i][j] and case < 1000): 
               TBL_Ghost_IA[i][j] = min_case
               # Si mise à jour il y a, on passe updated à True
               updated = True
   # Affiche la carte des distances des fantômes
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         info = TBL_Ghost_IA[x][y]
         if info >= 1000 : info = ""
         SetInfo2(x,y,info)

   PacManEatingGum()
   
   # Carte des distances PacGum
   # On initialise à True au début pour commencer la boucle
   updated = True
   while(updated):
      # On remet à false, comme ça il repasse à true uniquement si mise à jour il y a
      updated = False
      # On parcourt chaque case du tableau, dénué de ses murs
      for j in range(1,HAUTEUR-1):
         for i in range(1,LARGEUR-1):
            # On stocke les valeurs de la case et de ses cases adjacentes
            case = TBL_IA[i][j]
            case_haut = TBL_IA[i][j + 1]
            case_bas = TBL_IA[i][j - 1]
            case_gauche = TBL_IA[i - 1][j]
            case_droite = TBL_IA[i + 1][j]
            # On mémorise le minimum des trois et on lui ajoute un
            # on obtient la longueur du meilleur chemin possible en empruntant une de ces 4 cases
            min_case = min(case_haut, case_bas,  case_gauche, case_droite) + 1
            # # Si la valeur calculée est meilleure que la valeur de la case courante
            # # on la met à jour
            if(min_case < TBL_IA[i][j] and case < 1000): 
               TBL_IA[i][j] = min_case
               # Si mise à jour il y a, on passe updated à True
               updated = True
               
   # Affiche la carte de distances des PacGums
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         info = TBL_IA[x][y]
         if info >= 1000 : info = "+∞"
         SetInfo1(x,y,info)
   
   # Super Mode
   global Super, SuperCount
   # Décompte tours Super
   if(Super):
      SuperCount -= 1
      print(SuperCount)
      
   # Reset compteur Super
   if(SuperCount == 0):
      Super = False
      SuperCount = 16
         
   global GameState, GameStateMsg, ScorePlayer
   for F in Ghosts:
      if (F[0] == PacManPos[0] and F[1] == PacManPos[1]):
         if (not Super):
            GameState = 1
            GameStateMsg = "Perdu"
         else:
            ScorePlayer += 2000
            F[0] = LARGEUR//2
            F[1] = HAUTEUR//2
            
   if np.all(GUM == 0):
      GameState = 2
      GameStateMsg = "Gagné"
      
   #deplacement Pacman
   L = PacManPossibleMove(TBL_IA, TBL_Ghost_IA)
   PacManPos[0] += L[0]
   PacManPos[1] += L[1]

   
def IAGhosts():
   global PacManPos
   #deplacement Fantome
   for F in Ghosts:
      global GameState, GameStateMsg, Super, ScorePlayer
      if (F[0] == PacManPos[0] and F[1] == PacManPos[1]):
         if (not Super):
            GameState = 1
            GameStateMsg = "Perdu"
         else:
            ScorePlayer += 2000
            F[0] = LARGEUR//2
            F[1] = HAUTEUR//2
      L = GhostsPossibleMove(F[0],F[1],F[3])
      choix = random.randrange(len(L))
      # on associe le fantôme à sa direction courante
      F[3] = (L[choix][0],L[choix][1])
      F[0] += L[choix][0]
      F[1] += L[choix][1]
         

      
      
def PacManEatingGum():
   global ScorePlayer, Super
   if( IsGum() == True):
      # Si la gomme est mangée, on passe la position dans le tableau GUM à 0 car la gomme n'est plus là
      GUM[PacManPos[0]][PacManPos[1]] = 0
      ScorePlayer += 100
      
   if(IsSuperGum()):
      GUM[PacManPos[0]][PacManPos[1]] = 0
      Super = True
      ScorePlayer += 100
 

 
#  Boucle principale de votre jeu appelée toutes les 500ms

iteration = 0
def PlayOneTurn():
   global iteration, Super,GameStateMsg
   
   if (not PAUSE_FLAG) and GameState == 0: 
      iteration += 1
      if iteration % 2 == 0 :   IAPacman()
      else:                     IAGhosts()
      
      # Affiche en bleu si en mode super, en jaune sinon
      if (Super):
         Affiche(PacmanColor = "blue", message = GameStateMsg)  
      else:
         Affiche(PacmanColor = "yellow", message = GameStateMsg)  
 
 
###########################################:
#  demarrage de la fenetre - ne pas toucher

Window.mainloop()

 
   
   
    
   
   