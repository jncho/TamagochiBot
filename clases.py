#!/usr/bin/python
# -*- coding: utf-8 -*-
from time import sleep
from threading import Thread
import time

# Clase del tamagochi encargada de almacenar los datos y de
#   generar mensajes cada cierto tiempo de su estado
class Tamagochi:

	# Constructor
	def __init__(self,bot,chat_id):

		# Informacion necesaria para enviar mensajes al usuario
		self.bot = bot
		self.chat_id = chat_id

		# Atributos de tamagochi
		self.nivelHambre=50
		self.nivelSed=50
		self.nivelAburrimiento=50
		self.nivelSueno=50

		self.muerto = False

		# Tiempo inicial 
		self.tiempoActualHambre=int(time.time())
		self.tiempoActualSed=int(time.time())
		self.tiempoActualAburrimiento=int(time.time())
		self.tiempoActualSueno=int(time.time())

		# Intervalo de tiempo para la reduccion de atributos en segundos
		self.intHambre=5
		self.intSed=2
		self.intAburrimiento=10
		self.intSueno=30

		# Cantidad de puntuaje que se resta cuando el intervalo de tiempo
		#  llega a su fin.
		self.restHambre=5
		self.restSed=2
		self.restAburrimiento=10
		self.restSueno=30

		# Marcas de tiempo, si se pasa una marca envia un mensaje
		self.hambreflag10 = True
		self.hambreflag20 = True
		self.hambreflag40 = True
		self.hambreflag60 = True

		self.sedflag10 = True
		self.sedflag20 = True
		self.sedflag40 = True
		self.sedflag60 = True

		# Hilo encargado de enviar mensajes del estado del bot al usuario
		self.thread = Thread(target = self.comprueba_estado_thread)
		self.thread.start()

	# Muestra el estado de los atributos del tamagochi
	def status(self):
		
		text = 'Hambre: ' + str(self.nivelHambre) + '%\n'
		text += 'Sed: ' + str(self.nivelSed) + '%\n'
		text += 'Aburrimiento: ' + str(self.nivelAburrimiento) + '%\n'
		text += 'Sueño: ' + str(self.nivelSueno) + '%\n'

		return text

	# Cada cierto tiempo consulta los atributos del tamagochi
	#   y envia un mensaje al usuario advirtiendole
	def comprueba_estado_thread(self):
		while True:
			
			sleep(1)
			
			if (self.decrementa_hambre(int(time.time())) == False):
				return False
			if (self.decrementa_sed(int(time.time())) == False):
				return False



			

	# Comprueba el atributo hambre
	def decrementa_hambre(self,tiempo_actual):
		

		if (tiempo_actual - self.tiempoActualHambre) > self.intHambre:

			self.nivelHambre -= self.restHambre

			if  self.nivelHambre <= 0:
				self.muerto = True
				self.enviar('TU TAMAGOCHI MURIÓ DE HAMBRE')
				self.enviar(self.status())
				return False
			elif self.nivelHambre < 10 and self.hambreflag10:
				self.enviar('¡O me das de comer o me MUEROO maldita sea!')
				self.enviar(self.status())
				self.hambreflag10 = False
			elif self.nivelHambre < 20 and self.hambreflag20:
				self.enviar('¡Tengo muchísima hambre!')
				self.enviar(self.status())
				self.hambreflag20 = False
			elif self.nivelHambre < 40 and self.hambreflag40:
				self.enviar('¡Noto un vacio en mi estómago!')
				self.enviar(self.status())
				self.hambreflag40 = False
			elif self.nivelHambre < 60 and self.hambreflag60:
				self.enviar('Hmmm, quiero picar algo...')
				self.enviar(self.status())
				self.hambreflag60 = False

			self.tiempoActualHambre = tiempo_actual

		return True

	def decrementa_sed(self,tiempo_actual):
		

		if (tiempo_actual - self.tiempoActualSed) > self.intSed:

			self.nivelSed -= self.restSed

			if  self.nivelSed <= 0:
				self.muerto = True
				self.enviar('TU TAMAGOCHI MURIÓ DE SED')
				self.enviar(self.status())
				return False
			elif self.nivelSed < 10 and self.sedflag10:
				self.enviar('¡O me das de beber o me MUEROO maldita sea!')
				self.enviar(self.status())
				self.sedflag10 = False
			elif self.nivelSed < 20 and self.sedflag20:
				self.enviar('¡Tengo muchísima sed!')
				self.enviar(self.status())
				self.sedflag20 = False
			elif self.nivelSed < 40 and self.sedflag40:
				self.enviar('¡Noto un vacio en mi paladar!')
				self.enviar(self.status())
				self.sedflag40 = False
			elif self.nivelSed < 60 and self.sedflag60:
				self.enviar('Hmmm, quiero beber algo...')
				self.enviar(self.status())
				self.sedflag60 = False

			self.tiempoActualSed = tiempo_actual

		return True

	# El bot envia al chat el texto pasado por argumento
	def enviar(self,texto):
		self.bot.send_message(chat_id=self.chat_id,text=texto)