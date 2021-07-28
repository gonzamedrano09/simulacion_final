
class Evento:

    tipo = None
    rnd = None
    tiempo = None
    tiempo_fin = None
    empleado = None
    trabajo = None

    TIPO_INICIALIZACION = "inicializacion"
    TIPO_LLEGADA_TRABAJO = "llegada_trabajo"
    TIPO_FIN_ZURCIDO = "fin_zurcido"
    TIPO_FIN_COSTURA = "fin_costura"
    TIPO_FIN_PLANCHADO = "fin_planchado"
    TIPO_FIN_INSPECCION = "fin_inspeccion"

    def __init__(self, tipo_evento=None, rnd=None, tiempo=None, tiempo_fin=None, empleado=None, trabajo=None):
        self.tipo = tipo_evento
        self.rnd = rnd
        self.tiempo = tiempo
        self.tiempo_fin = tiempo_fin
        self.empleado = empleado
        self.trabajo = trabajo

    def __eq__(self, other):
        return True if self.tiempo_fin == other.tiempo_fin else False

    def __ne__(self, other):
        return True if self.tiempo_fin != other.tiempo_fin else False

    def __gt__(self, other):
        return True if self.tiempo_fin > other.tiempo_fin else False

    def __lt__(self, other):
        return True if self.tiempo_fin < other.tiempo_fin else False

    def __ge__(self, other):
        return True if self.tiempo_fin >= other.tiempo_fin else False

    def __le__(self, other):
        return True if self.tiempo_fin <= other.tiempo_fin else False

    def __str__(self):
        return "Evento(tipo={tipo}, rnd={rnd}, tiempo={tiempo}, tiempo_fin={tiempo_fin}, empleado={empleado}, " \
               "trabajo={trabajo})".format(
                    tipo=self.tipo,
                    rnd=str(self.rnd),
                    tiempo=str(self.tiempo),
                    tiempo_fin=str(self.tiempo_fin),
                    empleado=self.empleado.id if self.empleado is not None else "None",
                    trabajo=self.trabajo.id if self.trabajo is not None else "None"
                )

    def __repr__(self):
        return "Evento(tipo={tipo}, rnd={rnd}, tiempo={tiempo}, tiempo_fin={tiempo_fin}, empleado={empleado}, " \
               "trabajo={trabajo})".format(
                    tipo=self.tipo,
                    rnd=str(self.rnd),
                    tiempo=str(self.tiempo),
                    tiempo_fin=str(self.tiempo_fin),
                    empleado=self.empleado.id if self.empleado is not None else "None",
                    trabajo=self.trabajo.id if self.trabajo is not None else "None"
                )
