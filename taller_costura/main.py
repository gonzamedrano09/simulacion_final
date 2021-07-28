import sys
from PyQt5.QtWidgets import QApplication
from interfaz.recursos import sim
from interfaz.ventana_taller_costura import VentanaTallerCostura


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = VentanaTallerCostura(app)
    window.show()
    app.exec_()
