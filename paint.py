# -*- coding: utf-8 -*-
from Tkinter import *
import math
import random

#radioButton:
# fen = Tk()
# fen.title('Choix matériel')
# 
# frame = Frame(fen)
# frame.pack()
# myvar = StringVar(fen)
# def lireValeur():
	# print myvar.get()
	# print "--"
# 
# l1 = Label(frame, text="Type de matériel")
# 
# #myvar prend la valeur du bouton coché. Le texte est fixé ("Crayon")
# r1 = Radiobutton(frame,text="Crayon",variable=myvar,value="Crayon", command=lireValeur)
# r2 = Radiobutton(frame,text="Pinceau simple",variable=myvar,value="Pinceau simple", command=lireValeur)
# r3 = Radiobutton(frame,text="Pinceau zigzag",variable=myvar,value="Pinceau zigzag", command=lireValeur)
# 
# l1.grid(row=0, column=0)
# r1.grid(row=1, column=0)
# r2.grid(row=2, column=0)
# r3.grid(row=3, column=0)
# 
# fen.mainloop()

#slider:
fen = Tk()
fen.title('Largeur trait')
def ok(value):
	selection = "Valeur = "+ value
	lab.config(text=selection, fg='blue')
var = DoubleVar(fen)
scale = Scale(fen, variable=var, orient=HORIZONTAL, command=ok)
lab = Label(fen, text='Choisir la largeur du trait')
scale.pack(anchor=CENTER)
lab.pack()
fen.mainloop()


class main:
	def __init__(self,fen):
		self.fen = fen
		self.color_fg = 'black'#couleur du trait
		self.color_bg = 'white'#couleur de fond
		self.penwidth = var.get()
		self.vueWidgets()
		self.c.bind('<B1-Motion>',self.paint)#souris pressée et bouge
		self.c.bind('<Button-1>',self.downClick)#souris est pressée 
		self.c.bind('<ButtonRelease-1>',self.mouseRelease)#bouton relaché
		self.time=0#compte le nombre de formes dessinées pendant le dessin d'un trait
		self.lines=[]#pour stocker les objets qui forment un trait 
		self.list_stroke = []#pour stocker les traits
		self.max_mem = 100# nombre maximal de traits qu'on enregistre. au delà on efface le premier trait de la liste avant d'en rajouter
		
	
	
	#pinceaux et crayons:
	def crayon(self, x,y):
		"""dessine une ligne entre (x,y) et (old_x,old_y)"""
		if self.time>0:
			#dessine la ligne capstyle=ROUND arrondis les fin de trait et permet des jonctions sans trous 
			self.lines.append(self.c.create_line(self.old_x,self.old_y,x,y,width=self.penwidth,fill=self.color_fg,capstyle=ROUND))
		self.old_x = x
		self.old_y = y
	
	def pinceau(self,x,y):
		if(self.time>0): #initialisations au temps 0
			self.lines.append(fill=self.color_fg)
			self.old_ax = x#pour le point 0 la largeur est nulle
			self.old_ay = y
			self.old_bx = x
			self.old_by = y
			self.old_x = x
			self.old_y = y
			
		else:	
			#calcule la largeur du pinceau à partir du temps (nombre de polygones dejà dessinés)
			largeur = self.penwidth*1/(1+1.0/(0.4*self.time))
			#****************************************************************
			#calcul du vecteur normé perpendiculaire au trait
			dx = x-self.old_x
			dy = y-self.old_y
			norm = math.sqrt(dx*dx+dy*dy)
			#normalize and perpendicular:
			if norm!=0:
				fool= dx
				dx = -dy/norm
				dy = fool/norm
				ax = x+dx*largeur
				ay = y+dy*largeur
				bx = x-dx*largeur
				by = y-dy*largeur
			else:
				ax = old_ax
				ay = old_ay
				bx = old_bx
				by = old_by
				dx =0
				dy = 0
			#****************************************************************	
			#calcul des points a et b:
			ax = x+dx*largeur
			ay = y+dy*largeur
			bx = x-dx*largeur
			by = y-dy*largeur
			#****************************************************************	
			#le polygone
			coords = [self.old_ax,self.old_ay,self.old_bx,self.old_by,bx,by,ax,ay]
			#****************************************************************	
			#dessiner le polygone
			poly = self.c.create_polygon(coords,outline=self.color_fg, fill=self.color_fg)
			#****************************************************************
			#remplacer les anciennes coordonnées pour le polygone suivant:
			self.old_ax = ax#pour le point 0 largeur =0
			self.old_ay = ay
			self.old_bx = bx
			self.old_by = by
			self.old_x = x
			self.old_y = y
			#renvoyer l'objet polygone, utile si on veut le mettre dans une liste afin 
			#de pouvoir l'effacer ou le modifier plus tard
			return poly
		
				
	#événements:
	def downClick(self,e):
		"""méthode appelée quand la souris est pressée"""
		self.time=0
		self.paint(e)

	def paint(self,e):
		"""dessine quand la souris bouge"""
		if(self.var1.get()==0):#simple lines
			self.crayon(e.x, e.y)
		self.time+=1
		
			
	def mouseRelease(self,e):# 
		""" quand la souris est relachée"""
		if(self.var1.get() == 0):
			#ajoute le trait à la liste des traits. La fonction list()
			#permet de copier la liste entière et non juste l'adresse
			self.list_stroke.append(list(self.lines))
			self.lines = []#le trait est une liste vide
		if(len(self.list_stroke)>self.max_mem):
			self.list_stroke.pop(0)#enlève le premier el. de la liste si elle est trop longue
	def effaceDernier(self):
		"""efface le dernier trait"""
		if(len(self.list_stroke)>0):
			for el in self.list_stroke.pop():
				self.c.delete(el)

	
	#une fonction qui va effacer tout le contenu du canvas
	def effaceTout(self):
		"""efface tout le contenu"""
		self.c.delete('all')


	#deux fonctions pour convertir les couleurs car 
	#les couleurs de Tkinter sont au format hexadécimal
	# par exemple : rouge = "#ff0000"
	def convert_rgb(self,r,g,b):
		"convertit les couleurs de r,g,b à hexadécimal"
		return '#{:02x}{:02x}{:02x}'.format( r, g , b )
	def convert_hex(self,hex):
		"convertit lées couleurs de hexadécimal à un tuple (r,g,b)"
		#la fonction int() permet de convertir automatiquement un nombre  hexadécimal
		# dans le format 0x123 en un entier. On sépare le nombre #abcdef en trois couleurs 
		# hexadécimales ab, cd, ef, on rajoute le préfixe 0x  et on les convertit avec int():
		return (int("0x"+hex[1:3], 16),int("0x"+hex[3:5], 16),int("0x"+hex[5:7], 16))
	#################################################################################
	#vue des widgets:
	#################################################################################	
	def vueWidgets(self):
		#************************paint widgets:********************************
		self.controls = Frame(self.fen,padx = 5,pady = 5)
		#*************************Le canvas*************************************
		self.c = Canvas(self.fen,width=600,height=600,bg=self.color_bg,borderwidth=1, relief="solid")
		self.c.pack(fill=BOTH,expand=True)
		
		#*************************menus*************************************
		menu = Menu(self.fen)
		menucouleurs = Menu(self.fen)
		self.fen.config(menu=menu)
		#menus  Outils:
		self.var1 = IntVar()
		self.var1.set(0)#choix de départ
		
		
		menu1 = Menu(self.fen)
		self.menu.add_cascade(label="Outils", menu = menu1)
		menu1.add_radiobutton(label="Crayon", value = 0, variable=self.var1)
		menu1.add_radiobutton(label="Pinceau simple", value = 1, variable=self.var1)
		menu1.add_radiobutton(label="Pinceau zigzag", value = 2, variable=self.var1)
		menu1.add_command(label='Effacer le dernier trait',command=self.effaceDernier)
		menu1.add_command(label='Effacer tout',command=self.effaceTout)
		
		menu1.add_separator()
		
		menucouleurs = Menu(self.fen)
		self.menu.add_cascade(label='Couleurs',menu=menucouleurs)
        menucouleurs.add_command(label='Couleur')
        menucouleurs.add_command(label='Couleur de fond')
		#************************************************************************
		
fen = Tk()
main(fen)
fen.title('Paint')
fen.mainloop()