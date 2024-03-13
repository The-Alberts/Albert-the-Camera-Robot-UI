import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFrame
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor, QPolygonF
from PyQt5.QtCore import QPointF
import math

class SimulateurGrueCamera(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Positionnement de la grue de la caméra")
        self.resize(800, 1200)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Créer la zone d'affichage
        self.canvas = QLabel()
        self.layout.addWidget(self.canvas)

        # Initialiser les variables de position de la grue
        self.angle_rotation = 90
        self.angle_inclinaison = -60
        self.longueur_bras = 100
        self.longueur_telescope = 0
        self.increment_telescope = 10

        # Initialiser les vitesses des moteurs
        self.vitesse_moteur1 = 0
        self.vitesse_moteur2 = 0
        self.vitesse_moteur3 = 0
        self.vitesse_moteur4 = 0

        # Variable pour suivre l'état du robot
        self.robot_actif = False

        # Créer les étiquettes pour afficher les vitesses des moteurs
        self.etiquette_moteur1 = QLabel("Vitesse moteur 1 : " + str(self.vitesse_moteur1))
        self.layout.addWidget(self.etiquette_moteur1)
        self.etiquette_moteur2 = QLabel("Vitesse moteur 2 : " + str(self.vitesse_moteur2))
        self.layout.addWidget(self.etiquette_moteur2)
        self.etiquette_moteur3 = QLabel("Vitesse moteur 3 : " + str(self.vitesse_moteur3))
        self.layout.addWidget(self.etiquette_moteur3)
        self.etiquette_moteur4 = QLabel("Vitesse moteur 4 : " + str(self.vitesse_moteur4))
        self.layout.addWidget(self.etiquette_moteur4)

        # Créer le bouton d'activation
        self.bouton_activer = QPushButton("Activer", clicked=self.toggle_robot)
        self.layout.addWidget(self.bouton_activer)

        # Créer le cadre pour les contrôles
        self.cadre_controle = QFrame()
        self.layout.addWidget(self.cadre_controle)
        self.layout_controle = QVBoxLayout(self.cadre_controle)

        # Créer des boutons pour contrôler la grue
        self.creer_boutons_controle()

        # Initialiser la QPixmap pour dessiner
        self.base_pixmap = QPixmap(600, 600)
        self.dessiner_grue_camera()  # Appel initial pour dessiner la grue

    def toggle_robot(self):
        self.robot_actif = not self.robot_actif
        if self.robot_actif:
            self.bouton_activer.setText("Désactiver")
            self.bouton_activer.setStyleSheet("background-color: green; color: white;")
        else:
            self.bouton_activer.setText("Activer")
            self.bouton_activer.setStyleSheet("background-color: red; color: white;")

    def rotation_positive(self):
        if self.robot_actif:
            self.angle_rotation += 5
            self.dessiner_grue_camera()

    def rotation_negative(self):
        if self.robot_actif:
            self.angle_rotation -= 5
            self.dessiner_grue_camera()

    def creer_boutons_controle(self):
        boutons = [
            ("Rotation positive", self.rotation_positive),
            ("Rotation négative", self.rotation_negative),
            ("Incliner vers le haut", self.incliner_haut),
            ("Incliner vers le bas", self.incliner_bas),
            ("Télescoper +", self.etendre_telescope),
            ("Télescoper -", self.retracter_telescope)
        ]

        for texte, fonction in boutons:
            bouton = QPushButton(texte, clicked=fonction)
            self.layout_controle.addWidget(bouton)

    def incliner_haut(self):
        if self.robot_actif:
            self.angle_inclinaison += 5
            self.dessiner_grue_camera()

    def incliner_bas(self):
        if self.robot_actif:
            self.angle_inclinaison -= 5
            self.dessiner_grue_camera()

    def etendre_telescope(self):
        if self.robot_actif and self.longueur_telescope < 100:
            self.longueur_telescope += self.increment_telescope
            self.dessiner_grue_camera()

    def retracter_telescope(self):
        if self.robot_actif and self.longueur_telescope > 0:
            self.longueur_telescope -= self.increment_telescope
            self.dessiner_grue_camera()

    def dessiner_grue_camera(self):
        # Effacer la pixmap
        self.base_pixmap.fill(QColor("white"))

        # Dessiner les coordonnées
        painter = QPainter(self.base_pixmap)
        painter.setPen(QPen(QColor("black")))

        # Dessiner l'axe y
        painter.drawLine(20, 20, 20, 100)
        painter.drawText(20, 20, "Y")

        # Dessiner l'axe x
        painter.drawLine(20, 100, 100, 100)
        painter.drawText(110, 100, "X")

        # Dessiner la base de la grue (triangle inversé)
        base_coords = [QPointF(200, 330), QPointF(170, 360), QPointF(230, 360)]
        painter.setBrush(QColor("black"))
        painter.drawPolygon(QPolygonF(base_coords))

        # Calculer les coordonnées des articulations
        x1 = int(200 + self.longueur_bras * math.cos(math.radians(self.angle_rotation)))
        y1 = int(350 - self.longueur_bras * math.sin(math.radians(self.angle_rotation)))
        x2 = int(x1 + (self.longueur_bras + self.longueur_telescope) * math.cos(math.radians(self.angle_rotation + self.angle_inclinaison)))
        y2 = int(y1 - (self.longueur_bras + self.longueur_telescope) * math.sin(math.radians(self.angle_rotation + self.angle_inclinaison)))

        # Dessiner le bras de la grue
        painter.setPen(QPen(QColor("blue"), 5))
        painter.drawLine(QPointF(200, 350), QPointF(x1, y1))
        painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))

        # Dessiner la caméra
        painter.setBrush(QColor("black"))
        painter.drawEllipse(QPointF(x2, y2), 15, 15)

        # Détruire le QPainter
        painter.end()

        # Mettre à jour l'affichage
        self.canvas.setPixmap(self.base_pixmap)
        self.canvas.update()  # Mise à jour forcée du widget

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimulateurGrueCamera()
    window.show()
    sys.exit(app.exec_())
