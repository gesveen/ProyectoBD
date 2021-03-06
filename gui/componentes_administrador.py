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
		self.dialogoInfo = DialogInformacion(self)

		#=========================================> VARIABLES
		self.controladorDaosEmpleados = controlador
		self.tipo_operacion = tipo_operacion
		
		#=========================================> WIDGETS
		self.widgetTipoEmpleadoEnfermera = WidgetTipoEmpleadoEnfermera( self.widgetTipoEmpleado, controlador.conexion )
		self.widgetTipoEmpleadoEnfermera.hide()
		self.widgetTipoEmpleadoMedico = WidgetTipoEmpleadoMedico( self.widgetTipoEmpleado, controlador.conexion )
		self.widgetTipoEmpleadoMedico.hide()

		#=========================================> SENIALES Y SLOTS
		self.connect( self.comboBoxTipoEmpleado, SIGNAL( "currentIndexChanged(int)" ), self.mostrarTipoEmpleado )
		self.connect( self.pushButtonGuardar, SIGNAL( "clicked()" ), self.guardarEmpleado )
		self.connect( self.pushButtonConsultar, SIGNAL( "clicked()" ), self.consultarEmpleado )
		self.connect( self.pushButtonLimpiar, SIGNAL( "clicked()" ), self.limpiarCampos )
		self.connect( self.pushButtonEliminar, SIGNAL( "clicked()" ), self.eliminarEmpleado )

		#==========================================>MODIFICACIONES
		# self.mostrarTipoEmpleado(0)

		# NUEVO EMPLEADO
		if self.tipo_operacion is 1:			

			self.setWindowTitle("Agregar Empleado")
			self.pushButtonGuardar.setText("Guardar")
			self.pushButtonConsultar.hide()
			self.pushButtonEliminar.hide()

		# MODIFICAR EMPLEADO
		if self.tipo_operacion is 2:

			self.setWindowTitle("Modificar Empleado")
			self.pushButtonGuardar.setText("Guardar cambios")
			self.pushButtonConsultar.show()


	# MOSTRAR WIDGET PARA TIPO EMPLEADO
	#****************************************************************************************************************
	def mostrarTipoEmpleado( self, indice ):
		if( indice == 0 ):

			self.widgetTipoEmpleadoEnfermera.show()
			self.widgetTipoEmpleadoMedico.hide()
		
		elif( indice == 1 ):
			
			self.widgetTipoEmpleadoMedico.show()
			self.widgetTipoEmpleadoEnfermera.hide()


	# CONSULTAR EL EMPLEADO
	#****************************************************************************************************************
	def consultarEmpleado( self ):
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
				self.widgetTipoEmpleadoEnfermera.lineEditAniosExperiencia.setText( resultado[8] )
				habilidades = resultado[9]
				self.widgetTipoEmpleadoEnfermera.llenarTablaHabilidadesEnfermera( habilidades )
				self.lineEditIdentificacion.setReadOnly(True)
		
		# CONSULTAR MEDICO
		if indice is 1:
			resultado = self.controladorDaosEmpleados.consultarDatosMedico( self.identificacion )
			if isinstance(resultado, str):
				self.dialogoInfo.showMensaje( "Consultar Medico", resultado )
			if isinstance(resultado, tuple):
				self.lineEditIdentificacion.setText( str(resultado[0]) )
				self.lineEditNombre.setText( resultado[1] )
				self.lineEditDireccion.setText( resultado[2] )
				self.lineEditTelefono.setText( str(resultado[3]) )
				self.lineEditCodigoArea.setText( str(resultado[4]) )
				self.lineEditEmail.setText( resultado[5] )
				self.lineEditSalario.setText( str(resultado[6]) )
				self.lineEditJefe.setText( str(resultado[7]) )
				# Datos medico
				self.widgetTipoEmpleadoMedico.lineEditEspecialidad.setText( resultado[8] )
				self.widgetTipoEmpleadoMedico.lineEditUniversidad.setText( resultado[9] )
				self.widgetTipoEmpleadoMedico.lineEditNumeroLicencia.setText( str(resultado[10]) )
				self.lineEditIdentificacion.setReadOnly(True)

	

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
			numero_filas = self.widgetTipoEmpleadoEnfermera.tableWidgetHabilidades.rowCount()
			
			# Falta: metodo para recuperar habilidades de enfermera desde el widget
			#arreglo_habilidades = self.widgetTipoEmpleadoEnfermera.habilidadesEnfermera()
			
			# GUARDAR
			if self.tipo_operacion is 1:
				identificacion = str( self.lineEditIdentificacion.text() )
				result = self.controladorDaosEmpleados.insertarEnfermera( identificacion, nombre, direccion, telefono,
					codigo_area, email, salario, id_jefe, anios_experiencia, [1] )
				self.dialogoInfo.showMensaje( "Insertar Enfermera", result )

			
			# MODIFICAR
			if self.tipo_operacion is 2:
				result = self.controladorDaosEmpleados.actualizarDatosEnfermera( self.identificacion, nombre, direccion, telefono,
					codigo_area, email, salario, id_jefe, anios_experiencia, [1] )
				self.dialogoInfo.showMensaje( "Modificar Enfermera", result )
				#hab = self.widgetTipoEmpleadoEnfermera.habilidadesEnfermera()
				#print hab
		
		# MEDICO:
		if indice is 1:

			especialidad = str(self.widgetTipoEmpleadoMedico.lineEditEspecialidad.text())
			universidad = str (self.widgetTipoEmpleadoMedico.lineEditUniversidad.text())
			numero_licencia = str(self.widgetTipoEmpleadoMedico.lineEditNumeroLicencia.text())
			
			# GUARDAR
			if self.tipo_operacion is 1:
				identificacion = str( self.lineEditIdentificacion.text() )
				result = self.controladorDaosEmpleados.insertarMedico(identificacion, nombre, direccion, telefono,
					str(codigo_area), email, salario, id_jefe, especialidad, universidad, numero_licencia)
				self.dialogoInfo.showMensaje( "Insertar Medico", result )

			# MODIFICAR
			if self.tipo_operacion is 2:
				identificacion = str( self.lineEditIdentificacion.text() )
				result = self.controladorDaosEmpleados.actualizarDatosMedico(self.identificacion, nombre, direccion, telefono,
					str(codigo_area), email, salario, id_jefe, especialidad, universidad, numero_licencia)
				self.dialogoInfo.showMensaje( "Modificar Medico", result )

	# ELIMINAR EMPLEADO
	#****************************************************************************************************************
	def eliminarEmpleado( self ):
		identificacion = str( self.lineEditIdentificacion.text() )
		indice =  self.comboBoxTipoEmpleado.currentIndex()

		# ENFERMERA
		if indice is 0:
			eliEnf = self.controladorDaosEmpleados.eliminarEnfermera( identificacion )
			self.dialogoInfo.showMensaje( "Consultar Enfermera", eliEnf )

		# MEDICO
		if indice is 1:
			eliMed = self.controladorDaosEmpleados.eliminarMedico( identificacion )
			self.dialogoInfo.showMensaje( "Consultar Enfermera", eliMed )
	
	# LIMPIAR CAMPOS DE LA VENTANA
	#****************************************************************************************************************
	def limpiarCampos( self ):

		self.lineEditIdentificacion.setText( "" )
		self.lineEditNombre.setText( "" )
		self.lineEditDireccion.setText( "" )
		self.lineEditTelefono.setText( "" )
		self.lineEditCodigoArea.setText( "" )
		self.lineEditEmail.setText( "" )
		self.lineEditSalario.setText( "" )
		self.lineEditJefe.setText( "" )
		self.lineEditIdentificacion.setReadOnly(False)

		#self.comboBoxCodigoArea.currentText()
		#self.comboBoxCodigoJefe.currentText()

		# self.widgetTipoEmpleadoEnfermera.lineEditAniosExperiencia.setText("")
		# numero_filas = self.widgetTipoEmpleadoEnfermera.tableWidgetHabilidadesEnfermera.rowCount()
		# if numero_filas > 0:
		# 	self.widgetTipoEmpleadoEnfermera.tableWidgetHabilidadesEnfermera.clear()

		# self.widgetTipoEmpleadoMedico.lineEditEspecialidad.setText("")
		# self.widgetTipoEmpleadoMedico.lineEditUniversidad.setText("")
		# self.widgetTipoEmpleadoMedico.lineEditNumeroLicencia.setText("")
	


#============================================> TIPO EMPLEADO ENFERMERA <================================================

W_Enfermera_class , W_Enfermera_Base_class = uic.loadUiType('gui/administrador_uis/WidgetTipoEmpleadoEnfermera.ui')

class WidgetTipoEmpleadoEnfermera( QWidget, W_Enfermera_class ):

	def __init__( self, parent=None, conexion=None ):

		#Constructor padre
		QWidget.__init__( self, parent )
		#Configuracion de la interfaz	
		self.setupUi( self )

		#=============================================> VARIABLES
		self.controladorHabilidad = ControlDaoHabilidades(conexion)

		#=============================================> SENIALES Y SLOTS
		self.connect( self.pushButtonAgregar, SIGNAL( "clicked()" ), self.agregar )
		self.connect( self.pushButtonEliminar, SIGNAL( "clicked()" ), self.eliminar )

		
		self.llenarTablaHabilidades( )

	#==================================================> METODOS

	# HABILIDADES DESDE LA BASE DE DATOS
	def llenarTablaHabilidades( self):

		# AQUI SE DEBE ACTUALIZAR LA TABLA QUE CONTIENE LAS HABILIDADES DE LA ENFERMERA CON LA
		# INFROMACION DE LA BASE DE DATOS
		#self.tableWidgetHabilidadesEnfermera.clearContents()
		result = self.controladorHabilidad.buscarHabilidades()

		# for i in range( 0, self.tableWidgetHabilidadesEnfermera.rowCount() ):
		#  	self.tableWidgetHabilidades.removeRow(0)

		for row in result:
			self.tableWidgetHabilidades.insertRow( 0 )
			self.tableWidgetHabilidades.setItem( 0, 0, QTableWidgetItem( str(row[0]) ) )
			self.tableWidgetHabilidades.setItem( 0, 1, QTableWidgetItem( row[1] ) )

	def llenarTablaHabilidadesEnfermera( self, habilidades ):
			# AQUI SE DEBE ACTUALIZAR LA TABLA QUE CONTIENE LAS HABILIDADES DE LA ENFERMERA CON LA
			# INFROMACION DE LA BASE DE DATOS

			for i in range( 0, self.tableWidgetHabilidadesEnfermera.rowCount() ):
			  	self.tableWidgetHabilidadesEnfermera.removeRow(0)

			for row in habilidades:
				self.tableWidgetHabilidadesEnfermera.insertRow( 0 )
				self.tableWidgetHabilidadesEnfermera.setItem( 0, 0, QTableWidgetItem( str(row[0]) ) )
				self.tableWidgetHabilidadesEnfermera.setItem( 0, 1, QTableWidgetItem( row[1] ) )

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

	def __init__( self, parent=None, conexion=None):

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
		mostrarError = QErrorMessage(self)

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
