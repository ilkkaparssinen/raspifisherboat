# Motors . skid steering - control two motors

from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor


class Motors:
    def __init__(self, brainz=None, verbose=False):
        self.verbose = verbose
        self.brainz = brainz
        self.started = False
        self.cycle_time = 0

    def __print(self, str):
        if self.verbose:
            print ( str)

    def start(self):
        self.started = True
        self.mh = Adafruit_MotorHAT(addr=0x60)
        self.leftMotor = self.mh.getMotor(1)
        self.rightMotor = self.mh.getMotor(2)

    def stop(self):
        self.leftMotor.run(Adafruit_MotorHAT.RELEASE)
        self.rightMotor.run(Adafruit_MotorHAT.RELEASE)

    def tick(self,interval):

        if not self.started:
            return
        self.cycle_time += interval
        self.set_speed()

    def set_speed(self):
        new_speed = 0
        if self.brainz.speed_change_percent < 1:
            new_speed = self.brainz.speed
        else:
            if self.cycle_time > self.brainz.speed_change_cycle:
                self.cycle_time = 0
            if self.cycle_time > self.brainz.speed_motors_full_percent *  self.brainz.speed_change_cycle / 100.0:
                new_speed = self.brainz.speed * (100 - self.brainz.speed_change_percent) / 100.0
            else:
                new_speed = self.brainz.speed

        # Divide speed to two motors


        new_right_motor_speed = new_speed * (1.0 - self.brainz.turn ) / 2.0
        new_left_motor_speed = new_speed * (1.0 + self.brainz.turn ) / 2.0

        self.leftMotor.setSpeed(new_left_motor_speed * 255)
        self.rightMotor.setSpeed(new_right_motor_speed * 255)

    def set_speed_motor(self,motor,speed):
        self.__print("Set speed:" + str(motor) + " " + str(speed))


