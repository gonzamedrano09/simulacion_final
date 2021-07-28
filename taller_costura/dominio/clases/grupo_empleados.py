import bisect
from dominio.clases.empleado import Empleado


class GrupoEmpleados:

    empleados = []
    cola = None

    def __init__(self, empleados=[], cola=None):
        self.empleados = empleados
        self.cola = cola

    def agregar_empleado(self, empleado):
        bisect.insort(self.empleados, empleado)

    def existe_empleado_libre(self):
        for i in range(len(self.empleados) - 1, -1, -1):
            if self.empleados[i].estado == Empleado.ESTADO_LIBRE:
                return True
        return False

    def obtener_empleado_libre(self):
        for i in range(0, len(self.empleados)):
            if self.empleados[i].estado == Empleado.ESTADO_LIBRE:
                return self.empleados[i]
        return None

    def __str__(self):
        empleados = ""
        for i in range(0, len(self.empleados)):
            empleados += self.empleados[i].id
            if i != len(self.empleados) - 1:
                empleados += ", "
        return "GrupoEmpleados(empleados=[{empleados}], cola={cola})".format(
            empleados=empleados,
            cola=self.cola
        )

    def __repr__(self):
        empleados = ""
        for i in range(0, len(self.empleados)):
            empleados += self.empleados[i].id
            if i != len(self.empleados) - 1:
                empleados += ", "
        return "GrupoEmpleados(empleados=[{empleados}], cola={cola})".format(
            empleados=empleados,
            cola=self.cola
        )
