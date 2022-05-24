# -*- coding: utf-8 -*-
"""
Created on Mon May  2 11:28:26 2022 for MINI_POO project

@author: Alain ETIENNE - Arts et Métiers 2022
"""

import tkinter as TK
import tkinter.ttk as TTK
import xml.etree.ElementTree as ET
import tkinter.filedialog as TKFD
import random as RND


class Pimped_Entry(TK.Entry):
    ''' Zone de texte adaptée au besoin de porter des informations supplémentaires (gestion des flux d'éléments dans la cellule)'''

    def __init__(self, master, **param):
        super().__init__(master, **param)
        self._orientation = 270 # Par défaut le flux est vers le bas
        self._flux = str() # Par défaut la cellule n'est ni un puits ni une source
        
    def change_orientation(self):
        _values = [0,90,180,270]
        _index = (_values.index(self._orientation) + 1) % len(_values)
        self._orientation = _values[_index]
        print(self._orientation)
    
    def change_typeflux(self):
        _values = ["Puits", "Source", ""]
        _index = (_values.index(self._flux) + 1) % len(_values)
        self._flux = _values[_index]
        self.update_shape()
    
    def update_shape(self):
        _convention_couleurs = {"": "white", "Source":"green", "Puits":"red"}
        self.configure(bg =_convention_couleurs[self._flux])
        
    
    def _get_flux(self):
        return self._flux
    def _get_orientation(self):
        return self._orientation
    my_orientation = property(_get_orientation)
    my_flow = property(_get_flux)
                

class Interface():
    '''Classe gérant l'interface de conception de grille pour le projet MINI_POO'''
    
    def __init__(self, nbligne_grille, nbcolonne_grille):        
        self._grille =  {}
        self._fenetre = TK.Tk()
        self._fenetre.title("Générateur de niveau pour le projet MINI_POO")
        self._origine_grille = (5,1) # Position du coin haut gauche de la grille de zones de texte
        self._dimensions = (int(nbligne_grille) , int(nbcolonne_grille))
        
        self._titre = TK.StringVar()
        TK.Label(self._fenetre, text = "Nom de la carte :").grid(row = 0 , column = 0, sticky = "e")
        TK.Entry(self._fenetre, textvariable = self._titre).grid(row = 0 , column = 1, columnspan =  nbcolonne_grille, sticky = "w e", padx = 2, pady = 2)
        
        self._nb_coups = TK.IntVar()
        TK.Label(self._fenetre, text = "Nombre de coups :").grid(row = 2 , column = 0, sticky = "e")
        TK.Entry(self._fenetre, textvariable = self._nb_coups).grid(row = 2 , column = 1, columnspan =  nbcolonne_grille, sticky = "w e", padx = 2, pady = 2)
        
        self._nb_couleurs = TK.IntVar()
        self._nb_couleurs.set(2)
        TK.Label(self._fenetre, text = "Combien de couleurs [2, 5] :").grid(row = 1 , column = 0, sticky = "e")
        TK.Entry(self._fenetre, textvariable = self._nb_couleurs).grid(row = 1 , column = 1, columnspan =  nbcolonne_grille, sticky = "w e", padx = 2, pady = 2)
        
        TK.Label(self._fenetre, text = "Selectionner l'objectifs à atteindre :").grid(row = 3 , column = 0, sticky = "e")
        self._objectif = TTK.Combobox(self._fenetre)
        self._objectif["values"] = ["Bonus", "Etoiles", "green", "red", "yellow", "blue", "pink"]
        self._objectif.grid(row = 3 , column = 1, columnspan =  2, sticky = "w e", padx = 2, pady = 2)
        self._nb_objectif = TK.IntVar()
        TK.Entry(self._fenetre, textvariable = self._nb_objectif).grid(row = 3 , column = 3, columnspan =  2, sticky = "w e", padx = 2, pady = 2)
        TK.Button(self._fenetre, text = "Ajouter objectif", command = self.ajouter_un_objectif).grid(row = 3 , column = 5, columnspan =  nbcolonne_grille - 4, sticky = "w e", padx = 2, pady = 2)
        
        self._objectifs_crees = TK.Listbox(self._fenetre, height = 3)
        self._objectifs_crees.grid(row = 4 , column = 1, columnspan =  nbcolonne_grille, sticky = "w e", padx = 2, pady = 2)
        
        
        # Generation de la grille et stockage des entry pour capter leurs valeurs
        for _ligne in range(int(nbligne_grille)):
            for _colonne in range(int(nbcolonne_grille)):
                # Test de la zone de texte fait maison
                _entrytemp = Pimped_Entry(self._fenetre, width = 8)
                #_entrytemp = TK.Entry(self._fenetre, width = 8)
                
                self._grille[(_ligne,_colonne)] = _entrytemp
                _entrytemp.grid(row = self._origine_grille[0] + _ligne, column = self._origine_grille[1] + _colonne, padx = 2, pady = 2)
                
                # Test event arg
                _entrytemp.bind("<Double-Button-1>", self.dbl_clic_droit_entry)
                _entrytemp.bind("<Double-Button-2>", self.dbl_clic_gauche_entry)
                _entrytemp.bind("<Double-Button-3>", self.dbl_clic_gauche_entry)
                
        TK.Button(self._fenetre, text = "Générer la grille en XML", command = self.generer_XML, height = 3).grid(row = self._origine_grille[0] + nbligne_grille + 3, column = 0, columnspan = nbcolonne_grille + 1, sticky = "n s e w", padx = 2, pady = 2)
    
        self._fenetre.mainloop()
             
    def generer_XML(self):
        if self._titre.get() !="" and self._nb_couleurs.get() != "" and self._nb_coups.get() > 0:
            # Construction du contenu du fichier XML
            couleurs = ["green", "red", "yellow", "blue", "magenta"]
            tronc = ET.Element("Map", {"titre":self._titre.get(), "nb_coup":str(self._nb_coups.get()), "nb_colonnes":str(self._dimensions[1]), "nb_lignes":str(self._dimensions[0]), "couleurs": str(couleurs[:self._nb_couleurs.get()])})
            grille_XML = ET.Element("Grille")
            objectifs_XML = ET.Element("Objectifs")
            tronc.append(grille_XML)
            tronc.append(objectifs_XML)
            
            for _index in range(self._objectifs_crees.size()):
                _infos = self._objectifs_crees.get(_index).split("-")
                objectifs_XML.append(ET.Element("Objectif", {"Nombre":str(_infos[0]), "Cible":_infos[1]}))
            
            # Dictionnaires de gestion des codes saisis vers le XML
            dico_contenu = {"B":"Bombe", "A":"Avion", "RV":"Roquette verticale", "RH":"Roquette Horizontale", "D":"Deflagrateur", "E":"Etoile"}
            for i in range(1,self._nb_couleurs.get() + 1):
                dico_contenu[str(i)] = couleurs[i-1]
            dico_orientation = {"H":"Haut", "B":"Bas", "D":"Droit", "G":"Gauche"}
            print(dico_contenu)
                        
            for _key, _element in self._grille.items():
                if _element.get() == "":
                    # Cellule vide
                    grille_XML.append(ET.Element("Cellule_Vide", {"ligne":str(_key[0]) , "colonne":str(_key[1])}))
                
                else:
                    _options = {option[0]:option[1:] for  option in _element.get().replace(" ", "").split("-")}
        
                    _cellule = None
                    if "G" in _options:
                        _cellule = ET.Element("Cellule_Gelee", {"ligne":str(_key[0]) , "colonne":str(_key[1])})
                        _cellule.attrib["niveau_gel"] = _options["G"]
                    else:
                        _cellule = ET.Element("Cellule", {"ligne":str(_key[0]) , "colonne":str(_key[1])})
                    
                    if "C" in _options and _options["C"] in dico_contenu:
                        _cellule.attrib["contenu"] = dico_contenu[_options["C"]]
                    else:
                        # Il faut gérer le contenu d'une cellule à qui rien n'a été affecté ou un élément non autorisé (rnd)
                        # On choisi aléatoirement une couleur parmis celles autorisée
                        _cellule.attrib["contenu"] = dico_contenu[RND.randint(1,self._nb_couleurs.get())]
                    
                    if _element.my_flow != "Puits":
                        if "O" in _options and _options["O"] in dico_orientation:
                            _cellule.attrib["orientation"] = dico_orientation[_options["O"]]
                        else:
                            _cellule.attrib["orientation"] = "Bas"
                        
                    if _element.my_flow in ["Puits","Source"]:
                        _cellule.attrib["flux"] = _element.my_flow 
                    
                    if "T" in _options:
                        #  Vérification que la cible du TP est bien dans la grille (convention ligne, colonne)
                        coordonnees = _options["T"][1:-1].split(",")
                        if int(coordonnees[0]) <= self._dimensions[0] and int(coordonnees[1]) <= self._dimensions[1]:
                            _cellule.attrib["flux_tp_vers"] = _options["T"]
                        else:
                            TK.messagebox.showwarning(title = "Erreur de saisie pour une téléportation", message = "La cellule de coordonnées {} a un problème de dimension".format(_key)) 
                 
                    grille_XML.append(_cellule)
                            
            # Gestion du pretty XML
            def indent(elem, level=0):
                i = "\n" + level*"  "
                if len(elem):
                    if not elem.text or not elem.text.strip():
                        elem.text = i + "  "
                    if not elem.tail or not elem.tail.strip():
                        elem.tail = i
                    for elem in elem:
                        indent(elem, level+1)
                    if not elem.tail or not elem.tail.strip():
                        elem.tail = i
                else:
                    if level and (not elem.tail or not elem.tail.strip()):
                        elem.tail = i
            
            # Enregistrement dans un arbre XML et enregistrement du fichier associé
            indent(tronc)
            arbreXML = ET.ElementTree(tronc)
            cheminenregistrement = TKFD.asksaveasfilename(title = "Enregistrer la carte en XML..." , defaultextension = ".xml", filetypes = [("XML","*.xml")])
            if cheminenregistrement != "":
                arbreXML.write(cheminenregistrement)
                print("Ecriture du fichier XML réalisée au chemin précisé : {}".format(cheminenregistrement))    
            del(arbreXML)
            
        else:
            TK.messagebox.showwarning(title = "Erreur de saisie", message = "Plusieurs champs n'ont pas été saisis, veuillez les compléter")
        
    # Gestion des événements sur les contrôleS zone de texte
    def dbl_clic_droit_entry(self, event):
        if isinstance(event.widget, Pimped_Entry):
            event.widget.change_orientation()
    
    def dbl_clic_gauche_entry(self, event):
        if isinstance(event.widget, Pimped_Entry):
            event.widget.change_typeflux()

    def ajouter_un_objectif(self):
        if self._objectif.get() != "" and self._nb_objectif.get() > 0:
            self._objectifs_crees.insert('end', "{} - {}".format(self._nb_objectif.get(), self._objectif.get()))

# Lancement de l'interface de conception de carte:
Interface(9,10)