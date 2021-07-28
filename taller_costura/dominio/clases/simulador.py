import math
import random
import bisect
import copy
from dominio.clases.manejador_eventos import ManejadorEventos
from dominio.clases.evento import Evento
from dominio.clases.grupo_empleados import GrupoEmpleados
from dominio.clases.empleado import Empleado
from dominio.clases.cola import Cola
from dominio.clases.trabajo import Trabajo
from soporte.helper import truncar


class Simulador:
    
    # Atributos para conexión con controlador
    controlador = None

    # Atributos con parámetros generales de la simulación
    tiempo_simulacion = None
    tiempo_desde = None
    cantidad_iteraciones = None

    # Atributos con parámetros específicos de la simulación
    tiempo_llegada_trabajo = None
    tiempo_zurcido = None
    tiempo_costura = None
    tiempo_planchado = None
    tiempo_inspeccion = None
    empleados_generales = None
    cantidad_empleados_generales = None
    cantidad_empleados_zurcido = None
    cantidad_empleados_costura = None
    cantidad_empleados_planchado = None
    cantidad_inspectores = None
    porcentaje_trabajos_rechazados = None

    # Atributos para el manejo de los objetos de la simulación
    manejador_eventos = None
    grupo_empleados_zurcido = None
    grupo_empleados_costura = None
    grupo_empleados_planchado = None
    grupo_inspectores = None
    rnd_trabajo_rechazado = None
    trabajo_rechazado = None
    trabajos_terminados = 0
    trabajos_terminados_promedio = 0
    cantidad_cola_maxima = 0
    cola_maxima = None

    # Atributos para el manejo de los objetos de la simulación y del vector estado
    ultimo_n_iteracion = -1
    ultimo_id_trabajo = 0
    ids_trabajos_iteraciones = []
    trabajos = []

    def __init__(self, controlador, tiempo_simulacion, tiempo_desde, cantidad_iteraciones, tiempo_llegada_trabajo,
                 tiempo_zurcido, tiempo_costura, tiempo_planchado, tiempo_inspeccion, empleados_generales,
                 cantidad_empleados_generales, cantidad_empleados_zurcido, cantidad_empleados_costura,
                 cantidad_empleados_planchado, cantidad_inspectores, porcentaje_trabajos_rechazados):
        self.controlador = controlador

        self.tiempo_simulacion = tiempo_simulacion
        self.tiempo_desde = tiempo_desde
        self.cantidad_iteraciones = cantidad_iteraciones

        self.tiempo_llegada_trabajo = tiempo_llegada_trabajo
        self.tiempo_zurcido = tiempo_zurcido
        self.tiempo_costura = tiempo_costura
        self.tiempo_planchado = tiempo_planchado
        self.tiempo_inspeccion = tiempo_inspeccion
        self.empleados_generales = empleados_generales
        self.cantidad_empleados_generales = cantidad_empleados_generales
        self.cantidad_empleados_zurcido = cantidad_empleados_zurcido
        self.cantidad_empleados_costura = cantidad_empleados_costura
        self.cantidad_empleados_planchado = cantidad_empleados_planchado
        self.cantidad_inspectores = cantidad_inspectores
        self.porcentaje_trabajos_rechazados = porcentaje_trabajos_rechazados

    def generar_vector_estado(self, evento_actual, nuevos_eventos):
        self.ultimo_n_iteracion += 1
        n_iteracion = self.ultimo_n_iteracion
        evento = evento_actual.tipo
        if evento_actual.trabajo is not None:
            evento += " (" + str(evento_actual.trabajo.id) + ")"
        if evento_actual.empleado is not None:
            evento += " (" + str(evento_actual.empleado.id) + ")"
        reloj = evento_actual.tiempo_fin

        vector_estado = {
            "n_iteracion": n_iteracion,
            "evento": evento,
            "reloj": reloj,

            "rnd_tiempo_proxima_llegada": None,
            "tiempo_proxima_llegada": None,
            "proxima_llegada": None,

            "rnd_tiempo_zurcido": None,
            "tiempo_zurcido": None,
            "fines_zurcido": {},

            "rnd_tiempo_costura": None,
            "tiempo_costura": None,
            "fines_costura": {},

            "rnd_tiempo_planchado": None,
            "tiempo_planchado": None,
            "fines_planchado": {},

            "rnd_tiempo_inspeccion": None,
            "tiempo_inspeccion": None,
            "fines_inspeccion": {},

            "rnd_trabajo_rechazado": None,
            "trabajo_rechazado": None,

            "estado_empleados": {},
            "cola_zurcido": None,
            "cola_costura": None,
            "cola_planchado": None,

            "estado_inspectores": {},
            "cola_inspeccion": None,

            "trabajos_terminados": None,
            "trabajos_terminados_promedio": None,
            "cantidad_cola_maxima": None,
            "cola_maxima": None,

            "trabajos": {},
        }

        for empleado in self.grupo_empleados_zurcido.empleados:
            vector_estado["fines_zurcido"][empleado.id] = None
            vector_estado["estado_empleados"][empleado.id] = empleado.estado
        for empleado in self.grupo_empleados_costura.empleados:
            vector_estado["fines_costura"][empleado.id] = None
            vector_estado["estado_empleados"][empleado.id] = empleado.estado
        for empleado in self.grupo_empleados_planchado.empleados:
            vector_estado["fines_planchado"][empleado.id] = None
            vector_estado["estado_empleados"][empleado.id] = empleado.estado
        for empleado in self.grupo_inspectores.empleados:
            vector_estado["fines_inspeccion"][empleado.id] = None
            vector_estado["estado_inspectores"][empleado.id] = empleado.estado

        # TODO: Mejorar
        for evento_anterior in self.manejador_eventos.eventos:
            if evento_anterior.tipo == Evento.TIPO_LLEGADA_TRABAJO:
                vector_estado["proxima_llegada"] = evento_anterior.tiempo_fin
            elif evento_anterior.tipo == Evento.TIPO_FIN_ZURCIDO:
                vector_estado["fines_zurcido"][evento_anterior.empleado.id] = evento_anterior.tiempo_fin
            elif evento_anterior.tipo == Evento.TIPO_FIN_COSTURA:
                vector_estado["fines_costura"][evento_anterior.empleado.id] = evento_anterior.tiempo_fin
            elif evento_anterior.tipo == Evento.TIPO_FIN_PLANCHADO:
                vector_estado["fines_planchado"][evento_anterior.empleado.id] = evento_anterior.tiempo_fin
            elif evento_anterior.tipo == Evento.TIPO_FIN_INSPECCION:
                vector_estado["fines_inspeccion"][evento_anterior.empleado.id] = evento_anterior.tiempo_fin

        for nuevo_evento in nuevos_eventos:
            if nuevo_evento.tipo == Evento.TIPO_LLEGADA_TRABAJO:
                vector_estado["rnd_tiempo_proxima_llegada"] = nuevo_evento.rnd
                vector_estado["tiempo_proxima_llegada"] = nuevo_evento.tiempo
                vector_estado["proxima_llegada"] = nuevo_evento.tiempo_fin
            elif nuevo_evento.tipo == Evento.TIPO_FIN_ZURCIDO:
                vector_estado["rnd_tiempo_zurcido"] = nuevo_evento.rnd
                vector_estado["tiempo_zurcido"] = nuevo_evento.tiempo
            elif nuevo_evento.tipo == Evento.TIPO_FIN_COSTURA:
                vector_estado["rnd_tiempo_costura"] = nuevo_evento.rnd
                vector_estado["tiempo_costura"] = nuevo_evento.tiempo
            elif nuevo_evento.tipo == Evento.TIPO_FIN_PLANCHADO:
                vector_estado["rnd_tiempo_planchado"] = nuevo_evento.rnd
                vector_estado["tiempo_planchado"] = nuevo_evento.tiempo
            elif nuevo_evento.tipo == Evento.TIPO_FIN_INSPECCION:
                vector_estado["rnd_tiempo_inspeccion"] = nuevo_evento.rnd
                vector_estado["tiempo_inspeccion"] = nuevo_evento.tiempo

        vector_estado["rnd_trabajo_rechazado"] = self.rnd_trabajo_rechazado
        vector_estado["trabajo_rechazado"] = self.trabajo_rechazado

        vector_estado["cola_zurcido"] = len(self.grupo_empleados_zurcido.cola.trabajos)
        vector_estado["cola_costura"] = len(self.grupo_empleados_costura.cola.trabajos)
        vector_estado["cola_planchado"] = len(self.grupo_empleados_planchado.cola.trabajos)
        vector_estado["cola_inspeccion"] = len(self.grupo_inspectores.cola.trabajos)

        vector_estado["trabajos_terminados"] = self.trabajos_terminados
        vector_estado["trabajos_terminados_promedio"] = self.trabajos_terminados_promedio
        vector_estado["cantidad_cola_maxima"] = self.cantidad_cola_maxima
        vector_estado["cola_maxima"] = self.cola_maxima

        # TODO: Mejorar
        for trabajo in self.trabajos:
            vector_estado["trabajos"][trabajo.id] = copy.deepcopy(trabajo)

        return vector_estado

    def simular_iteracion(self):

        # Reestablezco atributos necesarios para el manejo de la iteracion
        self.rnd_trabajo_rechazado = None
        self.trabajo_rechazado = None
        
        # Obtengo evento actual
        evento_actual = self.manejador_eventos.obtener_proximo_evento()

        # Inicializo lista de eventos generados durante la iteración
        eventos_iteracion = []
        
        # Relizo la acción correspondiente de acuerdo al evento a procesar

        # Evento actual inicializacion
        if evento_actual.tipo == Evento.TIPO_INICIALIZACION:

            # Genero evento llegada trabajo
            tipo = Evento.TIPO_LLEGADA_TRABAJO
            rnd = truncar(random.random(), 2)
            tiempo = round(-1 * self.tiempo_llegada_trabajo * math.log(1 - rnd), 2)
            tiempo_fin = truncar(evento_actual.tiempo_fin + tiempo, 2)
            nuevo_evento = Evento(tipo, rnd, tiempo, tiempo_fin)

            # Agrego evento al manejador de eventos
            self.manejador_eventos.agregar_evento(nuevo_evento)

            # Agrego evento a lista de eventos generados durante la iteración
            eventos_iteracion.append(nuevo_evento)

        # Evento llegada trabajo
        elif evento_actual.tipo == Evento.TIPO_LLEGADA_TRABAJO:

            # Obtengo empleado libre en el grupo de empleados de zurcido si existe
            empleado_libre = None
            if self.grupo_empleados_zurcido.existe_empleado_libre():
                empleado_libre = self.grupo_empleados_zurcido.obtener_empleado_libre()

            # Creo nuevo trabajo
            self.ultimo_id_trabajo += 1
            id_trabajo = self.ultimo_id_trabajo
            estado = Trabajo.ESTADO_SIENDO_ZURCIDO if empleado_libre is not None else Trabajo.ESTADO_ESPERANDO_ZURCIDO
            hora_inicio_espera_zurcido = None if empleado_libre is not None else evento_actual.tiempo_fin
            trabajo = Trabajo(id_trabajo, estado, empleado_libre, hora_inicio_espera_zurcido)

            # Seteo trabajo a evento actual
            evento_actual.trabajo = trabajo

            # Agrego trabajo a lista general de trabajos
            bisect.insort(self.trabajos, trabajo)

            # Si se encontró empleado libre
            if empleado_libre is not None:

                # Asigno trabajo a empleado libre
                empleado_libre.asignar_trabajo(trabajo)
                empleado_libre.cambiar_a_estado_ocupado()

                # Genero evento fin zurcido
                tipo = Evento.TIPO_FIN_ZURCIDO
                rnd = truncar(random.random(), 2)
                tiempo = round(-1 * self.tiempo_zurcido * math.log(1 - rnd), 2)
                tiempo_fin = truncar(evento_actual.tiempo_fin + tiempo, 2)
                nuevo_evento = Evento(tipo, rnd, tiempo, tiempo_fin, empleado_libre, trabajo)

                # Agrego evento al manejador de eventos
                self.manejador_eventos.agregar_evento(nuevo_evento)

                # Agrego evento a lista de eventos generados durante la iteración
                eventos_iteracion.append(nuevo_evento)

            # Si no se encontró empleado libre
            else:

                # Asigno trabajo a cola de zurcido
                self.grupo_empleados_zurcido.cola.agregar_trabajo(trabajo)

            # Creo nuevo evento llegada trabajo
            tipo = Evento.TIPO_LLEGADA_TRABAJO
            rnd = truncar(random.random(), 2)
            tiempo = round(-1 * self.tiempo_llegada_trabajo * math.log(1 - rnd), 2)
            tiempo_fin = truncar(evento_actual.tiempo_fin + tiempo, 2)
            nuevo_evento = Evento(tipo, rnd, tiempo, tiempo_fin)

            # Agrego nuevo evento al manejador de eventos
            self.manejador_eventos.agregar_evento(nuevo_evento)

            # Agrego evento a lista de eventos generados durante la iteración
            eventos_iteracion.append(nuevo_evento)

        # Evento fin zurcido
        elif evento_actual.tipo == Evento.TIPO_FIN_ZURCIDO:

            # Manejo de trabajo asociado a evento

            # Obtengo trabajo liberando al empleado asignado
            empleado_ocupado = evento_actual.empleado
            empleado_ocupado.cambiar_a_estado_libre()
            trabajo = empleado_ocupado.desasignar_trabajo()
            trabajo.empleado = None

            # Obtengo empleado libre en el grupo de empleados de costura si existe
            empleado_libre = None
            if self.grupo_empleados_costura.existe_empleado_libre():
                empleado_libre = self.grupo_empleados_costura.obtener_empleado_libre()

            # Actualizo trabajo obtenido
            estado = Trabajo.ESTADO_SIENDO_COSIDO if empleado_libre is not None else Trabajo.ESTADO_ESPERANDO_COSIDO
            hora_inicio_espera_costura = None if empleado_libre is not None else evento_actual.tiempo_fin
            trabajo.estado = estado
            trabajo.empleado = empleado_libre
            trabajo.hora_inicio_espera_costura = hora_inicio_espera_costura

            # Si se encontró empleado libre
            if empleado_libre is not None:

                # Asigno trabajo a empleado libre
                empleado_libre.asignar_trabajo(trabajo)
                empleado_libre.cambiar_a_estado_ocupado()

                # Genero evento fin costura
                tipo = Evento.TIPO_FIN_COSTURA
                rnd = truncar(random.random(), 2)
                tiempo = round(-1 * self.tiempo_costura * math.log(1 - rnd), 2)
                tiempo_fin = truncar(evento_actual.tiempo_fin + tiempo, 2)
                nuevo_evento = Evento(tipo, rnd, tiempo, tiempo_fin, empleado_libre, trabajo)

                # Agrego evento al manejador de eventos
                self.manejador_eventos.agregar_evento(nuevo_evento)

                # Agrego evento a lista de eventos generados durante la iteración
                eventos_iteracion.append(nuevo_evento)

            # Si no se encontró empleado libre
            else:

                # Asigno trabajo a cola de costura
                self.grupo_empleados_costura.cola.agregar_trabajo(trabajo)

            # Búsqueda de trabajo en cola

            # Si existe algún trabajo en la cola de zurcido y si existe algun empleado libre en el grupo de empleados
            # de zurcido
            if self.grupo_empleados_zurcido.cola.existe_proximo_trabajo() and \
                    self.grupo_empleados_zurcido.existe_empleado_libre():

                # Obtengo trabajo desde la cola
                trabajo = self.grupo_empleados_zurcido.cola.obtener_proximo_trabajo()

                # Obtengo empleado libre en el grupo de empleados de zurcido
                empleado_libre = self.grupo_empleados_zurcido.obtener_empleado_libre()

                # Actualizo trabajo obtenido
                estado = Trabajo.ESTADO_SIENDO_ZURCIDO
                trabajo.estado = estado
                trabajo.empleado = empleado_libre

                # Asigno trabajo a empleado libre
                empleado_libre.asignar_trabajo(trabajo)
                empleado_libre.cambiar_a_estado_ocupado()

                # Genero evento fin zurcido
                tipo = Evento.TIPO_FIN_ZURCIDO
                rnd = truncar(random.random(), 2)
                tiempo = round(-1 * self.tiempo_zurcido * math.log(1 - rnd), 2)
                tiempo_fin = truncar(evento_actual.tiempo_fin + tiempo, 2)
                nuevo_evento = Evento(tipo, rnd, tiempo, tiempo_fin, empleado_libre, trabajo)

                # Agrego evento al manejador de eventos
                self.manejador_eventos.agregar_evento(nuevo_evento)

                # Agrego evento a lista de eventos generados durante la iteración
                eventos_iteracion.append(nuevo_evento)

        # Evento fin costura
        elif evento_actual.tipo == Evento.TIPO_FIN_COSTURA:

            # Manejo de trabajo asociado a evento

            # Obtengo trabajo liberando al empleado asignado
            empleado_ocupado = evento_actual.empleado
            empleado_ocupado.cambiar_a_estado_libre()
            trabajo = empleado_ocupado.desasignar_trabajo()
            trabajo.empleado = None

            # Obtengo empleado libre en el grupo de empleados de planchado si existe
            empleado_libre = None
            if self.grupo_empleados_planchado.existe_empleado_libre():
                empleado_libre = self.grupo_empleados_planchado.obtener_empleado_libre()

            # Actualizo trabajo obtenido
            estado = Trabajo.ESTADO_SIENDO_PLANCHADO if empleado_libre is not None \
                else Trabajo.ESTADO_ESPERANDO_PLANCHADO
            hora_inicio_espera_planchado = None if empleado_libre is not None else evento_actual.tiempo_fin
            trabajo.estado = estado
            trabajo.empleado = empleado_libre
            trabajo.hora_inicio_espera_planchado = hora_inicio_espera_planchado

            # Si se encontró empleado libre
            if empleado_libre is not None:

                # Asigno trabajo a empleado libre
                empleado_libre.asignar_trabajo(trabajo)
                empleado_libre.cambiar_a_estado_ocupado()

                # Genero evento fin planchado
                tipo = Evento.TIPO_FIN_PLANCHADO
                rnd = truncar(random.random(), 2)
                tiempo = round(-1 * self.tiempo_planchado * math.log(1 - rnd), 2)
                tiempo_fin = truncar(evento_actual.tiempo_fin + tiempo, 2)
                nuevo_evento = Evento(tipo, rnd, tiempo, tiempo_fin, empleado_libre, trabajo)

                # Agrego evento al manejador de eventos
                self.manejador_eventos.agregar_evento(nuevo_evento)

                # Agrego evento a lista de eventos generados durante la iteración
                eventos_iteracion.append(nuevo_evento)

            # Si no se encontró empleado libre
            else:

                # Asigno trabajo a cola de costura
                self.grupo_empleados_planchado.cola.agregar_trabajo(trabajo)

            # Búsqueda de trabajo en cola

            # Si existe algún trabajo en la cola de costura y si existe algun empleado libre en el grupo de empleados
            # de costura
            if self.grupo_empleados_costura.cola.existe_proximo_trabajo() and \
                    self.grupo_empleados_costura.existe_empleado_libre():

                # Obtengo trabajo desde la cola
                trabajo = self.grupo_empleados_costura.cola.obtener_proximo_trabajo()

                # Obtengo empleado libre en el grupo de empleados de costura
                empleado_libre = self.grupo_empleados_costura.obtener_empleado_libre()

                # Actualizo trabajo obtenido
                estado = Trabajo.ESTADO_SIENDO_COSIDO
                trabajo.estado = estado
                trabajo.empleado = empleado_libre

                # Asigno trabajo a empleado libre
                empleado_libre.asignar_trabajo(trabajo)
                empleado_libre.cambiar_a_estado_ocupado()

                # Genero evento fin costura
                tipo = Evento.TIPO_FIN_COSTURA
                rnd = truncar(random.random(), 2)
                tiempo = round(-1 * self.tiempo_costura * math.log(1 - rnd), 2)
                tiempo_fin = truncar(evento_actual.tiempo_fin + tiempo, 2)
                nuevo_evento = Evento(tipo, rnd, tiempo, tiempo_fin, empleado_libre, trabajo)

                # Agrego evento al manejador de eventos
                self.manejador_eventos.agregar_evento(nuevo_evento)

                # Agrego evento a lista de eventos generados durante la iteración
                eventos_iteracion.append(nuevo_evento)

            # Si los empleados son generales, realizo el mismo proceso de búsqueda en cola pero en colas anteriores
            if self.empleados_generales:

                # Si existe algún trabajo en la cola de zurcido y si existe algun empleado libre en el grupo de
                # empleados de zurcido
                if self.grupo_empleados_zurcido.cola.existe_proximo_trabajo() and \
                        self.grupo_empleados_zurcido.existe_empleado_libre():
                    # Obtengo trabajo desde la cola
                    trabajo = self.grupo_empleados_zurcido.cola.obtener_proximo_trabajo()

                    # Obtengo empleado libre en el grupo de empleados de zurcido
                    empleado_libre = self.grupo_empleados_zurcido.obtener_empleado_libre()

                    # Actualizo trabajo obtenido
                    estado = Trabajo.ESTADO_SIENDO_ZURCIDO
                    trabajo.estado = estado
                    trabajo.empleado = empleado_libre

                    # Asigno trabajo a empleado libre
                    empleado_libre.asignar_trabajo(trabajo)
                    empleado_libre.cambiar_a_estado_ocupado()

                    # Genero evento fin zurcido
                    tipo = Evento.TIPO_FIN_ZURCIDO
                    rnd = truncar(random.random(), 2)
                    tiempo = round(-1 * self.tiempo_zurcido * math.log(1 - rnd), 2)
                    tiempo_fin = truncar(evento_actual.tiempo_fin + tiempo, 2)
                    nuevo_evento = Evento(tipo, rnd, tiempo, tiempo_fin, empleado_libre, trabajo)

                    # Agrego evento al manejador de eventos
                    self.manejador_eventos.agregar_evento(nuevo_evento)

                    # Agrego evento a lista de eventos generados durante la iteración
                    eventos_iteracion.append(nuevo_evento)

        # Evento fin planchado
        elif evento_actual.tipo == Evento.TIPO_FIN_PLANCHADO:

            # Manejo de trabajo asociado a evento

            # Obtengo trabajo liberando al empleado asignado
            empleado_ocupado = evento_actual.empleado
            empleado_ocupado.cambiar_a_estado_libre()
            trabajo = empleado_ocupado.desasignar_trabajo()
            trabajo.empleado = None

            # Obtengo empleado libre en el grupo de inspectores si existe
            empleado_libre = None
            if self.grupo_inspectores.existe_empleado_libre():
                empleado_libre = self.grupo_inspectores.obtener_empleado_libre()

            # Actualizo trabajo obtenido
            estado = Trabajo.ESTADO_SIENDO_INSPECCIONADO if empleado_libre is not None \
                else Trabajo.ESTADO_ESPERANDO_INSPECCIONADO
            hora_inicio_espera_inspeccion = None if empleado_libre is not None else evento_actual.tiempo_fin
            trabajo.estado = estado
            trabajo.empleado = empleado_libre
            trabajo.hora_inicio_espera_inspeccion = hora_inicio_espera_inspeccion

            # Si se encontró empleado libre
            if empleado_libre is not None:

                # Asigno trabajo a empleado libre
                empleado_libre.asignar_trabajo(trabajo)
                empleado_libre.cambiar_a_estado_ocupado()

                # Genero evento fin inspección
                tipo = Evento.TIPO_FIN_INSPECCION
                rnd = truncar(random.random(), 2)
                tiempo = round(-1 * self.tiempo_inspeccion * math.log(1 - rnd), 2)
                tiempo_fin = truncar(evento_actual.tiempo_fin + tiempo, 2)
                nuevo_evento = Evento(tipo, rnd, tiempo, tiempo_fin, empleado_libre, trabajo)

                # Agrego evento al manejador de eventos
                self.manejador_eventos.agregar_evento(nuevo_evento)

                # Agrego evento a lista de eventos generados durante la iteración
                eventos_iteracion.append(nuevo_evento)

            # Si no se encontró empleado libre
            else:

                # Asigno trabajo a cola de inspección
                self.grupo_inspectores.cola.agregar_trabajo(trabajo)

            # Búsqueda de trabajo en cola

            # Si existe algún trabajo en la cola de planchado y si existe algun empleado libre en el grupo de empleados
            # de planchado
            if self.grupo_empleados_planchado.cola.existe_proximo_trabajo() and \
                    self.grupo_empleados_planchado.existe_empleado_libre():

                # Obtengo trabajo desde la cola
                trabajo = self.grupo_empleados_planchado.cola.obtener_proximo_trabajo()

                # Obtengo empleado libre en el grupo de empleados de planchado
                empleado_libre = self.grupo_empleados_planchado.obtener_empleado_libre()

                # Actualizo trabajo obtenido
                estado = Trabajo.ESTADO_SIENDO_PLANCHADO
                trabajo.estado = estado
                trabajo.empleado = empleado_libre

                # Asigno trabajo a empleado libre
                empleado_libre.asignar_trabajo(trabajo)
                empleado_libre.cambiar_a_estado_ocupado()

                # Genero evento fin planchado
                tipo = Evento.TIPO_FIN_PLANCHADO
                rnd = truncar(random.random(), 2)
                tiempo = round(-1 * self.tiempo_planchado * math.log(1 - rnd), 2)
                tiempo_fin = truncar(evento_actual.tiempo_fin + tiempo, 2)
                nuevo_evento = Evento(tipo, rnd, tiempo, tiempo_fin, empleado_libre, trabajo)

                # Agrego evento al manejador de eventos
                self.manejador_eventos.agregar_evento(nuevo_evento)

                # Agrego evento a lista de eventos generados durante la iteración
                eventos_iteracion.append(nuevo_evento)

            # Si los empleados son generales, realizo el mismo proceso de búsqueda en cola pero en colas anteriores
            if self.empleados_generales:

                # Si existe algún trabajo en la cola de zurcido y si existe algun empleado libre en el grupo de
                # empleados de zurcido
                if self.grupo_empleados_zurcido.cola.existe_proximo_trabajo() and \
                        self.grupo_empleados_zurcido.existe_empleado_libre():
                    # Obtengo trabajo desde la cola
                    trabajo = self.grupo_empleados_zurcido.cola.obtener_proximo_trabajo()

                    # Obtengo empleado libre en el grupo de empleados de zurcido
                    empleado_libre = self.grupo_empleados_zurcido.obtener_empleado_libre()

                    # Actualizo trabajo obtenido
                    estado = Trabajo.ESTADO_SIENDO_ZURCIDO
                    trabajo.estado = estado
                    trabajo.empleado = empleado_libre

                    # Asigno trabajo a empleado libre
                    empleado_libre.asignar_trabajo(trabajo)
                    empleado_libre.cambiar_a_estado_ocupado()

                    # Genero evento fin zurcido
                    tipo = Evento.TIPO_FIN_ZURCIDO
                    rnd = truncar(random.random(), 2)
                    tiempo = round(-1 * self.tiempo_zurcido * math.log(1 - rnd), 2)
                    tiempo_fin = truncar(evento_actual.tiempo_fin + tiempo, 2)
                    nuevo_evento = Evento(tipo, rnd, tiempo, tiempo_fin, empleado_libre, trabajo)

                    # Agrego evento al manejador de eventos
                    self.manejador_eventos.agregar_evento(nuevo_evento)

                    # Agrego evento a lista de eventos generados durante la iteración
                    eventos_iteracion.append(nuevo_evento)

                # Si existe algún trabajo en la cola de costura y si existe algun empleado libre en el grupo de
                # empleados de costura
                if self.grupo_empleados_costura.cola.existe_proximo_trabajo() and \
                        self.grupo_empleados_costura.existe_empleado_libre():
                    # Obtengo trabajo desde la cola
                    trabajo = self.grupo_empleados_costura.cola.obtener_proximo_trabajo()

                    # Obtengo empleado libre en el grupo de empleados de costura
                    empleado_libre = self.grupo_empleados_costura.obtener_empleado_libre()

                    # Actualizo trabajo obtenido
                    estado = Trabajo.ESTADO_SIENDO_COSIDO
                    trabajo.estado = estado
                    trabajo.empleado = empleado_libre

                    # Asigno trabajo a empleado libre
                    empleado_libre.asignar_trabajo(trabajo)
                    empleado_libre.cambiar_a_estado_ocupado()

                    # Genero evento fin costura
                    tipo = Evento.TIPO_FIN_COSTURA
                    rnd = truncar(random.random(), 2)
                    tiempo = round(-1 * self.tiempo_costura * math.log(1 - rnd), 2)
                    tiempo_fin = truncar(evento_actual.tiempo_fin + tiempo, 2)
                    nuevo_evento = Evento(tipo, rnd, tiempo, tiempo_fin, empleado_libre, trabajo)

                    # Agrego evento al manejador de eventos
                    self.manejador_eventos.agregar_evento(nuevo_evento)

                    # Agrego evento a lista de eventos generados durante la iteración
                    eventos_iteracion.append(nuevo_evento)

        # Evento fin inspección
        else:

            # Manejo de trabajo asociado a evento

            # Obtengo trabajo liberando al empleado asignado
            empleado_ocupado = evento_actual.empleado
            empleado_ocupado.cambiar_a_estado_libre()
            trabajo = empleado_ocupado.desasignar_trabajo()
            trabajo.empleado = None

            # Obtengo el resultado de la inspección
            self.rnd_trabajo_rechazado = truncar(random.random(), 2)
            self.trabajo_rechazado = True if 0 <= self.rnd_trabajo_rechazado < \
                                             (self.porcentaje_trabajos_rechazados / 100) else False

            # Si el trabajo fue rechazado
            if self.trabajo_rechazado:

                # Obtengo empleado libre en el grupo de empleados de zurcido si existe
                empleado_libre = None
                if self.grupo_empleados_zurcido.existe_empleado_libre():
                    empleado_libre = self.grupo_empleados_zurcido.obtener_empleado_libre()

                # Actualizo trabajo obtenido
                estado = Trabajo.ESTADO_SIENDO_ZURCIDO if empleado_libre is not None \
                    else Trabajo.ESTADO_ESPERANDO_ZURCIDO
                hora_inicio_espera_zurcido = None if empleado_libre is not None else evento_actual.tiempo_fin
                trabajo.estado = estado
                trabajo.empleado = empleado_libre
                trabajo.hora_inicio_espera_zurcido = hora_inicio_espera_zurcido

                # Si se encontró empleado libre
                if empleado_libre is not None:

                    # Asigno trabajo a empleado libre
                    empleado_libre.asignar_trabajo(trabajo)
                    empleado_libre.cambiar_a_estado_ocupado()

                    # Genero evento fin costura
                    tipo = Evento.TIPO_FIN_ZURCIDO
                    rnd = truncar(random.random(), 2)
                    tiempo = round(-1 * self.tiempo_costura * math.log(1 - rnd), 2)
                    tiempo_fin = truncar(evento_actual.tiempo_fin + tiempo, 2)
                    nuevo_evento = Evento(tipo, rnd, tiempo, tiempo_fin, empleado_libre)

                    # Agrego evento al manejador de eventos
                    self.manejador_eventos.agregar_evento(nuevo_evento)

                    # Agrego evento a lista de eventos generados durante la iteración
                    eventos_iteracion.append(nuevo_evento)

                # Si no se encontró empleado libre
                else:

                    # Asigno trabajo a cola de zurcido
                    self.grupo_empleados_zurcido.cola.agregar_trabajo(trabajo)

            # Si el trabajo no fue rechazado
            else:

                # Elimino trabajo de lista de trabajos
                index = None
                for i in range(0, len(self.trabajos)):
                    if self.trabajos[i].id == trabajo.id:
                        index = i
                        break
                if index is not None:
                    del self.trabajos[index]

                # Actualizo contador
                self.trabajos_terminados += 1

            # Búsqueda de trabajo en cola

            # Si existe algún trabajo en la cola de inspección y si existe algun empleado libre en el grupo de
            # inspectores de planchado
            if self.grupo_inspectores.cola.existe_proximo_trabajo() and \
                    self.grupo_inspectores.existe_empleado_libre():

                # Obtengo trabajo desde la cola
                trabajo = self.grupo_inspectores.cola.obtener_proximo_trabajo()

                # Obtengo inspector libre en el grupo de inspectores
                empleado_libre = self.grupo_inspectores.obtener_empleado_libre()

                # Actualizo trabajo obtenido
                estado = Trabajo.ESTADO_SIENDO_INSPECCIONADO
                trabajo.estado = estado
                trabajo.empleado = empleado_libre

                # Asigno trabajo a empleado libre
                empleado_libre.asignar_trabajo(trabajo)
                empleado_libre.cambiar_a_estado_ocupado()

                # Genero evento fin inspección
                tipo = Evento.TIPO_FIN_INSPECCION
                rnd = truncar(random.random(), 2)
                tiempo = round(-1 * self.tiempo_planchado * math.log(1 - rnd), 2)
                tiempo_fin = truncar(evento_actual.tiempo_fin + tiempo, 2)
                nuevo_evento = Evento(tipo, rnd, tiempo, tiempo_fin, empleado_libre)

                # Agrego evento al manejador de eventos
                self.manejador_eventos.agregar_evento(nuevo_evento)

                # Agrego evento a lista de eventos generados durante la iteración
                eventos_iteracion.append(nuevo_evento)

        # Verifico cola máxima
        if self.grupo_empleados_zurcido.cola.existe_proximo_trabajo() or \
                self.grupo_empleados_costura.cola.existe_proximo_trabajo() or \
                self.grupo_empleados_planchado.cola.existe_proximo_trabajo() or \
                self.grupo_inspectores.cola.existe_proximo_trabajo():
            if self.cola_maxima is None:
                self.cola_maxima = self.grupo_empleados_zurcido.cola.id
                self.cantidad_cola_maxima = self.grupo_empleados_zurcido.cola.obtener_longitud()
            if self.grupo_empleados_zurcido.cola.obtener_longitud() > self.cantidad_cola_maxima:
                self.cola_maxima = self.grupo_empleados_zurcido.cola.id
                self.cantidad_cola_maxima = self.grupo_empleados_costura.cola.obtener_longitud()
            if self.grupo_empleados_costura.cola.obtener_longitud() > self.cantidad_cola_maxima:
                self.cola_maxima = self.grupo_empleados_costura.cola.id
                self.cantidad_cola_maxima = self.grupo_empleados_costura.cola.obtener_longitud()
            if self.grupo_empleados_planchado.cola.obtener_longitud() > self.cantidad_cola_maxima:
                self.cola_maxima = self.grupo_empleados_planchado.cola.id
                self.cantidad_cola_maxima = self.grupo_empleados_planchado.cola.obtener_longitud()
            if self.grupo_inspectores.cola.obtener_longitud() > self.cantidad_cola_maxima:
                self.cola_maxima = self.grupo_inspectores.cola.id
                self.cantidad_cola_maxima = self.grupo_inspectores.cola.obtener_longitud()

        # Verifico promedio de trabajos terminados
        if evento_actual.tipo != Evento.TIPO_INICIALIZACION:
            self.trabajos_terminados_promedio = round(self.trabajos_terminados / (evento_actual.tiempo_fin / 60), 2)

        return self.generar_vector_estado(evento_actual, eventos_iteracion)

    def simular(self):

        # Reestablezco atributos necesarios para el manejo de la simulacion
        self.manejador_eventos = None
        self.grupo_empleados_zurcido = None
        self.grupo_empleados_costura = None
        self.grupo_empleados_planchado = None
        self.grupo_inspectores = None
        self.rnd_trabajo_rechazado = None
        self.trabajo_rechazado = None
        self.trabajos_terminados = 0
        self.trabajos_terminados_promedio = 0
        self.cantidad_cola_maxima = 0
        self.cola_maxima = None
        self.ultimo_n_iteracion = -1
        self.ultimo_id_trabajo = 0
        self.ids_trabajos_iteraciones = []
        self.trabajos = []

        # Creo manejador de eventos inicial
        self.manejador_eventos = ManejadorEventos(eventos=[])

        # Agrego evento inicial a manejador de eventos
        tipo = Evento.TIPO_INICIALIZACION
        reloj = 0
        evento = Evento(tipo, None, None, reloj, None)
        self.manejador_eventos.agregar_evento(evento)

        # Creo grupos de empleados iniciales de acuerdo a alternativa elegida
        cola_zurcido = Cola(id_cola="zurcido", trabajos=[])
        cola_costura = Cola(id_cola="costura", trabajos=[])
        cola_planchado = Cola(id_cola="planchado", trabajos=[])
        cola_inspeccion = Cola(id_cola="inspeccion", trabajos=[])
        if self.empleados_generales:
            empleados_generales = []
            for i in range(0, self.cantidad_empleados_generales):
                id_empleado = "g" + str(i)
                empleados_generales.append(Empleado(id_empleado=id_empleado, estado=Empleado.ESTADO_LIBRE))
            self.grupo_empleados_zurcido = GrupoEmpleados(empleados=empleados_generales, cola=cola_zurcido)
            self.grupo_empleados_costura = GrupoEmpleados(empleados=empleados_generales, cola=cola_costura)
            self.grupo_empleados_planchado = GrupoEmpleados(empleados=empleados_generales, cola=cola_planchado)
        else:
            empleados_zurcido = []
            empleados_costura = []
            empleados_planchado = []
            for i in range(0, self.cantidad_empleados_zurcido):
                id_empleado = "z" + str(i)
                empleados_zurcido.append(Empleado(id_empleado=id_empleado, estado=Empleado.ESTADO_LIBRE))
            for i in range(0, self.cantidad_empleados_costura):
                id_empleado = "c" + str(i)
                empleados_costura.append(Empleado(id_empleado=id_empleado, estado=Empleado.ESTADO_LIBRE))
            for i in range(0, self.cantidad_empleados_planchado):
                id_empleado = "p" + str(i)
                empleados_planchado.append(Empleado(id_empleado=id_empleado, estado=Empleado.ESTADO_LIBRE))
            self.grupo_empleados_zurcido = GrupoEmpleados(empleados=empleados_zurcido, cola=cola_zurcido)
            self.grupo_empleados_costura = GrupoEmpleados(empleados=empleados_costura, cola=cola_costura)
            self.grupo_empleados_planchado = GrupoEmpleados(empleados=empleados_planchado, cola=cola_planchado)
        inspectores = []
        for i in range(0, self.cantidad_inspectores):
            id_empleado = "i" + str(i)
            inspectores.append(Empleado(id_empleado=id_empleado, estado=Empleado.ESTADO_LIBRE))
        self.grupo_inspectores = GrupoEmpleados(empleados=inspectores, cola=cola_inspeccion)

        # Calculo cada cuantas simulaciones mostrar el porcentaje de simulación
        if self.tiempo_simulacion <= 100:
            paso_muestra_datos = 1
        else:
            paso_muestra_datos = round(self.tiempo_simulacion / 50)
        proxima_muestra_datos = paso_muestra_datos

        # Flujo principal de simulación
        ultimo_vector_estado_agregado = True
        cantidad_iteraciones_agregadas = 0
        iteraciones_simuladas = []
        while 1:

            # Controlo que el reloj aún no supere el tiempo a simular
            vector_estado_proximo = self.simular_iteracion()
            if vector_estado_proximo.get("reloj") > self.tiempo_simulacion:
                break

            # Si no se salió del bucle, seteo que no se agrego el último vector de estado
            ultimo_vector_estado_agregado = False

            # Seteo vector estado
            vector_estado = vector_estado_proximo

            # Agrego iteración a iteraciones simuladas si el reloj y la cantidad de iteraciones están dentro de los
            # parámetros solicitados, controlando si se agregó el último vector para no agregarlo mas tarde
            if vector_estado.get("reloj") >= self.tiempo_desde and \
                    cantidad_iteraciones_agregadas < self.cantidad_iteraciones:
                ultimo_vector_estado_agregado = True
                cantidad_iteraciones_agregadas += 1
                iteraciones_simuladas.append(vector_estado)

                # Agrego id de trabajo a los ids de trabajos generados durante las iteraciones a mostrar
                if len(self.ids_trabajos_iteraciones) == 0:
                    for trabajo in self.trabajos:
                        self.ids_trabajos_iteraciones.append(trabajo.id)
                else:
                    if self.ultimo_id_trabajo != self.ids_trabajos_iteraciones[-1]:
                        self.ids_trabajos_iteraciones.append(self.ultimo_id_trabajo)

            # Muestro porcentaje de simulación cuando corresponda
            if vector_estado.get("reloj") >= proxima_muestra_datos:
                porcentaje = round(vector_estado.get("reloj") * 100 / self.tiempo_simulacion)
                self.controlador.mostrar_porcentaje_simulacion(porcentaje)
                while proxima_muestra_datos <= vector_estado.get("reloj"):
                    proxima_muestra_datos += paso_muestra_datos

        # Agrego ultimo vector de estado si aún no se agregó o modifico el último agregado si si se hizo
        if not ultimo_vector_estado_agregado:
            vector_estado = vector_estado_proximo
            vector_estado["trabajos"] = {}
            iteraciones_simuladas.append(vector_estado)

        # Genero diccionario con información sobre la simulación
        ids_empleados_generales = []
        ids_empleados_zurcido = []
        ids_empleados_costura = []
        ids_empleados_planchado = []
        if self.empleados_generales:
            ids_empleados_generales = [empleado.id for empleado in self.grupo_empleados_zurcido.empleados]
        else:
            ids_empleados_zurcido = [empleado.id for empleado in self.grupo_empleados_zurcido.empleados]
            ids_empleados_costura = [empleado.id for empleado in self.grupo_empleados_costura.empleados]
            ids_empleados_planchado = [empleado.id for empleado in self.grupo_empleados_planchado.empleados]
        ids_inspectores = [inspector.id for inspector in self.grupo_inspectores.empleados]
        ids_colas_empleados = [
            self.grupo_empleados_zurcido.cola.id,
            self.grupo_empleados_costura.cola.id,
            self.grupo_empleados_planchado.cola.id
        ]
        ids_colas_inspectores = [
            self.grupo_inspectores.cola.id
        ]
        ids_trabajos = self.ids_trabajos_iteraciones
        informacion_simulacion = {
            "ids_empleados_generales": ids_empleados_generales,
            "ids_empleados_zurcido": ids_empleados_zurcido,
            "ids_empleados_costura": ids_empleados_costura,
            "ids_empleados_planchado": ids_empleados_planchado,
            "ids_inspectores": ids_inspectores,
            "ids_colas_empleados": ids_colas_empleados,
            "ids_colas_inspectores": ids_colas_inspectores,
            "ids_trabajos": ids_trabajos,
            "cantidad_iteraciones_realizadas": iteraciones_simuladas[-1].get("n_iteracion"),
        }

        # Muestro porcentaje de simulación final
        self.controlador.mostrar_porcentaje_simulacion(100)

        # Devuelvo iteraciones simuladas de interés
        return iteraciones_simuladas, informacion_simulacion
