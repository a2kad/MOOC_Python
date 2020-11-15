'''
Projet château
--------------
Auteur: RESHETNIKOFF Ruslan
Date: 14 novembre 2020
Ce projet permet de réaliser un petit jeu d’évasion dans un château-labyrinthe.
Le but (du jeu) consiste à l’aide du clavier à déplacer un personnage dans un dédale de couloirs et de pièces jusqu’à la
sortie. Des portes devront être déverrouillées en répondant à des questions et des indices, disséminés dans le château,
aideront le héros dans sa progression.
'''
from CONFIGS import * #Importer le fichier de configuration
import turtle #Importer la tortue

position_global = POSITION_DEPART #Variable globale. L'emplacement du personnage. Le point de départ est indiqué ici.
position_txt = POINT_AFFICHAGE_INVENTAIRE[1]

turtle.hideturtle() # Cacher une tortue
turtle.speed(0) # Vitesse de la tortue

def lire_matrice(fichier):
    '''
    Une fonction recevra en argument le nom d’un fichier texte contenant le plan à tracer.
    Elle ouvrira ce fichier et renverra en sortie une matrice.
    '''
    matrix = []
    with open(fichier) as lm:
        for i in range (NOMBRE_DE_LIGNES):
            srtok = lm.readline()
            srtok = srtok.strip('\n')
            lst = srtok.split(' ')
            matrix.append(lst)
        return matrix

def calculer_pas(matrice):
    '''
    La fonction, qui calcule la dimension à donner aux cases pour que le plan tienne dans la zone de la fenêtre turtle.
    '''
    WTH = abs(ZONE_PLAN_MINI[0] - ZONE_PLAN_MAXI[0])
    HTH = abs(ZONE_PLAN_MINI[1] - ZONE_PLAN_MAXI[1])
    hth = len(matrice)
    wth = len(matrice[0])
    h = HTH/hth
    w = WTH/wth
    if h < w:
        return h
    else:
        return w

matrice_global = lire_matrice(fichier_plan) # Variable globale qui stocke la matrice du plan du château
square_size = calculer_pas(matrice_global) # Longueur du côté carré
personage_radius = square_size/2 # Rayon de personage


def coordonnees(case, pas):
    '''
    La fonction, qui calcule les coordonnées en pixels turtle du coin inférieur gauche d’une case définie par ses
    coordonnées (numéros de ligne et de colonne).
    '''
    y = ZONE_PLAN_MAXI[1]
    x = ZONE_PLAN_MINI[1]
    if case == 0:
        y = y
    else:
        for i in range(case):
            y = y - square_size
    if pas == 0:
        x = x
    else:
        for j in  range(pas):
            x = x + square_size
    coordinat =(x,y)
    return coordinat

def tracer_carre(dimension):
    '''
    Traçant un carré dont la dimension en pixels turtle est donnée en argument.
    '''
    for i in range(4):
        turtle.forward(dimension)
        turtle.left(90)

def tracer_case(case, couleur, pas):
    '''
    La fonction recevant en arguments un couple de coordonnées en indice dans la matrice contenant le plan, une couleur,
    et un pas (taille d'un côté) et qui va appeler la fonction tracer_carre pour tracer un carré d’une certaine couleur
    et taille à un certain endroit.
    '''
    x = case[0]
    y = case[1]
    crd = coordonnees(x,y)
    turtle.color('white')
    turtle.penup()
    turtle.goto(crd[0], crd[1])
    turtle.pensize(pas)
    turtle.pendown()
    turtle.fillcolor(couleur)
    turtle.begin_fill()
    tracer_carre(square_size)
    turtle.end_fill()
    turtle.penup()


def afficher_plan(matrice):
    '''
    La fonction, qui va appeler la fonction tracer_case pour chaque ligne et chaque colonne du plan, par deux boucles
    imbriquées.
    Pour chaque élément ligne de la matrice, pour chaque élément colonne de cet élément ligne, tracer une case à
    l’emplacement correspondant, dans une couleur correspondant à ce que dit la matrice.
    '''
    for ligne in range(len(matrice)):
        for colonne in range(len(matrice[0])):
            coor = (ligne,colonne)
            numbre_color = int(matrice[ligne][colonne])
            color = COULEUR_CASES
            if numbre_color == 0:
                color = COULEUR_COULOIR
            elif numbre_color == 1:
                color = COULEUR_MUR
            elif numbre_color == 2:
                color = COULEUR_OBJECTIF
            elif numbre_color == 3:
                color = COULEUR_PORTE
            elif numbre_color == 4:
                color = COULEUR_OBJET
            tracer_case(coor,color,1)

def deplacer_gauche():
    '''
    Déclenchent par la flèche sur le clavier: à gauche.
    '''
    turtle.onkeypress(None, "Left")
    gauche_x = position_global[0]
    gauche_y = position_global[1]
    new_gauche_x = gauche_x
    new_gauche_y = gauche_y - 1
    deplacer(matrice_global, (gauche_x, gauche_y), (new_gauche_x, new_gauche_y))
    turtle.onkeypress(deplacer_gauche, "Left")

def deplacer_droite():
    '''
    Déclenchent par la flèche sur le clavier: à droite.
    '''
    turtle.onkeypress(None, "Right")  # Désactive la touche Left
    droite_x = position_global[0]
    droite_y = position_global[1]
    new_droite_x = droite_x
    new_droite_y = droite_y + 1
    deplacer(matrice_global, (droite_x, droite_y), (new_droite_x, new_droite_y))
    turtle.onkeypress(deplacer_droite, "Right")

def deplacer_haut():
    '''
    Déclenchent par la flèche sur le clavier: haut.
    '''
    turtle.onkeypress(None, "Up")  # Désactive la touche Left
    haut_x = position_global[0]
    haut_y = position_global[1]
    new_haut_x = haut_x - 1
    new_haut_y = haut_y
    deplacer(matrice_global, (haut_x, haut_y), (new_haut_x, new_haut_y))
    turtle.onkeypress(deplacer_haut, "Up")

def deplacer_bas():
    '''
    Déclenchent par la flèche sur le clavier: vers le bas.
    '''
    turtle.onkeypress(None, "Down")  # Désactive la touche Left
    bas_x = position_global[0]
    bas_y = position_global[1]
    new_bas_x = bas_x + 1
    new_bas_y = bas_y
    deplacer(matrice_global, (bas_x,bas_y), (new_bas_x, new_bas_y))
    turtle.onkeypress(deplacer_bas, "Down")

def mouvement_de_personnage(old_x, old_y, new_x, new_y, old_personage_radius_x, old_personage_radius_y,
                            new_personage_radius_x, new_personage_radius_y):
        turtle.penup()
        turtle.goto(old_personage_radius_x, old_personage_radius_y)
        turtle.pendown()
        tracer_case((old_x, old_y), COULEUR_VUE, 1)
        tracer_case((new_x, new_y), COULEUR_VUE, 1)
        turtle.penup()
        turtle.goto(new_personage_radius_x, new_personage_radius_y)
        turtle.pendown()
        turtle.dot(square_size, COULEUR_PERSONNAGE)
        turtle.penup()

def deplacer(matrice, position, mouvement):
    '''
    La fonction de déplacement du personnage.
    '''
    # ------Calcul des coordonnées-----
    global position_global
    global matrice_global
    old_x = position[0]
    old_y = position[1]
    new_x = mouvement[0]
    new_y = mouvement[1]
    old_dot_coordonnees = coordonnees(old_x, old_y)
    old_personage_radius_x = old_dot_coordonnees[0] + personage_radius
    old_personage_radius_y = old_dot_coordonnees[1] + personage_radius
    new_dot_coordonnees = coordonnees(new_x, new_y)
    new_personage_radius_x = new_dot_coordonnees[0] + personage_radius
    new_personage_radius_y = new_dot_coordonnees[1] + personage_radius
    # ---------------------------
    if new_x<0 or new_x >= len(matrice):
        print('Stop - end of the map')
    elif int(matrice[new_x][new_y]) == 1:
        print('Stop - gris')
    elif int(matrice[new_x][new_y]) == 2:
        mouvement_de_personnage(old_x, old_y, new_x, new_y, old_personage_radius_x, old_personage_radius_y,
                                new_personage_radius_x, new_personage_radius_y)
        clear_banner()
        banniere('Gagné!')
    elif int(matrice[new_x][new_y]) == 3:
        poser_question(matrice, (old_x, old_y), (new_x, new_y))
    elif int(matrice[new_x][new_y]) == 4:
        mouvement_de_personnage(old_x, old_y, new_x, new_y, old_personage_radius_x, old_personage_radius_y,
                                new_personage_radius_x, new_personage_radius_y)
        position_global = (new_x, new_y)
        matrice_global[new_x][new_y] = str(0)
        ramasser_objet((new_x,new_y))
    else:
        mouvement_de_personnage(old_x, old_y, new_x, new_y, old_personage_radius_x, old_personage_radius_y,
                                new_personage_radius_x, new_personage_radius_y)
        position_global = (new_x, new_y)

# Déterminez combien de trois (questions) sur le plan.
trois = 0
for q1 in range(len(matrice_global)):
    for q2 in range(len(matrice_global[0])):
        if int(matrice_global[q1][q2]) == 3:
            trois += 1
def creer_dictionnaire_des_questions(fichier_questions):
    '''
    Créant un dictionnaire de questions à partir du fichier fichier_questions
     '''
    dict_quest = {}
    with open(fichier_questions) as des_quest:
        for i in range(trois):
            line_quest = des_quest.readline()
            val, key = eval(line_quest)
            dict_quest.setdefault(val,key)
        return dict_quest

# Déterminez combien de quatr (objets) sur le plan
quatr = 0
for t1 in range(len(matrice_global)):
    for t2 in range(len(matrice_global[0])):
        if int(matrice_global[t1][t2]) == 4:
            quatr += 1

def creer_dictionnaire_des_objets(fichier_des_objets):
    '''
    Créant un dictionnaire d’objets à partir du fichier fichier_des_objets.
    '''
    dict_obj = {}
    with open(fichier_des_objets) as des_obj:
        for i in range(quatr):
            line_obect = des_obj.readline()
            val, key = eval(line_obect)
            dict_obj.setdefault(val,key)
        return dict_obj

def clear_banner():
    '''
    Efface la bannière: dessine un rectangle blanc.
    '''
    turtle.goto(-240, 260)
    turtle.pendown()
    turtle.pencolor('white')
    turtle.fillcolor('white')
    turtle.begin_fill()
    for i in range(2):
        turtle.speed(9)
        turtle.forward(480)
        turtle.left(90)
        turtle.forward(60)
        turtle.left(90)
    turtle.end_fill()
    turtle.penup()

def banniere(txt):
    '''
    Cette fonction place une inscription dans une bannière
    '''
    turtle.speed(0)
    turtle.penup()
    turtle.goto(-235,290)
    turtle.pendown()
    turtle.pencolor('black')
    turtle.write(txt, font = ('Arial', 12, 'normal'))
    turtle.penup()

def ramasser_objet(coord_obj):
    '''
    Cette fonction décrit les actions à effectuer pour prendre un objet.
    '''
    global position_txt
    dict_obj = creer_dictionnaire_des_objets(fichier_objets)
    txt_obj = dict_obj[coord_obj]
    clear_banner()
    banniere(txt_obj)
    turtle.goto(70, position_txt)
    turtle.pendown()
    turtle.pencolor('black')
    turtle.write(txt_obj, font=('Arial', 10, 'normal'))
    turtle.penup()
    position_txt = position_txt - 20 # La réponse suivante sera rendue 20 pixels ci-dessous

def poser_question(matrice, case, mouvement):
    '''
    Cette fonction décrit les actions à effectuer pour ouvrir la porte.
    '''
    #------Calcul des coordonnées-----
    global position_global
    global matrice_global
    old_x = case[0]
    old_y = case[1]
    new_x = mouvement[0]
    new_y = mouvement[1]
    old_dot_coordonnees = coordonnees(old_x, old_y)
    old_personage_radius_x = old_dot_coordonnees[0] + personage_radius
    old_personage_radius_y = old_dot_coordonnees[1] + personage_radius
    new_dot_coordonnees = coordonnees(new_x, new_y)
    new_personage_radius_x = new_dot_coordonnees[0] + personage_radius
    new_personage_radius_y = new_dot_coordonnees[1] + personage_radius
    #---------------------------
    dict_quest = creer_dictionnaire_des_questions(fichier_questions)
    lst_quest = dict_quest[mouvement]
    question = lst_quest[0]
    request = lst_quest[1]
    input_request = turtle.textinput('Question', question)
    turtle.listen()
    if input_request != request:
        clear_banner()
        banniere('Cette porte est fermée.')

    else:
        clear_banner()
        banniere('La porte s’ouvre')
        mouvement_de_personnage(old_x, old_y, new_x, new_y, old_personage_radius_x, old_personage_radius_y,
                                new_personage_radius_x, new_personage_radius_y)
        position_global = (new_x, new_y)
        matrice_global[new_x][new_y] = 0

afficher_plan(matrice_global) # Nous commençons à dessiner le plan en utilisant la matrice
# Installer le personnage au point de départ
x = position_global[0]
y = position_global[1]
dot_coordonnees = coordonnees(x,y)
personage_radius_x = dot_coordonnees[0] + personage_radius
personage_radius_y = dot_coordonnees[1] + personage_radius
turtle.penup()
turtle.goto(personage_radius_x,personage_radius_y)
turtle.pendown()
turtle.dot(square_size, COULEUR_PERSONNAGE)
turtle.listen()  # Déclenche l’écoute du clavier
turtle.onkeypress(deplacer_gauche, "Left")  # Associe à la touche Left une fonction appelée deplacer_gauche
turtle.onkeypress(deplacer_droite, "Right") # Associe à la touche Left une fonction appelée deplacer_droite
turtle.onkeypress(deplacer_haut, "Up") # Associe à la touche Left une fonction appelée deplacer_haut
turtle.onkeypress(deplacer_bas, "Down") # Associe à la touche Left une fonction appelée deplacer_bas
turtle.mainloop()