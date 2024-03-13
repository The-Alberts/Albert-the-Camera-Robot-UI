import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFrame
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor, QPolygonF
from PyQt5.QtCore import QPointF
import math

class fenetre(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Positionnement de la grue caméra")
        self.setGeometry(600,50,700,1050)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.canvas = QLabel()
        self.layout.addWidget(self.canvas)

        self.angle_rotation = 90
        self.angle_inclinaison = -60
        self.longueur_bras = 100
        self.longueur_telescope = 0
        self.allongement_telescope = 10

        self.vitesse_moteur1 = 0
        self.vitesse_moteur2 = 0
        self.vitesse_moteur3 = 0
        self.vitesse_moteur4 = 0

        self.robot_actif = False

        self.nom_moteur1 = QLabel("Vitesse moteur 1 : " + str(self.vitesse_moteur1))
        self.layout.addWidget(self.nom_moteur1)
        self.nom_moteur2 = QLabel("Vitesse moteur 2 : " + str(self.vitesse_moteur2))
        self.layout.addWidget(self.nom_moteur2)
        self.nom_moteur3 = QLabel("Vitesse moteur 3 : " + str(self.vitesse_moteur3))
        self.layout.addWidget(self.nom_moteur3)
        self.nom_moteur4 = QLabel("Vitesse moteur 4 : " + str(self.vitesse_moteur4))
        self.layout.addWidget(self.nom_moteur4)

        self.bouton_activer = QPushButton("Désactivé", clicked=self.activation)
        self.layout.addWidget(self.bouton_activer)

        self.cadre_controle = QFrame()
        self.layout.addWidget(self.cadre_controle)
        self.layout_controle = QVBoxLayout(self.cadre_controle)

        self.boutons()

        self.base_triangle = QPixmap(600, 600)
        self.simulation()

    def activation(self):
        self.robot_actif = not self.robot_actif
        if self.robot_actif:
            self.bouton_activer.setText("Activé")
            self.bouton_activer.setStyleSheet("background-color: green; color: white;")
        else:
            self.bouton_activer.setText("Désactivé")
            self.bouton_activer.setStyleSheet("background-color: red; color: white;")

    def rotation_pos(self):
        if self.robot_actif:
            self.angle_rotation += 5
            self.simulation()

    def rotation_neg(self):
        if self.robot_actif:
            self.angle_rotation -= 5
            self.simulation()

    def boutons(self):
        boutons = [
            ("Rotation positive", self.rotation_pos),
            ("Rotation négative", self.rotation_neg),
            ("Incliner vers le haut", self.incliner_haut),
            ("Incliner vers le bas", self.incliner_bas),
            ("Télescoper +", self.telescope_pos),
            ("Télescoper -", self.telescope_neg)
        ]

        for texte, fonction in boutons:
            bouton = QPushButton(texte, clicked=fonction)
            self.layout_controle.addWidget(bouton)

    def incliner_haut(self):
        if self.robot_actif:
            self.angle_inclinaison += 5
            self.simulation()

    def incliner_bas(self):
        if self.robot_actif:
            self.angle_inclinaison -= 5
            self.simulation()

    def telescope_pos(self):
        if self.robot_actif:
            self.longueur_telescope = self.longueur_telescope + self.allongement_telescope
            self.simulation()

    def telescope_neg(self):
        if self.robot_actif:
            self.longueur_telescope = self.longueur_telescope - self.allongement_telescope
            self.simulation()

    def simulation(self):
        self.base_triangle.fill(QColor("white"))

        painter = QPainter(self.base_triangle)
        painter.setPen(QPen(QColor("black")))

        painter.drawLine(20, 20, 20, 80)
        painter.drawText(16, 15, "Y")

        painter.drawLine(20, 80, 80, 80)
        painter.drawText(90, 80, "X")

        base_coords = [QPointF(200, 330), QPointF(170, 360), QPointF(230, 360)]
        painter.setBrush(QColor("gray"))
        painter.drawPolygon(QPolygonF(base_coords))

        x1 = int(200 + self.longueur_bras * math.cos(math.radians(self.angle_rotation)))
        y1 = int(350 - self.longueur_bras * math.sin(math.radians(self.angle_rotation)))
        x2 = int(x1 + (self.longueur_bras + self.longueur_telescope) * math.cos(math.radians(self.angle_rotation + self.angle_inclinaison)))
        y2 = int(y1 - (self.longueur_bras + self.longueur_telescope) * math.sin(math.radians(self.angle_rotation + self.angle_inclinaison)))

        painter.setPen(QPen(QColor("black"), 5))
        painter.drawLine(QPointF(200, 350), QPointF(x1, y1))
        painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))

        painter.setBrush(QColor("blue"))
        painter.drawEllipse(QPointF(x2, y2), 10, 10)

        painter.end()

        self.canvas.setPixmap(self.base_triangle)
        self.canvas.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = fenetre()
    window.show()
    sys.exit(app.exec_())
