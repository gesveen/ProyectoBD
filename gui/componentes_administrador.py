from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic

from control import ControlDaoHabilidades
from adminHabilidadCamaCausa import *
from DialogMedicamento import *


#=======================================================================================================================
# INTEGRANTES:
# Bryan Stiven Tabarez Mestra	- 1131782
# Aurelio Antonio Vivas Meza	- 1110348
# George Romero Ramirez		    - 1130924
#=======================================================================================================================
#InterfazEnfermera

#=======================================================================================================================


#=============================================> DIALOGO DE INFORMACION <================================================

D_Informacion_class , D_Informacion_Base_class = uic.loadUiType( 'gui/administrador_uis/DialogInformacion.ui' )

class DialogInformacion( QDialog, D_Informacion_class ):

	def __init__( self, parent=None ):

		QDialog.__init__( self, parent )
		self.setupUi( self )

	def showMensaje( self, encabezado, mensaje ):

		self.labelEncabezado.setText( encabezado )
		self.plainTextEditCuerpo.setPlainText( mensaje )
		self.show()



#=============================================> EMPLEADO <==============================================================


D_Empleado_class , D_Emeplado_Base_class = uic.loadUiType( 'gui/administrador_uis/DialogEmpleado.ui' )

class DialogEmpleado( QDialog, D_Empleado_class ):


	def __init__( self, tipo_operacion=1, controlador=None, parent=None ):


		#Constructor padre
		QDialog.__init__( self, parent )
		#Configuracion de la interfaz
		self.setupUi( self )

		#=========================================> VARIABLES
		self.controladorDaosEmpleados = controlador
		self.tipo_operacion = tipo_operacion
		
		#=========================================> WIDGETS
		self.widgetTipoEmpleadoEnfermera = WidgetTipoEmpleadoEnfermera( self.widgetTipoEmpleado )
		self.widgetTipoEmpleadoEnfermera.hide()
		self.widgetTipoEmpleadoMedico = WidgetTipoEmpleadoMedico( self.widgetTipoEmpleado )
		self.widgetTipoEmpleadoMedico.hide()

		#=========================================> SENIALES Y SLOTS
		self.connect( self.comboBoxTipoEmpleado, SIGNAL( "currentIndexChanged(int)" ), self.mostrarTipoEmpleado )
		self.connect( self.pushButtonInsertar, SIGNAL( "clicked()" ), self.realizarOperacionEmpleado )
		self.connect( self.pushButtonConsultar, SIGNAL( "clicked()" ), self.consultarEmpleado )
		self.connect( self.pushButtonCancelar, SIGNAL( "clicked()" ), self.limpiarCampos )

		#==========================================>MODIFICACIONES
		self.mostrarTipoEmpleado(0)

		# NUEVO EMPLEADO
		if self.tipo_operacion is 1:			

			self.setWindowTitle("Nuevo Empleado")
			self.pushButtonInsertar.setText("Insertar")
			self.pushButtonConsultar.hide()

		# MODIFICAR EMPLEADO
		if self.tipo_operacion is 2:

			self.setWindowTitle("Actualizar Empleado")
			self.pushButtonInsertar.setText("Actualizar")
			self.pushButtonConsultar.show()

		# ELIMINAR EMPLEADO

	#=============================================> METODOS
	def mostrarTipoEmpleado( self, indice ):
		if( indice == 0 ):

			self.widgetTipoEmpleadoEnfermera.show()
			self.widgetTipoEmpleadoMedico.hide()
		
		elif( indice == 1 ):
			
			self.widgetTipoEmpleadoMedico.show()
			self.widgetTipoEmpleadoEnfermera.hide()


	# CAMBIAR FUNCION DEL BOTON DEPENDIENDO LA VENTANA
	# OPERACION EN DB: INSERT, DELETE, UPDATE
	def realizarOperacionEmpleado( self ):
		self.identificacion = str( self.lineEditIdentificacion.text() )
		self.nombre = str ( self.lineEditNombre.text() )
		self.direccion = str( self.lineEditDireccion.text() )
		self.telefono = str ( self.lineEditTelefono.text() )
		self.email = str ( self.lineEditEmail.text() )
		self.salario = str ( self.lineEditSalario.text() )
		self.codigo_area = str( self.lineEditCodigoArea.text() )
		self.id_jefe = str( self.lineEditJefe.text() )
		self.accionPorTipoEmpleado()

	# CONSULTAR EL EMPLEADO
	def consultarEmpleado( self ):

		identificacion = str( self.lineEditIdentificacion.text() )
		resultado = self.controladorDaosEmpleados.consultarDatosEnfermera( identificacion )

		if type(resultado) is list:
			self.lineEditIdentificacion.setText( resultado[0] )
			self.lineEditNombre.setText( resultado[1] )
			self.lineEditDireccion.setText( resultado[2] )
			self.lineEditTelefono.setText( resultado[3] )
			self.lineEditCodigoArea.setText( resultado[4] )
			self.lineEditEmail.setText( resultado[5] )
			self.lineEditSalario.setText( resultado[6] )
			self.lineEditJefe.setText( resultado[7] )
		if type(resultado) is None:
			"Sin resultados!"

	def accionPorTipoEmpleado( self ):
		# INDICE 0: ENFERMERA  INDICE 0: MEDICO
		indice =  self.comboBoxTipoEmpleado.currentIndex()
		
		# INDICE = 1 -> ENFERMERA

		self.identificacion = str( self.lineEditIdentificacion.text() )
		indice =  self.comboBoxTipoEmpleado.currentIndex()

		# CONSULTAR ENFERMERA
		if indice is 0:
			resultado = self.controladorDaosEmpleados.consultarDatosEnfermera( self.identificacion )

			if isinstance(resultado, str):
				self.dialogoInfo.showMensaje( "Consultar Enfermera", resultado )
			if isinstance(resultado, list):
				self.lineEditIdentificacion.setText( resultado[0] )
				self.lineEditNombre.setText( resultado[1] )
				self.lineEditDireccion.setText( resultado[2] )
				self.lineEditTelefono.setText( resultado[3] )
				self.lineEditCodigoArea.setText( resultado[4] )
				self.lineEditEmail.setText( resultado[5] )
				self.lineEditSalario.setText( resultado[6] )
				self.lineEditJefe.setText( resultado[7] )
				#self.widgetTipoEmpleadoEnfermera.lineEditAniosExperiencia.text( resultado[8] )
				habilidades = resultado[9]
				self.widgetTipoEmpleadoEnfermera.llenarTablaHabilidadesEnfermera( habilidades )

		# CONSULTAR MEDICO
		if indice is 1:
			pass
	

	# GUARDAR O MODIFICAR EMPLEADO
	#****************************************************************************************************************
	def guardarEmpleado( self ):
		#identificacion = str( self.lineEditIdentificacion.text() )
		nombre = str ( self.lineEditNombre.text() )
		direccion = str( self.lineEditDireccion.text() )
		telefono = str ( self.lineEditTelefono.text() )
		email = str ( self.lineEditEmail.text() )
		salario = str ( self.lineEditSalario.text() )
		codigo_area = str( self.lineEditCodigoArea.text() )
		id_jefe = str( self.lineEditJefe.text() )

		indice =  self.comboBoxTipoEmpleado.currentIndex()

		# ENFERMERA:

		if indice is 0:
			anios_experiencia = str( self.widgetTipoEmpleadoEnfermera.lineEditAniosExperiencia.text() )
			# ATRUBUTOS PARA HABILIDADES:
			numero_filas = self.widgetTipoEmpleadoEnfermera.tableWidgetHabilidades.rowCount()
			
			# Falta: metodo para recuperar habilidades de enfermera desde el widget
			#arreglo_habilidades = self.widgetTipoEmpleadoEnfermera.habilidadesEnfermera()
			
			# INSERTAR ENFERMERA
			if self.tipo_operacion is 1:

				self.controladorDaosEmpleados.insertarEnfermera( self.identificacion, self.nombre, self.direccion, self.telefono,
					self.codigo_area, self.email, self.salario, self.id_jefe, anios_experiencia, [1] )
				# identificacion, nombre, direccion, telefono, codigo_area,
				#     		email, salario, id_jefe, anhos_experiencia, habilidades

				identificacion = str( self.lineEditIdentificacion.text() )
				result = self.controladorDaosEmpleados.insertarEnfermera( identificacion, nombre, direccion, telefono,
					codigo_area, email, salario, id_jefe, anios_experiencia, [1] )
				self.dialogoInfo.showMensaje( "Insertar Enfermera", result )


			
			# ACTUALIZAR/MODIFICAR ENFERMERA
			if self.tipo_operacion is 2:

				pass


		# INDICE = 2 -> MEDICO

				result = self.controladorDaosEmpleados.actualizarDatosEnfermera( self.identificacion, nombre, direccion, telefono,
					codigo_area, email, salario, id_jefe, anios_experiencia, [1] )
				self.dialogoInfo.showMensaje( "Modificar Enfermera", result )
				#hab = self.widgetTipoEmpleadoEnfermera.habilidadesEnfermera()
				#print hab
		
		# MEDICO:

		if indice is 1:

			especialidad = self.widgetCuerpo.widgetTipoEmpleadoMedico.lineEditEspecialidad.text()
			universidad = self.widgetCuerpo.widgetTipoEmpleadoMedico.lineEditUniversidad.text()
			numero_licencia = self.widgetCuerpo.widgetTipoEmpleadoMedico.lineEditNumeroLicencia.text()
			
<<<<<<< HEAD
			# GUARDAR
			if self.tipo_operacion is 1:
				identificacion = str( self.lineEditIdentificacion.text() )
				result = self.controladorDaosEmpleados.insertarMedico(identificacion, nombre, direccion, telefono,
					codigo_area, email, salario, id_jefe, especialidad, universidad, numero_licencia)
				self.dialogoInfo.showMensaje( "Insertar Enfermera", result )

			# MODIFICAR
			if self.tipo_operacion is 1:
=======
			#INSERTE DATOS A LA BASE DE DATOS DE MEDICOS
			if self.tipo_operacion is 2:
				pass

			else:
				#Cuando la operacion es de actualizacion
>>>>>>> 0694eaf04ff65eb0a257f6456e8ef1ba16439554
				pass

	def limpiarCampos( self ):

		self.lineEditIdentificacion.setText("")
		self.lineEditNombre.setText("")
		self.lineEditDireccion.setText("")
		self.lineEditTelefono.setText("")
		self.lineEditEmail.setText("")
		self.lineEditEmail.setText("")
		self.lineEditCargo.setText("")
		#self.comboBoxCodigoArea.currentText()
		#self.comboBoxCodigoJefe.currentText()

		self.widgetTipoEmpleadoEnfermera.lineEditAniosExperiencia.setText("")
		numero_filas = self.widgetTipoEmpleadoEnfermera.tableWidgetHabilidadesEnfermera.rowCount()
		if numero_filas > 0:
			self.widgetTipoEmpleadoEnfermera.tableWidgetHabilidadesEnfermera.clear()

		self.widgetTipoEmpleadoMedico.lineEditEspecialidad.setText("")
		self.widgetTipoEmpleadoMedico.lineEditUniversidad.setText("")
		self.widgetTipoEmpleadoMedico.lineEditNumeroLicencia.setText("")


#============================================> TIPO EMPLEADO ENFERMERA <================================================

W_Enfermera_class , W_Enfermera_Base_class = uic.loadUiType('gui/administrador_uis/WidgetTipoEmpleadoEnfermera.ui')

class WidgetTipoEmpleadoEnfermera( QWidget, W_Enfermera_class ):

	def __init__( self, parent=None ):

		#Constructor padre
		QWidget.__init__( self, parent )
		#Configuracion de la interfaz	
		self.setupUi( self )

		#=============================================> VARIABLES
		self.controladorHabilidad = " " #AQUI VA EL CONTROLADOR DE HABILIDADES DE LA ENFERMERA
		self.codigo = ""
		self.descripcion = " "

		#=============================================> SENIALES Y SLOTS
		self.connect( self.pushButtonAgregar, SIGNAL( "clicked()" ), self.agregar )
		self.connect( self.pushButtonEliminar, SIGNAL( "clicked()" ), self.eliminar )

	#==================================================> METODOS

	def actualizar( self ):

		#AQUI SE DEBE ACTUALIZAR LA TABLA QUE CONTIENE LAS HABILIDADES DE LA ENFERMERA CON LA
		#INFROMACION DE LA BASE DE DATOS
		#self.tableWidgetHabilidadesEnfermera.clearContents()
		#self.tableWidgetHabilidadesEnfermera.insertRow( 0 )
		#self.tableWidgetHabilidadesEnfermera.setItem( 0, 0, QTableWidgetItem( "Codigo" ) )
		#self.tableWidgetHabilidadesEnfermera.setItem( 0, 1, QTableWidgetItem( "descripcion" ) )
		pass


	def agregar( self ):

		fila_seleccionada = self.tableWidgetHabilidades.currentRow()
		if fila_seleccionada == -1:
			self.dialogInformacion = DialogInformacion( self )
			self.dialogInformacion.showMensaje( "Nuevo Empleado"
				,"Por favor seleccione un hablidad para la enfermera  de la tabla habilidades" )
		else:

			self.codigo = self.tableWidgetHabilidades.item( fila_seleccionada,0 ).text()
			self.descripcion = self.tableWidgetHabilidades.item( fila_seleccionada, 1 ).text()
			self.tableWidgetHabilidades.removeRow( fila_seleccionada )
			self.tableWidgetHabilidadesEnfermera.insertRow( 0 )
			self.tableWidgetHabilidadesEnfermera.setItem( 0, 0, QTableWidgetItem( self.codigo ) )
			self.tableWidgetHabilidadesEnfermera.setItem( 0, 1, QTableWidgetItem( self.descripcion ) )
			

	def eliminar( self ):

		fila_seleccionada = self.tableWidgetHabilidadesEnfermera.currentRow()
		if fila_seleccionada == -1 :
			self.dialogInformacion = DialogInformacion( self )
			self.dialogInformacion.showMensaje( "Nuevo Empleado"
				,"Por favor seleccione la habilidad de la tabla 'Habilidades Enfermera que desea eliminar'" )
		else:

			self.codigo = self.tableWidgetHabilidadesEnfermera.item( fila_seleccionada,0 ).text()
			self.descripcion = self.tableWidgetHabilidadesEnfermera.item( fila_seleccionada, 1 ).text()
			self.tableWidgetHabilidadesEnfermera.removeRow( fila_seleccionada )
			self.tableWidgetHabilidades.insertRow( 0 )
			self.tableWidgetHabilidades.setItem( 0, 0, QTableWidgetItem( self.codigo ) )
			self.tableWidgetHabilidades.setItem( 0, 1, QTableWidgetItem( self.descripcion ) )

			

	def habilidadesEnfermera( self ):
		numero_filas =  self.tableWidgetHabilidadesEnfermera.rowCount()
		#arreglo_habilidades = [" "] * numero_filas
		
		for i in range( 0, numero_filas ):

			self.tableWidgetHabilidadesEnfermera.insertRow( 0 )
			arreglo_habilidades = self.tableWidgetHabilidadesEnfermera.item( 0, 0 ).text()

		return arreglo_habilidades


#===========================================> TIPO EMPLEADO MEDICO <====================================================

W_Medico_class , W_Medico_Base_class = uic.loadUiType('gui/administrador_uis/WidgetTipoEmpleadoMedico.ui')


class WidgetTipoEmpleadoMedico( QWidget, W_Medico_class ):

	def __init__( self, parent=None ):

		#Constructor padre
		QWidget.__init__( self, parent )
		#Configuracion de la interfaz
		self.setupUi( self )
	

			

#============================================> EMPLEADOS POR AREAS <====================================================


W_Empleados_Area_class , W__Empleados_Area_Base_class = uic.loadUiType('gui/administrador_uis/WidgetEmpleadosPorArea.ui')

class WidgetEmpleadosPorArea( QWidget , W_Empleados_Area_class ):

	def __init__( self, parent=None ):

		#Constructor padre
		QWidget.__init__( self, parent )
		#Configuracion de la interfaz
		self.setupUi( self )

		#==========================================> VARIABLES
		self.controladorEmpleado = " " #AQUI VA EL CONTROLADOR PARA EMPLEADO


	#===============================================> METODOS
	def actualizar( self ):

		
		#area_seleccionada = str( self.comboBoxAreaEmpleado.currentText() )
		#self.tableWidgetEmpleados.clearContents()
		#AQUI SE LISTAN LOS EMPLEADOS POR AREAS
		#self.tableWidgetEmpleados.insertRow( 0 )
		#self.tableWidgetEmpleados.setItem( 0, 0, QTableWidgetItem( "Codigo" ) )
		#self.tableWidgetEmpleados.setItem( 0, 1, QTableWidgetItem( "descripcion" ) )
		pass

		
#===============================================> AREAS <===============================================================

D_Area_class , D_Area_Base_class = uic.loadUiType( 'gui/administrador_uis/DialogArea.ui' )

class DialogArea( QDialog, D_Area_class ):

	def __init__( self, tipo_operacion=1, controlador=None, parent=None ):

		#Constructor padre
		QDialog.__init__( self, parent )
		#Configuracion interfaz
		self.setupUi( self )

		#================================================> VARIABLES
		self.controladorArea = controlador
		self.tipo_operacion = tipo_operacion

		
		#=================================================> MODIFICACIONES

		# OPERACION --> NUEVA AREA
		if tipo_operacion is 1:

			self.setWindowTitle( "Nueva Area" )
			self.pushButtonInsertar.setText( "Insertar" )
			self.pushButtonConsultar.hide()
			self.lineEditCodigo.setText( "Automatico" )
			self.lineEditCodigo.setReadOnly(True)

		# OPERACION --> MODIFICAR AREA
		if tipo_operacion is 2:

			self.setWindowTitle( "Modificar Area" )
			self.pushButtonInsertar.setText( "Modificar" )
			self.pushButtonConsultar.show()
			# self.lineEditCodigo.setText( "" )
			self.lineEditCodigo.setReadOnly(True)

		# OPERACION --> ELIMINAR AREA
		if tipo_operacion is 3:

			self.setWindowTitle( "Eliminar Area" )
			self.pushButtonInsertar.setText( "Eliminar" )
			self.pushButtonConsultar.show()
			# self.lineEditCodigo.setText( "" )
			self.lineEditCodigo.setReadOnly(True)		


		#=================================================> SENIALES Y SLOTS
		self.connect( self.pushButtonInsertar, SIGNAL( "clicked()" ), self.realizarOperacionArea )
		#self.connect( self.pushButtonCancelar, SIGNAL( "clicked()" ), self.limpiarCampos  )
		self.connect( self.pushButtonConsultar, SIGNAL( "clicked()" ), self.consultar )

	#====================================================> METODOS
	# INSERTAR, MODIFICAR, ELIMINAR
	def realizarOperacionArea( self ):

		nombre = str(self.lineEditNombre.text())
		descripcion = str(self.lineEditDescripcion.text())
		codigo = str(self.lineEditCodigo.text())

		# AQUI SE INSERTA LA INFORMACION A LA BASE DE DATOS
		if self.tipo_operacion is 1:
			self.controladorArea.insertarArea(codigo, nombre, descripcion)
			self.close()
		if self.tipo_operacion is 2:
			self.controladorArea.actualizarArea(codigo, nombre, descripcion)
			self.close()
		if self.tipo_operacion is 3:
			self.controladorArea.eliminarArea(codigo)
			self.close()

	def limpiarCampos( self ):

		if self.nuevo_registro:
			
			self.lineEditNombre.setText( "" )
			self.lineEditDescripcion.text( "" )
		
		else:
			
			self.lineEditCodigo.setText( "" )
			self.lineEditNombre.setText( "" )
			self.lineEditDescripcion.setText( "" )

	def consultar( self ):
			nombre = str(self.lineEditNombre.text())
			codigo, descripcion = self.controladorArea.buscarArea(nombre)
			self.lineEditDescripcion.setText(descripcion)
			self.lineEditCodigo.setText(codigo)
		
#===========================================> LISTAR AREAS <============================================================

W_Areas_class , W_Areas_Base_class = uic.loadUiType('gui/administrador_uis/WidgetListarAreas.ui')


class WidgetListarAreas( QWidget, W_Areas_class ):
	
	def __init__( self, parent=None ):

		#Constructor padre
		QWidget.__init__( self, parent )
		#Configuracion interfaz
		self.setupUi( self )

		#========================================> VARIABLES
		self.controladorArea = " " #AQUI VA EL CONTROLADOR DE AREA

	#============================================> METODOS
	def actualizar( self ):
		#AQUI SE LISTAN LAS AREAS EN LA TABLA DE AREAS
		#self.tableWidgetAreas.clearContents()
		#self.tableWidgetAreas.insertRow( 0 )
		#self.tableWidgetAreas.setItem( 0, 0, QTableWidgetItem( "Codigo" ) )
		#self.tableWidgetAreas.setItem( 0, 1, QTableWidgetItem( "descripcion" ) )
		pass

	
#===============================================> CAMA <================================================================

D_Cama_class , D_Cama_Base_class = uic.loadUiType( 'gui/administrador_uis/DialogCama.ui' )

class DialogCama( QDialog, D_Cama_class ):

	def __init__( self, nuevo_registro=True, controlador=None, parent=None ):

		#Constructor padre
		QDialog.__init__( self, parent )
		#Configuracion interfaz
		self.setupUi( self )

		#=======================================> VARIABLES
		self.nuevo_registro = nuevo_registro
		self.controladorCama = controlador

		#=================================================> MODIFICACIONES

		if self.nuevo_registro:

			self.setWindowTitle( "Nueva Cama" )
			self.pushButtonInsertar.setText( "Insertar" )
			self.pushButtonConsultar.hide()
			self.lineEditNumeroDeCama.setText( "Automatico" )
			self.lineEditNumeroDeCama.setReadOnly(True)

		else:

			self.setWindowTitle( "Modificar Cama" )
			self.pushButtonInsertar.setText( "Actualizar" )
			self.pushButtonConsultar.show()
			self.lineEditNumeroDeCama.setText( "" )
			self.lineEditNumeroDeCama.setReadOnly(False)


		#========================================> SENIALES Y SLOTS
		self.connect( self.pushButtonInsertar, SIGNAL( "clicked()" ), self.insertarActualizarCama )
		self.connect( self.pushButtonCancelar, SIGNAL( "clicked()" ), self.limpiarCampos )
		self.connect( self.pushButtonConsultar, SIGNAL( "clicked()" ), self.consultar )

	#============================================> METODOS
	def insertarActualizarCama( self ):

		codigo_area = self.lineEditCodigoArea.text()
		numero_cama = self.lineEditNumeroDeCama.text()
		descripcion = self.lineEditDescripcion.text()

		#AQUIE SE INGRESAN LOS DATOS A LA BASE DE DATOS
		if self.nuevo_registro:
			#EN CASO DE SE UN NUEVO REGISTRO
			pass

		else:
			#EN CASO DE SER UNA ACTUALIZACION
			pass

		self.limpiarCampos()

	def limpiarCampos( self ):

		if self.nuevo_registro:
			
			self.lineEditNumeroDeCama.setText( "" )
			self.lineEditDescripcion.setText( "" )

		else:

			self.lineEditCodigoArea.setText( "" )
			self.lineEditNumeroDeCama.setText( "" )
			self.lineEditDescripcion.setText( "" )

	def consultar( self ):

		#AQUI VA LA CONSULTA DE LA CAMA
		pass

#==================================================> LISTAR CAMAS <=====================================================

W_Camas_class , W_Camas_Base_class = uic.loadUiType('gui/administrador_uis/WidgetListarCamas.ui')


class WidgetListarCamas( QWidget, W_Camas_class ):

	def __init__( self, parent=None ):

		#Constructor padre
		QWidget.__init__( self, parent )
		#Configuracion de la interfaz
		self.setupUi( self )

		#========================================> VARIABLES
		self.controladorCama = " " #AQUI VA EL CONTROLADOR DE CAMA


	#============================================> METODOS
	def actualizar( self ):
		#area_seleccionada = self.comboBoxAreaCamas.currentText()
		#AQUI SE LISTAN LAS CAMAS EN LA TABLA DE CAMAS
		#self.tableWidgetCamas.clearContents()
		#self.tableWidgetCamas.insertRow( 0 )
		#self.tableWidgetCamas.setItem( 0, 0, QTableWidgetItem( "Codigo" ) )
		#self.tableWidgetCamas.setItem( 0, 1, QTableWidgetItem( "descripcion" ) )
		pass
			


# ===========================================> MEDICAMENTO <============================================================

D_Medicamento_class , D_Medicamento_Base_class = uic.loadUiType( 'gui/administrador_uis/DialogMedicamento.ui' )

class DialogMedicamento( QDialog, D_Medicamento_class ):

	def __init__( self, nuevo_registro=True, controlador=None, parent=None ):

		#Construtor padre
		QDialog.__init__( self, parent )
		#Configuracion interfaz
		self.setupUi( self )

		#=====================================> VARIABLES
		self.controladorMedicamento = controlador
		self.nuevo_registro = nuevo_registro

		#=====================================> MODIFICACIONES

		if self.nuevo_registro:

			self.setWindowTitle( "Nuevo Medicamento" )
			self.lineEditCodigo.setText( "Automatico" )
			self.lineEditCodigo.setReadOnly(True)
			self.pushButtonConsultar.hide()

		else:

			self.setWindowTitle( "Actualizar Medicamento" )
			self.lineEditCodigo.setText( "" )
			self.lineEditCodigo.setReadOnly(False)
			self.pushButtonConsultar.show()

		#========================================> SENIALES Y SLOTS
		self.connect( self.pushButtonInsertar, SIGNAL( "clicked()" ), self.insertarActualizarMedicamento )
		self.connect( self.pushButtonCancelar, SIGNAL( "clicked()" ), self.limpiarCampos )
		self.connect( self.pushButtonConsultar, SIGNAL( "clicked()" ), self.consultar )

	#=============================================> METODOS
	def insertarActualizarMedicamento( self ):

		codigo = self.lineEditCodigo.text()
		nombre = self.lineEditNombre.text()
		costo = self.lineEditCosto.text()
		descripcion = self.lineEditDescripcion.text()

		#AQUI SE INGRESA LA INFOMACION EN LA BASE DE DATOS
		if self.nuevo_registro:
			#EN CASO DE UN NUEVO REGISTRO
			pass
		else:
			#EN CASO DE UNA ACTUALIZACION
			pass

		self.limpiarCampos()

	def limpiarCampos( self ):

		if self.nuevo_registro:

			self.lineEditNombre.text()
			self.lineEditCosto.text()
			self.lineEditDescripcion.text()

		else:

			self.lineEditCodigo.text()
			self.lineEditNombre.text()
			self.lineEditCosto.text()
			self.lineEditDescripcion.text()

	
	def consultar( self ):
		#AQUI VA LA CONSULTA DEL MEDICAMENTO
		pass



#=========================================> Listar medicamentos <=======================================================

W_Medicamentos_class , W_MedicamentosBase_class = uic.loadUiType('gui/administrador_uis/WidgetListarMedicamentos.ui')


class WidgetListarMedicamentos( QWidget, W_Medicamentos_class ):

	def __init__( self, parent=None ):

		#Constructor padre
		QWidget.__init__( self, parent )
		#Configuracion interfaz
		self.setupUi( self )

		#========================================> VARIABLES
		self.controladorMedicamento = " " #AQUI VA EL CONTROLADOR DE MEDICAMENTO


	#============================================> METODOS
	def actualizar( self ):
		
		#AQUI SE LISTAN LAS CAMAS EN LA TABLA DE CAMAS
		#self.tableWidgetMedicamentos.clearContents()
		#self.tableWidgetMedicamentos.insertRow( 0 )
		#self.tableWidgetMedicamentos.setItem( 0, 0, QTableWidgetItem( "Codigo" ) )
		#self.tableWidgetMedicamentos.setItem( 0, 1, QTableWidgetItem( "descripcion" ) )
		pass

#===========================================> HABILIDAD <===============================================================

D_Habilidad_class , D_Habilidad_Base_class = uic.loadUiType( 'gui/administrador_uis/DialogHabilidad.ui' )


class DialogHabilidad( QDialog, D_Habilidad_class ):

	def __init__( self, nuevo_registro=True, controlador=None, parent=None ):

		#Constructor padre
		QDialog.__init__( self, parent )
		#Configuracion interfaz
		self.setupUi( self )
		
		#=========================================> VARIABLES
		self.controladorHabilidad = controlador
		self.nuevo_registro = nuevo_registro

		#=========================================> MODIFICACIONES

		if self.nuevo_registro:

			self.setWindowTitle( "Nueva Habilidad" )
			self.lineEditCodigo.setReadOnly( True )
			self.lineEditCodigo.setText( "Automatico" )
			self.pushButtonInsertar.setText( "Insertar" )
			self.pushButtonConsultar.hide()

		else:

			self.setWindowTitle( "Nueva Habilidad" )
			self.lineEditCodigo.setReadOnly( False )
			self.lineEditCodigo.setText( "" )
			self.pushButtonInsertar.setText( "Actualizar" )
			self.pushButtonConsultar.show()

		#=============================================> SENIALES Y SLOTS
		self.connect( self.pushButtonInsertar, SIGNAL( "clicked()" ), self.insertarActualizarHabilidad )
		self.connect( self.pushButtonCancelar,SIGNAL( "clicked()" ), self.limpiarCampos )
		self.connect( self.pushButtonConsultar, SIGNAL( "clicked()" ), self.consultar )

	#=================================================> METODOS
	def insertarActualizarHabilidad( self ):

		codigo = self.lineEditCodigo.text()
		descripcion = self.lineEditDescripcion.text()

		#AQUI SE INSEGRESA LA HABILIDAD A LA BASE DE DATOS
		if self.nuevo_registro:
			#EN CASO DE QUE SE INGRESE UN NUEVO REGISTRO
			pass
		else:
			#EN CASO DE QUE SE ESTE ACTUALIZANDO
			pass

		self.limpiarCampos()

	def limpiarCampos( self ):

		if self.nuevo_registro:

			self.lineEditDescripcion.setText( "" )

		else:

			self.lineEditCodigo.setText( "" )
			self.lineEditDescripcion.setText( "" )


	def consultar( self ):
		#AQUI SE CONSULTA LA HABILIDAD
		pass



#============================================> LISTAR HABILIDADES <=====================================================

W_Habilidades_class , W_Habilidades_Base_class = uic.loadUiType('gui/administrador_uis/WidgetListarHabilidades.ui')


class WidgetListarHabilidades( QWidget, W_Habilidades_class ):

	def __init__( self, parent=None ):
		
		#Constrcutro padre
		QWidget.__init__( self, parent )
		#Configuracion interfaz
		self.setupUi( self )

		#========================================> VARIABLES
		self.controladorMedicamento = " " #AQUI VA EL CONTROLADOR DE HABILIDADES


	#============================================> METODOS
	def actualizar( self ):
		
		#AQUI SE LISTAN LAS HABILIDADES EN LA TABLA DE HABILIDADES_ENFERMERA DE LA BASE DE DATOS
		#self.tableWidgetHabilidades.clearContents()
		#self.tableWidgetHabilidades.insertRow( 0 )
		#self.tableWidgetHabilidades.setItem( 0, 0, QTableWidgetItem( "Codigo" ) )
		#self.tableWidgetHabilidades.setItem( 0, 1, QTableWidgetItem( "descripcion" ) )
		pass
		

	
#=================================================> CAUSA <=============================================================

D_Causa_class , D_Causa_Base_class = uic.loadUiType( 'gui/administrador_uis/DialogCausa.ui' )

class DialogCausa( QDialog, D_Causa_class ):

	def __init__( self, nuevo_registro=True, controlador=None, parent=None ):


		#Constructor padre
		QDialog.__init__( self, parent )
		#Configuracion interfaz
		self.setupUi( self )

		#========================================> VARIABLES
		self.controladorCausa = controlador
		self.nuevo_registro = nuevo_registro

		#========================================> MODIFICACIONES

		if self.nuevo_registro:

			self.setWindowTitle( "Nueva Causa" )
			self.lineEditCodigo.setText( "Automatico" )
			self.lineEditCodigo.setReadOnly( True )
			self.pushButtonConsultar.hide()

		else:

			self.setWindowTitle( "Modiicar Causa" )
			self.lineEditCodigo.setText( "" )
			self.lineEditCodigo.setReadOnly( False )
			self.pushButtonConsultar.show()

		#============================================> SENIALES Y SLOTS
		self.connect( self.pushButtonInsertar, SIGNAL( "clicked()" ), self.insertarActualizarCausa )
		self.connect( self.pushButtonCancelar, SIGNAL( "clicked()" ), self.limpiarCampos )
		self.connect( self.pushButtonConsultar, SIGNAL( "clicked()" ), self.consultar )

	#=================================================> METODOS
	def insertarActualizarCausa( self ):

		codigo = self.lineEditCodigo.text()
		nombre = self.lineEditNombre.text()
		descripcion = self.lineEditDescripcion.text()

		#AQUI SE INGRESAN LOS DATOS A LA BASE DE DATOS
		if self.nuevo_registro:
			#EN CASO DE QUE SE INGRESE UN UEVO REGISTRO
			pass

		else:
			#EN CASO DE QUE SE ESTE ACTUALUZANDO
			pass

		self.limpiarCampos()

	def limpiarCampos( self ):

		if self.nuevo_registro:

			
			self.lineEditNombre.setText( "" )
			self.lineEditDescripcion.setText( "" )

		else:

			self.lineEditCodigo.setText( "" )
			self.lineEditNombre.setText( "" )
			self.lineEditDescripcion.setText( "" )

	

	def consultar( self ):

		#AQUI SE HACE LA CONSULTA DE LA CAUSA
		pass




#=============================================> LISTAR CAUSAS <=========================================================

W_Causas_class , W_Causas_Base_class = uic.loadUiType( 'gui/administrador_uis/WidgetListarCausas.ui' )

class WidgetListarCausas( QWidget, W_Causas_class ):

	def __init__( self, parent=None ):

		
		#Constructor padre
		QWidget.__init__( self, parent )
		#Configuracion interfaz
		self.setupUi( self )

		#========================================> VARIABLES
		self.controladorCausa = " " #AQUI VA EL CONTROLADOR DE CAUSA


	#============================================> METODOS
	def actualizar( self ):
		
		#AQUI SE LISTAN LAS CAUSAS DE LA BASE DE DATOS
		#self.tableWidgetListarCausas.clearContents()
		#self.tableWidgetListarCausas.insertRow( 0 )
		#self.tableWidgetListarCausas.setItem( 0, 0, QTableWidgetItem( "Codigo" ) )
		#self.tableWidgetListarCausas.setItem( 0, 1, QTableWidgetItem( "descripcion" ) )
		pass



#=============================================> INFORMES <==============================================================

#=======================================> AGENDA MEDICO MES

W_AgendaMedicoMes_class , W_AgendaMedicoMes_Base_class = uic.loadUiType("gui/administrador_uis/WidgetAgendaMedico.ui");

class WidgetAgendaMedicoMes( QWidget, W_AgendaMedicoMes_class ):

	def __init__( self, parent=None ):

		#Constructor padre
		QWidget.__init__( self, parent )
		#Configuracion interfaz
		self.setupUi( self )


#========================================> HISTORIA CLINICA PACIENTE

W_HistoriaPaciente_class , W_HistoriaPaciente_Base_class = uic.loadUiType("gui/administrador_uis/WidgetHistoriaClinica.ui");

class WidgetHistoriaClinicaPaciente( QWidget, W_HistoriaPaciente_class ):

	def __init__( self, parent=None ):

		#Constructor padre
		QWidget.__init__( self, parent )
		#Configuracion interfaz
		self.setupUi( self )

#=====================================> CITAS ATENDIDAS MEDICO MES

W_CitasMedico_class , W_CitasMedico_Base_class = uic.loadUiType("gui/administrador_uis/WidgetNumeroCitasMedico.ui");

class WidgetNumeroCitasMedico( QWidget, W_CitasMedico_class ):

	def __init__( self, parent=None ):

		#Constructor padre
		QWidget.__init__( self, parent )
		#Confifuracion interfaz
		self.setupUi( self )

#=====================================> COSTO PACIENTE MES ANIO

W_Costo_Paciente_class , W_Costo_Paciente_Base_class = uic.loadUiType("gui/administrador_uis/WidgetCostoPromedioPaciente.ui");

class WidgetCostoPromedioPaciente( QWidget, W_Costo_Paciente_class ):

	def __init__( self, parent=None ):

		#Constructor padre
		QWidget.__init__( self, parent )
		#Configuracion interfaz
		self.setupUi( self )
