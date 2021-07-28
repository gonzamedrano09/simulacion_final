import math
from PyQt5 import uic
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from dominio.controlador_taller_costura import *
from soporte.validador_enteros import ValidadorEnteros
from soporte.validador_decimales import ValidadorDecimales
from soporte.ruta import Ruta


class VentanaTallerCostura(QMainWindow):

    """ Atributos """

    app = None
    controlador = None
    iteraciones_simuladas = None
    informacion_simulacion = None

    pagina_actual = None
    cantidad_paginas = None
    tamanio_pagina = 100

    """ Constructor """

    def __init__(self, app):

        # Guardo app
        self.app = app

        # Genero ventana a partir de ui y creo controlador
        QMainWindow.__init__(self)
        uic.loadUi(Ruta.generar_ruta("interfaz/ventana_taller_costura.ui"), self)
        self.controlador = ControladorTallerCostura(self)

        # Agrego validadores a los campos
        validador_7_enteros = ValidadorEnteros(7)
        validador_3_enteros = ValidadorEnteros(3)
        validador_2_enteros = ValidadorEnteros(2)
        validador_decimales = ValidadorDecimales(4, 2)
        self.txt_tiempo_simulacion.setValidator(validador_7_enteros)
        self.txt_tiempo_desde.setValidator(validador_7_enteros)
        self.txt_cantidad_iteraciones.setValidator(validador_7_enteros)
        self.txt_tiempo_llegada_trabajo.setValidator(validador_decimales)
        self.txt_tiempo_zurcido.setValidator(validador_decimales)
        self.txt_tiempo_costura.setValidator(validador_decimales)
        self.txt_tiempo_planchado.setValidator(validador_decimales)
        self.txt_tiempo_inspeccion.setValidator(validador_decimales)
        self.txt_cantidad_empleados_generales.setValidator(validador_2_enteros)
        self.txt_cantidad_empleados_zurcido.setValidator(validador_2_enteros)
        self.txt_cantidad_empleados_costura.setValidator(validador_2_enteros)
        self.txt_cantidad_empleados_planchado.setValidator(validador_2_enteros)
        self.txt_cantidad_inspectores.setValidator(validador_2_enteros)
        self.txt_porcentaje_trabajos_rechazados.setValidator(validador_3_enteros)

        # Conecto los botones con los eventos
        self.btn_pagina_anterior_1.clicked.connect(self.accion_volver_1_pagina)
        self.btn_pagina_anterior_10.clicked.connect(self.accion_volver_10_paginas)
        self.btn_pagina_siguiente_1.clicked.connect(self.accion_siguiente_1_pagina)
        self.btn_pagina_siguiente_10.clicked.connect(self.accion_siguiente_10_paginas)
        self.rb_empleados_generales.clicked.connect(self.accion_empleados_generales)
        self.rb_empleados_especializados.clicked.connect(self.accion_empleados_especializados)
        self.btn_limpiar.clicked.connect(self.accion_limpiar)
        self.btn_simular.clicked.connect(self.accion_simular)

    """ Acciones """

    def accion_volver_1_pagina(self):

        # verifico que se haya realizado una simulación
        if self.iteraciones_simuladas is not None:

            # Calculo nueva página controlando límites
            nueva_pagina = self.pagina_actual
            if (nueva_pagina - 1) < 1:
                nueva_pagina = 1
            else:
                nueva_pagina -= 1

            # Vuelvo a carga la tabla si corresponde
            if nueva_pagina != self.pagina_actual:
                self.pagina_actual = nueva_pagina
                self.cargar_tabla_iteraciones_simuladas()
                self.lbl_informacion_paginas.setText(str(self.pagina_actual) + "/" + str(self.cantidad_paginas))

    def accion_volver_10_paginas(self):

        # verifico que se haya realizado una simulación
        if self.iteraciones_simuladas is not None:

            # Calculo nueva página controlando límites
            nueva_pagina = self.pagina_actual
            if (nueva_pagina - 10) < 1:
                nueva_pagina = 1
            else:
                nueva_pagina -= 10

            # Vuelvo a carga la tabla si corresponde
            if nueva_pagina != self.pagina_actual:
                self.pagina_actual = nueva_pagina
                self.cargar_tabla_iteraciones_simuladas()
                self.lbl_informacion_paginas.setText(str(self.pagina_actual) + "/" + str(self.cantidad_paginas))

    def accion_siguiente_1_pagina(self):

        # verifico que se haya realizado una simulación
        if self.iteraciones_simuladas is not None:

            # Calculo nueva página controlando límites
            nueva_pagina = self.pagina_actual
            if (nueva_pagina + 1) > self.cantidad_paginas:
                nueva_pagina = self.cantidad_paginas
            else:
                nueva_pagina += 1

            # Vuelvo a carga la tabla si corresponde
            if nueva_pagina != self.pagina_actual:
                self.pagina_actual = nueva_pagina
                self.cargar_tabla_iteraciones_simuladas()
                self.lbl_informacion_paginas.setText(str(self.pagina_actual) + "/" + str(self.cantidad_paginas))

    def accion_siguiente_10_paginas(self):

        # verifico que se haya realizado una simulación
        if self.iteraciones_simuladas is not None:

            # Calculo nueva página controlando límites
            nueva_pagina = self.pagina_actual
            if (nueva_pagina + 10) > self.cantidad_paginas:
                nueva_pagina = self.cantidad_paginas
            else:
                nueva_pagina += 10

            # Vuelvo a carga la tabla si corresponde
            if nueva_pagina != self.pagina_actual:
                self.pagina_actual = nueva_pagina
                self.cargar_tabla_iteraciones_simuladas()
                self.lbl_informacion_paginas.setText(str(self.pagina_actual) + "/" + str(self.cantidad_paginas))

    def accion_empleados_generales(self):

        # Limpio txts
        self.txt_cantidad_empleados_generales.clear()
        self.txt_cantidad_empleados_zurcido.clear()
        self.txt_cantidad_empleados_costura.clear()
        self.txt_cantidad_empleados_planchado.clear()

        # Limpio radio butons
        self.rb_empleados_especializados.setChecked(False)

        # Deshabilito inputs dependiendo de tipos de empleados por defecto
        self.txt_cantidad_empleados_generales.setEnabled(True)
        self.txt_cantidad_empleados_zurcido.setEnabled(False)
        self.txt_cantidad_empleados_costura.setEnabled(False)
        self.txt_cantidad_empleados_planchado.setEnabled(False)

        # Cargo valores por defecto en txts
        self.txt_cantidad_empleados_generales.setText("10")
        self.txt_porcentaje_trabajos_rechazados.setText("20")

    def accion_empleados_especializados(self):

        # Limpio txts
        self.txt_cantidad_empleados_generales.clear()
        self.txt_cantidad_empleados_zurcido.clear()
        self.txt_cantidad_empleados_costura.clear()
        self.txt_cantidad_empleados_planchado.clear()

        # Limpio radio butons
        self.rb_empleados_generales.setChecked(False)

        # Deshabilito inputs dependiendo de tipos de empleados por defecto
        self.txt_cantidad_empleados_generales.setEnabled(False)
        self.txt_cantidad_empleados_zurcido.setEnabled(True)
        self.txt_cantidad_empleados_costura.setEnabled(True)
        self.txt_cantidad_empleados_planchado.setEnabled(True)

        # Cargo valores por defecto en txts
        self.txt_cantidad_empleados_zurcido.setText("2")
        self.txt_cantidad_empleados_costura.setText("5")
        self.txt_cantidad_empleados_planchado.setText("3")
        self.txt_porcentaje_trabajos_rechazados.setText("10")

    def accion_limpiar(self):

        # Restauro valores por defecto de interfaz y limpio tabla
        self.limpiar_datos()
        self.limpiar_interfaz()
        self.limpiar_tabla()
        self.preparar_tabla()
        self.mostrar_porcentaje_simulacion()
        self.mostrar_porcentaje_datos()
        self.mostrar_cantidad_iteraciones_realizadas()

    def accion_simular(self):

        # Obtengo parametros verificando que no sean vacios
        tiempo_simulacion = None
        tiempo_desde = None
        cantidad_iteraciones = None
        tiempo_llegada_trabajo = None
        tiempo_zurcido = None
        tiempo_costura = None
        tiempo_planchado = None
        tiempo_inspeccion = None
        empleados_generales = True
        cantidad_empleados_generales = None
        cantidad_empleados_zurcido = None
        cantidad_empleados_costura = None
        cantidad_empleados_planchado = None
        cantidad_inspectores = None
        porcentaje_trabajos_rechazados = None
        if self.txt_tiempo_simulacion.text() != "":
            tiempo_simulacion = int(self.txt_tiempo_simulacion.text())
        if self.txt_tiempo_desde.text() != "":
            tiempo_desde = int(self.txt_tiempo_desde.text())
        if self.txt_cantidad_iteraciones.text() != "":
            cantidad_iteraciones = int(self.txt_cantidad_iteraciones.text())
        if self.txt_tiempo_llegada_trabajo.text() != "":
            tiempo_llegada_trabajo = float(self.txt_tiempo_llegada_trabajo.text().replace(",", "."))
        if self.txt_tiempo_zurcido.text() != "":
            tiempo_zurcido = float(self.txt_tiempo_zurcido.text().replace(",", "."))
        if self.txt_tiempo_costura.text() != "":
            tiempo_costura = float(self.txt_tiempo_costura.text().replace(",", "."))
        if self.txt_tiempo_planchado.text() != "":
            tiempo_planchado = float(self.txt_tiempo_planchado.text().replace(",", "."))
        if self.txt_tiempo_inspeccion.text() != "":
            tiempo_inspeccion = float(self.txt_tiempo_inspeccion.text().replace(",", "."))
        if not self.rb_empleados_generales.isChecked():
            empleados_generales = False
        if self.txt_cantidad_empleados_generales.text() != "":
            cantidad_empleados_generales = int(self.txt_cantidad_empleados_generales.text())
        if self.txt_cantidad_empleados_zurcido.text() != "":
            cantidad_empleados_zurcido = int(self.txt_cantidad_empleados_zurcido.text())
        if self.txt_cantidad_empleados_costura.text() != "":
            cantidad_empleados_costura = int(self.txt_cantidad_empleados_costura.text())
        if self.txt_cantidad_empleados_planchado.text() != "":
            cantidad_empleados_planchado = int(self.txt_cantidad_empleados_planchado.text())
        if self.txt_cantidad_inspectores.text() != "":
            cantidad_inspectores = int(self.txt_cantidad_inspectores.text())
        if self.txt_porcentaje_trabajos_rechazados.text() != "":
            porcentaje_trabajos_rechazados = int(self.txt_porcentaje_trabajos_rechazados.text())

        # Valido parametros
        if tiempo_simulacion is None or tiempo_simulacion <= 0:
            self.mostrar_mensaje("Error", "El tiempo a simular tiene que ser mayor a cero")
            return
        if tiempo_desde is None:
            self.mostrar_mensaje("Error", "El tiempo desde el cuál mostrar la simulación no puede ser vacío")
            return
        if cantidad_iteraciones is None or cantidad_iteraciones <= 0:
            self.mostrar_mensaje("Error", "La cantidad de iteraciones a mostrar de la simulación tiene que ser mayor a "
                                          "cero")
            return
        if tiempo_desde > tiempo_simulacion:
            self.mostrar_mensaje("Error", "El tiempo desde el cuál mostrar la simulación no puede ser mayor a la "
                                          "cantidad de tiempo simulado")
            return
        if tiempo_llegada_trabajo is None or tiempo_llegada_trabajo <= 0:
            self.mostrar_mensaje("Error", "El tiempo medio de llegada de trabajos tiene que ser mayor a cero")
            return
        if tiempo_zurcido is None or tiempo_zurcido <= 0:
            self.mostrar_mensaje("Error", "El tiempo medio de zurcido tiene que ser mayor a cero")
            return
        if tiempo_costura is None or tiempo_costura <= 0:
            self.mostrar_mensaje("Error", "El tiempo medio de costura tiene que ser mayor a cero")
            return
        if tiempo_planchado is None or tiempo_planchado <= 0:
            self.mostrar_mensaje("Error", "El tiempo medio de planchado tiene que ser mayor a cero")
            return
        if tiempo_inspeccion is None or tiempo_inspeccion <= 0:
            self.mostrar_mensaje("Error", "El tiempo medio de inspección tiene que ser mayor a cero")
            return
        if empleados_generales:
            if cantidad_empleados_generales is None or cantidad_empleados_generales <= 0:
                self.mostrar_mensaje("Error", "La cantidad de empleados generales tiene que ser mayor a cero")
                return
        else:
            if cantidad_empleados_zurcido is None or cantidad_empleados_zurcido <= 0:
                self.mostrar_mensaje("Error", "La cantidad de empleados de zurcido tiene que ser mayor a cero")
                return
            if cantidad_empleados_costura is None or cantidad_empleados_costura <= 0:
                self.mostrar_mensaje("Error", "La cantidad de empleados de costura tiene que ser mayor a cero")
                return
            if cantidad_empleados_planchado is None or cantidad_empleados_planchado <= 0:
                self.mostrar_mensaje("Error", "La cantidad de empleados de planchado tiene que ser mayor a cero")
                return
        if cantidad_inspectores is None or cantidad_inspectores <= 0:
            self.mostrar_mensaje("Error", "La cantidad de inspectores tiene que ser mayor a cero")
            return
        if porcentaje_trabajos_rechazados is None or not (0 <= porcentaje_trabajos_rechazados <= 100):
            self.mostrar_mensaje("Error", "El porcentaje de trabajos rechazados debe ser entre 0% y 100%")
            return

        # Limpio elementos de interfaz
        self.limpiar_tabla()
        self.mostrar_porcentaje_simulacion()
        self.mostrar_porcentaje_datos()
        self.mostrar_cantidad_iteraciones_realizadas()

        # Realizo simulacion y obtengo iteraciones a mostrar
        self.iteraciones_simuladas, self.informacion_simulacion = self.controlador.simular(
            tiempo_simulacion, tiempo_desde, cantidad_iteraciones, tiempo_llegada_trabajo, tiempo_zurcido,
            tiempo_costura, tiempo_planchado, tiempo_inspeccion, empleados_generales, cantidad_empleados_generales,
            cantidad_empleados_zurcido, cantidad_empleados_costura, cantidad_empleados_planchado, cantidad_inspectores,
            porcentaje_trabajos_rechazados)

        # Obtengo datos necesarios para generacion de headers
        ids_empleados_generales = self.informacion_simulacion.get("ids_empleados_generales")
        ids_empleados_zurcido = self.informacion_simulacion.get("ids_empleados_zurcido")
        ids_empleados_costura = self.informacion_simulacion.get("ids_empleados_costura")
        ids_empleados_planchado = self.informacion_simulacion.get("ids_empleados_planchado")
        ids_inspectores = self.informacion_simulacion.get("ids_inspectores")
        ids_colas_empleados = self.informacion_simulacion.get("ids_colas_empleados")
        ids_colas_inspectores = self.informacion_simulacion.get("ids_colas_inspectores")
        ids_trabajos = self.informacion_simulacion.get("ids_trabajos")

        # Preparo headers de tabla de acuerdo a iteraciones simuladas
        self.preparar_tabla(empleados_generales, ids_empleados_generales, ids_empleados_zurcido, ids_empleados_costura,
                            ids_empleados_planchado, ids_inspectores, ids_colas_empleados, ids_colas_inspectores,
                            ids_trabajos)

        # Muestro dato de cantidad iteraciones efectivas realizadas
        self.mostrar_cantidad_iteraciones_realizadas(self.informacion_simulacion.get("cantidad_iteraciones_realizadas"))

        # Calculo y seteo datos de paginación y iteraciones efectivas realizadas
        self.pagina_actual = 1
        self.cantidad_paginas = math.ceil(len(self.iteraciones_simuladas) / self.tamanio_pagina)
        self.lbl_informacion_paginas.setText(str(self.pagina_actual) + "/" + str(self.cantidad_paginas))

        # Cargo tabla
        self.cargar_tabla_iteraciones_simuladas()

    """ Metodos """

    def limpiar_datos(self):

        # Limpio datos
        self.iteraciones_simuladas = None
        self.informacion_simulacion = None
        self.pagina_actual = None
        self.cantidad_paginas = None

    def limpiar_interfaz(self):

        # Limpio txts
        self.txt_tiempo_simulacion.clear()
        self.txt_tiempo_desde.clear()
        self.txt_cantidad_iteraciones.clear()
        self.txt_tiempo_llegada_trabajo.clear()
        self.txt_tiempo_zurcido.clear()
        self.txt_tiempo_costura.clear()
        self.txt_tiempo_planchado.clear()
        self.txt_tiempo_inspeccion.clear()
        self.txt_cantidad_empleados_generales.clear()
        self.txt_cantidad_empleados_zurcido.clear()
        self.txt_cantidad_empleados_costura.clear()
        self.txt_cantidad_empleados_planchado.clear()
        self.txt_cantidad_inspectores.clear()
        self.txt_porcentaje_trabajos_rechazados.clear()

        # Limpio radio butons
        self.rb_empleados_generales.setChecked(True)

        # Deshabilito inputs dependiendo de tipos de empleados por defecto
        self.txt_cantidad_empleados_generales.setEnabled(True)
        self.txt_cantidad_empleados_zurcido.setEnabled(False)
        self.txt_cantidad_empleados_costura.setEnabled(False)
        self.txt_cantidad_empleados_planchado.setEnabled(False)

        # Cargo valores por defecto en labels relacionados con paginación e iteraciones a mostrar
        self.lbl_informacion_paginas.setText("0/0")
        self.lbl_informacion_cantidad_total_iteraciones_realizadas.setText("0")

        # Cargo valores por defecto en txts
        self.txt_tiempo_llegada_trabajo.setText("2,5")
        self.txt_tiempo_zurcido.setText("4")
        self.txt_tiempo_costura.setText("12")
        self.txt_tiempo_planchado.setText("6")
        self.txt_tiempo_inspeccion.setText("3")
        self.txt_cantidad_empleados_generales.setText("10")
        self.txt_cantidad_inspectores.setText("2")
        self.txt_porcentaje_trabajos_rechazados.setText("20")

    def limpiar_tabla(self):

        # Limpio grilla de semanas simuladas
        self.grid_iteraciones_simuladas.clearSelection()
        self.grid_iteraciones_simuladas.setCurrentCell(-1, -1)
        self.grid_iteraciones_simuladas.setRowCount(0)

    def preparar_tabla(self, empleados_generales=True, ids_empleados_generales=None, ids_empleados_zurcido=None,
                       ids_empleados_costura=None, ids_empleados_planchado=None, ids_inspectores=None,
                       ids_colas_empleados=None, ids_colas_inspectores=None, ids_trabajos=None):

        # Genero listas vacias en caso de parametros None
        if ids_empleados_generales is None:
            ids_empleados_generales = ["g0"]
        if ids_empleados_zurcido is None:
            ids_empleados_zurcido = []
        if ids_empleados_costura is None:
            ids_empleados_costura = []
        if ids_empleados_planchado is None:
            ids_empleados_planchado = []
        if ids_inspectores is None:
            ids_inspectores = ["i0"]
        if ids_colas_empleados is None:
            ids_colas_empleados = ["zurcido", "costura", "planchado"]
        if ids_colas_inspectores is None:
            ids_colas_inspectores = ["inspeccion"]
        if ids_trabajos is None:
            ids_trabajos = [0]

        # Calculo la cantidad de columnas a generar
        cantidad_empleados_generales = len(ids_empleados_generales)
        cantidad_empleados_zurcido = len(ids_empleados_zurcido)
        cantidad_empleados_costura = len(ids_empleados_costura)
        cantidad_empleados_planchado = len(ids_empleados_planchado)
        cantidad_inspectores = len(ids_inspectores)
        cantidad_colas_empleados = len(ids_colas_empleados)
        cantidad_colas_inspectores = len(ids_colas_inspectores)
        cantidad_trabajos = len(ids_trabajos)
        cantidad_columas = 20
        if empleados_generales:
            cantidad_columas += cantidad_empleados_generales * 3
        else:
            cantidad_columas += cantidad_empleados_zurcido + cantidad_empleados_costura + cantidad_empleados_planchado
        cantidad_columas += cantidad_inspectores
        if empleados_generales:
            cantidad_columas += cantidad_empleados_generales
        else:
            cantidad_columas += cantidad_empleados_zurcido + cantidad_empleados_costura + cantidad_empleados_planchado
        cantidad_columas += cantidad_colas_empleados
        cantidad_columas += cantidad_inspectores
        cantidad_columas += cantidad_colas_inspectores
        # cantidad_columas += cantidad_trabajos * 5
        cantidad_columas += cantidad_trabajos

        # Preparo tabla de tiempo simulado
        self.grid_iteraciones_simuladas.setColumnCount(cantidad_columas)
        i = 0

        header = QTableWidgetItem("N° iteración")
        header.setBackground(QColor(204, 204, 204))
        self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
        i += 1
        header = QTableWidgetItem("Evento")
        header.setBackground(QColor(204, 204, 204))
        self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
        i += 1
        header = QTableWidgetItem("Reloj")
        header.setBackground(QColor(204, 204, 204))
        self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
        i += 1

        header = QTableWidgetItem("RND")
        header.setBackground(QColor(255, 242, 204))
        self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
        i += 1
        header = QTableWidgetItem("T. prox. trabajo")
        header.setBackground(QColor(255, 242, 204))
        self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
        i += 1
        header = QTableWidgetItem("Prox. trabajo")
        header.setBackground(QColor(255, 242, 204))
        self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
        i += 1

        header = QTableWidgetItem("RND")
        header.setBackground(QColor(208, 224, 227))
        self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
        i += 1
        header = QTableWidgetItem("T. zurcido")
        header.setBackground(QColor(208, 224, 227))
        self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
        i += 1
        if empleados_generales:
            for id_empleado_general in ids_empleados_generales:
                header = QTableWidgetItem("F. zurc. (" + str(id_empleado_general) + ")")
                header.setBackground(QColor(208, 224, 227))
                self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
                i += 1
        else:
            for id_empleado_zurcido in ids_empleados_zurcido:
                header = QTableWidgetItem("F. zurc. (" + str(id_empleado_zurcido) + ")")
                header.setBackground(QColor(208, 224, 227))
                self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
                i += 1

        header = QTableWidgetItem("RND")
        header.setBackground(QColor(217, 234, 211))
        self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
        i += 1
        header = QTableWidgetItem("T. cost.")
        header.setBackground(QColor(217, 234, 211))
        self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
        i += 1
        if empleados_generales:
            for id_empleado_general in ids_empleados_generales:
                header = QTableWidgetItem("F. cost. (" + str(id_empleado_general) + ")")
                header.setBackground(QColor(217, 234, 211))
                self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
                i += 1
        else:
            for id_empleado_costura in ids_empleados_costura:
                header = QTableWidgetItem("F. cost. (" + str(id_empleado_costura) + ")")
                header.setBackground(QColor(217, 234, 211))
                self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
                i += 1

        header = QTableWidgetItem("RND")
        header.setBackground(QColor(217, 210, 233))
        self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
        i += 1
        header = QTableWidgetItem("T. planc.")
        header.setBackground(QColor(217, 210, 233))
        self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
        i += 1
        if empleados_generales:
            for id_empleado_general in ids_empleados_generales:
                header = QTableWidgetItem("F. planc. (" + str(id_empleado_general) + ")")
                header.setBackground(QColor(217, 210, 233))
                self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
                i += 1
        else:
            for id_empleado_planchado in ids_empleados_planchado:
                header = QTableWidgetItem("F. planc. (" + str(id_empleado_planchado) + ")")
                header.setBackground(QColor(217, 210, 233))
                self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
                i += 1

        header = QTableWidgetItem("RND")
        header.setBackground(QColor(234, 209, 220))
        self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
        i += 1
        header = QTableWidgetItem("T. insp.")
        header.setBackground(QColor(234, 209, 220))
        self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
        i += 1
        for id_inspector in ids_inspectores:
            header = QTableWidgetItem("F. insp. (" + str(id_inspector) + ")")
            header.setBackground(QColor(234, 209, 220))
            self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
            i += 1

        header = QTableWidgetItem("RND")
        header.setBackground(QColor(187, 238, 253))
        self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
        i += 1
        header = QTableWidgetItem("T. rechazado")
        header.setBackground(QColor(187, 238, 253))
        self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
        i += 1

        if empleados_generales:
            for id_empleado_general in ids_empleados_generales:
                header = QTableWidgetItem("Est. emp. gral. (" + str(id_empleado_general) + ")")
                header.setBackground(QColor(207, 255, 218))
                self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
                i += 1
        else:
            for id_empleado_zurcido in ids_empleados_zurcido:
                header = QTableWidgetItem("Est. emp. zurc. (" + str(id_empleado_zurcido) + ")")
                header.setBackground(QColor(207, 255, 218))
                self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
                i += 1
            for id_empleado_costura in ids_empleados_costura:
                header = QTableWidgetItem("Est. emp. cost. (" + str(id_empleado_costura) + ")")
                header.setBackground(QColor(207, 255, 218))
                self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
                i += 1
            for id_empleado_planchado in ids_empleados_planchado:
                header = QTableWidgetItem("Est. emp. planc. (" + str(id_empleado_planchado) + ")")
                header.setBackground(QColor(207, 255, 218))
                self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
                i += 1

        for id_cola_empleados in ids_colas_empleados:
            header = QTableWidgetItem("Cola (" + str(id_cola_empleados) + ")")
            header.setBackground(QColor(207, 255, 218))
            self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
            i += 1

        for id_inspector in ids_inspectores:
            header = QTableWidgetItem("Est. inspect. (" + str(id_inspector) + ")")
            header.setBackground(QColor(244, 204, 204))
            self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
            i += 1

        for id_cola_inspectores in ids_colas_inspectores:
            header = QTableWidgetItem("Cola (" + str(id_cola_inspectores) + ")")
            header.setBackground(QColor(244, 204, 204))
            self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
            i += 1

        header = QTableWidgetItem("T. term.")
        header.setBackground(QColor(249, 203, 156))
        self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
        i += 1
        header = QTableWidgetItem("T. term. prom.")
        header.setBackground(QColor(249, 203, 156))
        self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
        i += 1
        header = QTableWidgetItem("Cant. cola max.")
        header.setBackground(QColor(249, 203, 156))
        self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
        i += 1
        header = QTableWidgetItem("Cola max.")
        header.setBackground(QColor(249, 203, 156))
        self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
        i += 1

        for id_trabajo in ids_trabajos:
            header = QTableWidgetItem("Est. trabajo (" + str(id_trabajo) + ")")
            header.setBackground(QColor(234, 153, 153))
            self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
            i += 1
            """
            header = QTableWidgetItem("H. ini. esp. zurc. (" + str(id_trabajo) + ")")
            header.setBackground(QColor(234, 153, 153))
            self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
            i += 1
            header = QTableWidgetItem("H. ini. esp. cost. (" + str(id_trabajo) + ")")
            header.setBackground(QColor(234, 153, 153))
            self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
            i += 1
            header = QTableWidgetItem("H. ini. esp. planc. (" + str(id_trabajo) + ")")
            header.setBackground(QColor(234, 153, 153))
            self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
            i += 1
            header = QTableWidgetItem("H. ini. esp. insp. (" + str(id_trabajo) + ")")
            header.setBackground(QColor(234, 153, 153))
            self.grid_iteraciones_simuladas.setHorizontalHeaderItem(i, header)
            i += 1
            """

    def mostrar_porcentaje_simulacion(self, porcenjate=0):
        porcenjate_str = str(porcenjate).replace(".", ",")
        self.lbl_informacion_porcentaje_simulacion.setText(porcenjate_str)
        self.app.processEvents()

    def mostrar_porcentaje_datos(self, porcenjate=0):
        porcenjate_str = str(porcenjate).replace(".", ",")
        self.lbl_informacion_porcentaje_datos.setText(porcenjate_str)
        self.app.processEvents()

    def mostrar_cantidad_iteraciones_realizadas(self, cantidad_iteraciones=0):
        cantidad_iteraciones_str = str(cantidad_iteraciones)
        self.lbl_informacion_cantidad_total_iteraciones_realizadas.setText(cantidad_iteraciones_str)
        self.app.processEvents()

    def mostrar_mensaje(self, titulo, mensaje):

        # Muestro mensaje
        box = QMessageBox()
        box.setWindowTitle(titulo)
        box.setText(mensaje)
        box.setStandardButtons(QMessageBox.Ok)
        box.exec_()

    def obtener_pagina_iteraciones_simuladas(self):

        # Obtengo página a partir de datos de paginación
        if len(self.iteraciones_simuladas) < self.tamanio_pagina:
            pagina = self.iteraciones_simuladas[0:len(self.iteraciones_simuladas)]
        else:
            index_inf = (self.pagina_actual - 1) * self.tamanio_pagina
            index_sup = index_inf + self.tamanio_pagina
            if index_sup > len(self.iteraciones_simuladas):
                index_sup = len(self.iteraciones_simuladas)
            pagina = self.iteraciones_simuladas[index_inf:index_sup]

        return pagina

    def cargar_tabla_iteraciones_simuladas(self):

        # Obtengo datos necesarios para generacion de headers
        ids_trabajos = self.informacion_simulacion.get("ids_trabajos")

        # Obtengo pagina de iteraciones simuladas a mostrar
        iteraciones_a_mostrar = self.obtener_pagina_iteraciones_simuladas()

        # Calculo cada cuantas finlas mostrar el porcentaje de datos cargados
        if len(iteraciones_a_mostrar) <= 100:
            paso_muestra_datos = 1
        else:
            paso_muestra_datos = round(len(iteraciones_a_mostrar) / 50)
        proxima_muestra_datos = paso_muestra_datos

        # Genero filas de tabla
        self.grid_iteraciones_simuladas.setRowCount(len(iteraciones_a_mostrar))
        index_f = 0
        for iteracion_a_mostrar in iteraciones_a_mostrar:
            index_c = 0

            # Obtengo datos en formato conveniente y agrego a fila
            n_iteracion = iteracion_a_mostrar.get("n_iteracion")
            n_iteracion_str = str(n_iteracion) if n_iteracion is not None else ""
            self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(n_iteracion_str))
            index_c += 1

            evento_str = iteracion_a_mostrar.get("evento")
            self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(evento_str))
            index_c += 1

            reloj = iteracion_a_mostrar.get("reloj")
            reloj_str = str(reloj).replace(".", ",") if reloj is not None else ""
            self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(reloj_str))
            index_c += 1

            rnd_tiempo_proxima_llegada = iteracion_a_mostrar.get("rnd_tiempo_proxima_llegada")
            rnd_tiempo_proxima_llegada_str = str(rnd_tiempo_proxima_llegada).replace(".", ",") \
                if rnd_tiempo_proxima_llegada is not None else ""
            self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(rnd_tiempo_proxima_llegada_str))
            index_c += 1

            tiempo_proxima_llegada = iteracion_a_mostrar.get("tiempo_proxima_llegada")
            tiempo_proxima_llegada_str = str(tiempo_proxima_llegada).replace(".", ",") \
                if tiempo_proxima_llegada is not None else ""
            self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(tiempo_proxima_llegada_str))
            index_c += 1

            proxima_llegada = iteracion_a_mostrar.get("proxima_llegada")
            proxima_llegada_str = str(proxima_llegada).replace(".", ",") if proxima_llegada is not None else ""
            self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(proxima_llegada_str))
            index_c += 1

            rnd_tiempo_zurcido = iteracion_a_mostrar.get("rnd_tiempo_zurcido")
            rnd_tiempo_zurcido_str = str(rnd_tiempo_zurcido).replace(".", ",") if rnd_tiempo_zurcido is not None else ""
            self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(rnd_tiempo_zurcido_str))
            index_c += 1

            tiempo_zurcido = iteracion_a_mostrar.get("tiempo_zurcido")
            tiempo_zurcido_str = str(tiempo_zurcido).replace(".", ",") if tiempo_zurcido is not None else ""
            self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(tiempo_zurcido_str))
            index_c += 1

            for fin_zurcido in iteracion_a_mostrar.get("fines_zurcido").values():
                fin_zurcido_str = str(fin_zurcido).replace(".", ",") if fin_zurcido is not None else ""
                self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(fin_zurcido_str))
                index_c += 1

            rnd_tiempo_costura = iteracion_a_mostrar.get("rnd_tiempo_costura")
            rnd_tiempo_costura_str = str(rnd_tiempo_costura).replace(".", ",") if rnd_tiempo_costura is not None else ""
            self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(rnd_tiempo_costura_str))
            index_c += 1

            tiempo_costura = iteracion_a_mostrar.get("tiempo_costura")
            tiempo_costura_str = str(tiempo_costura).replace(".", ",") if tiempo_costura is not None else ""
            self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(tiempo_costura_str))
            index_c += 1

            for fin_costura in iteracion_a_mostrar.get("fines_costura").values():
                fin_costura_str = str(fin_costura).replace(".", ",") if fin_costura is not None else ""
                self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(fin_costura_str))
                index_c += 1

            rnd_tiempo_planchado = iteracion_a_mostrar.get("rnd_tiempo_planchado")
            rnd_tiempo_planchado_str = str(rnd_tiempo_planchado).replace(".", ",") if rnd_tiempo_planchado is not None \
                else ""
            self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(rnd_tiempo_planchado_str))
            index_c += 1

            tiempo_planchado = iteracion_a_mostrar.get("tiempo_planchado")
            tiempo_planchado_str = str(tiempo_planchado).replace(".", ",") if tiempo_planchado is not None else ""
            self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(tiempo_planchado_str))
            index_c += 1

            for fin_planchado in iteracion_a_mostrar.get("fines_planchado").values():
                fin_costura_str = str(fin_planchado).replace(".", ",") if fin_planchado is not None else ""
                self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(fin_costura_str))
                index_c += 1

            rnd_tiempo_inspeccion = iteracion_a_mostrar.get("rnd_tiempo_inspeccion")
            rnd_tiempo_inspeccion_str = str(rnd_tiempo_inspeccion).replace(".", ",") \
                if rnd_tiempo_inspeccion is not None else ""
            self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(rnd_tiempo_inspeccion_str))
            index_c += 1

            tiempo_inspeccion = iteracion_a_mostrar.get("tiempo_inspeccion")
            tiempo_inspeccion_str = str(tiempo_inspeccion).replace(".", ",") if tiempo_inspeccion is not None else ""
            self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(tiempo_inspeccion_str))
            index_c += 1

            for fin_inspeccion in iteracion_a_mostrar.get("fines_inspeccion").values():
                fin_inspeccion_str = str(fin_inspeccion).replace(".", ",") if fin_inspeccion is not None else ""
                self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(fin_inspeccion_str))
                index_c += 1

            rnd_trabajo_rechazado = iteracion_a_mostrar.get("rnd_trabajo_rechazado")
            rnd_trabajo_rechazado_str = str(rnd_trabajo_rechazado).replace(".", ",") \
                if rnd_trabajo_rechazado is not None else ""
            self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(rnd_trabajo_rechazado_str))
            index_c += 1

            trabajo_rechazado = iteracion_a_mostrar.get("trabajo_rechazado")
            trabajo_rechazado_str = ""
            if trabajo_rechazado is not None:
                trabajo_rechazado_str = "Si" if trabajo_rechazado else "No"
            self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(trabajo_rechazado_str))
            index_c += 1

            for estado_empleado_str in iteracion_a_mostrar.get("estado_empleados").values():
                self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(estado_empleado_str))
                index_c += 1

            cola_zurcido = iteracion_a_mostrar.get("cola_zurcido")
            cola_zurcido_str = str(cola_zurcido) if cola_zurcido is not None else ""
            self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(cola_zurcido_str))
            index_c += 1

            cola_costura = iteracion_a_mostrar.get("cola_costura")
            cola_costura_str = str(cola_costura) if cola_costura is not None else ""
            self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(cola_costura_str))
            index_c += 1

            cola_planchado = iteracion_a_mostrar.get("cola_planchado")
            cola_planchado_str = str(cola_planchado) if cola_planchado is not None else ""
            self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(cola_planchado_str))
            index_c += 1

            for estado_inspector_str in iteracion_a_mostrar.get("estado_inspectores").values():
                self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(estado_inspector_str))
                index_c += 1

            cola_inspeccion = iteracion_a_mostrar.get("cola_inspeccion")
            cola_inspeccion_str = str(cola_inspeccion) if cola_inspeccion is not None else ""
            self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(cola_inspeccion_str))
            index_c += 1

            trabajos_terminados = iteracion_a_mostrar.get("trabajos_terminados")
            trabajos_terminados_str = str(trabajos_terminados) if trabajos_terminados is not None else ""
            self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(trabajos_terminados_str))
            index_c += 1

            trabajos_terminados_promedio = iteracion_a_mostrar.get("trabajos_terminados_promedio")
            trabajos_terminados_promedio_str = str(trabajos_terminados_promedio).replace(".", ",") \
                if trabajos_terminados_promedio is not None else ""
            self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(
                trabajos_terminados_promedio_str))
            index_c += 1

            cantidad_cola_maxima = iteracion_a_mostrar.get("cantidad_cola_maxima")
            cantidad_cola_maxima_str = str(cantidad_cola_maxima) if cantidad_cola_maxima is not None else ""
            self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(cantidad_cola_maxima_str))
            index_c += 1

            cola_maxima_str = iteracion_a_mostrar.get("cola_maxima")
            self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(cola_maxima_str))
            index_c += 1

            if ids_trabajos is not None:
                for id_trabajo in ids_trabajos:
                    trabajo = iteracion_a_mostrar.get("trabajos").get(id_trabajo)
                    if trabajo:
                        estado_str = trabajo.estado
                        if trabajo.empleado is not None:
                            estado_str += " (" + str(trabajo.empleado.id) + ")"
                        self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(estado_str))
                        index_c += 1

                        """
                        hora_inicio_espera_zurcido = trabajo.hora_inicio_espera_zurcido
                        hora_inicio_espera_zurcido_str = str(hora_inicio_espera_zurcido).replace(".", ",") \
                            if hora_inicio_espera_zurcido is not None else ""
                        self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(
                            hora_inicio_espera_zurcido_str))
                        index_c += 1

                        hora_inicio_espera_costura = trabajo.hora_inicio_espera_costura
                        hora_inicio_espera_costura_str = str(hora_inicio_espera_costura).replace(".", ",") \
                            if hora_inicio_espera_costura is not None else ""
                        self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(
                            hora_inicio_espera_costura_str))
                        index_c += 1

                        hora_inicio_espera_planchado = trabajo.hora_inicio_espera_planchado
                        hora_inicio_espera_planchado_str = str(hora_inicio_espera_planchado)\
                            .replace(".", ",") if hora_inicio_espera_planchado is not None else ""
                        self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(
                            hora_inicio_espera_planchado_str))
                        index_c += 1

                        hora_inicio_espera_inspeccion = trabajo.hora_inicio_espera_inspeccion
                        hora_inicio_espera_inspeccion_str = str(hora_inicio_espera_inspeccion)\
                            .replace(".", ",") if hora_inicio_espera_inspeccion is not None else ""
                        self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(
                            hora_inicio_espera_inspeccion_str))
                        index_c += 1
                        """

                    else:
                        estado_str = ""
                        self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(estado_str))
                        index_c += 1

                        """
                        hora_inicio_espera_zurcido_str = ""
                        self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(
                            hora_inicio_espera_zurcido_str))
                        index_c += 1

                        hora_inicio_espera_costura_str = ""
                        self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(
                            hora_inicio_espera_costura_str))
                        index_c += 1
                        hora_inicio_espera_planchado_str = ""
                        self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(
                            hora_inicio_espera_planchado_str))
                        index_c += 1
                        hora_inicio_espera_inspeccion_str = ""
                        self.grid_iteraciones_simuladas.setItem(index_f, index_c, QTableWidgetItem(
                            hora_inicio_espera_inspeccion_str))
                        index_c += 1
                        """

            index_f += 1

            # Muestro porcentaje de datos cargados cuando corresponda
            if index_f >= proxima_muestra_datos:
                porcentaje = round(index_f * 100 / len(iteraciones_a_mostrar))
                self.mostrar_porcentaje_datos(porcentaje)
                while proxima_muestra_datos <= index_f:
                    proxima_muestra_datos += paso_muestra_datos

        # Muestro porcentaje de datos cargados final
        self.mostrar_porcentaje_datos(100)

    """ Eventos """

    # Evento show
    def showEvent(self, QShowEvent):
        self.accion_limpiar()
