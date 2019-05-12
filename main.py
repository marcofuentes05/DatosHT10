#Nombre de la BD: Lab10
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
			d2 = graph.run("MATCH (n:Medicina) WHERE n.nombre = '"+medicina+"' RETURN n").data()
			if (len(d2)>0):
				#Crea la relacion paciente-doctor
				graph.run("MATCH (n:Paciente),(m:Doctor) WHERE n.nombre = '"+n1+"' AND m.nombre = '"+n2+"' CREATE (n)-[r:Visita{fecha: '"+fecha+"'}]->(m) ")
				#Crea la relacion doctor-medicina
				graph.run("MATCH (n:Doctor),(m:Medicina) WHERE n.nombre = '"+n2+"' AND m.nombre = '"+medicina+"' CREATE (n)-[r:Prescribe{desdeCuando: '"+desdeCuando+"',paraCuando:'"+paraCuando+"',dosis: '"+dosis+"'}]->(m) ")
				#Crea la relacion paciente-medicina
				graph.run("MATCH (n:Paciente),(m:Medicina) WHERE n.nombre = '"+n1+"' AND m.nombre = '"+medicina+"' CREATE (n)-[r:Toma]->(m) ")
				return True
			else:
				print ("No existe esa medicina")
				return False
		else:
			print("No hay doctor con ese nombre")
			return False
	else:
		print("No hay paciente con ese nombre")
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
	7. Recomendación Simple (Dada una persona)
	8. Recomendación Simple (Dado un doctor)
	9. Salir
"""
"""
m = Medicina()
m.nombre = "Paracetamol"
graph.push(m)"""

cond = True

while (cond):
	#print (menu)
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
		graph.push(d)
	elif (respuesta == "2"):
		p = Paciente()

		nombre = input ("Ingresa el nombre del paciente: ")
		telefono = input ("Ingresa el numero de telefono del paciente: ")

		p.nombre = nombre
		p.telefono = telefono
		graph.push(p)
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
		d = graph.run("MATCH (n:Doctor) WHERE n.especialidad = '"+especialidad+"' return n").data()
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
	elif(respuesta == "7"):
		resultado = ""
		nombreP = input ("¿Quien eres (Ingresa tu nombre de la BD)?\n")
		paciente = Paciente()
		paciente.nombre = nombreP
		graph.pull(paciente)
		especialidad = input ("¿Que especialidad necesitas?\n")
		#Reviso si ya lo ha visitado
		for d  in paciente.visita:
			if d.especialidad == especialidad:
				resultado += "Ya has visitado al doctor "+d.nombre+"\n"
		for conocido in paciente.conoce:
			#Luego busco si el conocido primario tiene el match
			for doc in conocido.visita:
				if doc.especialidad == especialidad:
					resultado += "El doctor "+doc.nombre+" atiende a tu conocido "+conocido.nombre+", y esta dispuesto a ayudarte :D\n"
			#Luego busco los conocidos secundarios
			for conoci2 in conocido.conoce:
				for doc2 in conoci2.visita:
					if doc2.especialidad == especialidad and conoci2 != paciente:
						resultado += "Tu conocido,"+conocido.nombre+" conoce a "+conoci2.nombre+", quien te recomienda al doctor "+doc2.nombre+" :D \n"
		if len(resultado) == 0:
			print ("No hay opciones, comienza a rezar :(")	
		else:
			print (resultado)
	elif (respuesta == "8"):
		resultado = ""
		nombreD = input("Bienvenido doctor, ¿Cuál es su nombre (de la base de datos)?\n")
		d = Doctor()
		d.nombre = nombreD
		graph.pull(d)
		especialidad = input ("¿Que especialidad está buscando?\n")
		for doc in d.conoce:
			#Primero veo los conocidos directos
			if doc.especialidad == especialidad:
				resultado+="Su conocido "+doc.nombre+" dice que está contento de ayudar\n"
			for doc2 in doc.conoce:
				if (doc2.especialidad == especialidad and doc2 != d):
					resultado += "El doctor "+doc2.nombre+", que es conocido de "+doc.nombre+" está disponible \n"
		if (len(resultado)>0):
			print(resultado)
		else:
			print("No hay resultados :(")
	elif (respuesta == "9"):
		print("\nHasta luego!\n")
		cond = False
	else:
		print ("Cleto")