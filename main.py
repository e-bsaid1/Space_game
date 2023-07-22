import pygame # Importation des librairies
from random import randint, choice # Importation des méthodes randint et choice :
                                   # randint() : crée des ombres aléatoires
                                   # choice () : crée des apparitions alétoires à partir d'une liste en fonction du nombre
                                   # de fois où un élément est mentionné : plus il est mentionné, plus il a de chances
                                   # d'apparaitre
from sys import exit

class Joueur(pygame.sprite.Sprite):
    """Classe définissant le comportement général du joueur"""
    def __init__(self):
        super().__init__()
        # Attribut de l'image du joueur
        self.image = pygame.image.load('Image/Fusee/Fusee_deplacement.png').convert_alpha()
        # Attribut du rectangle du joueur
        self.rect = self.image.get_rect(midbottom = (70, 240))
        # Attribut du masque permettant les collisions de pixel à pixel
        self.mask = pygame.mask.from_surface(self.image)

    def joueur_controles(self):
        """Contrôle le joueur"""
        # Affectation des contrôles du joueur à la variable controles
        controles = pygame.key.get_pressed()
        # Si le joueur est dans l'écran et qu'on appuie sur bas, descendre :
        if controles[pygame.K_DOWN] and self.rect.bottom <= hauteur:
            self.rect.y += 6
        # Si le joueur est dans l'écran et qu'on appuie sur haut, monter
        if controles[pygame.K_UP] and self.rect.top >= 0:
            self.rect.y -= 6

    def reset_position(self):
        """Réinitialise les positions x et y du joueur en cas de game over"""
        self.rect.x = 50
        self.rect.y = 240

    def update(self):
        self.joueur_controles()

class Obstacles(pygame.sprite.Sprite):
    """Classe définissant le comportement général des ennemis"""
    def __init__(self, type):
        super().__init__()

        # Si le type est un asteroide, créer des images des asteroides et les mettre dans l'attribut ennemi
        if type == 'Grand_asteroide':
            grand_asteroide = pygame.image.load('Image/Obstacles/Asteroides/Grand_asteroide.png').convert_alpha()
            position_y = randint(100, 480)
            self.ennemi = grand_asteroide
        if type == 'Moyen_asteroide':
            moyen_asteroide = pygame.image.load('Image/Obstacles/Asteroides/Moyen_asteroide.png').convert_alpha()
            position_y = randint(100,480)
            self.ennemi = moyen_asteroide
        if type == 'Petit_asteroide':
            petit_asteroide = pygame.image.load('Image/Obstacles/Asteroides/Petit_asteroide.png').convert_alpha()
            position_y = randint(100,480)
            self.ennemi = petit_asteroide

        # Attribut de l'image des astéroides
        self.image = self.ennemi
        # Attribut du rectangle des astéroides
        self.rect = self.image.get_rect(midbottom = (670,position_y))
        # Attribut de la vitesse de déplacement de l'asteroide à gauche
        self.gauche = 4.0
        # Attribut du masque permettant les collisions de pixel à pixel
        self.mask = pygame.mask.from_surface(self.image)
        # Attribut de la position x-y des asteroides
        self.position_y = position_y


    def asteroides_deplacements(self):
        """Définit les déplacements de l'obstacle"""
        self.rect.x -= self.gauche
        # Pour chaque image dans
        # Si le rectangle atteint l'extérieur de l'écran, rembobiner :
        if self.rect.x < -140:
            self.kill()

    def reset_position(self):
        """Réinitialise les positions x et y des obstacles"""
        self.rect.x = 670
        self.rect.y = self.position_y

    def update(self):
        """Met à jour toutes les méthodes précédentes"""
        self.asteroides_deplacements()

def collision_sprite():
    """Fonction pour détecter les collisions entre joueur/obstacle"""
    if pygame.sprite.spritecollide(joueur_groupe_sprite.sprite,asteroide_groupe_sprite,False,pygame.sprite.collide_mask):
        # Arrêter le jeu
        return False
    else : return True

def game_over():
    """Fonction pour afficher l'écran de game over en cas de collision"""
    # Affectation de la police de game over (taille et type de police)
    perdu_police = pygame.font.Font('Image/Etat_jeu/QuinqueFive.ttf', 15)
    # Affectation de la surface
    perdu_surface = perdu_police.render('Game Over', False, 'White')
    commande_perdu_surface = perdu_police.render('Appuie sur Echap', False, 'White')

    # S'il y a collision, afficher game_over et offrir la possibilité d'un game over
    if pygame.sprite.spritecollide(joueur_groupe_sprite.sprite,asteroide_groupe_sprite,False,pygame.sprite.collide_mask):
        fenetre.blit(perdu_surface,(220,200))
        fenetre.blit(commande_perdu_surface,(220,230))
        pygame.draw.rect(fenetre, 'Red',(215,200,310,60),2)
        # Si le joueur appuie sur Echap, le remettre à sa position d'origine
        joueur_groupe_sprite.sprite.reset_position()
        asteroide_groupe_sprite.empty()

def score_affichage(score):
    """Fonction affichant le score qui s'incrémente aux secondes depuis le début du jeu"""
    # Affectation de la police de score (taille et type de police)
    score_police = pygame.font.Font('Image/Etat_jeu/QuinqueFive.ttf', 15)
    # Affectation de la surface
    score_surface = score_police.render(f"Score : {score}", False, 'White')
    fenetre.blit(score_surface, (320, 20))

# Initialisation du programme pygame. A mettre avant toute chose.
pygame.init()

# Initialisation des dimensions de la fenêtre
hauteur = 480
longueur = 640

# Création de la fenêtre suivie du nom
fenetre = pygame.display.set_mode((longueur, hauteur))
pygame.display.set_caption('Space Game')

# Affectation de la fonction clock pour faire tourner le jeu optimalement
horloge = pygame.time.Clock()

# Initialisation de l'état du jeu
JeuActif = True

# Affectation d'une fonction pour afficher l'arrière-plan (espace et terre)
espace_surface = pygame.image.load('Image/Decor/Espace.png')
Terre_Surface = pygame.image.load('Image/Decor/Terre.png')

# Création du GroupeSingle
joueur_groupe_sprite = pygame.sprite.GroupSingle()
# Création de l'instance du sprite Joueur
joueur_sprite = Joueur()
# Ajout du sprite au groupe
joueur_groupe_sprite.add(joueur_sprite)

# Instanciation d'une classe à la variable asteroide
asteroide_groupe_sprite = pygame.sprite.Group()
# Affectation de la police de pause (taille et type de police)
pause_police = pygame.font.Font('Image/Etat_jeu/QuinqueFive.ttf', 15)
# Affectation de la surface (couleur et nom)
pause_surface = pause_police.render('Pause', False, 'White')


# Affectation d'un evenement utilisateur customisable qui s'enclenche en certains intervalles à la variable
# CompteurObstacle
CompteurObstacle = pygame.USEREVENT + 1
# Appel de la fonction pygame.time.set_timer() qui s'enclenche toutes les 4 secondes
pygame.time.set_timer(CompteurObstacle, 700)

# Score
seconde = 0


# Tant que la condition est vraie
while True:
    # Pour chaque évènement dans ceux de pygame
    for evenement in pygame.event.get():
        # Si le type d'évènement est pygame.quit (=appui sur la bouton arrêt), arrêter le jeu
        if evenement.type == pygame.QUIT:
            pygame.quit()
            exit()
        if JeuActif:
            # Si l'on presse la touche Echap, mettre le jeu en pause
            if evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_ESCAPE:
                    fenetre.blit(pause_surface,(280,200))
                    JeuActif = False
            # Si on appuie sur la touche entrée et que le jeu est actif, arrêter le jeu. Si on y appuie, le relancer
            # Si le jeu est actif (pas de collision ou de fermeture de fenêtres), ajouter les asteroides aléatoirement
            # en fonction du nombre de fois où le type d'asteroide est mentionné dans la méthode add.()
            if evenement.type == CompteurObstacle and JeuActif:
                asteroide_groupe_sprite.add(Obstacles(choice(['Grand_asteroide','Moyen_asteroide','Moyen_asteroide','Moyen_asteroide','Petit_asteroide'])))
        # Si le jeu n'est pas actif à cause de la pause, appuyer sur la touche Echap
        else:
            if evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_ESCAPE:
                    JeuActif = True

    if JeuActif:
        seconde = seconde + 1
        # Afficher l'arrière_plan à partir de la position X-Y
        fenetre.blit(espace_surface,(0,0))
        fenetre.blit(Terre_Surface,(510,20))
        # Afficher et mettre à jour le joueur
        joueur_groupe_sprite.draw(fenetre)
        joueur_groupe_sprite.update()
        # Afficher et mettre à jour le petit asteroid
        asteroide_groupe_sprite.draw(fenetre)
        asteroide_groupe_sprite.update()
        # Collision
        JeuActif = collision_sprite()
        game_over()
        # Score
        score_affichage(seconde)
    else:
        seconde = 0

    # Afficher tous les éléments
    pygame.display.update()
    # Appel de la fonction clock
    horloge.tick(60)



