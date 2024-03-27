import serial
import time
# import serial.tools.list_ports
from inputs import get_gamepad
import threading
import json
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFrame
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor, QPolygonF
from PyQt5.QtCore import QPointF, QTimer
import math

#ports = serial.tools.list_ports.comports()
#arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)
#serialInst = serial.Serial()

portsList = []


class XboxController(object):
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self):

        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0

        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()


    def read(self): # return the buttons/triggers that you care about in this methode
        thisdict = dict(
            LeftJoystickX   = self.LeftJoystickX,
            #LeftJoystickY   = self.LeftJoystickY,
            #RightJoystickX  = self.RightJoystickX,
            RightJoystickY  = self.RightJoystickY,
            LeftTrigger     = self.LeftTrigger,
            RightTrigger    = self.RightTrigger,
            #LeftBumper      = self.LeftBumper,
            #RightBumper     = self.RightBumper,
            #AButton         = self.A,
            #BButton         = self.B,
            #XButton         = self.X,
            #YButton         = self.Y,
            #LeftThumb       = self.LeftThumb,
            #RightThumb      = self.RightThumb,
            #LeftDpad        = self.LeftDPad,
            #RightDpad       = self.RightDPad,
            #UpDpad          = self.UpDPad,
            #DownDpad        = self.DownDPad,
            #BackButton      = self.Back,
            StartButton     = self.Start,
        )
        return thisdict

    def _monitor_controller(self):
        while True:
            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_Y':
                    self.LeftJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_X':
                    self.LeftJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RY':
                    self.RightJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RX':
                    self.RightJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_Z':
                    self.LeftTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'ABS_RZ':
                    self.RightTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'BTN_TL':
                    self.LeftBumper = event.state
                elif event.code == 'BTN_TR':
                    self.RightBumper = event.state
                elif event.code == 'BTN_SOUTH':
                    self.A = event.state
                elif event.code == 'BTN_NORTH':
                    self.Y = event.state #previously switched with X
                elif event.code == 'BTN_WEST':
                    self.X = event.state #previously switched with Y
                elif event.code == 'BTN_EAST':
                    self.B = event.state
                elif event.code == 'BTN_THUMBL':
                    self.LeftThumb = event.state
                elif event.code == 'BTN_THUMBR':
                    self.RightThumb = event.state
                elif event.code == 'BTN_SELECT':
                    self.Back = event.state
                elif event.code == 'BTN_START':
                    self.Start = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY1':
                    self.LeftDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY2':
                    self.RightDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY3':
                    self.UpDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY4':
                    self.DownDPad = event.state
            time.sleep(0.01)

class fenetre(QMainWindow):

    def __init__(self):
        super().__init__()

        # Mise en place de la fenêtre et paramètres de départ
        self.setWindowTitle("Positionnement de la grue caméra")
        self.setGeometry(1000, 100, 800, 1400)
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
        self.allongement_contrepoids = 2

        self.A_button_state = 0
        self.B_button_state = 0
        self.X_button_state = 0
        self.Y_button_state = 0

        self.robot_actif = False

        self.A_button = QLabel("A button state : " + str(self.A_button_state))
        self.layout.addWidget(self.A_button)
        self.B_button = QLabel("B button state : " + str(self.B_button_state))
        self.layout.addWidget(self.B_button)
        self.X_button = QLabel("X button state : " + str(self.X_button_state))
        self.layout.addWidget(self.X_button)
        self.Y_button = QLabel("Y button state : " + str(self.Y_button_state))
        self.layout.addWidget(self.Y_button)

        self.bouton_activer = QPushButton("Désactivé", clicked=self.activation)
        self.layout.addWidget(self.bouton_activer)

        self.cadre_controle = QFrame()
        self.layout.addWidget(self.cadre_controle)
        self.layout_controle = QVBoxLayout(self.cadre_controle)

        self.boutons()

        self.base_triangle = QPixmap(1000, 600)
        self.simulation()

        self.comInit()          #Set up the Serial communication
        self.periodicSetUp()    #will call the peiodic function at 100Hz

        self.update_button()
    def comInit(self):
        self.ser = serial.Serial("COM3", baudrate=9600,
                            timeout=2.5,
                            parity=serial.PARITY_NONE,
                            bytesize=serial.EIGHTBITS,
                            stopbits=serial.STOPBITS_ONE
                            )
        self.joy = XboxController()
    def periodicSetUp(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.communication)
        self.timer.timeout.connect(self.update_button)
        self.timer.start(50)    # 50ms interval
    def communication(self):
        json1 = json.dumps(self.joy.read())

        if self.ser.isOpen():
            data_js = json1.encode('ascii')
            print(data_js)
            self.ser.write(json1.encode('ascii'))
            self.ser.flush()
            try:
                self.incoming = self.ser.readline().decode("utf-8")
                print("got:", self.incoming)

            except Exception as e:
                print(e)
                pass
        else:
            print("opening error")

    def update_button(self):
        if self.joy.read().get('LefTrigger'):
            self.telescope_neg()
        if self.joy.read().get('RightTrigger'):
            self.telescope_pos()

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

    #def fermeture(self):
    #    sys.exit(app.exec_())
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
            #("Fermeture", self.fermeture)
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

        x2 = int(
            x1 + (self.longueur_bras + self.longueur_telescope) * math.cos(math.radians(90 + self.angle_inclinaison)))
        y2 = int(
            y1 - (self.longueur_bras + self.longueur_telescope) * math.sin(math.radians(90 + self.angle_inclinaison)))

        x3 = int(x1 - (self.longueur_contrepoids + self.longueur_contrepoids) * math.cos(
            math.radians(90 + self.angle_inclinaison)))
        y3 = int(y1 + (self.longueur_contrepoids + self.longueur_contrepoids) * math.sin(
            math.radians(90 + self.angle_inclinaison)))

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


if __name__ == '__main__':

    #Initialisation
    """
    ser = serial.Serial("COM3", baudrate=9600,
                        timeout=2.5,
                        parity=serial.PARITY_NONE,
                        bytesize=serial.EIGHTBITS,
                        stopbits=serial.STOPBITS_ONE
                        )
    joy = XboxController()
    """
    app = QApplication(sys.argv)
    window = fenetre()
    window.show()
    sys.exit(app.exec_())
    ###exit(0)
    """
    while True:

        #Converting dictionary to json strings
        json1 = json.dumps(joy.read())

        if ser.isOpen():
            data_js = json1.encode('ascii')
            print(data_js)
            ser.write(json1.encode('ascii'))
            ser.flush()
            try:
                incoming = ser.readline().decode("utf-8")
                print("got:", incoming)

            except Exception as e:
                print(e)
                pass
        else:
            print("opening error")

        """


        #if joy.read().get('YButton'):



        #ser.close()

