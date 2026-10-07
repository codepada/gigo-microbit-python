# GIGO MicroPython สำหรับ BBC micro:bit

เริ่มเขียนโปรแกรมควบคุมหุ่นยนต์ GIGO ด้วย BBC micro:bit Python Editor โดยเปิดไฟล์เริ่มต้น `GIGO-Starter.hex`

## เริ่มต้นใช้งาน

1. [ดาวน์โหลด GIGO-Starter.hex](https://github.com/codepada/gigo-microbit-python/releases/download/v1.0.0/GIGO-Starter.hex) แล้วบันทึกไว้ในคอมพิวเตอร์
2. เปิด [micro:bit Python Editor](https://python.microbit.org/)
3. กด **Open**
4. เลือกไฟล์ **GIGO-Starter.hex** ที่ดาวน์โหลดไว้
5. เริ่มเขียนโปรแกรมใน `main.py` โดยใส่คำสั่งนำเข้าไลบรารีด้านล่างไว้ตอนต้น

```python
from microbit import *
from gigo import *
```

เมื่อเขียนเสร็จ ใช้ปุ่ม **Send to micro:bit** หรือ **Download** ตามตัวเลือกที่แสดงใน Editor เพื่อนำโปรแกรมไปใช้กับบอร์ด

## คำสั่งพื้นฐาน

| คำสั่ง | การทำงาน |
| --- | --- |
| `forward(100)` | เดินหน้าด้วยความเร็ว 100% |
| `backward(100)` | ถอยหลังด้วยความเร็ว 100% |
| `turnleft(100)` | หมุนเลี้ยวซ้ายอยู่กับที่ด้วยความเร็ว 100% |
| `turnright(100)` | หมุนเลี้ยวขวาอยู่กับที่ด้วยความเร็ว 100% |
| `stop()` | หยุดมอเตอร์ของรถที่พอร์ต A และ B |
| `sonar(A)` | อ่านระยะทางจากเซนเซอร์ที่พอร์ต A หน่วยเซนติเมตร |

ความเร็วกำหนดได้ตั้งแต่ `0` ถึง `100` คำสั่งเคลื่อนที่จะทำงานต่อจนกว่าจะสั่งเปลี่ยนทิศทางหรือหยุด ใช้ `sleep()` เพื่อกำหนดเวลารอ โดยมีหน่วยเป็นมิลลิวินาที

คำสั่งขับรถใช้มอเตอร์ที่พอร์ต **A และ B** ทิศทางจริงขึ้นอยู่กับการติดตั้งมอเตอร์ของรถ

## ตัวอย่าง: เดินหน้าแล้วหยุด

```python
from microbit import *
from gigo import *

forward(100)
sleep(1000)
stop()
```

## ตัวอย่าง: ทดลองทิศทางการเคลื่อนที่

```python
from microbit import *
from gigo import *

forward(100)
sleep(1000)
stop()
sleep(500)

backward(100)
sleep(1000)
stop()
sleep(500)

turnleft(100)
sleep(500)
stop()
sleep(500)

turnright(100)
sleep(500)
stop()
```

## ตัวอย่าง: อ่านระยะทาง

ต่อเซนเซอร์ Sonar ที่พอร์ต **A** สำหรับตัวอย่างนี้

```python
from microbit import *
from gigo import *

while True:
    distance = sonar(A)
    display.scroll(str(distance))
    sleep(200)
```

เลือกพอร์ตอื่นได้ด้วย `sonar(B)`, `sonar(C)` หรือ `sonar(D)` หากใช้ Sonar ร่วมกับคำสั่งขับรถ ให้ต่อ Sonar ที่พอร์ต **C หรือ D** เพื่อไม่ใช้พอร์ตเดียวกับมอเตอร์ A และ B

## ไฟล์ในโปรเจกต์

- `GIGO-Starter.hex` — ไฟล์เริ่มต้นสำหรับเปิดใน micro:bit Python Editor
- `gigo.py` — ไฟล์ต้นฉบับไลบรารี GIGO สำหรับศึกษาและอ้างอิง

สำหรับการเริ่มเรียน ให้ดาวน์โหลดและเปิด `GIGO-Starter.hex` ตามขั้นตอนด้านบน

ดาวน์โหลดเวอร์ชันแรกได้จาก [Release v1.0.0](https://github.com/codepada/gigo-microbit-python/releases/tag/v1.0.0)
