#Nombre de la BD Lab10
#Contraseña: laboratorio

from py2neo import *
from clases import *
import pprint
graph = Graph (password = "laboratorio")

def agregarRelacion (n1, n2,fecha,medicina,desdeCuando,paraCuando,dosis):
	d = graph.run("MATCH (n:Paciente) WHERE n.nombre = '"+n1+"' RETURN n").data()
	if (len(d)>0):	
		d1 = graph.run("MATCH (n:Doctor) WHERE n.nombre = '"+n2+"' RETURN n").data()
		if (len(d1)>0):
			d2 = graph.run("MATCH (n:Medcina) WHERE n.nombre = '"+medicina+"' RETURN n").data()
			if (len(d2)>0):
				#Crea la relacion paciente-doctor
				graph.run("MATCH (n:Paciente),(m:Doctor) WHERE n.nombre = '"+n1+"' AND m.nombre = '"+n2+"' CREATE (n)-[r:Visita{fecha: "+fecha+"}]->(m) ")
				#Crea la relacion doctor-medicina
				graph.run("MATCH (n:Doctor),(m:Medicina) WHERE n.nombre = '"+n2+"' AND m.nombre = '"+medicina+"' CREATE (n)-[r:Prescribe{desdeCuando: "+desdeCuando+",paraCuando:"+paraCuando+",dosis: "+dosis+"}]->(m) ")
				#Crea la relacion paciente-medicina
				graph.run("MATCH (n:Paciente),(m:Medicina) WHERE n.nombre = '"+n1+"' AND m.nombre = '"+medicina+"' CREATE (n)-[r:Toma]->(m) ")
				return True
			return False
		return False
	return False

def agregarRelacionX (n1, n2,tipo):
	#tipo es True para pacientes y False para doctores
	if (tipo == True):
		d = graph.run("MATCH (n:Paciente) WHERE n.nombre = '"+n1+"' RETURN n").data()
		if (len(d)>0):	
			d1 = graph.run("MATCH (n:Paciente) WHERE n.nombre = '"+n2+"' RETURN n").data()
			if (len(d1)>0):
				graph.run("MATCH (n:Paciente),(m:Paciente) WHERE n.nombre = '"+n1+"' AND m.nombre = '"+n2+"' CREATE (n)-[r:conoce]->(m) CREATE (m) -[l:conoce]-> (n) ")
				return True
			return False
		return False
	else:
		d = graph.run("MATCH (n:Doctor) WHERE n.nombre = '"+n1+"' RETURN n").data()
		if (len(d)>0):	
			d1 = graph.run("MATCH (n:Doctor) WHERE n.nombre = '"+n2+"' RETURN n").data()
			if (len(d1)>0):
				graph.run("MATCH (n:Doctor),(m:Doctor) WHERE n.nombre = '"+n1+"' AND m.nombre = '"+n2+"' CREATE (n)-[r:conoce]->(m) CREATE (m) -[l:conoce]-> (n) ")
				return True
			return False
		return False

menu = """
		MENU
	1. Ingresar un nuevo doctor
	2. Ingresar un nuevo paciente
	3. Ingresar una visita de un paciente a su doctor
	4. Consulta de doctores por especialidad
	5. Añadir relaciones de pacientes
	6. Añadir relaciones de Doctores
	7. Salir
"""

cond = True

while (cond):
	respuesta = input (menu)
	if (respuesta == "1"):
		d = Doctor()
		nombre = input("Ingresa el nombre del doctor: ")
		colegiado = input ("Ingresa el colegiado del doctor: ")
		telefono = input ("Ingresa el numero de telefono del doctor: ")
		especialidad = input ("Ingresa la especialidad del doctor: ")

		d.nombre = nombre
		d.colegiado = colegiado
		d.telefono = telefono
		d.especialidad = especialidad
	elif (respuesta == "2"):
		p = Paciente()

		nombre = input ("Ingresa el nombre del paciente: ")
		telefono = input ("Ingresa el numero de telefono del paciente: ")

		p.nombre = nombre
		p.telefono = telefono
	elif (respuesta == "3"):
		n1 = input("Ingresa el nombre del paciente: ")
		n2 = input("Ingresa el nombre del doctor: ")
		fecha = input ("Ingresa la fecha de la consulta: ")
		medicina = input("Ingresa la medicina prescrita: ")
		desdeCuando = input("Desde cuando la toma: ")
		paraCuando = input("Hasta cuando la toma: ")
		dosis = input ("En que dosis la toma: ")

		if (agregarRelacion(n1,n2,fecha,medicina,desdeCuando,paraCuando,dosis) == False):
			print ("Hay algo mal, intentalo de nuevo con datos correctos....")

	elif (respuesta == "4"):
		especialidad = input ("Ingresa la especialidad que buscas: ")
		d = graph.run("MATCH (n:Doctor) WHERE n.especialidad = "+especialidad+"return n").data
		pp = pprint.PrettyPrinter(indent=4)
		pp.pprint(d)
	elif (respuesta == "5"):
		n1 = input ("Ingresa el nombre del primer paciente")
		n2 = input("Ingresa el nombre del segundo paciente")
		if (agregarRelacionX(n1,n2,True)==False):
			print ("Hay algo mal, intentalo de nuevo con datos correctos....")
	elif (respuesta == "6"):
		n1 = input ("Ingresa el nombre del primer doctor")
		n2 = input("Ingresa el nombre del segundo doctor")
		if (agregarRelacionX(n1,n2,False)==False):
			print ("Hay algo mal, intentalo de nuevo con datos correctos....")
	elif (respuesta == "7"):
		cond = False
	else:
		print ("Cleto")