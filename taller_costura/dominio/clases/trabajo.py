
class Trabajo:

    id = None
    estado = None
    empleado = None
    hora_inicio_espera_zurcido = None
    hora_inicio_espera_costura = None
    hora_inicio_espera_planchado = None
    hora_inicio_espera_inspeccion = None

    ESTADO_SIENDO_ZURCIDO = "Siendo zurcido"
    ESTADO_ESPERANDO_ZURCIDO = "Esperando zurcido"
    ESTADO_SIENDO_COSIDO = "Siendo cosido"
    ESTADO_ESPERANDO_COSIDO = "Esperando cosido"
    ESTADO_SIENDO_PLANCHADO = "Siendo planchado"
    ESTADO_ESPERANDO_PLANCHADO = "Esperando planchado"
    ESTADO_SIENDO_INSPECCIONADO = "Siendo inspeccionado"
    ESTADO_ESPERANDO_INSPECCIONADO = "Esperando inspeccionado"

    def __init__(self, id_trabajo=None, estado=None, empleado=None, hora_inicio_espera_zurcido=None,
                 hora_inicio_espera_costura=None, hora_inicio_espera_planchado=None,
                 hora_inicio_espera_inspeccion=None):
        self.id = id_trabajo
        self.estado = estado
        self.empleado = empleado
        self.hora_inicio_espera_zurcido = hora_inicio_espera_zurcido
        self.hora_inicio_espera_costura = hora_inicio_espera_costura
        self.hora_inicio_espera_planchado = hora_inicio_espera_planchado
        self.hora_inicio_espera_inspeccion = hora_inicio_espera_inspeccion

    def cambiar_a_estado_siendo_zurcido(self):
        self.estado = Trabajo.ESTADO_SIENDO_ZURCIDO

    def cambiar_a_estado_esperando_zurcido(self):
        self.estado = Trabajo.ESTADO_ESPERANDO_ZURCIDO

    def cambiar_a_estado_siendo_cosido(self):
        self.estado = Trabajo.ESTADO_SIENDO_COSIDO

    def cambiar_a_estado_esperando_cosido(self):
        self.estado = Trabajo.ESTADO_ESPERANDO_COSIDO

    def cambiar_a_estado_siendo_planchado(self):
        self.estado = Trabajo.ESTADO_SIENDO_PLANCHADO

    def cambiar_a_estado_esperando_planchado(self):
        self.estado = Trabajo.ESTADO_ESPERANDO_PLANCHADO

    def cambiar_a_estado_siendo_inspeccionado(self):
        self.estado = Trabajo.ESTADO_SIENDO_INSPECCIONADO

    def cambiar_a_estado_esperando_inspeccionado(self):
        self.estado = Trabajo.ESTADO_ESPERANDO_INSPECCIONADO

    def __eq__(self, other):
        return True if self.id == other.id else False

    def __ne__(self, other):
        return True if self.id != other.id else False

    def __gt__(self, other):
        return True if self.id > other.id else False

    def __lt__(self, other):
        return True if self.id < other.id else False

    def __ge__(self, other):
        return True if self.id >= other.id else False

    def __le__(self, other):
        return True if self.id <= other.id else False

    def __deepcopy__(self, memodict={}):
        return Trabajo(self.id, self.estado, self.empleado, self.hora_inicio_espera_zurcido,
                       self.hora_inicio_espera_costura, self.hora_inicio_espera_planchado,
                       self.hora_inicio_espera_inspeccion)

    def __str__(self):
        return "Trabajo(id={id}, estado={estado}, empleado={empleado}, " \
               "hora_inicio_espera_zurcido={hora_inicio_espera_zurcido}, " \
               "hora_inicio_espera_costura={hora_inicio_espera_costura}, " \
               "hora_inicio_espera_planchado={hora_inicio_espera_planchado}, " \
               "hora_inicio_espera_inspeccion={hora_inicio_espera_inspeccion})".format(
                    id=str(self.id),
                    estado=self.estado,
                    empleado=self.empleado.id if self.empleado is not None else "None",
                    hora_inicio_espera_zurcido=str(self.hora_inicio_espera_zurcido) or "None",
                    hora_inicio_espera_costura=str(self.hora_inicio_espera_costura) or "None",
                    hora_inicio_espera_planchado=str(self.hora_inicio_espera_planchado) or "None",
                    hora_inicio_espera_inspeccion=str(self.hora_inicio_espera_inspeccion) or "None"
                )

    def __repr__(self):
        return "Trabajo(id={id}, estado={estado}, empleado={empleado}, " \
               "hora_inicio_espera_zurcido={hora_inicio_espera_zurcido}, " \
               "hora_inicio_espera_costura={hora_inicio_espera_costura}, " \
               "hora_inicio_espera_planchado={hora_inicio_espera_planchado}, " \
               "hora_inicio_espera_inspeccion={hora_inicio_espera_inspeccion})".format(
                    id=str(self.id),
                    estado=self.estado,
                    empleado=self.empleado.id if self.empleado is not None else "None",
                    hora_inicio_espera_zurcido=str(self.hora_inicio_espera_zurcido) or "None",
                    hora_inicio_espera_costura=str(self.hora_inicio_espera_costura) or "None",
                    hora_inicio_espera_planchado=str(self.hora_inicio_espera_planchado) or "None",
                    hora_inicio_espera_inspeccion=str(self.hora_inicio_espera_inspeccion) or "None"
                )
