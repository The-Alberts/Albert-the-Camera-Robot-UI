import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFrame
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor, QPolygonF
from PyQt5.QtCore import QPointF
import math

class fenetre(QMainWindow):
    def __init__(self):
        super().__init__()

        # Mise en place de la fenêtre et paramètres de départ
        self.setWindowTitle("Positionnement de la grue caméra")
        self.setGeometry(1000,100,800,1400)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.canvas = QLabel()
        self.layout.addWidget(self.canvas)

        self.angle_rotation = 180
        self.angle_inclinaison = -60
        self.longueur_bras = 50
        self.longueur_telescope = 100
        self.allongement_telescope = 10
        self.longueur_contrepoids = 15
        self.allongement_contrepoids = 3

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

        self.base_triangle = QPixmap(1000, 600)
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
            self.angle_rotation += 3
            self.simulation()

    def rotation_neg(self):
        if self.robot_actif:
            self.angle_rotation -= 3
            self.simulation()

    def boutons(self):
        boutons = [
            ("Rotation positive", self.rotation_pos),
            ("Rotation négative", self.rotation_neg),
            ("Incliner vers le haut", self.incliner_haut),
            ("Incliner vers le bas", self.incliner_bas),
            ("Sortir télescope", self.telescope_pos),
            ("Rentrer télescope", self.telescope_neg),
            ("Avancer contrepoids", self.contrepoids_pos),
            ("Reculer contrepoids", self.contrepoids_neg),
        ]

        for texte, fonction in boutons:
            bouton = QPushButton(texte, clicked=fonction)
            self.layout_controle.addWidget(bouton)

    def incliner_haut(self):
        if self.robot_actif:
            self.angle_inclinaison += 3
            self.simulation()

    def incliner_bas(self):
        if self.robot_actif:
            self.angle_inclinaison -= 3
            self.simulation()

    def telescope_pos(self):
        if self.robot_actif:
            self.longueur_telescope = self.longueur_telescope + self.allongement_telescope
            self.simulation()

    def telescope_neg(self):
        if self.robot_actif:
            self.longueur_telescope = self.longueur_telescope - self.allongement_telescope
            self.simulation()

    def contrepoids_pos(self):
        if self.robot_actif:
            self.longueur_contrepoids = self.longueur_contrepoids + self.allongement_contrepoids
            self.simulation()

    def contrepoids_neg(self):
        if self.robot_actif:
            self.longueur_contrepoids = self.longueur_contrepoids - self.allongement_contrepoids
            self.simulation()

    def simulation(self):
        self.base_triangle.fill(QColor("white"))

        painter = QPainter(self.base_triangle)
        painter.setPen(QPen(QColor("black")))

        # Dessin du référentiel vue de côté
        painter.drawLine(20, 30, 20, 90)
        painter.drawText(16, 23, "Y")

        painter.drawLine(20, 90, 80, 90)
        painter.drawText(90, 93, "X")

        # Dessin du référentiel vue de dessus
        painter.drawLine(895, 80, 895, 20)
        painter.drawText(890, 105, "Z")

        painter.drawLine(895, 20, 955, 20)
        painter.drawText(965, 29, "X")

        # Dessin de la base triangulaire
        base_coords = [QPointF(200, 400), QPointF(170, 460), QPointF(230, 460)]
        painter.setBrush(QColor("gray"))
        painter.drawPolygon(QPolygonF(base_coords))

        # Calculs de l'angle des lignes dessinées
        x1 = int(150 + self.longueur_bras)
        y1 = int(350 - self.longueur_bras)

        x2 = int(x1 + (self.longueur_bras + self.longueur_telescope) * math.cos(math.radians(90 + self.angle_inclinaison)))
        y2 = int(y1 - (self.longueur_bras + self.longueur_telescope) * math.sin(math.radians(90 + self.angle_inclinaison)))

        x3 = int(x1 - (self.longueur_contrepoids + self.longueur_contrepoids) * math.cos(math.radians(90 + self.angle_inclinaison)))
        y3 = int(y1 + (self.longueur_contrepoids + self.longueur_contrepoids) * math.sin(math.radians(90 + self.angle_inclinaison)))

        x4 = int(x1 - 75 * math.cos(math.radians(90 + self.angle_inclinaison)))
        y4 = int(y1 + 75 * math.sin(math.radians(90 + self.angle_inclinaison)))

        xd = int(750 - 100 * math.cos(math.radians(self.angle_rotation)))
        yd = int(300 + 100 * math.sin(math.radians(self.angle_rotation)))

        # Dessin des lignes
        painter.setPen(QPen(QColor("black"), 5))
        painter.drawLine(QPointF(200, 430), QPointF(x1, y1))
        painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))
        painter.drawLine(QPointF(x1, y1), QPointF(x3, y3))
        painter.drawLine(QPointF(x1, y1), QPointF(x4, y4))

        # Dessin des éllipses
        painter.setBrush(QColor("blue"))
        painter.drawEllipse(QPointF(x2, y2), 13, 13)
        painter.setBrush(QColor("green"))
        painter.drawEllipse(QPointF(x3, y3), 10, 10)

        # Dessin de la vue de dessus
        painter.setPen(QPen(QColor("black"), 2))
        painter.setBrush(QColor("white"))
        painter.drawEllipse(QPointF(750, 300), 100, 100)
        painter.drawLine(QPointF(750, 300), QPointF(xd, yd))

        # Tracé des titres dans le pixmap
        painter.drawText(175, 150, "Vue de côté")
        painter.drawText(685, 150, "Vue de dessus")

        painter.end()

        self.canvas.setPixmap(self.base_triangle)
        self.canvas.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = fenetre()
    window.show()
    sys.exit(app.exec_())
