#Clases para la hoja de trabajo 10

from py2neo.ogm import *

class Paciente(GraphObject):
	__primarykey__ = "nombre"

	nombre = Property()
	telefono = Property()

	toma = Related("Medicina","Toma")
	visita = Related ("Doctor","Visita")
	conoce = Related("Paciente","conoce")

class Doctor(GraphObject):
	__primarykey__ = "nombre"

	nombre = Property()
	colegiado = Property()
	especialidad = Property()
	telefono = Property()

	conoce = Related("Doctor","conoce")
	prescribe = Related ("Medicina","Prescribe")

class Medicina (GraphObject):
	nombre = Property()
	