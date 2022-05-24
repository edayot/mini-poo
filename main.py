import numpy as np
import PIL
import random
import tkinter as TK
from PIL import Image, ImageTk
from tkinter import filedialog
import xml.etree.ElementTree as ET
import pyglet

atlas_bonbon=np.asanyarray(PIL.Image.open("assets/assets_candy.png"))
L_couleur=["yellow","blue","red","green","magenta"]
L_direction=["V","H"]
L_flux=["source","puits",""]
L_orientation=["haut","bas","gauche","droite",""]

def icon(i,j):
    #return a 100x100 icon at position i,j
    return atlas_bonbon[i*100:(i+1)*100,j*100:(j+1)*100]
def display(icon):
    return PIL.Image.fromarray(icon)
def combine(icon1,icon2):
    #combine two icons
    img1=display(icon1)
    img2=display(icon2)
    img=PIL.Image.new("RGBA",(100,100))
    img.paste(img1,(0,0))
    img.paste(img2,(0,0),mask=img2)
    return np.asanyarray(img)

def l():
    global J
    J=Jeu(n=7,m=8)
    J.start()

def play_random_sound():
    L_sound=["assets\sounds\Delicious!.ogg","assets\sounds\Divine!.ogg","assets\sounds\Sweet!.ogg","assets\sounds\Tasty!.ogg"]
    sound=pyglet.media.load(random.choice(L_sound))
    sound.play()

class Element():
    """Classe de tout les éléments possibles d'une case"""
    def get_icon(self):
        return self._icon
    def set_icon(self,icon):
        if isinstance(icon,np.ndarray):
            self._icon=icon
        else:
            raise TypeError("icon must be an np.ndarray'")
    icon=property(get_icon,set_icon)
        
    def __init__(self) -> None:
        self._icon=icon(6,6)  
class Bonbon_normal(Element):
    """Est un bonbon normal, il a une couleur"""
    def get_couleur(self):
        return self._couleur
    def set_couleur(self,couleur):
        if couleur in L_couleur:
            self._couleur=couleur
        else:
            raise ValueError("couleur must be in "+str(L_couleur))
    couleur=property(get_couleur,set_couleur)

    def __init__(self,couleur="Ja") -> None:
        super().__init__()
        if couleur in L_couleur:
            self._couleur=couleur
        else:
            self._couleur="yellow"
        self.icon=icon(0,L_couleur.index(self.couleur))
    def __repr__(self) -> str:
        return ""+self.couleur
    def __str__(self) -> str:
        return ""+self.couleur    
class Bonus(Element):
    """Regroupe tout les bonus, n'as aucune méthode"""
    pass
class Roquette(Bonus):
    """Est une roquette, a une direction"""
    def get_direction(self):
        return self._direction
    def set_direction(self,direction):
        if direction in L_direction:
            self._direction=direction
        else:
            raise ValueError("direction must be in "+str(L_direction))
    direction=property(get_direction,set_direction)
    def __init__(self,direction):
        super().__init__()
        if direction in L_direction:
            self._direction=direction
        else:
            self._direction="H"
        self.icon=icon(4,L_direction.index(self.direction))
    def __repr__(self) -> str:
        return "Roquette"
    def __str__(self) -> str:
        return "Roquette"
class Bombe(Bonus):
    """Est une bombe avec un rayon d'effet"""
    def __init__(self):
        super().__init__()
        self.icon=icon(4,2)
    def __repr__(self) -> str:
        return "Bombe"
    def __str__(self) -> str:
        return "Bombe"  
class Avion(Bonus):
    def __init__(self):
        super().__init__()
        self.icon=icon(4,3)
    def __repr__(self) -> str:
        return "Avion"
    def __str__(self) -> str:
        return "Avion"
class Déflagrateur(Bonus):
    def __init__(self):
        super().__init__()
        self.icon=icon(0,5)
    def __repr__(self) -> str:
        return "Déflagateur"
    def __str__(self) -> str:
        return "Déflagateur"        
class Etoile(Bonus):
    def __init__(self):
        super().__init__()
        self.icon=icon(3,6)
    def __repr__(self) -> str:
        return "Etoile"
    def __str__(self) -> str:
        return "Etoile"
class Vide(Element):
    """Est un élément vide,
     il garantit qu'il a toute les attribut et toutes les méthodes d'un élément"""
    def __init__(self) -> None:
        super().__init__()
    def __repr__(self) -> str:
        return "Vide"
    def __str__(self) -> str:
        return "Vide"
#définition des cases vide normal et gelée
class Case():
    """Est une des cellules de la grille
    Si elle n'est pas une sous classe Normale ou gelée, c'est une case vide"""
    def get_i(self):
        return self._i
    def set_i(self,i):
        if isinstance(i,int):
            self._i=i
        else:
            raise TypeError("i must be an int")
    i=property(get_i,set_i)
    def get_j(self):
        return self._j
    def set_j(self,j):
        if isinstance(j,int):
            self._j=j
        else:
            raise TypeError("j must be an int")
    j=property(get_j,set_j)

    def get_flux(self):
        return self._flux
    def set_flux(self,flux):
        if flux in L_flux:
            self._flux=flux
        else:
            raise ValueError("flux must be in "+str(L_flux))
    flux=property(get_flux,set_flux)

    def get_orientation(self):
        return self._orientation
    def set_orientation(self,orientation):
        if orientation in L_orientation:
            self._orientation=orientation
        else:
            raise ValueError("orientation must be in "+str(L_orientation))
    orientation=property(get_orientation,set_orientation)

    def get_icon_placement(self):
        return self._icon_placement
    def set_icon_placement(self,icon_placement):
        if isinstance(icon_placement,tuple) and len(icon_placement)==2 and isinstance(icon_placement[0],int) and isinstance(icon_placement[1],int):
            self._icon_placement=icon_placement
        else:
            raise TypeError("icon_placement must be a tuple of 2 int")
    icon_placement=property(get_icon_placement,set_icon_placement)

    def get_teleporter(self):
        return self._teleporter
    def set_teleporter(self,teleporter):
        if isinstance(teleporter,tuple) and len(teleporter)==2 and isinstance(teleporter[0],int) and isinstance(teleporter[1],int):
            self._teleporter=teleporter
        else:
            raise TypeError("teleporter must be a tuple of 2 int")
    teleporter=property(get_teleporter,set_teleporter)

    def get_teleporter_exit(self):
        return self._teleporter_exit
    def set_teleporter_exit(self,teleporter_exit):
        if isinstance(teleporter_exit,bool):
            self._teleporter_exit=teleporter_exit
        else:
            raise TypeError("teleporter_exit must be a bool")
    teleporter_exit=property(get_teleporter_exit,set_teleporter_exit)

    def get_element(self):
        return self._element
    def set_element(self,element):
        if isinstance(element,Element):
            self._element=element
        else:
            raise TypeError("element must be an Element")
    element=property(get_element,set_element)

    def __init__(self,i,j,flux,orientation,teleporter=None,teleporter_exit=False) -> None:
        self._element=Vide() #initialisée avec un élément Vide()
        self._i=int(i)
        self._j=int(j)
        if flux in L_flux:
            self._flux=flux
        else:
            self._flux=""
        if orientation in L_orientation:
            self._orientation=orientation
        else:
            self._orientation=""
        self._icon_placement=(5,5)
        
        if isinstance(teleporter,tuple) and len(teleporter)==2 and isinstance(teleporter[0],int) and isinstance(teleporter[1],int):
            self._teleporter=teleporter
        else:
            self._teleporter=None
        self._teleporter_exit=bool(teleporter_exit)
    
    def icon(self):
        if self.teleporter!=None:
            i,j=self.icon_placement
            return combine(combine(icon(i,j),icon(5,2)),self.element.icon)
        elif self.teleporter_exit:
            i,j=self.icon_placement
            return combine(combine(icon(i,j),icon(5,3)),self.element.icon)
        else:
            i,j=self.icon_placement
            return combine(icon(i,j),self.element.icon)
    def __repr__(self) -> str:
        return self.element.__repr__()
    def __str__(self) -> str:
        return self.element.__str__()
    def destruction(self,grille,spawn_bool=True):
        if isinstance(self.element,Bonbon_normal):
            couleur=self.element.couleur
            grille.element_detruit["bonbon_normal"][couleur]+=1
            self.element=Vide()
        if isinstance(self.element,Roquette):
            grille.element_detruit["roquette"]+=1
            self.element=Vide()
        if isinstance(self.element,Bombe):
            grille.element_detruit["bombe"]+=1
            self.element=Vide()
        if isinstance(self.element,Avion):
            grille.element_detruit["avion"]+=1
            self.element=Vide()
        if isinstance(self.element,Déflagrateur):
            grille.element_detruit["déflagrateur"]+=1
            self.element=Vide()
        if isinstance(self.element,Etoile):
            grille.element_detruit["etoiles"]+=1
            self.element=Vide()

    def gestion_flux(self,grille):
        """
        Méthode définissant la gestion des flux du niveau,
        cad la ou la case va chercher un nouveau élément si elle est vide
        """
        result=False
        if (isinstance(self,Case_Normale) and not(isinstance(self.element,Vide))):
            if self.orientation=="haut":
                if 0<=self.i-1<grille.n and 0<=self.j<grille.m and isinstance(grille.grille[self.i-1,self.j],Case_Normale) and isinstance(grille.grille[self.i-1,self.j].element,Vide):
                    grille.grille[self.i-1,self.j].element=self.element
                    self.element=Vide()
                    result=True
            
            elif self.orientation=="bas":
                if 0<=self.i+1<grille.n and 0<=self.j<grille.m and isinstance(grille.grille[self.i+1,self.j],Case_Normale) and isinstance(grille.grille[self.i+1,self.j].element,Vide):
                    grille.grille[self.i+1,self.j].element=self.element
                    self.element=Vide()
                    result=True

            elif self.orientation=="gauche":
                if 0<=self.i<grille.n and 0<=self.j-1<grille.m and isinstance(grille.grille[self.i,self.j-1],Case_Normale) and isinstance(grille.grille[self.i,self.j-1].element,Vide):
                    grille.grille[self.i,self.j-1].element=self.element
                    self.element=Vide()
                    result=True

            elif self.orientation=="droite":
                if 0<=self.i<grille.n and 0<=self.j+1<grille.m and isinstance(grille.grille[self.i,self.j+1],Case_Normale) and isinstance(grille.grille[self.i,self.j+1].element,Vide):
                    grille.grille[self.i,self.j+1].element=self.element
                    self.element=Vide()
                    result=True
            if self.teleporter!=None and isinstance(grille.grille[self.teleporter[0],self.teleporter[1]].element,Vide) and not isinstance(self.element,Vide): #check teleporter
                grille.grille[self.teleporter[0],self.teleporter[1]].element=self.element
                self.element=Vide()
                result=True

        if isinstance(self,Case_Normale) and isinstance(self.element,Etoile) and self.flux=="puits":
            self.element=Vide()
            grille.element_detruit["etoiles"]+=1
            result=True
        elif isinstance(self,Case_Normale) and isinstance(self.element,Vide) and self.flux=="source":
            self.element=Bonbon_normal(random.choice(L_couleur))
            result=True
        return result

    def gestion_flux_secondaire(self,grille):
        result=False
        if (isinstance(self,Case_Normale) and not(isinstance(self.element,Vide))):
            if self.orientation=="haut":
                if 0<=self.i-1<grille.n and 0<=self.j-1<grille.m and isinstance(grille.grille[self.i-1,self.j-1],Case_Normale)  and isinstance(grille.grille[self.i-1,self.j-1].element,Vide):
                    grille.grille[self.i-1,self.j-1].element=self.element
                    self.element=Vide()
                    result=True
                elif 0<=self.i-1<grille.n and 0<=self.j+1<grille.m and isinstance(grille.grille[self.i-1,self.j+1],Case_Normale) and isinstance(grille.grille[self.i-1,self.j+1].element,Vide):
                    grille.grille[self.i-1,self.j+1].element=self.element
                    self.element=Vide()
                    result=True
            
            elif self.orientation=="bas":
                if 0<=self.i+1<grille.n and 0<=self.j-1<grille.m and isinstance(grille.grille[self.i+1,self.j-1],Case_Normale) and isinstance(grille.grille[self.i+1,self.j-1].element,Vide):
                    grille.grille[self.i+1,self.j-1].element=self.element
                    self.element=Vide()
                    result=True
                elif 0<=self.i+1<grille.n and 0<=self.j+1<grille.m and isinstance(grille.grille[self.i+1,self.j+1],Case_Normale) and isinstance(grille.grille[self.i+1,self.j+1].element,Vide):
                    grille.grille[self.i+1,self.j+1].element=self.element
                    self.element=Vide()
                    result=True

            elif self.orientation=="gauche":
                if 0<=self.i-1<grille.n and 0<=self.j-1<grille.m and isinstance(grille.grille[self.i-1,self.j-1],Case_Normale) and isinstance(grille.grille[self.i-1,self.j-1].element,Vide):
                    grille.grille[self.i-1,self.j-1].element=self.element
                    self.element=Vide()
                    result=True
                elif 0<=self.i+1<grille.n and 0<=self.j-1<grille.m and isinstance(grille.grille[self.i+1,self.j-1],Case_Normale) and isinstance(grille.grille[self.i+1,self.j-1].element,Vide):
                    grille.grille[self.i+1,self.j-1].element=self.element
                    self.element=Vide()
                    result=True

            elif self.orientation=="droite":
                if 0<=self.i-1<grille.n and 0<=self.j+1<grille.m and isinstance(grille.grille[self.i-1,self.j+1],Case_Normale) and isinstance(grille.grille[self.i-1,self.j+1].element,Vide):
                    grille.grille[self.i-1,self.j+1].element=self.element
                    self.element=Vide()
                    result=True
                elif 0<=self.i+1<grille.n and 0<=self.j+1<grille.m and isinstance(grille.grille[self.i+1,self.j+1],Case_Normale) and isinstance(grille.grille[self.i+1,self.j+1].element,Vide):
                    grille.grille[self.i+1,self.j+1].element=self.element
                    self.element=Vide()
                    result=True
        return result
    def update(self,grille,couleur=None):
        """
        mise à jour de la case en fonction de son élément (quand il est échangé)
        est récursive pour permettre de mettre à jour les cases affectées par l'élément avant de les détruire
        """
        if isinstance(self,Case_Gelee):
            return None
        if isinstance(self.element,Roquette):
            if self.element.direction=="H":
                self.destruction(grille)
                for i in range(grille.n):
                    if i!=self.i:
                        grille.grille[i,self.j].update(grille)
                        grille.grille[i,self.j].destruction(grille)
                        

            elif self.element.direction=="V":
                self.destruction(grille)
                for j in range(grille.m):
                    if j!=self.j:
                        grille.grille[self.i,j].update(grille)
                        grille.grille[self.i,j].destruction(grille)
                        
        if isinstance(self.element,Bombe):
            self.destruction(grille)
            L_bombe=[(self.i-1,self.j),(self.i+1,self.j),(self.i,self.j-1),(self.i,self.j+1),(self.i+1,self.j+1),(self.i-1,self.j-1),(self.i+1,self.j-1),(self.i-1,self.j+1),(self.i+2,self.j),(self.i-2,self.j),(self.i,self.j+2),(self.i,self.j-2)]
            for (i,j) in L_bombe:
                if i>=0 and j>=0 and i<grille.grille.shape[0] and j<grille.grille.shape[1]:
                    grille.grille[i,j].update(grille)
                    grille.grille[i,j].destruction(grille)
        if isinstance(self.element,Avion):
            self.destruction(grille)
            L_avion=[(self.i-1,self.j),(self.i+1,self.j),(self.i,self.j-1),(self.i,self.j+1)]
            L_etoile=[]
            for i in range(grille.n):
                for j in range(grille.m):
                    if isinstance(grille.grille[i,j].element,Etoile):
                        L_etoile.append((i,j))
            if len(L_etoile)>0:
                L_avion.append(random.choice(L_etoile))
            else:
                
                test=(random.randint(0,grille.m-1),random.randint(0,grille.n-1))
                while test in L_avion or not (isinstance(grille.grille[test[0],test[1]],Case_Normale) or isinstance(grille.grille[test[0],test[1]],Case_Gelee)):
                    test=(random.randint(0,grille.m-1),random.randint(0,grille.n-1))
                L_avion.append(test)

            for (i,j) in L_avion:
                if i>=0 and j>=0 and i<grille.grille.shape[0] and j<grille.grille.shape[1]:
                    grille.grille[i,j].update(grille)
                    grille.grille[i,j].destruction(grille)
        if isinstance(self.element,Déflagrateur):
            self.destruction(grille)
            if couleur==None:
                couleur=random.choice(L_couleur)
            for i in range(grille.n):
                for j in range(grille.m):
                    if isinstance(grille.grille[i,j].element,Bonbon_normal) and grille.grille[i,j].element.couleur==couleur:
                        grille.grille[i,j].update(grille)
                        grille.grille[i,j].destruction(grille)      
class Case_Normale(Case):
    """est une case normale, a une icone remplie et un élement"""
    def __init__(self,i,j,flux,orientation,element,teleporter=None) -> None:
        super().__init__(i,j,flux,orientation,teleporter)
        if isinstance(element,Element):
            self.element=element
        self.icon_placement=(5,0)
class Case_Gelee(Case):
    """est une case gelée, a une icone remplie mais gelée et un élément"""
    def get_niveau_gel(self):
        return self._niveau_gel
    def set_niveau_gel(self,niveau_gel):
        if isinstance(niveau_gel,int) and niveau_gel>=0 and niveau_gel<=3:
            self._niveau_gel=niveau_gel
        elif not isinstance(niveau_gel,int):
            raise TypeError("niveau_gel must be a int")
        else:
            raise ValueError("niveau_gel must be between 0 and 3")
    niveau_gel=property(get_niveau_gel,set_niveau_gel)

    
    def __init__(self,i,j,flux,orientation,element,niveau_gel,teleporter=None) -> None:
        super().__init__(i,j,flux,orientation,teleporter)
        if isinstance(element,Element):
            self.element=element
        self.icon_placement=(3,0)
        self._niveau_gel=int(niveau_gel)
    
    def __repr__(self) -> str:
        return super().__repr__() + "- Gelée"
    def __str__(self) -> str:
        return super().__str__() + "- Gelée"
    def icon(self):
        if self.niveau_gel==1:
            self.icon_placement=(3,0)
        elif self.niveau_gel==2:
            self.icon_placement=(5,1)
        elif self.niveau_gel==3:
            self.icon_placement=(3,1)
        i,j=self.icon_placement
        return combine(combine(icon(5,0),self.element.icon),icon(i,j))

    def destruction(self, grille, spawn_bool=True):
        if spawn_bool and self.niveau_gel>0:
            print("yolor")
            self.niveau_gel-=1
        if spawn_bool and self.niveau_gel==0:
            grille.grille[self.i,self.j]=Case_Normale(self.i,self.j,self.flux,self.orientation,self.element)

class Case_Vide(Case):
    """est une case vide, a une icone vide et un élément vide"""
    def __init__(self,i,j,flux,orientation,teleporter=None) -> None:
        super().__init__(i,j,flux,orientation,teleporter)
        self.element=Vide()
        self.icon_placement=(3,3)
#Grille :
class Grille():
    """est une grille, a une liste de cases"""
    def get_grille(self):
        return self._grille
    def set_grille(self,grille):
        if isinstance(grille,np.ndarray) and grille.shape[0]==self.n and grille.shape[1]==self.m:
            self._grille=grille
        else:
            raise TypeError("grille must be a numpy array of size n*m")
    grille=property(get_grille,set_grille)

    def get_n(self):
        return self._n
    def set_n(self,n):
        if isinstance(n,int) and n>0:
            self._n=n
        else:
            raise TypeError("n must be a int > 0")
    n=property(get_n,set_n)

    def get_m(self):
        return self._m
    def set_m(self,m):
        if isinstance(m,int) and m>0:
            self._m=m
        else:
            raise TypeError("m must be a int > 0")
    m=property(get_m,set_m)

    def get_element_detruit(self):
        return self._element_detruit
    def set_element_detruit(self,element_detruit):
        if isinstance(element_detruit,dict):
            self._element_detruit=element_detruit
        else:
            raise TypeError("element_detruit must be a dict")
    element_detruit=property(get_element_detruit,set_element_detruit)

    def get_L_objectifs(self):
        return self._L_objectifs
    def set_L_objectifs(self,L_objectifs):
        if isinstance(L_objectifs,list):
            self._L_objectifs=L_objectifs
        else:
            raise TypeError("L_objectifs must be a list")
    L_objectifs=property(get_L_objectifs,set_L_objectifs)
    def __init__(self,n=5,m=5) -> None:
        self._grille=np.empty((int(n),int(m)),dtype=Case)
        self._n=int(n)
        self._m=int(m)
        self._element_detruit={
            "roquette":0,
            "bombe":0,
            "avion":0,
            "déflagrateur":0,  
            "etoiles":0,
            "bonbon_normal":{
                "yellow":0,
                "blue":0,
                "red":0,
                "green":0,
                "magenta":0
            }
        }
        self._L_objectifs=[
            {"Nombre":10, "Cible":"red"}
        ]
        self.generate()
    def generate(self):
        """ génère une grille aléatoire"""
        for i in range(self.n):
            for j in range(self.m):
                if i==0:
                    self.grille[i,j]=Case_Normale(i,j,"source","bas",Bonbon_normal(random.choice(L_couleur)))
                elif i==self.n-1:
                    self.grille[i,j]=Case_Gelee(i,j,"puits","",Bonbon_normal(random.choice(L_couleur)),3)
                else:
                    self.grille[i,j]=Case_Normale(i,j,"","bas",Bonbon_normal(random.choice(L_couleur)))
                
    def echange(self,coo1,coo2):
        i1,j1=coo1
        i2,j2=coo2
        Case1=self.grille[i1,j1]
        Case2=self.grille[i2,j2]
        di=abs(i1-i2)
        dj=abs(j1-j2)
        if isinstance(Case1,Case_Normale) and isinstance(Case2,Case_Normale) and di in [0,1] and dj in [0,1] and (di+dj==1 or di+dj==0):
            Case1.element,Case2.element=Case2.element,Case1.element
            try:
                color1=Case1.element.couleur
            except:
                color1=None
            try:
                color2=Case2.element.couleur
            except:
                color2=None            
            Case1.update(self,couleur=color2),Case2.update(self,couleur=color1)            
            return True
        return False
    def __repr__(self) -> str:
        return self.grille.__repr__()
    def __str__(self) -> str:
        return self.grille.__str__()
    def gestion_flux(self):
        res=False
        for i in range(self.n):
            for j in range(self.m):
                res = self.grille[i,j].gestion_flux(self) or res
        return res
    def gestion_flux_secondaire(self):
        res=False
        for i in range(self.n):
            for j in range(self.m):
                res=self.grille[i,j].gestion_flux_secondaire(self) or res
        return res
    def liste_vides(self):
        L=[]
        for i in range(self.n):
            for j in range(self.m):
                if isinstance(self.grille[i,j],Case_Normale) and isinstance(self.grille[i,j].element,Vide):
                    L.append(self.grille[i,j])
        return L
    def display_orientation(self):
        res=np.empty((self.n,self.m),dtype=str)
        for i in range(self.n):
            for j in range(self.m):
                if isinstance(self.grille[i,j],Case_Normale) or isinstance(self.grille[i,j],Case_Gelee):
                    if self.grille[i,j].orientation=="bas":
                        res[i,j]="⬇️"
                    elif self.grille[i,j].orientation=="droite":
                        res[i,j]="➡️"
                    elif self.grille[i,j].orientation=="haut":
                        res[i,j]="⬆️"
                    elif self.grille[i,j].orientation=="gauche":
                        res[i,j]="⬅️"
                else:
                    res[i,j]=" "
        for i in range(self.n):
            for j in range(self.m):
                if res[i,j]=="":
                    res[i,j]=" "
        return res
    def display_flux(self):
        res=np.empty((self.n,self.m),dtype=str)
        for i in range(self.n):
            for j in range(self.m):
                if isinstance(self.grille[i,j],Case_Normale) or isinstance(self.grille[i,j],Case_Gelee):
                    if self.grille[i,j].flux=="source":
                        res[i,j]="S"
                    elif self.grille[i,j].flux=="puits":
                        res[i,j]="P"
                    elif self.grille[i,j].flux=="":
                        res[i,j]=" "
                else:
                    res[i,j]=" "
        for i in range(self.n):
            for j in range(self.m):
                if res[i,j]=="":
                    res[i,j]=" "
        return res
    def display_type_case(self):
        res=np.empty((self.n,self.m),dtype=str)
        for i in range(self.n):
            for j in range(self.m):
                if isinstance(self.grille[i,j],Case_Normale):
                    res[i,j]="N"
                elif isinstance(self.grille[i,j],Case_Gelee):
                    res[i,j]="G"
                else:
                    res[i,j]=" "
        for i in range(self.n):
            for j in range(self.m):
                if res[i,j]=="":
                    res[i,j]=" "
        return res
    def display_teleporter(self):
        res=np.empty((self.n,self.m),dtype=str)
        for i in range(self.n):
            for j in range(self.m):
                if isinstance(self.grille[i,j],Case_Normale):
                    if self.grille[i,j].teleporter==None:
                        res[i,j]=" "
                    else:
                        res[i,j]="T"
                else:
                    res[i,j]=" "
        for i in range(self.n):
            for j in range(self.m):
                if res[i,j]=="":
                    res[i,j]=" "
        return res
    def display_teleporter_exit(self):
        res=np.empty((self.n,self.m),dtype=str)
        for i in range(self.n):
            for j in range(self.m):
                if isinstance(self.grille[i,j],Case_Normale):
                    if self.grille[i,j].teleporter!=None:
                        res[self.grille[i,j].teleporter[0],self.grille[i,j].teleporter[1]]="E"
        for i in range(self.n):
            for j in range(self.m):
                if res[i,j]=="":
                    res[i,j]=" "
        return res
    def recherche_pattern(self,spawn_bool=True):
        result=False
        def spawn_pattern(pattern,element,c,d):
            r=False
            for i in range(self.n-pattern.shape[0]+1):
                for j in range(self.m-pattern.shape[1]+1):
                    res=np.zeros(pattern.shape,dtype=bool)
                    for a in range(pattern.shape[0]):
                        for b in range(pattern.shape[1]):
                            res[a,b]=not(pattern[a,b]) or map[i+a,j+b]
                    #res=not(pattern) or map[i,i+len(pattern.shape[0]),j,j+len(pattern.shape[1])]
                    #print(pattern,grille,res,"\n")
                    if np.all(res):
                        r=True
                        if spawn_bool:
                            play_random_sound()
                        print(pattern," trouvé à l'indice : ",i,j)
                        
                        for a in range(pattern.shape[0]):
                            for b in range(pattern.shape[1]):
                                if pattern[a,b]==1:
                                    map[i+a,j+b]=0
                                    self.grille[i+a,j+b].destruction(self)
                        if spawn_bool:
                            self.grille[i+c,j+d].element=element
                        for a in range(pattern.shape[0]):
                            for b in range(pattern.shape[1]):
                                if isinstance(self.grille[i+a,j+b].element,Vide):
                                    self.grille[i+a,j+b].explosion=True
            return r
    
                               
        for couleur in L_couleur:
            map=np.zeros((self.n,self.m))
            for i in range(self.n):
                for j in range(self.m):
                    if (isinstance(self.grille[i,j],Case_Normale) or isinstance(self.grille[i,j],Case_Gelee)) and isinstance(self.grille[i,j].element,Bonbon_normal) and self.grille[i,j].element.couleur==couleur:
                        map[i,j]=1
            print(map,"\n\n\n")
            #Recherche Déflagrateur
            result=spawn_pattern(np.array([[1,1,1,1,1]]),Déflagrateur(),0,2) or result
            result=spawn_pattern(np.array([[1],[1],[1],[1],[1]]),Déflagrateur(),2,0) or result
            #Recherche Bombes
            result=spawn_pattern(np.array([
                [1,1,1],
                [0,1,0],
                [0,1,0],
            ]),Bombe(),0,1) or result
            result=spawn_pattern(np.array([
                [0,1,0],
                [0,1,0],
                [1,1,1],
            ]),Bombe(),2,1) or result
            result=spawn_pattern(np.array([
                [1,0,0],
                [1,1,1],
                [1,0,0],
            ]),Bombe(),1,2) or result
            result=spawn_pattern(np.array([
                [0,0,1],
                [1,1,1],
                [0,0,1],
            ]),Bombe(),1,2) or result
            #Recherche Roquette
            result=spawn_pattern(np.array([[1,1,1,1]]),Roquette("V"),0,1) or result
            result=spawn_pattern(np.array([[1],[1],[1],[1]]),Roquette("H"),1,0) or result
            #Recherche Avion
            result=spawn_pattern(np.array([
                [1,1],
                [1,1]]),Avion(),0,0) or result
            #Recherche Normal
            result=spawn_pattern(np.array([[1,1,1]]),Vide(),0,0) or result
            result=spawn_pattern(np.array([[1],[1],[1]]),Vide(),0,0) or result
        return result
    def check_objectif(self):
        # Mettre dans la classe grilles
        result=True
        for ob in self.L_objectifs:
            if ob["Cible"] in L_couleur:
                result = result and self.element_detruit["bonbon_normal"][ob["Cible"]]>=ob["Nombre"]
            else:
                result = result and self.element_detruit[ob["Cible"]]>=ob["Nombre"]
        return result
class Jeu(TK.Tk):
    def get_previous(self):
        return self._previous
    def set_previous(self,previous):
        if previous==None:
            self._previous=None
        elif isinstance(previous,tuple) and len(previous)==2 and isinstance(previous[0],int) and isinstance(previous[1],int):
            self._previous=previous
        else:
            raise ValueError("previous must be None or a tuple of 2 int")
    previous=property(get_previous,set_previous)

    def get_echange_autorise(self):
        return self._echange_autorise
    def set_echange_autorise(self,echange_autorise):
        if isinstance(echange_autorise,bool):
            self._echange_autorisee=echange_autorise
        else:
            raise ValueError("echange_autorisee must be a boolean")
    echange_autorise=property(get_echange_autorise,set_echange_autorise)

    def get_grille(self):
        return self._grille
    def set_grille(self,grille):
        if isinstance(grille,Grille):
            self._grille=grille
        else:
            raise ValueError("grille must be a Grille")
    grille=property(get_grille,set_grille)

    def get_n(self):
        return self._n
    def set_n(self,n):
        if isinstance(n,int):
            self._n=n
        else:
            raise ValueError("n must be an int")
    n=property(get_n,set_n)

    def get_m(self):
        return self._m
    def set_m(self,m):
        if isinstance(m,int):
            self._m=m
        else:
            raise ValueError("m must be an int")
    m=property(get_m,set_m)

    def get_liste_img(self):
        return self._liste_img
    def set_liste_img(self,liste_img):
        if isinstance(liste_img,list):
            self._liste_img=liste_img
        else:
            raise ValueError("liste_img must be a list")
    liste_img=property(get_liste_img,set_liste_img)

    def get_liste_label(self):
        return self._liste_label
    def set_liste_label(self,liste_label):
        if isinstance(liste_label,list):
            self._liste_label=liste_label
        else:
            raise ValueError("liste_label must be a list")
    liste_label=property(get_liste_label,set_liste_label)

    def get_nb_coup(self):
        return self._nb_coup
    def set_nb_coup(self,nb_coup):
        if isinstance(nb_coup,int) and nb_coup>=0:
            self._nb_coup=nb_coup
        else:
            raise ValueError("nb_coup must be an int")
    nb_coup=property(get_nb_coup,set_nb_coup)

    def __init__(self,n=6,m=6,grille=None,nb_coup=10,coo="+100+100") -> None:
        super().__init__()
        self.geometry("1024x768"+coo)
        #icone de fenetre
        self.iconbitmap("assets/icon.ico")
        self._previous=None
        self._echange_autorise=True
        if grille==None or not isinstance(grille,Grille):
            self._grille=Grille(n,m)
            while self.grille.recherche_pattern(False) or len(self.grille.liste_vides())>0:
                self.grille.gestion_flux()
        else:
            self._grille=grille
        self._n=n
        self._m=m
        self.title("Candy Crash Samba")
        self._liste_img=[]
        self._liste_label=[]
        self._time_interval=150
        self.protocol("WM_DELETE_WINDOW",self.quitter)
        if isinstance(nb_coup,int) and nb_coup>0:
            self._nb_coup=nb_coup
        else:
            self.nb_coup=10
        self.wm_attributes("-transparentcolor", 'grey')
        #Background
        self._bgimg = Image.open('assets/background_blur.png') 
        self._l = TK.Label(self)
        self._l.place(x=0, y=0, relwidth=1, relheight=1) 
        self._l.bind('<Configure>', self.on_resize) 
        #Bouton de chargement de fichier askopenfilename
        Button=TK.Button(self,text="Charger",command=self.load)
        Button.grid(row=1,column=0,sticky="nsew")
        #Affichage statistiques
        self._label_stats=TK.Label(self,text="")
        self._label_stats.grid(row=2,column=0,columnspan=2,rowspan=5,sticky="nsew")
        #Music player
        self._music_player=pyglet.media.Player()
        self._music_player.queue(pyglet.media.load("assets\sounds\music.mp3"))
        self._music_player.volume=0.5
    
    def quitter(self):
        self.destroy()
        self._music_player.pause()
    def on_resize(self, event):
        image = self._bgimg.resize((event.width, event.height), Image.ANTIALIAS)
        self._l.image = ImageTk.PhotoImage(image)
        self._l.config(image=self._l.image)
    def end(self,win):
        """
        Affiche une pop up de fin de partie
        """
        self._top= TK.Toplevel(self)
        self._top.title(win)
        self._top.iconbitmap("assets/icon.ico")
        #Boutons de reset
        Button=TK.Button(self._top,text="Recharger un niveau aléatoire",command=self.reset)
        Button.grid(row=0,column=0,sticky="nsew")
        Button=TK.Button(self._top,text="Charger XML",command=self.load)
        Button.grid(row=0,column=1,sticky="nsew")
        self.echange_autorise=False
    def reset(self):
        self._top.destroy()
        self.destroy()
        self.__init__(self.n,self.m)
        self.start()
    def load(self):
        try:
            self.top.destroy()
        except:
            pass
        print("Load")
        path= TK.filedialog.askopenfilename(title="Selectionnez un fichier XML d'un niveau", filetypes=(("Fichier XML","*.xml"),("Tous les fichiers","*.*")))
        if path!="":
            niveau=ET.parse(path)
            niveau=niveau.getroot()
            for label in self.liste_label:
                label.destroy()
            self.liste_label=[]
            for img in self.liste_img:
                del img
            self.liste_img=[]
            self.n=int(niveau.attrib["nb_lignes"])
            self.m=int(niveau.attrib["nb_colonnes"])
            del self._grille
            self.grille=Grille(self.n,self.m)
            self.title("Candy Crash Samba - "+niveau.attrib["titre"])
            self.nb_coup=int(niveau.attrib["nb_coup"])
            self.grille.L_objectifs=[]
            for obj in niveau.find("Objectifs").iter("Objectif"):
                self.grille.L_objectifs.append({"Cible":obj.attrib["Cible"][1:].lower(),"Nombre":int(obj.attrib["Nombre"])})
            L_teleporter=[]
            c=False
            for case in niveau.find("Grille").iter():
                if c:
                    i=int(case.attrib["ligne"])
                    j=int(case.attrib["colonne"])
                    try:
                        contenu=case.attrib["contenu"]
                    except:
                        contenu=None
                    try:
                        orientation=case.attrib["orientation"].lower()
                    except:
                        orientation=""
                    try:
                        flux=case.attrib["flux"].lower()
                    except:
                        flux=""
                    try:
                        niveau_gel=int(case.attrib["niveau_gel"].lower())
                    except:
                        niveau_gel=3
                    try:
                        teleporter=(int(case.attrib["flux_tp_vers"][1]),int(case.attrib["flux_tp_vers"][3]))
                    except:
                        teleporter=None
                    if teleporter!=None:
                        L_teleporter.append(teleporter)
                    if contenu in L_couleur:
                        if case.tag=="Cellule":
                            self.grille.grille[i,j]=Case_Normale(i,j,flux,orientation,Bonbon_normal(contenu),teleporter)
                        elif case.tag=="Cellule_Gelee":
                            self.grille.grille[i,j]=Case_Gelee(i,j,flux,orientation,Bonbon_normal(contenu),niveau_gel,teleporter)
                    elif contenu=="Roquette Horizontale":
                        if case.tag=="Cellule":
                            self.grille.grille[i,j]=Case_Normale(i,j,flux,orientation,Roquette("H"),teleporter)
                        elif case.tag=="Cellule_Gelee":
                            self.grille.grille[i,j]=Case_Gelee(i,j,flux,orientation,Roquette("H"),niveau_gel,teleporter)
                    elif contenu=="Roquette verticale":
                        if case.tag=="Cellule":
                            self.grille.grille[i,j]=Case_Normale(i,j,flux,orientation,Roquette("V"),teleporter)
                        elif case.tag=="Cellule_Gelee":
                            self.grille.grille[i,j]=Case_Gelee(i,j,flux,orientation,Roquette("V"),niveau_gel,teleporter)
                    elif contenu=="Avion":
                        if case.tag=="Cellule":
                            self.grille.grille[i,j]=Case_Normale(i,j,flux,orientation,Avion(),teleporter)
                        elif case.tag=="Cellule_Gelee":
                            self.grille.grille[i,j]=Case_Gelee(i,j,flux,orientation,Avion(),niveau_gel,teleporter)
                    elif contenu=="Bombe":
                        if case.tag=="Cellule":
                            self.grille.grille[i,j]=Case_Normale(i,j,flux,orientation,Bombe(),teleporter)
                        elif case.tag=="Cellule_Gelee":
                            self.grille.grille[i,j]=Case_Gelee(i,j,flux,orientation,Bombe(),niveau_gel,teleporter)
                    elif contenu=="Etoile":
                        if case.tag=="Cellule":
                            self.grille.grille[i,j]=Case_Normale(i,j,flux,orientation,Etoile(),teleporter)
                        elif case.tag=="Cellule_Gelee":
                            self.grille.grille[i,j]=Case_Gelee(i,j,flux,orientation,Etoile(),niveau_gel,teleporter)
                    elif contenu=="Deflagrateur":
                        if case.tag=="Cellule":
                            self.grille.grille[i,j]=Case_Normale(i,j,flux,orientation,Déflagrateur(),teleporter)
                        elif case.tag=="Cellule_Gelee":
                            self.grille.grille[i,j]=Case_Gelee(i,j,flux,orientation,Déflagrateur(),niveau_gel,teleporter)
                    elif case.tag=="Cellule_Vide":
                        self.grille.grille[i,j]=Case_Vide(i,j,flux,orientation)
                if not c:
                    c=True
            self.grille.element_detruit={
            "roquette":0,
            "bombe":0,
            "avion":0,
            "déflagrateur":0,  
            "etoiles":0,
            "bonbon_normal":{
                "yellow":0,
                "blue":0,
                "red":0,
                "green":0,
                "magenta":0
            }}
            for teleporter_exit in L_teleporter:
                self.grille.grille[teleporter_exit[0],teleporter_exit[1]].teleporter_exit=True
        self.display()
    def display(self):
        d_n=0
        d_m=4
        print("display update !")
        img_size=768/(self.n+2)
        if img_size<50:
            img_size=50
        if img_size>100:
            img_size=100
        img_size=int(img_size)
        for i in range(self.n):
            for j in range(self.m):
                #Display image at i,j
                img=PIL.Image.fromarray(self.grille.grille[i,j].icon())
                img=img.resize((img_size,img_size))
                img=PIL.ImageTk.PhotoImage(img,master=self)
                self.liste_img.append(img)
                label = TK.Label(self, image = img)
                label.image = img
                label.bind("<Button-1>" ,lambda event,i=i,j=j:self.click(i,j))
                label.grid(row=i+d_n,column=j+d_m)
                #label.wm_attributes("-transparentcolor", 'grey')
                self.liste_label.append(label)  
        string_stats="Elements detruits :\n"
        for i in range(len(L_couleur)):
            string_stats+="Bonbon "+L_couleur[i]+" : "+str(self.grille.element_detruit["bonbon_normal"][L_couleur[i]])+"\n"
        string_stats+="Roquette: "+str(self.grille.element_detruit["roquette"])+"\n"
        string_stats+="Bombe: "+str(self.grille.element_detruit["bombe"])+"\n"
        string_stats+="Avion: "+str(self.grille.element_detruit["avion"])+"\n"
        string_stats+="Déflagrateur: "+str(self.grille.element_detruit["déflagrateur"])+"\n"
        string_stats+="Etoile: "+str(self.grille.element_detruit["etoiles"])+"\n"
        string_stats+="\nNombre de coup restant : "+ str(self.nb_coup)
        string_stats+="\n\nObjectifs : "
        for ob in self.grille.L_objectifs:
            string_stats+="\n Détruitre "+str(ob["Nombre"])+" "+ob["Cible"]
        self._label_stats.config(text=string_stats)
    def clear_display(self):
        for label in self.liste_label:
            label.destroy()
            del label
        for img in self.liste_img:
            del img
    def restart_window(self):
        print("Restart window !")
        try:
            self._top.destroy()
        except:
            pass
        x,y=str(self.winfo_x()),str(self.winfo_y())
        self.destroy()
        self.__init__(n=self.n,m=self.m,grille=self.grille,nb_coup=self.nb_coup,coo="+"+x+"+"+y)
        self.display()
        self.mainloop()
    def click(self,i,j):
        print(i,j)
        if self.echange_autorise and self.nb_coup>0:
            if self.previous==None:
                self.previous=i,j
            else:
                if self.grille.echange(self.previous,(i,j)):
                    self.echange_autorise=False
                    self.display()
                    self.nb_coup-=1
                    self.after(10*self._time_interval,self.cadencage,True,i,j,self.previous)                    
                print(self.grille)
                self.previous=None
    def cadencage(self,first_time=False,i=None,j=None,previous=None):
        if not first_time:
            print("iteration")
            if self.grille.recherche_pattern():
                print("yo")
                self.after(self._time_interval,self.refill)
            else:
                self.after(self._time_interval,self.refill)
        else:
            print("first time")
            if self.grille.recherche_pattern():
                print("yo")
                self.after(self._time_interval,self.refill)
            elif len(self.grille.liste_vides())>0:
                self.after(self._time_interval,self.refill)
            else:
                self.echange_autorise=True
                self.grille.echange(previous,(i,j))
                self.nb_coup+=1
                self.display()
    def refill(self):
        print("Refill des cases")
        L=self.grille.liste_vides()
        if len(L)>0:
            self.boucle_refill(L)
        else:
            
            if self.grille.recherche_pattern():
                self.echange_autorise=False
                self.after(self._time_interval,self.refill)
            elif self.grille.check_objectif():
                print("fin")
                self.end("Gagné")
            elif self.nb_coup==0:
                print("fin")
                self.end("Perdu")
            else:
                self.echange_autorise=True
                self.display()
                self.restart_window()
    def boucle_refill(self,L):
        if len(L)>0:
            if not self.grille.gestion_flux():
                self.grille.gestion_flux_secondaire()
            self.display()
            self.after(self._time_interval,self.boucle_refill,L[1:])
        else:
            self.display()
            self.after(self._time_interval,self.refill)
    def start(self):
        print("Start")
        self.grille.element_detruit={
            "roquette":0,
            "bombe":0,
            "avion":0,
            "déflagrateur":0,  
            "etoiles":0,
            "bonbon_normal":{
                "yellow":0,
                "blue":0,
                "red":0,
                "green":0,
                "magenta":0
            }
        }
        self.display()
        print(self.grille)
        self._music_player.play()
        self.mainloop()