#!/usr/bin/python
# -*- coding: utf-8 -*-
from time import sleep
from threading import Thread
import time
import telegram
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

		self.comida = 1000
		self.agua = 1000
		self.entretenimiento = 1000
		self.descanso = 1000

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

		self.aburrimientoflag10 = True
		self.aburrimientoflag20 = True
		self.aburrimientoflag40 = True
		self.aburrimientoflag60 = True

		self.suenoflag10 = True
		self.suenoflag20 = True
		self.suenoflag40 = True
		self.suenoflag60 = True

		# Botoneras del juego
		row1 = [telegram.InlineKeyboardButton(text="Comida",callback_data="comida"), 
			telegram.InlineKeyboardButton(text="Bebida",callback_data="bebida")]
		row2 = [telegram.InlineKeyboardButton(text="Jugar",callback_data="jugar"),
			telegram.InlineKeyboardButton(text="Dormir",callback_data="dormir")]
		
		self.menu = telegram.InlineKeyboardMarkup([row1,row2])

		# Mensajes de estado y stats que se actualizaran a cada rato
		self.crear_mensajes_estaticos()

		# Hilo encargado de enviar mensajes del estado del bot al usuario
		self.thread = Thread(target = self.comprueba_estado_thread)
		self.thread.start()



	def crear_mensajes_estaticos(self):
		self.dialogo_tamagochi = self.enviar("¡Hola amigo!")
		self.stats_tamagochi = self.enviar(self.status(),botonera=self.menu)

	def actualizar_dialogo(self,text):
		try:
			self.dialogo_tamagochi.edit_text(text=text,parse_mode=telegram.ParseMode.MARKDOWN)
		except Exception:
			return
	def actualizar_stats(self):
		try:
			self.stats_tamagochi.edit_text(text=self.status(),parse_mode=telegram.ParseMode.MARKDOWN,reply_markup=self.menu)
		except Exception:
			return

	# Muestra el estado de los atributos del tamagochi
	def status(self):
		
		text =  '`Hambre:       `*' + str(self.nivelHambre) + '%*\n'
		text += '`Sed:          `*' + str(self.nivelSed) + '%*\n'
		text += '`Aburrimiento: `*' + str(self.nivelAburrimiento) + '%*\n'
		text += '`Sueño:        `*' + str(self.nivelSueno) + '%*\n\n'
		text += '`Tu comida:          `' + str(self.comida) + ' unidades\n'
		text += '`Tu agua:            `' + str(self.agua) + ' unidades\n'
		text += '`Tu entretenimiento: `' + str(self.entretenimiento) + ' unidades\n'
		text += '`Tu descanso:        `' + str(self.descanso) + ' unidades\n'

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
			if (self.decrementa_aburrimiento(int(time.time())) == False):
				return False
			if (self.decrementa_sueno(int(time.time())) == False):
				return False

	# Comprueba el atributo hambre
	def decrementa_hambre(self,tiempo_actual):
		

		if (tiempo_actual - self.tiempoActualHambre) > self.intHambre:

			self.nivelHambre -= self.restHambre

			if  self.nivelHambre <= 0:
				self.muerto = True
				self.actualizar_dialogo('TU TAMAGOCHI MURIÓ DE HAMBRE')
				self.actualizar_stats()
				return False
			elif self.nivelHambre < 10 and self.hambreflag10:
				self.actualizar_dialogo('¡O me das de comer o me MUEROO maldita sea!')
				self.actualizar_stats()
				self.hambreflag10 = False
			elif self.nivelHambre < 20 and self.hambreflag20:
				self.actualizar_dialogo('¡Tengo muchísima hambre!')
				self.actualizar_stats()
				self.hambreflag20 = False
			elif self.nivelHambre < 40 and self.hambreflag40:
				self.actualizar_dialogo('¡Noto un vacio en mi estómago!')
				self.actualizar_stats()
				self.hambreflag40 = False
			elif self.nivelHambre < 60 and self.hambreflag60:
				self.actualizar_dialogo('Hmmm, quiero picar algo...')
				self.actualizar_stats()
				self.hambreflag60 = False

			self.tiempoActualHambre = tiempo_actual

		return True

	def decrementa_sed(self,tiempo_actual):
		

		if (tiempo_actual - self.tiempoActualSed) > self.intSed:

			self.nivelSed -= self.restSed

			if self.nivelSed <= 0:
				self.muerto = True
				self.actualizar_dialogo('TU TAMAGOCHI MURIÓ DE SED')
				self.actualizar_stats()
				return False
			elif self.nivelSed < 10 and self.sedflag10:
				self.actualizar_dialogo('¡O me das de beber o me MUEROO maldita sea!')
				self.actualizar_stats()
				self.sedflag10 = False
			elif self.nivelSed < 20 and self.sedflag20:
				self.actualizar_dialogo('¡Tengo muchísima sed!')
				self.actualizar_stats()
				self.sedflag20 = False
			elif self.nivelSed < 40 and self.sedflag40:
				self.actualizar_dialogo('¡Noto un vacio en mi paladar!')
				self.actualizar_stats()
				self.sedflag40 = False
			elif self.nivelSed < 60 and self.sedflag60:
				self.actualizar_dialogo('Hmmm, quiero beber algo...')
				self.actualizar_stats()
				self.sedflag60 = False

			self.tiempoActualSed = tiempo_actual

		return True

	def decrementa_aburrimiento(self,tiempo_actual):
		

		if (tiempo_actual - self.tiempoActualAburrimiento) > self.intAburrimiento:

			self.nivelAburrimiento -= self.restAburrimiento

			if  self.nivelAburrimiento <= 0:
				self.muerto = True
				self.actualizar_dialogo('TU TAMAGOCHI MURIÓ DE ABURRIMIENTO')
				self.actualizar_stats()
				return False
			elif self.nivelAburrimiento < 10 and self.aburrimientoflag10:
				self.actualizar_dialogo('¡O juegas conmigo o me muero!')
				self.actualizar_stats()
				self.aburrimientoflag10 = False
			elif self.nivelAburrimiento < 20 and self.aburrimientoflag20:
				self.actualizar_dialogo('¡Me aburro muchísimo!')
				self.actualizar_stats()
				self.aburrimientoflag20 = False
			elif self.nivelAburrimiento < 40 and self.aburrimientoflag40:
				self.actualizar_dialogo('¡Quiero jugar a algo ya!')
				self.actualizar_stats()
				self.aburrimientoflag40 = False
			elif self.nivelAburrimiento < 60 and self.aburrimientoflag60:
				self.actualizar_dialogo('Me apetece jugar...')
				self.actualizar_stats()
				self.aburrimientoflag60 = False

			self.tiempoActualAburrimiento = tiempo_actual

		return True

	def decrementa_sueno(self,tiempo_actual):
		

		if (tiempo_actual - self.tiempoActualSueno) > self.intSueno:

			self.nivelSueno -= self.restSueno

			if  self.nivelSueno <= 0:
				self.muerto = True
				self.actualizar_dialogo('TU TAMAGOCHI MURIÓ DE SUEÑO')
				self.actualizar_stats()
				return False
			elif self.nivelSueno < 10 and self.suenoflag10:
				self.actualizar_dialogo('¡O me ACUESTAS o me MUEROO maldita sea!')
				self.actualizar_stats()
				self.suenoflag10 = False
			elif self.nivelSueno < 20 and self.suenoflag20:
				self.actualizar_dialogo('¡Tengo muchísimo sueño!')
				self.actualizar_stats()
				self.suenoflag20 = False
			elif self.nivelSueno < 40 and self.suenoflag40:
				self.actualizar_dialogo('¡Quiero acostarme!')
				self.actualizar_stats()
				self.suenoflag40 = False
			elif self.nivelSueno < 60 and self.suenoflag60:
				self.actualizar_dialogo('Hmmm, empiezo a bostezar...')
				self.actualizar_stats()
				self.suenoflag60 = False

			self.tiempoActualSueno = tiempo_actual

		return True

	def comer(self,unidades):

		if self.comida < unidades:
			return 'No tienes comida suficiente'
		elif self.nivelHambre + unidades > 100:
			return 'No puedo comer tanto'

		self.nivelHambre += unidades
		self.comida -= unidades
		self.actualizar_stats()

		if self.nivelHambre >= 10:
			self.hambreflag10 = True
		elif self.nivelHambre >= 20:
			self.hambreflag20 = True
		elif self.nivelHambre >= 40:
			self.hambreflag40 = True
		elif self.nivelHambre >= 60:
			self.hambreflag60 = True

		return '¡Gracias por la comida!'

	def beber(self,unidades):

		if self.agua < unidades:
			return 'No tienes gua suficiente'
		elif self.nivelSed + unidades > 100:
			return 'No puedo beber tanto'

		self.nivelSed += unidades
		self.agua -= unidades
		self.actualizar_stats()

		if self.nivelSed >= 10:
			self.sedflag10 = True
		elif self.nivelSed >= 20:
			self.sedflag20 = True
		elif self.nivelSed >= 40:
			self.sedflag40 = True
		elif self.nivelSed >= 60:
			self.sedflag60 = True

		return '¡Gracias por el agua!'

	def jugar(self,unidades):

		if self.entretenimiento < unidades:
			return 'No tienes entretenimiento suficiente'
		elif self.nivelAburrimiento + unidades > 100:
			return 'No puedo jugar tanto'

		self.nivelAburrimiento += unidades
		self.entretenimiento -= unidades
		self.actualizar_stats()

		if self.nivelAburrimiento >= 10:
			self.aburrimientoflag10 = True
		elif self.nivelAburrimiento >= 20:
			self.aburrimientoflag20 = True
		elif self.nivelAburrimiento >= 40:
			self.aburrimientoflag40 = True
		elif self.nivelAburrimiento >= 60:
			self.aburrimientoflag60 = True

		return '¡Gracias por jugar conmigo!'

	def dormir(self,unidades):

		if self.descanso < unidades:
			return 'No tienes descanso suficiente suficiente'
		elif self.nivelSueno + unidades > 100:
			return 'No puedo dormir tanto'

		self.nivelSueno += unidades
		self.descanso -= unidades
		self.actualizar_stats()

		if self.nivelSueno >= 10:
			self.suenoflag10 = True
		elif self.nivelSueno >= 20:
			self.suenoflag20 = True
		elif self.nivelSueno >= 40:
			self.suenoflag40 = True
		elif self.nivelSueno >= 60:
			self.suenoflag60 = True

		return '¡Estoy con energías renovadas!'

	# El bot envia al chat el texto pasado por argumento
	def enviar(self,texto,botonera=None):
		return self.bot.send_message(chat_id=self.chat_id,parse_mode=telegram.ParseMode.MARKDOWN,text=texto
			,reply_markup=botonera)