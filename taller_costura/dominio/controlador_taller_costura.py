from dominio.clases.simulador import Simulador


class ControladorTallerCostura:

    # Atibutos para interacción con la ventana
    ventana = None

    def __init__(self, ventana=None):
        self.ventana = ventana

    def mostrar_porcentaje_simulacion(self, porcentaje):
        self.ventana.mostrar_porcentaje_simulacion(porcentaje)

    def simular(self, tiempo_simulacion, tiempo_desde, cantidad_iteraciones, tiempo_llegada_trabajo,
                tiempo_zurcido, tiempo_costura, tiempo_planchado, tiempo_inspeccion, empleados_generales,
                cantidad_empleados_generales, cantidad_empleados_zurcido, cantidad_empleados_costura,
                cantidad_empleados_planchado, cantidad_inspectores, porcentaje_trabajos_rechazados):

        # Creo objeto simulador con parametros correspondientes
        simulador = Simulador(self, tiempo_simulacion, tiempo_desde, cantidad_iteraciones,
                              tiempo_llegada_trabajo, tiempo_zurcido, tiempo_costura, tiempo_planchado,
                              tiempo_inspeccion, empleados_generales, cantidad_empleados_generales,
                              cantidad_empleados_zurcido, cantidad_empleados_costura, cantidad_empleados_planchado,
                              cantidad_inspectores, porcentaje_trabajos_rechazados)

        # Realizo simulación
        iteraciones_simuladas, informacion_simulacion = simulador.simular()

        # Retorno iteraciones simuladas
        return iteraciones_simuladas, informacion_simulacion
