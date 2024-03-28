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

class Mainwindow(QMainWindow):

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

        self.rotation_angle = 180
        self.tilt_angle = -60
        self.arm_length = 50
        self.telescope_length = 100
        self.telescope_elongation = 5
        self.counterweight_length = 15
        self.counterweight_elongation = 2

        self.A_button_state = 0
        self.B_button_state = 0
        self.X_button_state = 0
        self.Y_button_state = 0

        self.active_robot = False

        self.A_button = QLabel("A button state : " + str(self.A_button_state))
        self.layout.addWidget(self.A_button)
        self.B_button = QLabel("B button state : " + str(self.B_button_state))
        self.layout.addWidget(self.B_button)
        self.X_button = QLabel("X button state : " + str(self.X_button_state))
        self.layout.addWidget(self.X_button)
        self.Y_button = QLabel("Y button state : " + str(self.Y_button_state))
        self.layout.addWidget(self.Y_button)

        self.activation_button = QPushButton("Desactivated", clicked=self.activation)
        self.layout.addWidget(self.activation_button)

        self.frame = QFrame()
        self.layout.addWidget(self.frame)
        self.layout_controle = QVBoxLayout(self.frame)

        self.buttons()

        self.base_triangle = QPixmap(1000, 600)
        self.simulation()

        self.comInit()          #Set up the Serial communication
        self.periodicSetUp()    #will call the peiodic function at 100Hz

        self.update_button()
    def comInit(self):
        self.ser = serial.Serial("COM5", baudrate=9600,
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
            self.retract_telescope()
        if self.joy.read().get('RightTrigger'):
            self.extend_telescope()

    def activation(self):
        self.active_robot = not self.active_robot
        if self.active_robot:
            self.activation_button.setText("Activated")
            self.activation_button.setStyleSheet("background-color: green; color: white;")
        else:
            self.activation_button.setText("Desactivated")
            self.activation_button.setStyleSheet("background-color: red; color: white;")
    def positive_rotation(self):
        if self.active_robot:
            self.rotation_angle += 3
            self.simulation()
    def negative_rotation(self):
        if self.active_robot:
            self.rotation_angle -= 3
            self.simulation()

    #def fermeture(self):
    #    sys.exit(app.exec_())
    def buttons(self):
        buttons = [
            ("Positive rotation", self.positive_rotation),
            ("Negative rotation", self.negative_rotation),
            ("Tilt up", self.tilt_up),
            ("Tilt down", self.tilt_down),
            ("Retract telescope", self.extend_telescope),
            ("Take out telescope", self.retract_telescope),
            #("Avancer contrepoids", self.contrepoids_pos),
            #("Reculer contrepoids", self.contrepoids_neg),
            #("Fermeture", self.fermeture)
        ]

        for texte, fonction in buttons:
            bouton = QPushButton(texte, clicked=fonction)
            self.layout_controle.addWidget(bouton)

    def tilt_up(self):
        if self.active_robot:
            self.tilt_angle += 3
            self.simulation()
    def tilt_down(self):
        if self.active_robot:
            self.tilt_angle -= 3
            self.simulation()
    def extend_telescope(self):
        if self.active_robot:
            self.telescope_length = self.telescope_length + self.telescope_elongation
            self.simulation()
    def retract_telescope(self):
        if self.active_robot:
            self.telescope_length = self.telescope_length - self.telescope_elongation
            self.simulation()
    def contrepoids_pos(self):
        if self.active_robot:
            self.counterweight_length = self.counterweight_length + self.counterweight_elongation
            self.simulation()
    def contrepoids_neg(self):
        if self.active_robot:
            self.counterweight_length = self.counterweight_length - self.counterweight_elongation
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
        x1 = int(150 + self.arm_length)
        y1 = int(350 - self.arm_length)

        x2 = int(
            x1 + (self.arm_length + self.telescope_length) * math.cos(math.radians(90 + self.tilt_angle)))
        y2 = int(
            y1 - (self.arm_length + self.telescope_length) * math.sin(math.radians(90 + self.tilt_angle)))

        x3 = int(x1 - (self.counterweight_length + self.counterweight_length) * math.cos(
            math.radians(90 + self.tilt_angle)))
        y3 = int(y1 + (self.counterweight_length + self.counterweight_length) * math.sin(
            math.radians(90 + self.tilt_angle)))

        x4 = int(x1 - 75 * math.cos(math.radians(90 + self.tilt_angle)))
        y4 = int(y1 + 75 * math.sin(math.radians(90 + self.tilt_angle)))

        xd = int(750 - 100 * math.cos(math.radians(self.rotation_angle)))
        yd = int(300 + 100 * math.sin(math.radians(self.rotation_angle)))

        # Dessin des lignes
        painter.setPen(QPen(QColor("black"), 5))
        painter.drawLine(QPointF(200, 430), QPointF(x1, y1))
        painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))
        painter.drawLine(QPointF(x1, y1), QPointF(x3, y3))
        painter.drawLine(QPointF(x1, y1), QPointF(x4, y4))

        # Dessin des éllipses
        painter.setBrush(QColor("blue"))
        painter.drawEllipse(QPointF(x2, y2), 13, 13)
        #painter.setBrush(QColor("green"))
        #painter.drawEllipse(QPointF(x3, y3), 10, 10)

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
    window = Mainwindow()
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