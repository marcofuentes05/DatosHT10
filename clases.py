#Clases para la hoja de trabajo 10

from py2neo.ogm import *

class Paciente(GraphObject):
	__primarykey__ = "nombre"

	nombre = Property()
	telefono = Property()

class Doctor(GraphObject):
	__primarykey__ = "nombre"

	nombre = Property()
	colegiado = Property()
	especialidad = Property()
	telefono = Property()

class Medicina (GraphObject):
	nombre = Property()
	