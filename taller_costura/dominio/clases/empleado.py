
class Empleado:

    id = None
    estado = None
    trabajo = None

    ESTADO_LIBRE = "Libre"
    ESTADO_OCUPADO = "Ocupado"

    def __init__(self, id_empleado=None, estado=None, trabajo=None):
        self.id = id_empleado
        self.estado = estado
        self.trabajo = trabajo

    def cambiar_a_estado_libre(self):
        self.estado = Empleado.ESTADO_LIBRE

    def cambiar_a_estado_ocupado(self):
        self.estado = Empleado.ESTADO_OCUPADO

    def asignar_trabajo(self, trabajo):
        self.trabajo = trabajo

    def desasignar_trabajo(self):
        trabajo = self.trabajo
        self.trabajo = None
        return trabajo

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

    def __str__(self):
        return "Empleado(id={id}, estado={estado}, trabajo={trabajo})".format(
            id=str(self.id),
            estado=self.estado,
            trabajo=self.trabajo.id if self.trabajo is not None else "None"
        )

    def __repr__(self):
        return "Empleado(id={id}, estado={estado}, trabajo={trabajo})".format(
            id=str(self.id),
            estado=self.estado,
            trabajo=self.trabajo.id if self.trabajo is not None else "None"
        )
