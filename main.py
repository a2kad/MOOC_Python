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
import turtle

position_global = POSITION_DEPART #Variable globale. L'emplacement du personnage. Le point de départ est indiqué ici.
position_txt = POINT_AFFICHAGE_INVENTAIRE[1]

def lire_matrice(fichier):
    '''
    Une fonction recevra en argument le nom d’un fichier texte contenant le plan à tracer.
    Elle ouvrira ce fichier et renverra en sortie une matrice.
    :param fichier: le nom d’un fichier texte contenant le plan à tracer.
    :return: ouvrira le fichier et renverra en sortie une matrice
    '''
    matrix = []
    with open(fichier) as lm:
        for i in range (27):
            srtok = lm.readline()
            srtok = srtok.strip('\n')
            lst = srtok.split(' ')
            matrix.append(lst)
        return matrix

def calculer_pas(matrice):
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

matrice_global = lire_matrice(fichier_plan)
c_p = calculer_pas(matrice_global)
rad = c_p/2


def coordonnees(case, pas):
    y = ZONE_PLAN_MAXI[1]
    x = ZONE_PLAN_MINI[1]
    mtr = lire_matrice(fichier_plan)
    c_p = calculer_pas(mtr)
    if case == 0:
        y = y
    else:
        for i in range(case):
            y = y - c_p
    if pas == 0:
        x = x
    else:
        for j in  range(pas):
            x = x + c_p
    coord =(x,y)
    return coord

def tracer_carre(dimension):
    for i in range(4):
        turtle.forward(dimension)
        turtle.left(90)

def tracer_case(case, couleur, pas):
    z = c_p
    x = case[0]
    y = case[1]
    crd = coordonnees(x,y)
    turtle.hideturtle()
    turtle.speed(0)
    turtle.color('white')
    turtle.penup()
    turtle.goto(crd[0], crd[1])
    turtle.pensize(pas)
    turtle.pendown()
    turtle.fillcolor(couleur)
    turtle.begin_fill()
    tracer_carre(z)
    turtle.end_fill()
    turtle.penup()


def afficher_plan(matrice):
    for strok in range(len(matrice)):
        for stolb in range(len(matrice[0])):
            coor = (strok,stolb)
            numbre_color = int(matrice[strok][stolb])
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
    turtle.onkeypress(None, "Left")
    print("Left")
    gauche_x = position_global[0]
    gauche_y = position_global[1]
    new_gauche_x = gauche_x
    new_gauche_y = gauche_y - 1
    deplacer(matrice_global, (gauche_x, gauche_y), (new_gauche_x, new_gauche_y))
    # traitement associé à la flèche gauche appuyée par le joueur
    turtle.onkeypress(deplacer_gauche, "Left")

def deplacer_droite():
    turtle.onkeypress(None, "Right")  # Désactive la touche Left
    print("Right")
    droite_x = position_global[0]
    droite_y = position_global[1]
    new_droite_x = droite_x
    new_droite_y = droite_y + 1
    deplacer(matrice_global, (droite_x, droite_y), (new_droite_x, new_droite_y))
    # traitement associé à la flèche gauche appuyée par le joueur
    turtle.onkeypress(deplacer_droite, "Right")

def deplacer_haut():
    turtle.onkeypress(None, "Up")  # Désactive la touche Left
    print("Up")
    haut_x = position_global[0]
    haut_y = position_global[1]
    new_haut_x = haut_x - 1
    new_haut_y = haut_y
    deplacer(matrice_global, (haut_x, haut_y), (new_haut_x, new_haut_y))
    # traitement associé à la flèche gauche appuyée par le joueur
    turtle.onkeypress(deplacer_haut, "Up")

def deplacer_bas():
    turtle.onkeypress(None, "Down")  # Désactive la touche Left
    print("Down")
    bas_x = position_global[0]
    bas_y = position_global[1]
    new_bas_x = bas_x + 1
    new_bas_y = bas_y
    deplacer(matrice_global, (bas_x,bas_y), (new_bas_x, new_bas_y))
    # traitement associé à la flèche gauche appuyée par le joueur
    turtle.onkeypress(deplacer_bas, "Down")

def deplacer(matrice, position, mouvement):
    global position_global
    global matrice_global
    old_x = position[0]
    old_y = position[1]
    new_x = mouvement[0]
    new_y = mouvement[1]
    old_dot_coordonnees = coordonnees(old_x, old_y)
    old_rad_x = old_dot_coordonnees[0] + rad
    old_rad_y = old_dot_coordonnees[1] + rad
    new_dot_coordonnees = coordonnees(new_x, new_y)
    new_rad_x = new_dot_coordonnees[0] + rad
    new_rad_y = new_dot_coordonnees[1] + rad
    #print(matrice[new_x][new_y])
    if new_x<0 or new_x >= len(matrice):
        print('Stop - end of the map')
    elif int(matrice[new_x][new_y]) == 1:
        print('Stop - gris')
    elif int(matrice[new_x][new_y]) == 4:
        poser_question(matrice, (old_x, old_y), (new_x, new_y))
    elif int(matrice[new_x][new_y]) == 3:
        turtle.penup()
        turtle.goto(old_rad_x, old_rad_y)
        turtle.pendown()
        tracer_case((old_x, old_y), 'wheat', 1)
        tracer_case((new_x, new_y), 'wheat', 1)
        turtle.penup()
        turtle.goto(new_rad_x, new_rad_y)
        turtle.pendown()
        turtle.dot(c_p, 'red')
        turtle.penup()
        position_global = (new_x, new_y)
        matrice_global[new_x][new_y] = 0
        ramasser_objet((new_x,new_y))
    else:
        print('Old X,Y: (',old_x,', ',old_y,'); New X,Y: (',new_x,', ',new_y,')')
        turtle.penup()
        turtle.goto(old_rad_x, old_rad_y)
        turtle.pendown()
        tracer_case((old_x,old_y),'wheat', 1)
        turtle.penup()
        turtle.goto(new_rad_x, new_rad_y)
        turtle.pendown()
        turtle.dot(c_p, 'red')
        turtle.penup()
        position_global = (new_x, new_y)

#Определяем, cколько четверок (объектов) на карте
quatr = 0
for q1 in range(len(matrice_global)):
    for q2 in range(len(matrice_global[0])):
        if int(matrice_global[q1][q2]) == 4:
            quatr += 1

def creer_dictionnaire_des_objets(fichier_des_objets):
    dict_obj = {}
    with open(fichier_des_objets) as des_obj:
        for i in range(quatr):
            line_obect = des_obj.readline()
            val, key = eval(line_obect)
            dict_obj.setdefault(val,key)
        return dict_obj

trois = 0
for t1 in range(len(matrice_global)):
    for t2 in range(len(matrice_global[0])):
        if int(matrice_global[t1][t2]) == 3:
            trois += 1

def creer_dictionnaire_des_questions(fichier_questions):
    dict_quest = {}
    with open(fichier_questions) as des_quest:
        for i in range(quatr):
            line_quest = des_quest.readline()
            val, key = eval(line_quest)
            dict_quest.setdefault(val,key)
        return dict_quest

def clear_banner():
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

def ramasser_objet(coord_obj):
    global position_txt
    dict_obj = creer_dictionnaire_des_objets(fichier_objets)
    txt_obj = dict_obj[coord_obj]
    turtle.speed(0)
    turtle.penup()
    turtle.goto(-235,290)
    turtle.pendown()
    turtle.pencolor('black')
    turtle.write(txt_obj, font = ('Arial', 12, 'normal'))
    turtle.penup()
    clear_banner()
    turtle.goto(70, position_txt)
    turtle.pendown()
    turtle.pencolor('black')
    turtle.write(txt_obj, font=('Arial', 10, 'normal'))
    turtle.penup()
    position_txt = position_txt - 20

def poser_question(matrice, case, mouvement):
    #------Расчет координат-----
    global position_global
    global matrice_global
    old_x = case[0]
    old_y = case[1]
    new_x = mouvement[0]
    new_y = mouvement[1]
    old_dot_coordonnees = coordonnees(old_x, old_y)
    old_rad_x = old_dot_coordonnees[0] + rad
    old_rad_y = old_dot_coordonnees[1] + rad
    new_dot_coordonnees = coordonnees(new_x, new_y)
    new_rad_x = new_dot_coordonnees[0] + rad
    new_rad_y = new_dot_coordonnees[1] + rad
    #---------------------------
    dict_quest = creer_dictionnaire_des_questions(fichier_questions)
    lst_quest = dict_quest[mouvement]
    question = lst_quest[0]
    request = lst_quest[1]
    input_request = turtle.textinput('Question', question)
    turtle.listen()
    if input_request != request:
        turtle.speed(0)
        turtle.penup()
        turtle.goto(-235, 290)
        turtle.pendown()
        turtle.pencolor('black')
        turtle.write('Cette porte est fermée.', font=('Arial', 12, 'normal'))
        turtle.penup()
        clear_banner()
    else:
        turtle.speed(0)
        turtle.penup()
        turtle.goto(-235, 290)
        turtle.pendown()
        turtle.pencolor('black')
        turtle.write('La porte s’ouvre', font=('Arial', 12, 'normal'))
        turtle.penup()
        clear_banner()
        turtle.penup()
        turtle.goto(old_rad_x, old_rad_y)
        turtle.pendown()
        tracer_case((old_x, old_y), 'wheat', 1)
        tracer_case((new_x, new_y), 'wheat', 1)
        turtle.penup()
        turtle.goto(new_rad_x, new_rad_y)
        turtle.pendown()
        turtle.dot(c_p, 'red')
        turtle.penup()
        position_global = (new_x, new_y)
        matrice_global[new_x][new_y] = 0


afficher_plan(matrice_global)

x = 0
y = 1
dot_coordonnees = coordonnees(x,y)
rad_x = dot_coordonnees[0] + rad
rad_y = dot_coordonnees[1] + rad
turtle.penup()
turtle.goto(rad_x,rad_y)
turtle.pendown()
turtle.dot(c_p, 'red')
turtle.listen()  # Déclenche l’écoute du clavier
turtle.onkeypress(deplacer_gauche, "Left")  # Associe à la touche Left une fonction appelée deplacer_gauche
turtle.onkeypress(deplacer_droite, "Right")
turtle.onkeypress(deplacer_haut, "Up")
turtle.onkeypress(deplacer_bas, "Down")
turtle.mainloop()