import serial
import time
# import serial.tools.list_ports
from inputs import get_gamepad
import math
import threading
import json


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
            LeftJoystickY   = self.LeftJoystickY,
            RightJoystickX  = self.RightJoystickX,
            RightJoystickY  = self.RightJoystickY,
            LeftTrigger     = self.LeftTrigger,
            RightTrigger    = self.RightTrigger,
            LeftBumper      = self.LeftBumper,
            RightBumper     = self.RightBumper,
            AButton         = self.A,
            BButton         = self.B,
            XButton         = self.X,
            YButton         = self.Y,
            LeftThumb       = self.LeftThumb,
            RightThumb      = self.RightThumb,
            LeftDpad        = self.LeftDPad,
            RightDpad       = self.RightDPad,
            UpDpad          = self.UpDPad,
            DownDpad        = self.DownDPad,
            BackButton      = self.Back,
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

"""def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data
    """


if __name__ == '__main__':

    print("Ready...")

    ser = serial.Serial("COM3", baudrate=9600,
                        timeout=2.5,
                        parity=serial.PARITY_NONE,
                        bytesize=serial.EIGHTBITS,
                        stopbits=serial.STOPBITS_ONE
                        )
    joy = XboxController()
    while True:

        #Converting dictionary to json strings
        json1 = json.dumps(joy.read())

        if ser.isOpen():
            ser.write(json1.encode('ascii'))
            ser.flush()
            try:
                incoming = ser.readline().decode("utf-8")
                print(incoming)
            except Exception as e:
                print(e)
                pass
            ser.close()
        else:
            print("opening error")



        """
        #Attempt to send through serial port
        COM = input(joy.read())
        serialInst.write(COM.encode('utf-8'))
        """
