#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import *
import tkinter.font as tkFont
import tkinter
import math as m

class Pendule(object):
    "Instanciation de l'objet pendule"

    def __init__(self, t0, tn, u10, u20, v10, v20, m1, m2, l1, l2, g, n):
        "Constructeur de la classe pendule"

        self.t0=t0
        self.tn=tn
        self.u10=u10
        self.u20=u20
        self.v10=v10
        self.v20=v20
        self.m1=m1
        self.m2=m2
        self.l1=l1
        self.l2=l2
        self.g=g
        self.n=n
        self.i=1

    def home(self):
        "Fenêtre de configuration"

        self.fenetre_home=Tk()
        self.fenetre_home.title('Configuration')
        self.fenetre_home.geometry('700x300')
        self.fenetre_home.resizable(width=False, height=False)
        icon=tkinter.Image("photo", file='icons/settings.gif')  #Fichier de l'icône
        self.fenetre_home.tk.call('wm', 'iconphoto', self.fenetre_home._w, icon)

        self.ButtonFrame=LabelFrame(self.fenetre_home, text='Actions')
        self.ButtonFrame.grid(row=0, column=1, padx=10, pady=10)
        self.TimeFrame=LabelFrame(self.fenetre_home, text='Temps')
        self.TimeFrame.grid(row=0, column=0, padx=10, pady=10, ipadx=5, ipady=5, sticky='nsw')
        self.InitValuesFrame=LabelFrame(self.fenetre_home, text='Conditions Inititales')
        self.InitValuesFrame.grid(row=1, column=0)

        self.InitValuesFrame.grid_columnconfigure(0, weight=1)
        self.InitValuesFrame.grid_columnconfigure(3, weight=5)

        icon_start=PhotoImage(file='icons/start.gif')
        self.bouton_start=Button(self.ButtonFrame, text="Démarrer", image=icon_start, compound="left", command=self.start, height=30, width=110)
        self.bouton_start.grid(row=0, column=0, padx=5, pady=5)
        icon_reset=PhotoImage(file='icons/recycle.gif')
        self.bouton_reset=Button(self.ButtonFrame, text="Réinitialiser", image=icon_reset, compound="left", height=30, width=110)
        self.bouton_reset.grid(row=1, column=0, padx=5, pady=0)
        icon_quit=PhotoImage(file='icons/quit.gif')
        self.bouton_quit=Button(self.ButtonFrame, text="Quitter", image=icon_quit, compound="left", command=self.fenetre_home.destroy, height=30, width=110)
        self.bouton_quit.grid(row=2, column=0, padx=5, pady=5)


        self.t0_txt=Label(self.TimeFrame, text ='Date initiale:')
        self.t0_txt.grid(row=0, column=1)
        self.tn_txt=Label(self.TimeFrame, text ='Date finale:')
        self.tn_txt.grid(row=1, column=1)
        self.t0_ent=Entry(self.TimeFrame, width=7)
        self.t0_ent.grid(row=0, column=2)
        self.tn_ent=Entry(self.TimeFrame, width=7)
        self.tn_ent.grid(row=1, column=2)

        self.u10_txt=Label(self.InitValuesFrame, text ='θ1(0):')
        self.u10_txt.grid(row=0, column=1)
        self.u20_txt=Label(self.InitValuesFrame, text ='θ2(0):')
        self.u20_txt.grid(row=1, column=1)
        self.u10_ent=Entry(self.InitValuesFrame, width=7)
        self.u10_ent.grid(row=0, column=2)
        self.u20_ent=Entry(self.InitValuesFrame, width=7)
        self.u20_ent.grid(row=1, column=2)
        self.v10_txt=Label(self.InitValuesFrame, text ='v1(0):')
        self.v10_txt.grid(row=2, column=1)
        self.v20_txt=Label(self.InitValuesFrame, text ='v2(0):')
        self.v20_txt.grid(row=3, column=1)
        self.v10_ent=Entry(self.InitValuesFrame, width=7)
        self.v10_ent.grid(row=2, column=2)
        self.v20_ent=Entry(self.InitValuesFrame, width=7)
        self.v20_ent.grid(row=3, column=2)


        self.fenetre_home.mainloop()


    def pendule(self):
        "Méthode définissant le pendule"

        self.fenetre_pendule=Toplevel()  #Définition de la fenêtre et du canvas
        self.fenetre_pendule.title('Pendule double')
        icon=tkinter.Image("photo", file='icons/pendule.gif')  #Fichier de l'icône
        self.fenetre_pendule.tk.call('wm', 'iconphoto', self.fenetre_pendule._w, icon)
        self.can = Canvas(self.fenetre_pendule, width = 500, height = 500, bg='grey', highlightthickness=0)
        self.can.pack()

        self.menu_bar=Menu(self.fenetre_pendule)  #Création des menus
        self.fenetre_pendule.config(menu=self.menu_bar)
        self.file_menu=Menu(self.menu_bar, tearoff=0)
        self.help_menu=Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Fichier", menu=self.file_menu)
        self.file_menu.add_command(label="Nouveau", command=self.new)
        self.file_menu.add_command(label="Quitter", command=self.fenetre_home.destroy)
        self.menu_bar.add_cascade(label="Aide", menu=self.help_menu)
        self.help_menu.add_command(label="À propos", command=self.about)

        (self.T,self.U1,self.U2,self.V1,self.V2)=self.resolution(self.t0,self.tn,self.u10,self.u20,self.v10,self.v20,self.m1,self.m2,self.l1,self.l2,self.g,self.n)  #Appel de la résolution
        self.COORD1=self.conversion(self.U1,100)
        self.COORD2=self.conversion(self.U2,100)

        self.cx,self.cy=250,250 #Définition du système de coordonnées
        x1,y1=self.COORD1[0]
        x2,y2=self.COORD2[0]

        self.bras1 = self.can.create_line(self.cx, self.cy, self.cx+x1, self.cy+y1, fill = 'blue', width = 3)  #Création des objets du pendule
        self.bras2 = self.can.create_line(self.cx+x1, self.cy+y1, self.cx+x1+x2, self.cy+y1+y2, fill = 'green', width = 3)
        self.can.create_oval(self.cx-6,self.cy-6,self.cx+6,self.cy+6,fill='red')
        self.rond1 = self.can.create_oval(self.cx+x1-4, self.cy+y1-4, self.cx+x1+4, self.cy+y1+4, fill='black')
        self.rond2 = self.can.create_oval(self.cx+x1+x2-4, self.cy+y1+y2-4, self.cx+x1+x2+4, self.cy+y1+y2+4, fill='black')

        self.move()  #Appel de la méthode d'animation

        #self.fenetre_pendule.mainloop() 

    def resolution(self,t0,tn,u10,u20,v10,v20,m1,m2,l1,l2,g,n):
        "Méthode permettant la résolution des équations différentielles"

        pas=(tn-t0)/n
        T=[t0]
        U1=[u10]
        U2=[u20]
        V1=[v10]
        V2=[v20]
        for k in range(n):
            t1=t0+pas
            u11=u10+pas*v10
            u21=u20+pas*v20
            v11=v10+pas*((-g*(2*m1+m2)*m.sin(u10)-m2*g*m.sin(u10-2*u20)-2*m2*m.sin(u10-u20)*(l2*(v20)**2+l1*(v10)**2*m.cos(u10-u20)))/(l1*(2*m1+m2-m2*m.cos(2*u10-2*u20))))
            v21=v20+pas*(2*m.sin(u10-u20)*(l1*(m1+m2)*(v10)**2+g*(m1+m2)*m.cos(u10)+l2*m2*(v20)**2*m.cos(u10-u20))/(l2*(2*m1+m2-m2*m.cos(2*u10-2*u20))))
            T.append(t1)
            U1.append(u11)
            U2.append(u21)
            V1.append(v11)
            V2.append(v21)
            t0=t1
            u10=u11
            u20=u21
            v10=v11
            v20=v21
        return (T,U1,U2,V1,V2)


    def conversion(self,ANGLE,l):
        "Méthode permettant de passer des coordonnées polaires à carthésiennes"

        COORD=[]
        for k in range(len(ANGLE)):
            COORD.append((l*m.sin(ANGLE[k]),l*m.cos(ANGLE[k])))
        return COORD


    def move(self):
        "Méthode permettant l'animation du pendule"

        if self.i<len(self.COORD1):
            x1,y1=self.COORD1[self.i]
            x2,y2=self.COORD2[self.i]
            self.can.coords(self.bras1, self.cx, self.cy, self.cx+x1, self.cy+y1)  #Déplacement des objets
            self.can.coords(self.rond1, self.cx+x1-4, self.cy+y1-4, self.cx+x1+4, self.cy+y1+4)
            self.can.coords(self.bras2, self.cx+x1, self.cy+y1, self.cx+x1+x2, self.cy+y1+y2)
            self.can.coords(self.rond2, self.cx+x1+x2-4, self.cy+y1+y2-4, self.cx+x1+x2+4, self.cy+y1+y2+4)
            self.i+=1
            self.can.after(5, self.move)  #Répetition de la méthode

    def about(self):
        "Fenêtre About"

        self.fenetre_about=Toplevel() #Définition de la fenêtre
        self.fenetre_about.title('À propos')
        self.fenetre_about.geometry('250x150')
        icon=tkinter.Image("photo", file='icons/about.gif')  #Fichier de l'icône
        self.fenetre_about.tk.call('wm', 'iconphoto', self.fenetre_about._w, icon)
        self.fenetre_about.resizable(width=False, height=False)
        self.fenetre_about.transient(self.fenetre_pendule)
        self.fenetre_about.grab_set()
        font=tkFont.Font(size=13)
        Label(self.fenetre_about, text='Développé avec amour\npar Marc-Antoine GODDE', font=font).pack(padx=5, pady=10)
        Label(self.fenetre_about, text='Copyright © 2019').pack(padx=5, pady=5)
        self.bouton_ok=Button(self.fenetre_about, text='Ok', command=self.fenetre_about.destroy).pack(padx=5, pady=5)

    def new(self):
        "Double commande panneau configuration"

        self.fenetre_pendule.destroy()
        self.fenetre_home.deiconify()

    def start(self):
        "Double commande démarrage"

        self.fenetre_home.withdraw()
        self.pendule()


if __name__ == "__main__":

    pendule = Pendule(0,10000,m.pi+0.01,0,0,0,3,3,4,4,5,1000000)
    pendule.home()
