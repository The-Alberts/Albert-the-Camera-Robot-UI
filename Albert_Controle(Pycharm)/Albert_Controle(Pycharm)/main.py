# import serial
# import time
import serial.tools.list_ports
from inputs import get_gamepad
import math
import threading

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()

portsList = []

from inputs import get_gamepad
import math
import threading

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
        LJX = self.LeftJoystickX
        LJY = self.LeftJoystickY
        RJX = self.RightJoystickX
        RJY = self.RightJoystickY
        LT = self.LeftTrigger
        RT = self.RightTrigger
        LB = self.LeftBumper
        RB = self.RightBumper
        A = self.A
        B = self.B
        X = self.X
        Y = self.Y
        LTH = self.LeftThumb
        RTH = self.RightThumb
        Left = self.LeftDPad
        Right = self.RightDPad
        Up = self.UpDPad
        Down = self.DownDPad
        Back = self.Back
        Start = self.Start

        return [LJX,LJY,RJX,RJY,LT,RT,LB,RB,A,B,X,Y,LTH,RTH,Left,Right,Up,Down,Back,Start]


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




if __name__ == '__main__':
    """
    for onePort in ports:
        portsList.append(str(onePort))
        print(str(onePort))

    val = input("Select Port: COM")

    for x in range(0, len(portsList)):
        if portsList[x].startswith("COM" + str(val)):
            portVar = "COM" + str(val)
            print(portVar)

    serialInst.baudrate = 9600
    serialInst.port = portVar
    serialInst.open()
"""
    joy = XboxController()
    while True:
        print(joy.read())
        print("\n")
        #COM = input(joy.read())
        #serialInst.write(COM.encode('utf-8'))


# COMMUNICATION
"""
for onePort in ports:
    portsList.append(str(onePort))
    print(str(onePort))

val = input("Select Port: COM")

for x in range(0,len(portsList)):
    if portsList[x].startswith("COM" + str(val)):
        portVar = "COM" + str(val)
        print(portVar)

serialInst.baudrate = 9600
serialInst.port = portVar
serialInst.open()

while True:
    command = input("Arduino Command: (ON/OFF): ")
    serialInst.write(command.encode('utf-8'))

    if command == 'exit':
        exit()
"""