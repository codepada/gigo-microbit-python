"""
========================================================
GIGO Library for BBC micro:bit
========================================================

Library สำหรับควบคุมอุปกรณ์ GIGO ผ่าน micro:bit

รองรับ:
- Motor
- Ultrasonic Sonar
- Port A, B, C, D


========================================================
วิธีใช้งาน
========================================================

ใน main.py ให้เริ่มต้นด้วย

    from microbit import *
    from gigo import *


--------------------------------------------------------
1. SONAR
--------------------------------------------------------

ใช้สำหรับวัดระยะทาง หน่วยเป็นเซนติเมตร (cm)

รูปแบบคำสั่ง:

    sonar(port)

ตัวอย่าง:

    distance = sonar(A)
    print(distance)

สามารถเลือก Port ได้:

    sonar(A)
    sonar(B)
    sonar(C)
    sonar(D)


หาก Sonar อ่านค่าพลาดชั่วคราว
Library จะใช้ค่าระยะทางล่าสุดที่อ่านสำเร็จให้อัตโนมัติ

ดังนั้นใน main.py ไม่จำเป็นต้องตรวจสอบค่า -1


ตัวอย่างตรวจจับวัตถุใกล้กว่า 20 cm:

    distance = sonar(B)

    if distance < 20:
        display.show(Image.NO)
    else:
        display.show(Image.YES)


--------------------------------------------------------
2. MOTOR
--------------------------------------------------------

รูปแบบคำสั่ง:

    motor(port, direction, speed)

port:
    A
    B
    C
    D

direction:
    Left
    Right

speed:
    0 - 100


ตัวอย่าง:

    motor(A, Left, 100)

หมายถึง:
    Motor Port A
    หมุนทิศทาง Left
    ความเร็ว 100%


ตัวอย่างอื่น:

    motor(A, Right, 100)

    motor(B, Left, 80)

    motor(C, Right, 50)

    motor(D, Left, 30)


--------------------------------------------------------
3. MOTOR SPEED
--------------------------------------------------------

Speed กำหนดได้ตั้งแต่ 0 ถึง 100

ตัวอย่าง:

    motor(A, Left, 100)

    motor(A, Left, 50)

    motor(A, Left, 20)

Library จะแปลงค่า Speed 0-100
เป็น PWM 0-1023 ให้อัตโนมัติ


--------------------------------------------------------
4. STOP MOTOR
--------------------------------------------------------

หยุด Motor หนึ่ง Port:

    motor_stop(A)

ตัวอย่าง:

    motor(A, Left, 100)

    sleep(2000)

    motor_stop(A)


--------------------------------------------------------
5. STOP ALL MOTORS
--------------------------------------------------------

หยุด Motor ทุก Port:

    motor_stop_all()


--------------------------------------------------------
6. SONAR + MOTOR
--------------------------------------------------------

ตัวอย่าง:

ถ้าวัตถุอยู่ใกล้ 10 cm หรือน้อยกว่า
ให้ Motor ทำงาน

ถ้าวัตถุไกลกว่า 10 cm
ให้ Motor หยุด

    while True:

        distance = sonar(B)

        if distance <= 10:
            motor(A, Left, 100)
        else:
            motor_stop(A)

        sleep(100)


สามารถเขียนแบบสั้นได้:

    while True:

        if sonar(B) <= 10:
            motor(A, Left, 100)
        else:
            motor_stop(A)

        sleep(100)


========================================================
PORT PIN MAPPING
========================================================

MOTOR

Port A
    Direction = P2
    Speed     = P1

Port B
    Direction = P13
    Speed     = P8

Port C
    Direction = P15
    Speed     = P14

Port D
    Direction = P0
    Speed     = P16


SONAR

Port A
    Trig = P1
    Echo = P2

Port B
    Trig = P8
    Echo = P13

Port C
    Trig = P14
    Echo = P15

Port D
    Trig = P16
    Echo = P0


========================================================
QUICK REFERENCE
========================================================

SONAR

    sonar(A)
    sonar(B)
    sonar(C)
    sonar(D)


MOTOR

    motor(A, Left, 100)

    motor(A, Right, 100)

    motor_stop(A)

    motor_stop_all()


========================================================
"""


from microbit import *
from machine import time_pulse_us


# ======================================================
# CONSTANTS
# ======================================================

A = "A"
B = "B"
C = "C"
D = "D"

Left = "Left"
Right = "Right"


# ======================================================
# SONAR LAST DISTANCE
# ======================================================
#
# เก็บค่าระยะทางล่าสุดที่อ่านสำเร็จ
#
# ค่าเริ่มต้นกำหนดเป็น 100 cm
# เพื่อไม่ให้การอ่านผิดพลาดครั้งแรก
# ถูกตีความว่ามีวัตถุอยู่ใกล้
#

_last_distance = {
    A: 100,
    B: 100,
    C: 100,
    D: 100
}


# ======================================================
# MOTOR PIN MAP
# ======================================================

def _motor_pins(port):

    if port == A:
        return pin2, pin1

    elif port == B:
        return pin13, pin8

    elif port == C:
        return pin15, pin14

    elif port == D:
        return pin0, pin16

    return None, None


# ======================================================
# SONAR PIN MAP
# ======================================================

def _sonar_pins(port):

    if port == A:
        return pin1, pin2

    elif port == B:
        return pin8, pin13

    elif port == C:
        return pin14, pin15

    elif port == D:
        return pin16, pin0

    return None, None


# ======================================================
# MOTOR
# ======================================================

def motor(port, direction, speed):
    """
    ควบคุม Motor

    ตัวอย่าง:

        motor(A, Left, 100)

        motor(B, Right, 50)

    speed:
        0 - 100
    """

    direction_pin, speed_pin = _motor_pins(port)

    if direction_pin is None:
        return

    # จำกัดค่า Speed ให้อยู่ระหว่าง 0-100

    speed = max(0, min(100, speed))

    # แปลง Speed 0-100
    # เป็น PWM 0-1023

    pwm = int(speed * 1023 / 100)

    # กำหนดทิศทาง

    if direction == Left:

        direction_pin.write_digital(0)

    elif direction == Right:

        direction_pin.write_digital(1)

    else:

        speed_pin.write_analog(0)
        return

    # กำหนดความเร็ว Motor

    speed_pin.write_analog(pwm)


# ======================================================
# MOTOR STOP
# ======================================================

def motor_stop(port):
    """
    หยุด Motor หนึ่ง Port

    ตัวอย่าง:

        motor_stop(A)
    """

    direction_pin, speed_pin = _motor_pins(port)

    if speed_pin is not None:

        speed_pin.write_analog(0)


# ======================================================
# MOTOR STOP ALL
# ======================================================

def motor_stop_all():
    """
    หยุด Motor ทุก Port

    ตัวอย่าง:

        motor_stop_all()
    """

    motor_stop(A)
    motor_stop(B)
    motor_stop(C)
    motor_stop(D)

# ======================================================
# ROBOT MOVEMENT
# ======================================================

def forward(speed):
    """
    เดินหน้า

    ตัวอย่าง:
        forward(100)
    """
    motor(A, Left, speed)
    motor(B, Right, speed)


def backward(speed):
    """
    ถอยหลัง

    ตัวอย่าง:
        backward(100)
    """
    motor(A, Right, speed)
    motor(B, Left, speed)


def stop():
    """
    หยุดรถ

    ตัวอย่าง:
        stop()
    """
    motor_stop(A)
    motor_stop(B)


def turnleft(speed):
    """
    เลี้ยวซ้ายแบบหมุนอยู่กับที่

    ตัวอย่าง:
        turnleft(80)
    """
    motor(A, Right, speed)
    motor(B, Right, speed)


def turnright(speed):
    """
    เลี้ยวขวาแบบหมุนอยู่กับที่

    ตัวอย่าง:
        turnright(80)
    """
    motor(A, Left, speed)
    motor(B, Left, speed)
# ======================================================
# SONAR
# ======================================================

def sonar(port):
    """
    อ่านค่าระยะทางจาก Ultrasonic Sonar

    ตัวอย่าง:

        distance = sonar(B)

    Return:

        ระยะทาง หน่วย cm

    หากอ่านค่าพลาดชั่วคราว:
        จะคืนค่าระยะทางล่าสุดที่อ่านสำเร็จ
    """

    trig, echo = _sonar_pins(port)

    # ------------------------------------------
    # ตรวจสอบ Port
    # ------------------------------------------

    if trig is None:
        return 100


    # ------------------------------------------
    # ส่ง Trigger
    # ------------------------------------------
    #
    # ใช้ timing ตาม GIGO Control Box
    # ที่ทดสอบกับ HC-SR04+ แล้ว
    #

    trig.write_digital(0)
    sleep(2)

    trig.write_digital(1)
    sleep(10)

    trig.write_digital(0)


    # ------------------------------------------
    # อ่าน Echo Pulse
    # ------------------------------------------

    pulse_duration = time_pulse_us(
        echo,
        1,
        25000
    )


    # ------------------------------------------
    # ถ้าอ่าน Echo ไม่สำเร็จ
    # ------------------------------------------
    #
    # time_pulse_us() อาจคืนค่าติดลบ
    #
    # ไม่ส่ง -1 ไปยัง main.py
    # แต่ใช้ค่าครั้งล่าสุดแทน
    #

    if pulse_duration < 0:

        return _last_distance[port]


    # ------------------------------------------
    # คำนวณระยะทาง
    # ------------------------------------------
    #
    # ใช้สูตรเดียวกับ GIGO code
    # ที่ทดสอบกับอุปกรณ์จริง
    #

    distance = int(
        pulse_duration * 0.02
    )


    # ------------------------------------------
    # ตรวจสอบค่าที่ผิดปกติ
    # ------------------------------------------

    if distance <= 0:

        return _last_distance[port]


    # ------------------------------------------
    # บันทึกค่าที่อ่านสำเร็จ
    # ------------------------------------------

    _last_distance[port] = distance


    # ------------------------------------------
    # ส่งค่ากลับ
    # ------------------------------------------

    return distance