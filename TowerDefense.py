import pygame
import math
import os
import sys
from collections import deque

pygame.init()


# JUKEBOX (POO + FILE)


class Jukebox:
    def __init__(self, musiques):
        self.file_musiques = musiques[:]
        pygame.mixer.init()
        self.volume = 0.4
        self.jouer_musique()

    def jouer_musique(self):
        if self.file_musiques:
            pygame.mixer.music.load(self.file_musiques[0])
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play()

    def musique_suivante(self):
        musique = self.file_musiques.pop(0)
        self.file_musiques.append(musique)
        self.jouer_musique()

    def musique_en_cours(self):
        return os.path.basename(self.file_musiques[0])


#MUSIQUES


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MUSIQUES = [
    os.path.join(BASE_DIR, "welivewelove.mp3"),
    os.path.join(BASE_DIR, "nevergonnagiveyouup.mp3"),
    os.path.join(BASE_DIR, "outro.mp3"),
    os.path.join(BASE_DIR, "megalovania.mp3")
]

jukebox = Jukebox(MUSIQUES)

#  CONSTANTES 

LARGEUR = 1200
HAUTEUR = 800
HAUTEUR_INFO = 120
TAILLE_CASE = 50
MAX_TOURS = 3
VAGUES_MAX = 5
ENNEMIS_PAR_VAGUE = 8

COLONNES = LARGEUR // TAILLE_CASE
LIGNES = (HAUTEUR - HAUTEUR_INFO) // TAILLE_CASE


#  fenetre 


ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Tower Defense - Jukebox")

horloge = pygame.time.Clock()
police = pygame.font.SysFont(None, 28)

#Ecran instructions
def ecran_instructions():
    bouton_ok = pygame.Rect(LARGEUR//2 - 100, HAUTEUR - 150, 200, 60)
    attente = True

    while attente:
        ecran.fill((20, 20, 20))

        titre = pygame.font.SysFont(None, 48).render("COMMANDES DU JEU", True, (255,255,255))
        ecran.blit(titre, titre.get_rect(center=(LARGEUR//2, 80)))

        instructions = [
            "Clic gauche : placer une tour",
            "Maximum 3 tours (la plus ancienne disparaît)",
            "Bouton 'Lancer la vague' : démarrer une vague",
            "ESPACE : changer la musique",
            "ECHAP : quitter le jeu",
            "Empêche les ennemis d'atteindre la base !"
        ]

        y = 160
        for txt in instructions:
            ligne = police.render(txt, True, (200,200,200))
            ecran.blit(ligne, (LARGEUR//2 - 250, y))
            y += 40

        pygame.draw.rect(ecran, (80,80,80), bouton_ok)
        ok_txt = police.render("OK", True, (255,255,255))
        ecran.blit(ok_txt, ok_txt.get_rect(center=bouton_ok.center))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_ok.collidepoint(event.pos):
                    attente = False

        pygame.display.flip()
        horloge.tick(60)
def ecran_fin(message):
    bouton_ok = pygame.Rect(LARGEUR//2 - 100, HAUTEUR - 150, 200, 60)
    attente = True

    while attente:
        ecran.fill((20, 20, 20))

        titre = pygame.font.SysFont(None, 64).render(message, True, (255,255,255))
        ecran.blit(titre, titre.get_rect(center=(LARGEUR//2, HAUTEUR//2 - 50)))

        pygame.draw.rect(ecran, (80,80,80), bouton_ok)
        ok_txt = police.render("OK", True, (255,255,255))
        ecran.blit(ok_txt, ok_txt.get_rect(center=bouton_ok.center))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_ok.collidepoint(event.pos):
                    attente = False

        pygame.display.flip()
        horloge.tick(60)



#  CHEMINS  

chemins = [
    [(0,1),(3,1),(6,2),(9,2),(12,3),(15,3),(18,4),(19,5),(18,6),(15,6),(12,7),(9,7),(6,6),(3,6),(0,5)],
    [(0,6),(3,6),(6,7),(9,6),(12,5),(15,5),(18,6),(19,7),(18,8),(15,7),(12,6),(9,5),(6,4),(3,3),(0,3)],
    [(0,3),(3,3),(6,4),(9,5),(12,6),(15,7),(18,8),(19,6),(18,4),(15,3),(12,2),(9,1),(6,2),(3,2),(0,2)],
    [(0,2),(3,2),(6,3),(9,4),(12,5),(15,6),(18,7),(19,5),(18,3),(15,2),(12,1),(9,0),(6,1),(3,1),(0,1)],
    [(0,4),(3,4),(6,5),(9,6),(12,7),(15,6),(18,5),(19,6),(18,7),(15,7),(12,6),(9,5),(6,4),(3,3),(0,4)]
]

#  CLASSES 

class Base:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vie_max = 5
        self.vie = self.vie_max

    def dessiner(self):
        pygame.draw.rect(ecran, (255,255,0), (self.x, self.y, TAILLE_CASE, TAILLE_CASE))
        txt = police.render(str(self.vie), True, (0,0,0))
        ecran.blit(txt, txt.get_rect(center=(self.x+TAILLE_CASE//2, self.y+TAILLE_CASE//2)))

    def subir_degats(self):
        self.vie -= 1
        return self.vie <= 0
 
class Ennemi:
    def __init__(self, chemin, vitesse):
        self.chemin = chemin
        self.indice = 1
        self.x = chemin[0][0]*TAILLE_CASE + TAILLE_CASE//2
        self.y = chemin[0][1]*TAILLE_CASE + TAILLE_CASE//2 + HAUTEUR_INFO
        self.vitesse = vitesse
        self.vie = 40 * vitesse


    def avancer(self):
        if self.indice >= len(self.chemin):
            return
        cx = self.chemin[self.indice][0]*TAILLE_CASE + TAILLE_CASE//2
        cy = self.chemin[self.indice][1]*TAILLE_CASE + TAILLE_CASE//2 + HAUTEUR_INFO
        dx, dy = cx - self.x, cy - self.y
        dist = math.hypot(dx, dy)
        if dist < self.vitesse:
            self.x, self.y = cx, cy
            self.indice += 1
        else:
            self.x += self.vitesse*dx/dist
            self.y += self.vitesse*dy/dist

    def subir_degats(self, d):
        self.vie -= d

    def est_mort(self):
        return self.vie <= 0

    def dessiner(self):
        pygame.draw.rect(ecran, (255,0,0), (self.x-10, self.y-10, 20, 20))

class Tour:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.portee = 120
        self.degats = 25
        self.cadence = 50
        self.timer = 0

    def attaquer(self, ennemis):
        if self.timer > 0:
            self.timer -= 1
            return
        for e in ennemis:
            if math.hypot(e.x-(self.x+TAILLE_CASE//2), e.y-(self.y+TAILLE_CASE//2)) <= self.portee:
                e.subir_degats(self.degats)
                self.timer = self.cadence
                break

    def dessiner(self):
        pygame.draw.rect(ecran, (0,0,255), (self.x, self.y, TAILLE_CASE, TAILLE_CASE))
        pygame.draw.circle(ecran, (150,150,255), (self.x+TAILLE_CASE//2, self.y+TAILLE_CASE//2), self.portee, 1)


#  VARIABLES JEU 


vague = 0
vague_en_cours = False
ennemis = []
file_spawn = 0
timer_spawn = 0

tours = deque()  

chemin = chemins[0]
fin = chemin[-1]
base = Base(fin[0]*TAILLE_CASE, fin[1]*TAILLE_CASE+HAUTEUR_INFO)

btn_lancer = pygame.Rect(50, 20, 250, 50)
btn_quitter = pygame.Rect(LARGEUR-250-50, 20, 250, 50)


#  BOUCLE PRINCIPALE 

ecran_instructions()

jeu = True

while jeu:
    horloge.tick(60)
    ecran.fill((30,30,30))

    # Zone info
    pygame.draw.rect(ecran, (50,50,50), (0,0,LARGEUR,HAUTEUR_INFO))
    ecran.blit(police.render(f"Vague : {vague}/{VAGUES_MAX}", True, (255,255,255)), (350,40))
    ecran.blit(police.render(f"Vies : {base.vie}", True, (255,255,0)), (500,40))
    ecran.blit(police.render(f"Musique : {jukebox.musique_en_cours()}", True, (255,255,255)), (50,80))

    # Boutons
    pygame.draw.rect(ecran, (80,80,80), btn_lancer)
    pygame.draw.rect(ecran, (80,80,80), btn_quitter)
    ecran.blit(police.render("Lancer la vague", True, (255,255,255)), (btn_lancer.x + 20, btn_lancer.y + 10))
    ecran.blit(police.render("Quitter", True, (255,255,255)), (btn_quitter.x + 50, btn_quitter.y + 10))

    # Grille
    for x in range(0, LARGEUR, TAILLE_CASE):
        pygame.draw.line(ecran, (60,60,60), (x, HAUTEUR_INFO), (x, HAUTEUR))
    for y in range(HAUTEUR_INFO, HAUTEUR, TAILLE_CASE):
        pygame.draw.line(ecran, (60,60,60), (0, y), (LARGEUR, y))

    # Chemin
    for p in chemin:
        pygame.draw.circle(ecran, (255,255,0), (p[0]*TAILLE_CASE+TAILLE_CASE//2, p[1]*TAILLE_CASE+TAILLE_CASE//2+HAUTEUR_INFO), 8)

    base.dessiner()

    # evenemeny
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jeu = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                jeu = False
            if event.key == pygame.K_SPACE:
                jukebox.musique_suivante()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if btn_lancer.collidepoint((mx,my)) and not vague_en_cours and vague < VAGUES_MAX:
                vague += 1
                vague_en_cours = True
                chemin = chemins[vague-1]
                fin = chemin[-1]
                base = Base(fin[0]*TAILLE_CASE, fin[1]*TAILLE_CASE+HAUTEUR_INFO)
                file_spawn = ENNEMIS_PAR_VAGUE
                timer_spawn = 0

            elif btn_quitter.collidepoint((mx,my)):
                jeu = False
            elif my >= HAUTEUR_INFO:
                case_x = (mx // TAILLE_CASE) * TAILLE_CASE
                case_y = ((my - HAUTEUR_INFO) // TAILLE_CASE) * TAILLE_CASE + HAUTEUR_INFO
                if len(tours) >= MAX_TOURS:
                    tours.popleft()  # retire la première tour
                tours.append(Tour(case_x, case_y))  # ajoute la nouvelle tour

    # Dessin ennemis
    if vague_en_cours and file_spawn > 0:
        timer_spawn += 1
        if timer_spawn >= 40:
            ennemis.append(Ennemi(chemin, 2+vague))
            file_spawn -= 1
            timer_spawn = 0

    for e in ennemis[:]:
        e.avancer()
        e.dessiner()

        if e.est_mort():
            ennemis.remove(e)
            continue

        if e.indice >= len(chemin):
            ennemis.remove(e)
            if base.subir_degats():
                ecran_fin("PERDU")
                pygame.quit()
                sys.exit()



    # Dessin tours
    for t in tours:
        t.attaquer(ennemis)
        t.dessiner()

    #vague est terminée
    if vague_en_cours and not ennemis and file_spawn == 0:
        vague_en_cours = False
        if vague >= VAGUES_MAX:
            ecran_fin("GAGNÉ")
            pygame.quit()
            sys.exit()


    pygame.display.flip()

pygame.mixer.music.stop()
pygame.quit()
sys.exit()
