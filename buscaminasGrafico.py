# -*- coding: utf-8 -*-
# ! /usr/bin/env python
"""Hecho por David Meléndez Díez y Alejandro Nieto Gallego"""

#Buscaminas v2 (Gráfico)

# CONSTANTES

COE = u'\u2500'  # ─
CNS = u'\u2502'  # │
CES = u'\u250C'  # ┌
CSO = u'\u2510'  # ┐
CNE = u'\u2514'  # └
CON = u'\u2518'  # ┘
COES = u'\u252C'  # ┬
CNES = u'\u251C'  # ├
CONS = u'\u2524'  # ┤
CONE = u'\u2534'  # ┴
CSOM = u'\u2593'  # ▒

# IMPORTS
import pygtk

pygtk.require("2.0")
import gtk
from random import randint
from time import time
import gobject


class Buscaminas:

	def __init__(self):
		self.primeraJugada = True
		self.seguir = True
		self.imagenes = [] #Se crea una lista con las imágenes de las celdas, del botón de reinicio y la imagen final
		self.imagenes.append(gtk.gdk.pixbuf_new_from_file("Imagenes/abierta.png"))
		self.imagenes.append(gtk.gdk.pixbuf_new_from_file("Imagenes/uno.png"))
		self.imagenes.append(gtk.gdk.pixbuf_new_from_file("Imagenes/dos.png"))
		self.imagenes.append(gtk.gdk.pixbuf_new_from_file("Imagenes/tres.png"))
		self.imagenes.append(gtk.gdk.pixbuf_new_from_file("Imagenes/cuatro.png"))
		self.imagenes.append(gtk.gdk.pixbuf_new_from_file("Imagenes/cinco.png"))
		self.imagenes.append(gtk.gdk.pixbuf_new_from_file("Imagenes/seis.png"))
		self.imagenes.append(gtk.gdk.pixbuf_new_from_file("Imagenes/cerrada.png"))
		self.imagenes.append(gtk.gdk.pixbuf_new_from_file("Imagenes/marcada.png"))
		self.imagenes.append(gtk.gdk.pixbuf_new_from_file("Imagenes/malmarcada.png"))
		self.imagenes.append(gtk.gdk.pixbuf_new_from_file("Imagenes/question.png"))
		self.imagenes.append(gtk.gdk.pixbuf_new_from_file("Imagenes/boom.png"))
		self.imagenes.append(gtk.gdk.pixbuf_new_from_file("Imagenes/mina.png"))
		self.imagenes.append(gtk.gdk.pixbuf_new_from_file("Imagenes/imagenFinal.jpg"))
		self.imagenes.append(gtk.gdk.pixbuf_new_from_file("Imagenes/caritaFeliz.png"))
		self.imagenes.append(gtk.gdk.pixbuf_new_from_file("Imagenes/caritaTriste.png"))
		self.imagenes.append(gtk.gdk.pixbuf_new_from_file("Imagenes/caritaGafas.png"))
		self.menuInicial()
		return None

	def menuInicial(self):
		self.builder = gtk.Builder()
		self.builder.add_from_file("buscaminasGrafico.glade")
		#Se importa y configura la ventana que se mostrará cuando explote una mina
		self.ventanaExplosion = self.builder.get_object("ventanaExplosion")
		self.ventanaExplosion.set_default_size(775, 500)
		self.ventanaExplosion.set_position(gtk.WIN_POS_CENTER_ALWAYS)
		self.ventanaExplosion.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("black"))
		self.ventanaExplosion.connect("destroy",self.hideWindow,self.ventanaExplosion)
		self.fixedExplosion = self.builder.get_object("fixedExplosion")
		self.fixedExplosion.show()
		self.boxExplosion = gtk.EventBox()
		self.imagenExplosion = gtk.Image()
		self.imagenExplosion.set_from_pixbuf(self.imagenes[13])
		self.boxExplosion.add(self.imagenExplosion)
		self.boxExplosion.show()
		self.imagenExplosion.show()
		self.fixedExplosion.put(self.boxExplosion,50,50)
		#Se crea una eventBox con una imagen que funciona como "botón" para reiniciar la partida
		self.fixedReinicio = self.builder.get_object("fixedReinicio")
		self.boxReinicio = gtk.EventBox()
		self.imagenReinicio = gtk.Image()
		self.imagenReinicio.set_from_pixbuf(self.imagenes[14])
		self.boxReinicio.add(self.imagenReinicio)
		self.boxReinicio.connect("button-release-event", self.reiniciar)
		self.boxReinicio.show()
		self.imagenReinicio.show()
		self.fixedReinicio.put(self.boxReinicio, -25, 10)
		#Se guardan referencias a etiquetas necesarias para la pantalla de juego
		self.etiquetaMinasRestantes = self.builder.get_object("minasRestantes")
		self.etiquetaMarcadas = self.builder.get_object("marcadas")
		self.etiquetaMensajes = self.builder.get_object("label2")
		self.etiquetaMensajes.set_label("\n\n \n")
		self.etiquetaMensajes.show()
		# Se crea la ventana del menú inicial
		ventanaMenu = self.builder.get_object("window1")
		ventanaMenu.set_default_size(400, 300)
		ventanaMenu.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("#F2F5A9"))
		ventanaMenu.show()
		ventanaMenu.connect("destroy", gtk.main_quit)
		ventanaMenu.set_position(gtk.WIN_POS_CENTER_ALWAYS)
		etiqueta = self.builder.get_object("label1")
		etiqueta.show()
		boton1 = self.builder.get_object("button1")
		boton1.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("#E0ECF8"))
		boton1.show()
		boton1.connect("clicked", self.dificultad, "facil")
		boton1.connect("clicked", self.hideWindow, ventanaMenu)
		boton2 = self.builder.get_object("button2")
		boton2.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("#E0ECF8"))
		boton2.show()
		boton2.connect("clicked", self.dificultad, "intermedio")
		boton2.connect("clicked", self.hideWindow, ventanaMenu)
		boton3 = self.builder.get_object("button3")
		boton3.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("#E0ECF8"))
		boton3.show()
		boton3.connect("clicked", self.dificultad, "experto")
		boton3.connect("clicked", self.hideWindow, ventanaMenu)
		boton4 = self.builder.get_object("button4")
		boton4.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("#E0ECF8"))
		boton4.show()
		boton4.connect("clicked", self.dificultad, "fichero")
		boton4.connect("clicked", self.hideWindow, ventanaMenu)
		boton5 = self.builder.get_object("button5")
		boton5.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("#FA5858"))
		boton5.show()
		boton5.connect("clicked", gtk.main_quit)
		return None

	def hideWindow(self, widget, ventana):
		ventana.hide()
		return None

	def dificultad(self, widget, modo=None):
		#Función que crea los tableros y parámetros adecuados a la dificultad elegida por el usuario
		self.modo = modo
		self.marcadas = 0
		self.descubiertas = 0
		self.explosiones = 0
		self.num_aperturas = 0
		self.etiquetaMarcadas.set_label("Marcadas: 0")
		if modo == "facil":
			self.filas = 9
			self.columnas = 9
			self.minas = 10
			self.etiquetaMinasRestantes.set_label("Minas restantes: "+str(self.minas))
			self.minas_restantes = self.minas
			self.tableroOculto = self.generarTableroOculto(self.filas, self.columnas, self.minas)
			self.tableroUsuario = self.generarTablero(self.filas, self.columnas)
			self.crearVentana(self.filas, self.columnas)
		elif modo == "intermedio":
			self.filas = 16
			self.columnas = 16
			self.minas = 40
			self.etiquetaMinasRestantes.set_label("Minas restantes: "+str(self.minas))
			self.minas_restantes = self.minas
			self.tableroOculto = self.generarTableroOculto(self.filas, self.columnas, self.minas)
			self.tableroUsuario = self.generarTablero(self.filas, self.columnas)
			self.crearVentana(self.filas, self.columnas)
		elif modo == "experto":
			self.filas = 16
			self.columnas = 27
			self.minas = 99
			self.etiquetaMinasRestantes.set_label("Minas restantes: "+str(self.minas))
			self.minas_restantes = self.minas
			self.tableroOculto = self.generarTableroOculto(self.filas, self.columnas, self.minas)
			self.tableroUsuario = self.generarTablero(self.filas, self.columnas)
			self.crearVentana(self.filas, self.columnas)
		elif modo == "fichero":
			ficheroDialog=gtk.FileChooserDialog("Abrir fichero",None,gtk.FILE_CHOOSER_ACTION_OPEN,(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
			 gtk.STOCK_OPEN, gtk.RESPONSE_OK))
			if ficheroDialog.run()==gtk.RESPONSE_OK:
				nombreFichero=ficheroDialog.get_filename()
			else:
				nombreFichero=None
				self.menuInicial()
			ficheroDialog.destroy()

			try:

				fichero = open(nombreFichero, "r")
				listaLineas = fichero.readlines()

				# Cogemos el primer elemento de listaLineas que corresponde a la primera linea (string) y lo convertimos en lista despreciando el "espacio"
				primeraLinea = listaLineas[0].split()
				self.filas = int(primeraLinea[0])
				self.columnas = int(primeraLinea[1])

				if self.filas > 30 or self.columnas > 30:
					self.etiquetaMensajes.set_markup('<span color="red">\n\n   LAS DIMENSIONES DEL TABLERO EXCEDEN LOS LÍMITES ESPECIFICADOS\n</span>')

				else:
					self.minas = 0

					# Convertimos listaLineas en una matriz similar a las que usan nuestras funciones descartando la primera linea
					listaLineas = listaLineas[1:]
					self.tableroOculto = [[" "] * self.columnas for i in range(self.filas)]
					#Generamos una copia de tableroOculto para cuando el usuario reinicie la partida poder recrearlo
					self.tableroOcultoInicial = [[" "] * self.columnas for i in range(self.filas)]

					for i in range(self.filas):
						for j in range(self.columnas):
							if listaLineas[i][j] == "*":
								self.minas += 1
								self.tableroOculto[i][j] = "*"
								self.tableroOcultoInicial[i][j] = "*"

					n = 0
					for i in range(self.filas):
						for j in range(self.columnas):
							n = self.detectarVecinas(i, j, self.tableroOculto, "*", self.filas, self.columnas)
							if self.tableroOculto[i][j] != "*":
								if n != 0:
									self.tableroOculto[i][j] = str(n)
									self.tableroOcultoInicial[i][j] = str(n)
								else:
									self.tableroOculto[i][j] = " "
									self.tableroOcultoInicial[i][j] = " "

					self.etiquetaMinasRestantes.set_label("Minas restantes: " + str(self.minas))
					self.minas_restantes = self.minas
					self.tableroUsuario = self.generarTablero(self.filas, self.columnas)
					self.crearVentana(self.filas, self.columnas)


				fichero.close()


			except:
				self.etiquetaMensajes.set_markup('<span color="red">\n\n   ERROR AL ABRIR, LEER EL FICHERO O FICHERO INVÁLIDO\n</span>')

		else:
			print "Algo va mal" #Este print nunca debería ejecutarse
		return None

	def crearVentana(self, filas, columnas):
		#Función que crea una ventana según el número de filas y columnas dado
		self.botonResolver=self.builder.get_object("hack")
		self.botonResolver.connect("clicked",self.solve,self.tableroOculto,filas,columnas)
		self.botonResolver.show()

		self.etiquetaMensajes.set_label("\n\n  \n")
		self.ventana = self.builder.get_object("window2")
		self.ventana.set_default_size(19*columnas+370, 22*filas+70)
		self.ventana.show()
		self.ventana.connect("destroy", gtk.main_quit)
		self.ventana.set_position(gtk.WIN_POS_CENTER_ALWAYS)
		fixed = self.builder.get_object("fixed")
		fixed.show()
		self.timer_etq = self.builder.get_object("timer")
		#Bucle en el que se crean eventBoxes a las que se añade la imagen de la celda. Luego se conecta cada eventBox al evento button-release-event y se la añade al fixed

		for columna in range(columnas):
			for fila in range(filas):
				box = gtk.EventBox()
				imagen = gtk.Image()
				imagen.set_from_pixbuf(self.imagenes[7])
				box.add(imagen)
				box.connect("button-release-event", self.coordenadas, [columna, fila])
				box.show()
				imagen.show()
				if fila%2==0:
					fixed.put(box,170+columna*20+9,15+fila*22)
				else:
					fixed.put(box,170+columna*20,15+fila*22)

		#Obtenemos una lista de las eventBoxes colocadas en el contenedor fixed "por COLUMNAS"
		self.boxes = self.builder.get_object("fixed").get_children()
		#Es decir,self.boxes[0] es la eventBox de la celda de la columna 0 y fila 0;self.boxes[1] la de la celda de la columna 0 y fila 1
		self.tableroImagen = [[0] * columnas for i in range(filas)]
		a = 0
		#Recorrido por columnas
		for j in range(columnas):
			for i in range(filas):
				imagen = self.boxes[a].get_children()
				self.tableroImagen[i][j] = imagen[0]# De esta forma tenemos referencia al gtk.Image de cada celda
				a = a + 1

		return None

	def reiniciar(self,widget, event):
		#Función que reestablece los parámetros iniciales de la partida
		self.etiquetaMensajes.set_label("\n\n ")
		self.seguir = True
		self.explosiones = 0
		self.descubiertas = 0
		if self.timer!=None:
			gobject.source_remove(self.timer)
			self.timer=None
		self.timer_etq.set_label("Tiempo: 00:00")
		if event.button == 1:
			self.marcadas = 0
			self.minas_restantes = self.minas
			self.num_aperturas = 0
			self.boxReinicio.child.set_from_pixbuf(self.imagenes[14])
			self.primeraJugada = True
			if self.modo=="fichero":
				self.tableroOculto = [[" "] * self.columnas for i in range(self.filas)]
				#Recuperamos el tableroOculto inicial a partir de la "copia" generada al principio
				for i in range(self.filas):
					for j in range(self.columnas):
						self.tableroOculto[i][j]=self.tableroOcultoInicial[i][j]
			else:
				self.tableroOculto = self.generarTableroOculto(self.filas, self.columnas, self.minas)
			self.tableroUsuario = self.generarTablero(self.filas, self.columnas)
			self.etiquetaMarcadas.set_label(" Marcadas: " + str(self.marcadas))
			self.etiquetaMinasRestantes.set_label("Minas Restantes: " + str(self.minas_restantes))
			for i in range(self.filas):
				for j in range(self.columnas):
					self.tableroImagen[i][j].set_from_pixbuf(self.imagenes[7])
		return None


	def temporizador(self, tiempoIn):
		tiempo = int(time() - tiempoIn)
		self.timer_etq.set_label("Tiempo: {0:02}:{1:02}".format(tiempo / 60, tiempo % 60))
		return True

	def traducir(self, tableroUsuario,filas, columnas):
		#Función que "traduce" el tableroUsuario que se mostraba por consola en la anterior práctica a
		#la ventana gráfica mediante una asocicación de los caracteres de tableroUsuario con las imágenes
		#de las celdas y una modificación de la referencia al hijo de cada eventBox contenida en tableroImagen
		for fil in range(filas):
			for col in range(columnas):
				if tableroUsuario[fil][col] == CSOM:
					self.tableroImagen[fil][col].set_from_pixbuf(self.imagenes[7])
				if tableroUsuario[fil][col]==" ":
					self.tableroImagen[fil][col].set_from_pixbuf(self.imagenes[0])
				if tableroUsuario[fil][col]=="?":
					self.tableroImagen[fil][col].set_from_pixbuf(self.imagenes[10])
				if tableroUsuario[fil][col] == "1":
					self.tableroImagen[fil][col].set_from_pixbuf(self.imagenes[1])
				if tableroUsuario[fil][col] == "2":
					self.tableroImagen[fil][col].set_from_pixbuf(self.imagenes[2])
				if tableroUsuario[fil][col] == "3":
					self.tableroImagen[fil][col].set_from_pixbuf(self.imagenes[3])
				if tableroUsuario[fil][col] == "4":
					self.tableroImagen[fil][col].set_from_pixbuf(self.imagenes[4])
				if tableroUsuario[fil][col] == "5":
					self.tableroImagen[fil][col].set_from_pixbuf(self.imagenes[5])
				if tableroUsuario[fil][col] == "6":
					self.tableroImagen[fil][col].set_from_pixbuf(self.imagenes[6])
				if tableroUsuario[fil][col] == "X":
					self.tableroImagen[fil][col].set_from_pixbuf(self.imagenes[8])
				if tableroUsuario[fil][col] == "*":
					self.tableroImagen[fil][col].set_from_pixbuf(self.imagenes[12])
				if tableroUsuario[fil][col] == "#":
					self.tableroImagen[fil][col].set_from_pixbuf(self.imagenes[9])

		return None

	def solve(self,widget,tablero,filas,columnas):
		self.traducir(tablero,filas,columnas)


	def detectarVecinas(self, filaElegida, columnaElegida, tablero, caracter, filas, columnas):
		# Funcion que devuelve el número de celdas vecinas con el caracter especificado

		vecinasMarcadas = 0

		if filaElegida != 0 and columnaElegida != 0 and filaElegida != filas - 1 and columnaElegida != columnas - 1 and filaElegida % 2 != 0:

			if tablero[filaElegida - 1][columnaElegida] == caracter:
				vecinasMarcadas += 1

			if tablero[filaElegida - 1][columnaElegida - 1] == caracter:
				vecinasMarcadas += 1

			if tablero[filaElegida][columnaElegida - 1] == caracter:
				vecinasMarcadas += 1

			if tablero[filaElegida][columnaElegida + 1] == caracter:
				vecinasMarcadas += 1

			if tablero[filaElegida + 1][columnaElegida] == caracter:
				vecinasMarcadas += 1

			if tablero[filaElegida + 1][columnaElegida - 1] == caracter:
				vecinasMarcadas += 1

			return vecinasMarcadas

		elif filaElegida != 0 and columnaElegida != 0 and filaElegida != filas - 1 and columnaElegida != columnas - 1 and filaElegida % 2 == 0:

			if tablero[filaElegida - 1][columnaElegida] == caracter:
				vecinasMarcadas += 1

			if tablero[filaElegida - 1][columnaElegida + 1] == caracter:
				vecinasMarcadas += 1

			if tablero[filaElegida][columnaElegida - 1] == caracter:
				vecinasMarcadas += 1

			if tablero[filaElegida][columnaElegida + 1] == caracter:
				vecinasMarcadas += 1

			if tablero[filaElegida + 1][columnaElegida] == caracter:
				vecinasMarcadas += 1

			if tablero[filaElegida + 1][columnaElegida + 1] == caracter:
				vecinasMarcadas += 1

			return vecinasMarcadas

		elif columnaElegida == 0 and filaElegida == 0:
			if tablero[0][1] == caracter:
				vecinasMarcadas += 1

			if tablero[1][0] == caracter:
				vecinasMarcadas += 1

			if tablero[1][1] == caracter:
				vecinasMarcadas += 1

			return vecinasMarcadas

		elif columnaElegida == 0 and filaElegida == filas - 1 and filas % 2 != 0:

			if tablero[filas - 2][0] == caracter:
				vecinasMarcadas += 1

			if tablero[filas - 2][1] == caracter:
				vecinasMarcadas += 1

			if tablero[filas - 1][1] == caracter:
				vecinasMarcadas += 1

			return vecinasMarcadas

		elif columnaElegida == columnas - 1 and filaElegida == 0:

			if tablero[0][columnas - 2] == caracter:
				vecinasMarcadas += 1

			if tablero[1][columnas - 1] == caracter:
				vecinasMarcadas += 1

			return vecinasMarcadas

		elif columnaElegida == columnas - 1 and filaElegida == filas - 1 and filas % 2 != 0:

			if tablero[filas - 2][columnas - 1] == caracter:
				vecinasMarcadas += 1

			if tablero[filas - 1][columnas - 2] == caracter:
				vecinasMarcadas += 1

			return vecinasMarcadas

		elif columnaElegida == 0 and filaElegida == filas - 1 and filas % 2 == 0:

			if tablero[filas - 2][0] == caracter:
				vecinasMarcadas += 1

			if tablero[filas - 1][1] == caracter:
				vecinasMarcadas += 1

			return vecinasMarcadas

		elif columnaElegida == columnas - 1 and filaElegida == filas - 1 and filas % 2 == 0:

			if tablero[filas - 2][columnas - 1] == caracter:
				vecinasMarcadas += 1

			if tablero[filas - 1][columnas - 2] == caracter:
				vecinasMarcadas += 1

			if tablero[filas - 2][columnas - 2] == caracter:
				vecinasMarcadas += 1

			return vecinasMarcadas

		elif columnaElegida == 0:
			if filaElegida % 2 != 0:

				if tablero[filaElegida - 1][0] == caracter:
					vecinasMarcadas += 1

				if tablero[filaElegida][1] == caracter:
					vecinasMarcadas += 1

				if tablero[filaElegida + 1][0] == caracter:
					vecinasMarcadas += 1

				return vecinasMarcadas

			else:
				if tablero[filaElegida - 1][0] == caracter:
					vecinasMarcadas += 1

				if tablero[filaElegida][1] == caracter:
					vecinasMarcadas += 1

				if tablero[filaElegida - 1][1] == caracter:
					vecinasMarcadas += 1

				if tablero[filaElegida + 1][1] == caracter:
					vecinasMarcadas += 1

				if tablero[filaElegida + 1][0] == caracter:
					vecinasMarcadas += 1

				return vecinasMarcadas

		elif filaElegida == 0:

			if tablero[0][columnaElegida - 1] == caracter:
				vecinasMarcadas += 1

			if tablero[1][columnaElegida] == caracter:
				vecinasMarcadas += 1

			if tablero[1][columnaElegida + 1] == caracter:
				vecinasMarcadas += 1

			if tablero[0][columnaElegida + 1] == caracter:
				vecinasMarcadas += 1

			return vecinasMarcadas

		elif filaElegida == filas - 1:

			if tablero[filas - 1][columnaElegida - 1] == caracter:
				vecinasMarcadas += 1

			if tablero[filas - 2][columnaElegida] == caracter:
				vecinasMarcadas += 1

			if tablero[filas - 1][columnaElegida + 1] == caracter:
				vecinasMarcadas += 1

			if tablero[filas - 2][columnaElegida + 1] == caracter:
				vecinasMarcadas += 1

			return vecinasMarcadas

		elif columnaElegida == columnas - 1 and filaElegida % 2 != 0:

			if tablero[filaElegida - 1][columnaElegida - 1] == caracter:
				vecinasMarcadas += 1

			if tablero[filaElegida - 1][columnaElegida] == caracter:
				vecinasMarcadas += 1

			if tablero[filaElegida][columnaElegida - 1] == caracter:
				vecinasMarcadas += 1

			if tablero[filaElegida + 1][columnaElegida - 1] == caracter:
				vecinasMarcadas += 1

			if tablero[filaElegida + 1][columnaElegida] == caracter:
				vecinasMarcadas += 1

			return vecinasMarcadas

		elif columnaElegida == columnas - 1 and filaElegida % 2 == 0:

			if tablero[filaElegida + 1][columnaElegida] == caracter:
				vecinasMarcadas += 1

			if tablero[filaElegida - 1][columnaElegida] == caracter:
				vecinasMarcadas += 1

			if tablero[filaElegida][columnaElegida - 1] == caracter:
				vecinasMarcadas += 1

			return vecinasMarcadas

	def generarTableroOculto(self, filas, columnas, minas):
		# Crea un tablero oculto aleatorio

		tableroOculto = [[" "] * columnas for i in range(filas)]

		# Colocación aleatoria de minas
		while minas != 0:
			filaAleatoria = randint(0, filas - 1)
			columnaAleatoria = randint(0, columnas - 1)

			if tableroOculto[filaAleatoria][columnaAleatoria] != "*":
				tableroOculto[filaAleatoria][columnaAleatoria] = "*"
				minas -= 1

		n = 0
		for i in range(filas):
			for j in range(columnas):
				n = self.detectarVecinas(i, j, tableroOculto, "*", self.filas, self.columnas)
				if tableroOculto[i][j] != "*":
					if n != 0:
						tableroOculto[i][j] = str(n)
					else:
						tableroOculto[i][j] = " "

		return tableroOculto

	def generarTablero(self, filas, columnas):
		# Devuelve el tablero corespondiente a la opción elegida en su estado inicial

		tablero = [[CSOM] * columnas for i in range(filas)]
		return tablero

	def actualizarTablero(self, filas, columnas, tableroUsuario, tableroOculto):
		# Actualiza el numero relativo de minas por descubrir de cada casilla del tableroOculto y del tableroUsuario si procede
		for k in range(filas):
			for h in range(columnas):
				numMinas = self.detectarVecinas(k, h, tableroOculto, "*",filas,columnas)
				numMarcadas = self.detectarVecinas(k, h, tableroUsuario, "X",filas,columnas)
				numMinasRelativo = numMinas - numMarcadas

				if tableroOculto[k][h] != "*":
					if numMinasRelativo < 0:
						tableroOculto[k][h] = "?"
						if tableroUsuario[k][h] != CSOM and tableroUsuario[k][h] != "X":
							tableroUsuario[k][h] = tableroOculto[k][h]

					elif numMinasRelativo == 0:
						self.tableroOculto[k][h] = " "
						if tableroUsuario[k][h] != CSOM and tableroUsuario[k][h] != "X":
							tableroUsuario[k][h] = tableroOculto[k][h]
					else:
						tableroOculto[k][h] = str(numMinasRelativo)
						if tableroUsuario[k][h] != CSOM and tableroUsuario[k][h] != "X":
							tableroUsuario[k][h] = tableroOculto[k][h]
		return None

	def aperturaRecursiva(self, filaElegida, columnaElegida, filas, columnas, tableroUsuario, tableroOculto):
		# Si explota una mina se retorna un 1.En otro caso se retorna un 0.También altera el estado de tableroUsuario

		explosiones = 0
		if filaElegida != 0 and columnaElegida != 0 and filaElegida != filas - 1 and columnaElegida != columnas - 1 and filaElegida % 2 != 0:

			if tableroUsuario[filaElegida - 1][columnaElegida] == CSOM:
				if tableroOculto[filaElegida - 1][columnaElegida] == " ":
					tableroUsuario[filaElegida - 1][columnaElegida] = " "
					self.aperturaRecursiva(filaElegida - 1, columnaElegida, filas, columnas, tableroUsuario,
										   tableroOculto)
				elif tableroOculto[filaElegida - 1][columnaElegida] == "*":
					explosiones = 1
				else:
					tableroUsuario[filaElegida - 1][columnaElegida] = tableroOculto[filaElegida - 1][columnaElegida]

			if tableroUsuario[filaElegida - 1][columnaElegida - 1] == CSOM:
				if tableroOculto[filaElegida - 1][columnaElegida - 1] == " ":
					tableroUsuario[filaElegida - 1][columnaElegida - 1] = " "
					self.aperturaRecursiva(filaElegida - 1, columnaElegida - 1, filas, columnas, tableroUsuario,
										   tableroOculto)
				elif tableroOculto[filaElegida - 1][columnaElegida - 1] == "*":
					explosiones = 1

				else:
					tableroUsuario[filaElegida - 1][columnaElegida - 1] = tableroOculto[filaElegida - 1][
						columnaElegida - 1]

			if tableroUsuario[filaElegida][columnaElegida - 1] == CSOM:
				if tableroOculto[filaElegida][columnaElegida - 1] == " ":
					tableroUsuario[filaElegida][columnaElegida - 1] = " "
					self.aperturaRecursiva(filaElegida, columnaElegida - 1, filas, columnas, tableroUsuario,
										   tableroOculto)
				elif tableroOculto[filaElegida][columnaElegida - 1] == "*":
					explosiones = 1
				else:
					tableroUsuario[filaElegida][columnaElegida - 1] = tableroOculto[filaElegida][columnaElegida - 1]

			if tableroUsuario[filaElegida][columnaElegida + 1] == CSOM:
				if tableroOculto[filaElegida][columnaElegida + 1] == " ":
					tableroUsuario[filaElegida][columnaElegida + 1] = " "
					self.aperturaRecursiva(filaElegida, columnaElegida + 1, filas, columnas, tableroUsuario,
										   tableroOculto)
				elif tableroOculto[filaElegida][columnaElegida + 1] == "*":
					explosiones = 1
				else:
					tableroUsuario[filaElegida][columnaElegida + 1] = tableroOculto[filaElegida][columnaElegida + 1]

			if tableroUsuario[filaElegida + 1][columnaElegida] == CSOM:
				if tableroOculto[filaElegida + 1][columnaElegida] == " ":
					tableroUsuario[filaElegida + 1][columnaElegida] = " "
					self.aperturaRecursiva(filaElegida + 1, columnaElegida, filas, columnas, tableroUsuario,
										   tableroOculto)
				elif tableroOculto[filaElegida + 1][columnaElegida] == "*":
					explosiones = 1
				else:
					tableroUsuario[filaElegida + 1][columnaElegida] = tableroOculto[filaElegida + 1][columnaElegida]

			if tableroUsuario[filaElegida + 1][columnaElegida - 1] == CSOM:
				if tableroOculto[filaElegida + 1][columnaElegida - 1] == " ":
					tableroUsuario[filaElegida + 1][columnaElegida - 1] = " "
					self.aperturaRecursiva(filaElegida + 1, columnaElegida - 1, filas, columnas, tableroUsuario,
										   tableroOculto)
				elif tableroOculto[filaElegida + 1][columnaElegida - 1] == "*":
					explosiones = 1
				else:
					tableroUsuario[filaElegida + 1][columnaElegida - 1] = tableroOculto[filaElegida + 1][
						columnaElegida - 1]

			return explosiones

		elif filaElegida != 0 and columnaElegida != 0 and filaElegida != filas - 1 and columnaElegida != columnas - 1 and filaElegida % 2 == 0:

			if tableroUsuario[filaElegida - 1][columnaElegida] == CSOM:
				if tableroOculto[filaElegida - 1][columnaElegida] == " ":
					tableroUsuario[filaElegida - 1][columnaElegida] = " "
					self.aperturaRecursiva(filaElegida - 1, columnaElegida, filas, columnas, tableroUsuario,
										   tableroOculto)
				elif tableroOculto[filaElegida - 1][columnaElegida] == "*":
					explosiones = 1
				else:
					tableroUsuario[filaElegida - 1][columnaElegida] = tableroOculto[filaElegida - 1][columnaElegida]

			if tableroUsuario[filaElegida - 1][columnaElegida + 1] == CSOM:
				if tableroOculto[filaElegida - 1][columnaElegida + 1] == " ":
					tableroUsuario[filaElegida - 1][columnaElegida + 1] = " "
					self.aperturaRecursiva(filaElegida - 1, columnaElegida + 1, filas, columnas, tableroUsuario,
										   tableroOculto)
				elif tableroOculto[filaElegida - 1][columnaElegida + 1] == "*":
					explosiones = 1
				else:
					tableroUsuario[filaElegida - 1][columnaElegida + 1] = tableroOculto[filaElegida - 1][
						columnaElegida + 1]

			if tableroUsuario[filaElegida][columnaElegida - 1] == CSOM:
				if tableroOculto[filaElegida][columnaElegida - 1] == " ":
					tableroUsuario[filaElegida][columnaElegida - 1] = " "
					self.aperturaRecursiva(filaElegida, columnaElegida - 1, filas, columnas, tableroUsuario,
										   tableroOculto)
				elif tableroOculto[filaElegida][columnaElegida - 1] == "*":
					explosiones = 1
				else:
					tableroUsuario[filaElegida][columnaElegida - 1] = tableroOculto[filaElegida][columnaElegida - 1]

			if tableroUsuario[filaElegida][columnaElegida + 1] == CSOM:
				if tableroOculto[filaElegida][columnaElegida + 1] == " ":
					tableroUsuario[filaElegida][columnaElegida + 1] = " "
					self.aperturaRecursiva(filaElegida, columnaElegida + 1, filas, columnas, tableroUsuario,
										   tableroOculto)
				elif tableroOculto[filaElegida][columnaElegida + 1] == "*":
					explosiones = 1
				else:
					tableroUsuario[filaElegida][columnaElegida + 1] = tableroOculto[filaElegida][columnaElegida + 1]

			if tableroUsuario[filaElegida + 1][columnaElegida] == CSOM:
				if tableroOculto[filaElegida + 1][columnaElegida] == " ":
					tableroUsuario[filaElegida + 1][columnaElegida] = " "
					self.aperturaRecursiva(filaElegida + 1, columnaElegida, filas, columnas, tableroUsuario,
										   tableroOculto)
				elif tableroOculto[filaElegida + 1][columnaElegida] == "*":
					explosiones = 1
				else:
					tableroUsuario[filaElegida + 1][columnaElegida] = tableroOculto[filaElegida + 1][columnaElegida]

			if tableroUsuario[filaElegida + 1][columnaElegida + 1] == CSOM:
				if tableroOculto[filaElegida + 1][columnaElegida + 1] == " ":
					tableroUsuario[filaElegida + 1][columnaElegida + 1] = " "
					self.aperturaRecursiva(filaElegida + 1, columnaElegida + 1, filas, columnas, tableroUsuario,
										   tableroOculto)
				elif tableroOculto[filaElegida + 1][columnaElegida + 1] == "*":
					explosiones = 1
				else:
					tableroUsuario[filaElegida + 1][columnaElegida + 1] = tableroOculto[filaElegida + 1][
						columnaElegida + 1]
			return explosiones

		elif columnaElegida == 0 and filaElegida == 0:
			if tableroUsuario[0][1] == CSOM:
				if tableroOculto[0][1] == " ":
					tableroUsuario[0][1] = " "
					self.aperturaRecursiva(0, 1, filas, columnas, tableroUsuario, tableroOculto)
				elif tableroOculto[0][1] == "*":
					explosiones = 1
				else:
					tableroUsuario[0][1] = tableroOculto[0][1]

			if tableroUsuario[1][0] == CSOM:
				if tableroOculto[1][0] == " ":
					tableroUsuario[1][0] = " "
					self.aperturaRecursiva(1, 0, filas, columnas, tableroUsuario, tableroOculto)

				elif tableroOculto[1][0] == "*":
					explosiones = 1
				else:
					tableroUsuario[1][0] = tableroOculto[1][0]

			if tableroUsuario[1][1] == CSOM:
				if tableroOculto[1][1] == " ":
					tableroUsuario[1][1] = " "
					self.aperturaRecursiva(1, 1, filas, columnas, tableroUsuario, tableroOculto)

				elif tableroOculto[1][1] == "*":
					explosiones = 1
				else:
					tableroUsuario[1][1] = tableroOculto[1][1]
			return explosiones

		elif columnaElegida == 0 and filaElegida == filas - 1 and filas % 2 != 0:

			if tableroUsuario[filas - 2][0] == CSOM:
				if tableroOculto[filas - 2][0] == " ":
					tableroUsuario[filas - 2][0] = " "
					self.aperturaRecursiva(filas - 2, 0, filas, columnas, tableroUsuario, tableroOculto)

				elif tableroOculto[filas - 2][0] == "*":
					explosiones = 1

				else:
					tableroUsuario[filas - 2][0] = tableroOculto[filas - 2][0]

			if tableroUsuario[filas - 2][1] == CSOM:
				if tableroOculto[filas - 2][1] == " ":
					tableroUsuario[filas - 2][1] = " "
					self.aperturaRecursiva(filas - 2, 1, filas, columnas, tableroUsuario, tableroOculto)
				elif tableroOculto[filas - 2][1] == "*":
					explosiones = 1
				else:
					tableroUsuario[filas - 2][1] = tableroOculto[filas - 2][1]

			if tableroUsuario[filas - 1][1] == CSOM:
				if tableroOculto[filas - 1][1] == " ":
					tableroUsuario[filas - 1][1] = " "
					self.aperturaRecursiva(filas - 1, 1, filas, columnas, tableroUsuario, tableroOculto)
				elif tableroOculto[filas - 1][1] == "*":
					explosiones = 1
				else:
					tableroUsuario[filas - 1][1] = tableroOculto[filas - 1][1]
			return explosiones

		elif columnaElegida == columnas - 1 and filaElegida == 0:

			if tableroUsuario[0][columnas - 2] == CSOM:
				if tableroOculto[0][columnas - 2] == " ":
					tableroUsuario[0][columnas - 2] = " "
					self.aperturaRecursiva(0, columnas - 2, filas, columnas, tableroUsuario, tableroOculto)
				elif tableroOculto[0][columnas - 2] == "*":
					explosiones = 1
				else:
					tableroUsuario[0][columnas - 2] = tableroOculto[0][columnas - 2]

			if tableroUsuario[1][columnas - 1] == CSOM:
				if tableroOculto[1][columnas - 1] == " ":
					tableroUsuario[1][columnas - 1] = " "
					self.aperturaRecursiva(1, columnas - 1, filas, columnas, tableroUsuario, tableroOculto)
				elif tableroOculto[1][columnas - 1] == "*":
					explosiones = 1
				else:
					tableroUsuario[1][columnas - 1] = tableroOculto[1][columnas - 1]
			return explosiones

		elif columnaElegida == columnas - 1 and filaElegida == filas - 1 and filas % 2 != 0:

			if tableroUsuario[filas - 2][columnas - 1] == CSOM:
				if tableroOculto[filas - 2][columnas - 1] == " ":
					tableroUsuario[filas - 2][columnas - 1] = " "
					self.aperturaRecursiva(filas - 2, columnas - 1, filas, columnas, tableroUsuario, tableroOculto)
				elif tableroOculto[filas - 2][columnas - 1] == "*":
					explosiones = 1
				else:
					tableroUsuario[filas - 2][columnas - 1] = tableroOculto[filas - 2][columnas - 1]

			if tableroUsuario[filas - 1][columnas - 2] == CSOM:
				if tableroOculto[filas - 1][columnas - 2] == " ":
					tableroUsuario[filas - 1][columnas - 2] = " "
					self.aperturaRecursiva(filas - 1, columnas - 2, filas, columnas, tableroUsuario, tableroOculto)
				elif tableroOculto[filas - 1][columnas - 2] == "*":
					explosiones = 1
				else:
					tableroUsuario[filas - 1][columnas - 2] = tableroOculto[filas - 1][columnas - 2]
			return explosiones

		elif columnaElegida == 0 and filaElegida == filas - 1 and filas % 2 == 0:

			if tableroUsuario[filas - 2][0] == CSOM:
				if tableroOculto[filas - 2][0] == " ":
					tableroUsuario[filas - 2][0] = " "
					self.aperturaRecursiva(filas - 2, 0, filas, columnas, tableroUsuario, tableroOculto)
				elif tableroOculto[filas - 2][0] == "*":
					explosiones = 1
				else:
					tableroUsuario[filas - 2][0] = tableroOculto[filas - 2][0]

			if tableroUsuario[filas - 1][1] == CSOM:
				if tableroOculto[filas - 1][1] == " ":
					tableroUsuario[filas - 1][1] = " "
					self.aperturaRecursiva(filas - 1, 1, filas, columnas, tableroUsuario, tableroOculto)
				elif tableroOculto[filas - 1][1] == "*":
					explosiones = 1
				else:
					tableroUsuario[filas - 1][1] = tableroOculto[filas - 1][1]
			return explosiones

		elif columnaElegida == 0:

			if filaElegida % 2 != 0:

				if tableroUsuario[filaElegida - 1][0] == CSOM:
					if tableroOculto[filaElegida - 1][0] == " ":
						tableroUsuario[filaElegida - 1][0] = " "
						self.aperturaRecursiva(filaElegida - 1, 0, filas, columnas, tableroUsuario, tableroOculto)
					elif tableroOculto[filaElegida - 1][0] == "*":
						explosiones = 1
					else:
						tableroUsuario[filaElegida - 1][0] = tableroOculto[filaElegida - 1][0]

				if tableroUsuario[filaElegida][1] == CSOM:
					if tableroOculto[filaElegida][1] == " ":
						tableroUsuario[filaElegida][1] = " "
						self.aperturaRecursiva(filaElegida, 1, filas, columnas, tableroUsuario, tableroOculto)
					elif tableroOculto[filaElegida][1] == "*":
						explosiones = 1
					else:
						tableroUsuario[filaElegida][1] = tableroOculto[filaElegida][1]

				if tableroUsuario[filaElegida + 1][0] == CSOM:
					if tableroOculto[filaElegida + 1][0] == " ":
						tableroUsuario[filaElegida + 1][0] = " "
						self.aperturaRecursiva(filaElegida + 1, 0, filas, columnas, tableroUsuario, tableroOculto)
					elif tableroOculto[filaElegida + 1][0] == "*":
						explosiones = 1
					else:
						tableroUsuario[filaElegida + 1][0] = tableroOculto[filaElegida + 1][0]
				return explosiones

			else:
				if tableroUsuario[filaElegida - 1][0] == CSOM:
					if tableroOculto[filaElegida - 1][0] == " ":
						tableroUsuario[filaElegida - 1][0] = " "
						self.aperturaRecursiva(filaElegida - 1, 0, filas, columnas, tableroUsuario, tableroOculto)
					elif tableroOculto[filaElegida - 1][0] == "*":
						explosiones = 1
					else:
						tableroUsuario[filaElegida - 1][0] = tableroOculto[filaElegida - 1][0]

				if tableroUsuario[filaElegida][1] == CSOM:
					if tableroOculto[filaElegida][1] == " ":
						tableroUsuario[filaElegida][1] = " "
						self.aperturaRecursiva(filaElegida, 1, filas, columnas, tableroUsuario, tableroOculto)
					elif tableroOculto[filaElegida][1] == "*":
						explosiones = 1
					else:
						tableroUsuario[filaElegida][1] = tableroOculto[filaElegida][1]

				if tableroUsuario[filaElegida - 1][1] == CSOM:
					if tableroOculto[filaElegida - 1][1] == " ":
						tableroUsuario[filaElegida - 1][1] = " "
						self.aperturaRecursiva(filaElegida - 1, 1, filas, columnas, tableroUsuario, tableroOculto)
					elif tableroOculto[filaElegida - 1][1] == "*":
						explosiones = 1
					else:
						tableroUsuario[filaElegida - 1][1] = tableroOculto[filaElegida - 1][1]

				if tableroUsuario[filaElegida + 1][1] == CSOM:
					if tableroOculto[filaElegida + 1][1] == " ":
						tableroUsuario[filaElegida + 1][1] = " "
						self.aperturaRecursiva(filaElegida + 1, 1, filas, columnas, tableroUsuario, tableroOculto)
					elif tableroOculto[filaElegida + 1][1] == "*":
						explosiones = 1
					else:
						tableroUsuario[filaElegida + 1][1] = tableroOculto[filaElegida + 1][1]

				if tableroUsuario[filaElegida + 1][0] == CSOM:
					if tableroOculto[filaElegida + 1][0] == " ":
						tableroUsuario[filaElegida + 1][0] = " "
						self.aperturaRecursiva(filaElegida + 1, 0, filas, columnas, tableroUsuario, tableroOculto)
					elif tableroOculto[filaElegida + 1][0] == "*":
						explosiones = 1
					else:
						tableroUsuario[filaElegida + 1][0] = tableroOculto[filaElegida + 1][0]
				return explosiones

		elif filaElegida == 0:

			if tableroUsuario[0][columnaElegida - 1] == CSOM:
				if tableroOculto[0][columnaElegida - 1] == " ":
					tableroUsuario[0][columnaElegida - 1] = " "
					self.aperturaRecursiva(0, columnaElegida - 1, filas, columnas, tableroUsuario, tableroOculto)
				elif tableroOculto[0][columnaElegida - 1] == "*":
					explosiones = 1
				else:
					tableroUsuario[0][columnaElegida - 1] = tableroOculto[0][columnaElegida - 1]

			if tableroUsuario[1][columnaElegida] == CSOM:
				if tableroOculto[1][columnaElegida] == " ":
					tableroUsuario[1][columnaElegida] = " "
					self.aperturaRecursiva(1, columnaElegida, filas, columnas, tableroUsuario, tableroOculto)
				elif tableroOculto[1][columnaElegida] == "*":
					explosiones = 1
				else:
					tableroUsuario[1][columnaElegida] = tableroOculto[1][columnaElegida]

			if tableroUsuario[1][columnaElegida + 1] == CSOM:
				if tableroOculto[1][columnaElegida + 1] == " ":
					tableroUsuario[1][columnaElegida + 1] = " "
					self.aperturaRecursiva(1, columnaElegida + 1, filas, columnas, tableroUsuario, tableroOculto)
				elif tableroOculto[1][columnaElegida + 1] == "*":
					explosiones = 1
				else:
					tableroUsuario[1][columnaElegida + 1] = tableroOculto[1][columnaElegida + 1]

			if tableroUsuario[0][columnaElegida + 1] == CSOM:
				if tableroOculto[0][columnaElegida + 1] == " ":
					tableroUsuario[0][columnaElegida + 1] = " "
					self.aperturaRecursiva(0, columnaElegida + 1, filas, columnas, tableroUsuario, tableroOculto)
				elif tableroOculto[0][columnaElegida + 1] == "*":
					explosiones = 1
				else:
					tableroUsuario[0][columnaElegida + 1] = tableroOculto[0][columnaElegida + 1]
			return explosiones

		elif filaElegida == filas - 1:

			if tableroUsuario[filas - 1][columnaElegida - 1] == CSOM:
				if tableroOculto[filas - 1][columnaElegida - 1] == " ":
					tableroUsuario[filas - 1][columnaElegida - 1] = " "
					self.aperturaRecursiva(filas - 1, columnaElegida - 1, filas, columnas, tableroUsuario,
										   tableroOculto)
				elif tableroOculto[filas - 1][columnaElegida - 1] == "*":
					explosiones = 1
				else:
					tableroUsuario[filas - 1][columnaElegida - 1] = tableroOculto[filas - 1][columnaElegida - 1]

			if tableroUsuario[filas - 2][columnaElegida] == CSOM:
				if tableroOculto[filas - 2][columnaElegida] == " ":
					tableroUsuario[filas - 2][columnaElegida] = " "
					self.aperturaRecursiva(filas - 2, columnaElegida, filas, columnas, tableroUsuario, tableroOculto)
				elif tableroOculto[filas - 2][columnaElegida] == "*":
					explosiones = 1
				else:
					tableroUsuario[filas - 2][columnaElegida] = tableroOculto[filas - 2][columnaElegida]

			if tableroUsuario[filas - 1][columnaElegida + 1] == CSOM:
				if tableroOculto[filas - 1][columnaElegida + 1] == " ":
					tableroUsuario[filas - 1][columnaElegida + 1] = " "
					self.aperturaRecursiva(filas - 1, columnaElegida + 1, filas, columnas, tableroUsuario,
										   tableroOculto)
				elif tableroOculto[filas - 1][columnaElegida + 1] == "*":
					explosiones = 1
				else:
					tableroUsuario[filas - 1][columnaElegida + 1] = tableroOculto[filas - 1][columnaElegida + 1]

			if tableroUsuario[filas - 2][columnaElegida + 1] == CSOM:
				if tableroOculto[filas - 2][columnaElegida + 1] == " ":
					tableroUsuario[filas - 2][columnaElegida + 1] = " "
					self.aperturaRecursiva(filas - 2, columnaElegida + 1, filas, columnas, tableroUsuario,
										   tableroOculto)
				elif tableroOculto[filas - 2][columnaElegida + 1] == "*":
					explosiones = 1
				else:
					tableroUsuario[filas - 2][columnaElegida + 1] = tableroOculto[filas - 2][columnaElegida + 1]
			return explosiones

		elif columnaElegida == columnas - 1 and filaElegida % 2 != 0:

			if tableroUsuario[filaElegida - 1][columnaElegida - 1] == CSOM:
				if tableroOculto[filaElegida - 1][columnaElegida - 1] == " ":
					tableroUsuario[filaElegida - 1][columnaElegida - 1] = " "
					self.aperturaRecursiva(filaElegida - 1, columnaElegida - 1, filas, columnas, tableroUsuario,
										   tableroOculto)
				elif tableroOculto[filaElegida - 1][columnaElegida - 1] == "*":
					explosiones = 1
				else:
					tableroUsuario[filaElegida - 1][columnaElegida - 1] = tableroOculto[filaElegida - 1][
						columnaElegida - 1]

			if tableroUsuario[filaElegida - 1][columnaElegida] == CSOM:
				if tableroOculto[filaElegida - 1][columnaElegida] == " ":
					tableroUsuario[filaElegida - 1][columnaElegida] = " "
					self.aperturaRecursiva(filaElegida - 1, columnaElegida, filas, columnas, tableroUsuario,
										   tableroOculto)
				elif tableroOculto[filaElegida - 1][columnaElegida] == "*":
					explosiones = 1
				else:
					tableroUsuario[filaElegida - 1][columnaElegida] = tableroOculto[filaElegida - 1][columnaElegida]

			if tableroUsuario[filaElegida][columnaElegida - 1] == CSOM:
				if tableroOculto[filaElegida][columnaElegida - 1] == " ":
					tableroUsuario[filaElegida][columnaElegida - 1] = " "
					self.aperturaRecursiva(filaElegida, columnaElegida - 1, filas, columnas, tableroUsuario,
										   tableroOculto)
				elif tableroOculto[filaElegida][columnaElegida - 1] == "*":
					explosiones = 1
				else:
					tableroUsuario[filaElegida][columnaElegida - 1] = tableroOculto[filaElegida][columnaElegida - 1]

			if tableroUsuario[filaElegida + 1][columnaElegida - 1] == CSOM:
				if tableroOculto[filaElegida + 1][columnaElegida - 1] == " ":
					tableroUsuario[filaElegida + 1][columnaElegida - 1] = " "
					self.aperturaRecursiva(filaElegida + 1, columnaElegida - 1, filas, columnas, tableroUsuario,
										   tableroOculto)
				elif tableroOculto[filaElegida + 1][columnaElegida - 1] == "*":
					explosiones = 1
				else:
					tableroUsuario[filaElegida + 1][columnaElegida - 1] = tableroOculto[filaElegida + 1][
						columnaElegida - 1]

			if tableroUsuario[filaElegida + 1][columnaElegida] == CSOM:
				if tableroOculto[filaElegida + 1][columnaElegida] == " ":
					tableroUsuario[filaElegida + 1][columnaElegida] = " "
					self.aperturaRecursiva(filaElegida + 1, columnaElegida, filas, columnas, tableroUsuario,
										   tableroOculto)
				elif tableroOculto[filaElegida + 1][columnaElegida] == "*":
					explosiones = 1
				else:
					tableroUsuario[filaElegida + 1][columnaElegida] = tableroOculto[filaElegida + 1][columnaElegida]
			return explosiones

		elif columnaElegida == columnas - 1 and filaElegida % 2 == 0:

			if tableroUsuario[filaElegida + 1][columnaElegida] == CSOM:
				if tableroOculto[filaElegida + 1][columnaElegida] == " ":
					tableroUsuario[filaElegida + 1][columnaElegida] = " "
					self.aperturaRecursiva(filaElegida + 1, columnaElegida, filas, columnas, tableroUsuario,
										   tableroOculto)
				elif tableroOculto[filaElegida + 1][columnaElegida] == "*":
					explosiones = 1
				else:
					tableroUsuario[filaElegida + 1][columnaElegida] = tableroOculto[filaElegida + 1][columnaElegida]

			if tableroUsuario[filaElegida - 1][columnaElegida] == CSOM:
				if tableroOculto[filaElegida - 1][columnaElegida] == " ":
					tableroUsuario[filaElegida - 1][columnaElegida] = " "
					self.aperturaRecursiva(filaElegida - 1, columnaElegida, filas, columnas, tableroUsuario,
										   tableroOculto)
				elif tableroOculto[filaElegida - 1][columnaElegida] == "*":
					explosiones = 1
				else:
					tableroUsuario[filaElegida - 1][columnaElegida] = tableroOculto[filaElegida - 1][columnaElegida]

			if tableroUsuario[filaElegida][columnaElegida - 1] == CSOM:
				if tableroOculto[filaElegida][columnaElegida - 1] == " ":
					tableroUsuario[filaElegida][columnaElegida - 1] = " "
					self.aperturaRecursiva(filaElegida, columnaElegida - 1, filas, columnas, tableroUsuario,
										   tableroOculto)
				elif tableroOculto[filaElegida][columnaElegida - 1] == "*":
					explosiones = 1
				else:
					tableroUsuario[filaElegida][columnaElegida - 1] = tableroOculto[filaElegida][columnaElegida - 1]
			return explosiones

	def jugar(self, filas, columnas, minas, tableroOculto, tableroUsuario, jugada):
		# Función que recoge el desarrollo de una jugada
		filaElegida = jugada[1]
		columnaElegida = jugada[0]
		accion = jugada[2]

		# Desmarcado
		if tableroUsuario[filaElegida][columnaElegida] == "X" and accion == "!":
			tableroUsuario[filaElegida][columnaElegida] = CSOM
			self.actualizarTablero(filas, columnas, tableroUsuario, tableroOculto)
			self.marcadas -= 1
			self.minas_restantes += 1
			self.traducir(tableroUsuario, filas, columnas)
			self.etiquetaMarcadas.set_label("Marcadas: "+str(self.marcadas))
			self.etiquetaMinasRestantes.set_label("Minas Restantes: " +str(self.minas_restantes))
			self.etiquetaMensajes.set_label("\n\n \n")

			if tableroOculto[filaElegida][columnaElegida] == "*":
				self.descubiertas -= 1

		# Marcado
		elif tableroUsuario[filaElegida][columnaElegida] == CSOM and accion == "!":
			if self.marcadas < self.minas :

				tableroUsuario[filaElegida][columnaElegida] = "X"
				self.actualizarTablero(filas, columnas, tableroUsuario, tableroOculto)
				self.marcadas += 1
				self.minas_restantes -= 1
				self.traducir(tableroUsuario, filas, columnas)
				self.etiquetaMarcadas.set_label("Marcadas: " + str(self.marcadas))
				self.etiquetaMinasRestantes.set_label("Minas Restantes: " + str(self.minas_restantes))
				self.etiquetaMensajes.set_label("\n\n \n")

				if tableroOculto[filaElegida][columnaElegida] == "*":
					self.descubiertas += 1

			else:
				self.etiquetaMensajes.set_markup('<span color="red">\n\n   No se pueden marcar más celdas que minas\n</span>')

		# Apertura
		elif tableroUsuario[filaElegida][columnaElegida] == CSOM and accion == "*":
			if tableroOculto[filaElegida][columnaElegida] == "*":

				if self.num_aperturas == 0:

					self.etiquetaMensajes.set_label("\n\n \n")
					# Se cambia la mina de posición
					for i in range(filas):
						for j in range(columnas):
							if i < filas and j < columnas:
								if tableroOculto[i][j] != "*":

									tableroOculto[i][j] = tableroOculto[filaElegida][columnaElegida]
									tableroOculto[filaElegida][columnaElegida] = " "

									# Recorrido por filas para "actualizar" el numero relativo de minas por descubrir de cada casilla
									for k in range(filas):
										for h in range(columnas):
											numMinas = self.detectarVecinas(k, h, tableroOculto, "*",filas,columnas)
											numMarcadas = self.detectarVecinas(k, h, tableroUsuario, "X",filas,columnas)
											numMinasRelativo = numMinas - numMarcadas
											if tableroOculto[k][h] != "*":
												if numMinasRelativo < 0:
													tableroOculto[k][h] = "?"
												elif numMinasRelativo == 0:
													tableroOculto[k][h] = " "
												else:
													tableroOculto[k][h] = str(numMinasRelativo)

													self.num_aperturas += 1
													i = filas + 2
													j = columnas + 2

					# Ahora que ya no hay mina se abre la casilla
					if tableroOculto[filaElegida][columnaElegida] != " ":

						tableroUsuario[filaElegida][columnaElegida] = tableroOculto[filaElegida][columnaElegida]
						self.traducir(tableroUsuario, filas, columnas)

					else:
						# La casilla abierta está en blanco, luego se abren varias recursivamente
						tableroUsuario[filaElegida][columnaElegida] = " "
						self.explosiones = self.aperturaRecursiva(filaElegida, columnaElegida, filas, columnas,
																  tableroUsuario, tableroOculto)

						if self.explosiones == 1:
							# Fin del juego,ha explotado una mina durante la apertura recursiva
							tableroFinal = self.generarTableroFinal(filas, columnas, tableroUsuario, tableroOculto)
							self.traducir(tableroFinal, filas, columnas)
							self.ventanaExplosion.show()
							self.boxReinicio.child.set_from_pixbuf(self.imagenes[15])
							self.etiquetaMensajes.set_markup('<span color="red">\n\n   ¡Ha explotado una mina!\n</span>')
							self.seguir = False
							gobject.source_remove(self.timer)
							self.timer=None

						else:
							# Se imprime el tableroUsuario, que ha sido modificado tras la funcion aperturaRecursiva
							self.traducir(tableroUsuario, filas, columnas)
							self.etiquetaMensajes.set_label("\n\n \n")



				else:

					# Fin del juego, ha explotado una mina
					self.explosiones = 1
					tableroFinal = self.generarTableroFinal(filas, columnas, tableroUsuario, tableroOculto)
					self.traducir(tableroFinal, filas, columnas)
					self.tableroImagen[filaElegida][columnaElegida].set_from_pixbuf(self.imagenes[11])
					self.ventanaExplosion.show()
					self.boxReinicio.child.set_from_pixbuf(self.imagenes[15])
					self.etiquetaMensajes.set_markup('<span color="red">\n\n   ¡Ha explotado una mina!\n</span>')
					self.seguir = False
					gobject.source_remove(self.timer)
					self.timer = None




			else:
				# Se abre la casilla
				if tableroOculto[filaElegida][columnaElegida] != " ":

					tableroUsuario[filaElegida][columnaElegida] = tableroOculto[filaElegida][columnaElegida]
					self.traducir(tableroUsuario, filas, columnas)
					self.num_aperturas += 1
					self.etiquetaMensajes.set_label("\n\n \n")

				else:
					# La casilla abierta está en blanco, luego se abren varias recursivamente
					tableroUsuario[filaElegida][columnaElegida] = " "
					self.explosiones = self.aperturaRecursiva(filaElegida, columnaElegida, filas, columnas,
															  tableroUsuario, tableroOculto)

					if self.explosiones == 1:
						# Fin del juego,ha explotado una mina durante la apertura recursiva
						tableroFinal = self.generarTableroFinal(filas, columnas, tableroUsuario, tableroOculto)
						self.traducir(tableroFinal, filas, columnas)
						self.ventanaExplosion.show()
						self.boxReinicio.child.set_from_pixbuf(self.imagenes[15])
						self.etiquetaMensajes.set_markup('<span color="red">\n\n   ¡Ha explotado una mina!\n</span>')
						self.seguir = False
						gobject.source_remove(self.timer)
						self.timer = None



					else:
						# Se imprime el tableroUsuario, que ha sido modificado tras la funcion aperturaRecursiva
						self.traducir(tableroUsuario, filas, columnas)
						self.etiquetaMensajes.set_label("\n\n \n")
					self.num_aperturas += 1



		elif tableroUsuario[filaElegida][columnaElegida] != " " and tableroUsuario[filaElegida][
			columnaElegida] != "X" and tableroUsuario[filaElegida][columnaElegida] != CSOM and accion == "*":
			self.etiquetaMensajes.set_markup('<span color="red">\n   Celda ya abierta.\n   No se pueden abrir las celdas vecinas por número insuficiente de marcas\n</span>')

		elif tableroUsuario[filaElegida][columnaElegida] != CSOM and tableroUsuario[filaElegida][columnaElegida] != "X" and accion == "!":
			self.etiquetaMensajes.set_markup('<span color="red">\n\n   No se puede marcar una celda ya abierta\n</span>')

		elif tableroUsuario[filaElegida][columnaElegida] == "X" and accion == "*":
			self.etiquetaMensajes.set_markup('<span color="red">\n\n   No se puede abrir una celda marcada\n</span>')

		else:
			# SE ABREN TODAS LAS CELDAS VECINAS NO MARCADAS
			self.explosiones = self.aperturaRecursiva(filaElegida, columnaElegida, filas, columnas, tableroUsuario,
													  tableroOculto)
			if self.explosiones == 1:
				# Fin del juego,ha explotado una mina durante la apertura recursiva
				tableroFinal = self.generarTableroFinal(filas, columnas, tableroUsuario, tableroOculto)
				self.traducir(tableroFinal, filas, columnas)
				self.ventanaExplosion.show()
				self.boxReinicio.child.set_from_pixbuf(self.imagenes[15])
				self.etiquetaMensajes.set_markup('<span color="red">\n\n   ¡Ha explotado una mina!\n</span>')
				self.seguir = False
				gobject.source_remove(self.timer)
				self.timer = None



			else:
				# Se imprime el tableroUsuario, que ha sido modificado tras la funcion aperturaRecursiva
				self.traducir(tableroUsuario, filas, columnas)
				self.etiquetaMensajes.set_label("\n\n \n")

		casillasAbiertas = 0
		for i in range(filas):
			for j in range(columnas):
				if tableroUsuario[i][j] != CSOM and tableroUsuario[i][j] != "X":
					casillasAbiertas += 1

		if self.explosiones == 0 and casillasAbiertas == (
				(filas * columnas) - minas) and self.descubiertas == self.minas:
			self.explosiones = 1
			tableroFinal = self.generarTableroFinal(filas, columnas, tableroUsuario, tableroOculto)
			self.boxReinicio.child.set_from_pixbuf(self.imagenes[16])
			self.etiquetaMensajes.set_markup('<span color="green">\n\n   ¡Felicidades, has encontrado todas las minas!\n</span>')
			self.seguir = False
			gobject.source_remove(self.timer)
			self.timer = None

		return None

	def coordenadas(self, widget, event, data=None):
		#Función que localiza en cada click qué celda se ha pulsado y con qué botón del ratón se ha hecho
		#Encapsula estos datos en el formato de la anterior práctica y llama a la función jugar con ellos
		if self.seguir:
			if self.primeraJugada:
				self.tiempoIn = time()
				self.primeraJugada=False
				self.timer = gobject.timeout_add(1000, self.temporizador, self.tiempoIn)
			jugada = data
			#jugada[1]-->fila;jugada[0]-->columna
			if len(jugada) > 2:
				jugada.pop(2)

			if event.button == 1:  # click izquierdo
				jugada.append("*")
			elif event.button == 3:  # click derecho
				jugada.append("!")

			self.jugar(self.filas, self.columnas, self.minas, self.tableroOculto, self.tableroUsuario, jugada)

		return None


	def generarTableroFinal(self,filas, columnas, tableroUsuario, tableroOculto):
		# Genera el tablero que se mostrará al usuario al terminar la partida
		# Para ello modifica el tablero oculto según las marcas que haya efectuado el usuario

		for i in range(filas):
			for j in range(columnas):
				if tableroOculto[i][j] == "*" and tableroUsuario[i][j] == "X":
					# La mina estaba bien marcada
					tableroOculto[i][j] = "X"

				elif tableroUsuario[i][j] == "X" and tableroOculto[i][j] != "*":
					# La casilla estaba mal marcada
					tableroOculto[i][j] = "#"

		return tableroOculto


if __name__ == "__main__":
	Buscaminas()
	gtk.main()
