-- PROYECTO DB
-- Archivo SQL con la implementación del esquema
-- George Romero
-- Bryan Tabarez
-- Aurelio Vivaz

--=================>  CREANDO LAS TABLAS <=================

--DROP TABLE IF EXISTS PERSONA CASCADE;
--DROP TABLE IF EXISTS PACIENTE CASCADE;
--DROP TABLE IF EXISTS EMPLEADO CASCADE;
--DROP TABLE IF EXISTS MEDICO CASCADE;
--DROP TABLE IF EXISTS ENFERMERA CASCADE;
--DROP TABLE IF EXISTS ENFERMERA_HABILIDADES CASCADE;
--DROP TABLE IF EXISTS AREA CASCADE;
--DROP TABLE IF EXISTS CAMA CASCADE;
--DROP TABLE IF EXISTS CAMA_PACIENTE CASCADE;

--DROP TABLE IF EXISTS Historia_clinica CASCADE;

--DROP TABLE IF EXISTS CAUSA CASCADE;
--DROP TABLE IF EXISTS MEDICAMENTO CASCADE;
--DROP TABLE IF EXISTS CAMPANA CASCADE;
--DROP TABLE IF EXISTS CAMPANA_PACIENTE CASCADE;

--DROP TABLE IF EXISTS REGISTRO_HISTORIA CASCADE;
--DROP TABLE IF EXISTS REGISTRO_HISTORIA_MEDICAMENTO CASCADE;
--DROP TABLE IF EXISTS HORARIO CASCADE;
--DROP TABLE IF EXISTS CITA CASCADE;

CREATE TABLE PERSONA
(
	identificacion INTEGER NOT NULL PRIMARY KEY,
	nombre VARCHAR(50) NOT NULL,
	direccion VARCHAR (100) NOT NULL,
	telefono INTEGER NOT NULL
);


CREATE TABLE PACIENTE
(
	identificacion INTEGER NOT NULL PRIMARY KEY,
	fecha_nacimiento DATE NOT NULL,
	actividad_economica VARCHAR(100) NOT NULL,
	num_seguridad_social INTEGER NOT NULL,

	CONSTRAINT persona_fk FOREIGN KEY (identificacion)
	REFERENCES PERSONA (identificacion)
	ON UPDATE CASCADE ON DELETE NO ACTION 
);


CREATE TABLE EMPLEADO
(
	identificacion INTEGER NOT NULL PRIMARY KEY,
	codigo_area VARCHAR (10) NOT NULL,
	email VARCHAR(50) NOT NULL,
	salario MONEY NOT NULL,
	id_jefe INTEGER NOT NULL,

	CONSTRAINT empleado_fk FOREIGN KEY (id_jefe)
	REFERENCES EMPLEADO (identificacion)
	ON UPDATE CASCADE ON DELETE NO ACTION, 

	CONSTRAINT persona_fk FOREIGN KEY (identificacion)
	REFERENCES PERSONA (identificacion)
	ON UPDATE CASCADE ON DELETE NO ACTION 

);


CREATE TABLE MEDICO
(
	identificacion INTEGER NOT NULL PRIMARY KEY,
	especialidad VARCHAR (100) NOT NULL,
	universidad VARCHAR (100) NOT NULL,
	num_licencia INTEGER NOT NULL,

	CONSTRAINT empleado_fk FOREIGN KEY (identificacion)
	REFERENCES EMPLEADO (identificacion)
	ON UPDATE CASCADE ON DELETE NO ACTION
);


CREATE TABLE ENFERMERA
(
	identificacion INTEGER NOT NULL PRIMARY KEY,
	anos_experiencia INTEGER NOT NULL,


	CONSTRAINT empleado_fk FOREIGN KEY (identificacion)
	REFERENCES EMPLEADO (identificacion)
	ON UPDATE CASCADE ON DELETE NO ACTION
);


CREATE TABLE ENFERMERA_HABILIDADES
(
	identificacion INTEGER NOT NULL,
	habilidad INTEGER NOT NULL,
	
	CONSTRAINT enfermera_habilidades_pk PRIMARY KEY (identificacion),

	CONSTRAINT enfermera_fk FOREIGN KEY (identificacion)
	REFERENCES ENFERMERA (identificacion)
	ON UPDATE CASCADE ON DELETE NO ACTION,
	
	CONSTRAINT habilidad_fk FOREIGN KEY (habilidad)
	REFERENCES HABILIDAD (codigo)
	ON UPDATE CASCADE ON DELETE NO ACTION
);


CREATE TABLE HABILIDAD
(
	codigo INTEGER NOT NULL PRIMARY KEY,
	descripcion VARCHAR (50) NOT NULL
)
	

CREATE TABLE AREA
(
	cod_area VARCHAR (10) NOT NULL PRIMARY KEY,
	nombre VARCHAR (100) NOT NULL,
	descripcion VARCHAR (200) NOT NULL
);


CREATE TABLE CAMA
(
	num_cama INTEGER NOT NULL PRIMARY KEY,
	estado VARCHAR (20) NOT NULL,
	descripcion VARCHAR (200) NOT NULL,
	cod_area VARCHAR (10) NOT NULL,

	CONSTRAINT area_fk FOREIGN KEY (cod_area)
	REFERENCES AREA (cod_area)
	ON UPDATE CASCADE ON DELETE NO ACTION
);


CREATE TABLE CAMA_PACIENTE
(
	num_cama INTEGER NOT NULL,
	id_paciente INTEGER NOT NULL,
	fecha_asignacion DATE NOT NULL,

	CONSTRAINT cama_paciente_pk PRIMARY KEY (num_cama, id_paciente),

	CONSTRAINT cama_fk FOREIGN KEY (num_cama)
	REFERENCES CAMA (num_cama)
	ON UPDATE CASCADE ON DELETE NO ACTION,

	CONSTRAINT paciente_fk FOREIGN KEY (id_paciente)
	REFERENCES PACIENTE (identificacion)
	ON UPDATE CASCADE ON DELETE NO ACTION
);


CREATE TABLE Historia_clinica
(
	numero_historia INTEGER NOT NULL PRIMARY KEY,
	id_paciente INTEGER NOT NULL,
	fecha_apertura DATE NOT NULL,

	CONSTRAINT paciente_fk FOREIGN KEY (id_paciente)
	REFERENCES PACIENTE (identificacion)
	ON UPDATE CASCADE ON DELETE NO ACTION
);


CREATE TABLE REGISTRO_HISTORIA
(
	id_registro INTEGER NOT NULL PRIMARY KEY,
	num_historia INTEGER NOT NULL,
	precio MONEY NOT NULL,

	CONSTRAINT historia_fk FOREIGN KEY (num_historia)
	REFERENCES Historia_clinica (num_historia)
	ON UPDATE CASCADE ON DELETE NO ACTION
);


CREATE TABLE CAUSA
(
	codigo VARCHAR (10) NOT NULL PRIMARY KEY,
	nombre VARCHAR (20) NOT NULL,
	descripcion VARCHAR (200) NOT NULL,

);


CREATE TABLE MEDICAMENTO
(
	codigo VARCHAR (10) NOT NULL PRIMARY KEY,
	costo MONEY NOT NULL,
	nombre VARCHAR (50) NOT NULL,
	descripcion VARCHAR (200)
);



CREATE TABLE CAMPANA
(
	codigo VARCHAR (10) NOT NULL PRIMARY KEY,
	id_medico INTEGER NOT NULL,
	nombre VARCHAR (100) NOT NULL,
	fecha_realizacion DATE NOT NULL,
	objetivo VARCHAR (200) NOT NULL,

	CONSTRAINT medico_fk FOREIGN KEY (id_medico)
	REFERENCES MEDICO (identificacion)
	ON UPDATE CASCADE ON DELETE NO ACTION
);


CREATE TABLE CAMPANA_PACIENTE
(
	id_paciente INTEGER NOT NULL,
	codigo VARCHAR (10),

	CONSTRAINT campana_paciente_pk PRIMARY KEY (id_paciente, codigo),

	CONSTRAINT paciente_fk FOREIGN KEY (id_paciente)
	REFERENCES PACIENTE (identificacion)
	ON UPDATE CASCADE ON DELETE NO ACTION,

	CONSTRAINT campana_fk FOREIGN KEY (codigo)
	REFERENCES CAMPANA (codigo)
	ON UPDATE CASCADE ON DELETE NO ACTION
);


CREATE TABLE HORARIO
(
	id_horario INTEGER NOT NULL,
	id_medico INTEGER NOT NULL,
	fecha DATE NOT NULL,
	hora TIME NOT NULL, 
	num_horario INTEGER NOT NULL,
	estado VARCHAR (20),

	CONSTRAINT horario_pk PRIMARY KEY (id_horario),

	CONSTRAINT medico_fk FOREIGN KEY (id_medico)
	REFERENCES MEDICO (identificacion)
	ON UPDATE CASCADE ON DELETE NO ACTION
);


CREATE TABLE CITA
(
	id_horario INTEGER NOT NULL,
	numero_historia INTEGER NOT NULL,
	estado VARCHAR (20)


	CONSTRAINT citas_pk PRIMARY KEY (id_horario, numero_historia),

	CONSTRAINT horario_fk FOREIGN KEY (id_horario)
	REFERENCES HORARIO (id_horario)
	ON UPDATE CASCADE ON DELETE NO ACTION,

	CONSTRAINT horario_fk FOREIGN KEY (numero_historia)
	REFERENCES HORARIO (id_horario)
	ON UPDATE CASCADE ON DELETE NO ACTION
);






