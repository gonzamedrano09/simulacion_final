
class Cola:

    id = None
    trabajos = []

    def __init__(self, id_cola=None, trabajos=[]):
        self.id = id_cola
        self.trabajos = trabajos

    def agregar_trabajo(self, trabajo):
        self.trabajos.append(trabajo)

    def agregar_trabajo_al_principio(self, trabajo):
        self.trabajos.insert(0, trabajo)

    def existe_proximo_trabajo(self):
        return len(self.trabajos) != 0

    def obtener_proximo_trabajo(self):
        return self.trabajos.pop(0)

    def obtener_longitud(self):
        return len(self.trabajos)

    def __str__(self):
        trabajos = ""
        for i in range(0, len(self.trabajos)):
            trabajos += str(self.trabajos[i].id)
            if i != len(self.trabajos) - 1:
                trabajos += ", "
        return "Cola(id={id}, trabajos=[{trabajos}])".format(
            id=str(self.id),
            trabajos=trabajos
        )

    def __repr__(self):
        trabajos = ""
        for i in range(0, len(self.trabajos)):
            trabajos += str(self.trabajos[i].id)
            if i != len(self.trabajos) - 1:
                trabajos += ", "
        return "Cola(id={id}, trabajos=[{trabajos}])".format(
            id=str(self.id),
            trabajos=trabajos
        )
