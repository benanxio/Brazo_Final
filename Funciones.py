from time import sleep
import serial
from serial.tools import list_ports_windows

ser = serial.Serial()

def serial_ports():
    global ports
    ports = list_ports_windows.comports()
    puertos = []
    p = {}
    for pos,puerto in enumerate(ports):
        puertos.append(puerto)
        p.update({str(puerto):pos})
        
    return p


def conectar(option):
    global ser, ports
    
    if len(ports) > 0:
        ser.port = ports[option].device
        ser.baudrate = 9600
        try:
            ser.open()
            sleep(2)
        except:
            pass
        
def desconectar():
    global ser
    ser.close()


def verificar():
    global ser
    if ser.isOpen():
        return True
    else:
        return False


'''def enviar(x, y):
    global ser
    if x < 55:
        print("mover a la izquierda 0")
        ser.write(b"00001\n")
    elif x >= 55 and x < 110:
        # print("Mover a la izquierda 30")
        ser.write(b"00401\n")
    elif x >= 110 and x < 165:
        # print("Mover a la izquierda60")
        ser.write(b"00801\n")
    # Mover al centro
    elif x >= 165 and x < 220:
        #print("Mover al centro 90")
        ser.write(b"01201\n")
    elif x >= 220 and x < 275:
        #print("moviendo a la derecha120")
        ser.write(b"01601\n")
    elif x >= 275 and x < 330:
        #print("moviendo a la derecha150")
        ser.write(b"02001\n")
    elif x >= 330 and x < 385:
        #print("moviendo a la derecha150")
        ser.write(b"02401\n")
    elif x >= 385 and x < 440:
        #print("moviendo a la derecha150")
        ser.write(b"02801\n")
    elif x >= 440 and x < 495:
        #print("moviendo a la derecha150")
        ser.write(b"03201\n")
    elif x >= 495 and x < 550:
        #print("moviendo a la derecha150")
        ser.write(b"03601\n")
    elif x >= 550:
        #print("Moviendo a la derecha180")
        ser.write(b"04001\n")
    if y < 70:
        #print("Mover a la izquierda 0")
        ser.write(b"00002\n")
    elif y >= 70 and y < 140:
        #print("Mover a la izquierda30")
        ser.write(b"01002\n")
    elif y >= 140 and y < 210:
        #print("Mover a la izquierda60")
        ser.write(b"02002\n")
        # Mover al centro
    elif y >= 210 and y < 280:
        #print("Mover al centro 90")
        ser.write(b"03002\n")
    elif y >= 350 and y < 420:
        #print("moviendo a la derecha120")
        ser.write(b"04002\n")
    elif y >= 420 and y < 490:
        #print("moviendo a la derecha150")
        ser.write(b"05002\n")
    elif y >= 490:
        #print("Moviendo a la derecha180")
        ser.write(b"06002\n")
        # empuje
    if cv2.waitKey(1) == ord('l'):
        ser.write(b"03005\n")
    if cv2.waitKey(1) == ord('m'):
        ser.write(b"06005\n")
    # pinza
    if cv2.waitKey(1) == ord('o'):
        ser.write(b"15003\n")
    if cv2.waitKey(1) == ord('p'):
        ser.write(b"06004\n")
    # botar
    if cv2.waitKey(1) == ord('k'):
        ser.write(b"00007\n")
    # retonar despues de botar
    if cv2.waitKey(1) == ord('j'):
        ser.write(b"00008\n")
    # else:
    # print("nohay nada")'''
def enviar(x,y):
    global ser
    cad = f"{x},{y},\n"
    # cad = str(x) + "," + str("movobj\n") # se guarda en una string el valor de x y el movimiento predeterminado
    ser.write(cad.encode('ascii'))
    
def enviarColor(x,y,c):
    global ser

    cad = ""
    if len(c) > 0:    
        cad = f"{x},{y},ClassColor{c}\n"
        ser.write(cad.encode('ascii'))
        return True
    else:
        return False
    
def recibirConfirmacion():
    global ser
    if ser.in_waiting > 0:
        a = ser.readline()
        b = a.decode('utf').rstrip("\n")
        if b == "R" or b == "G" or b == "B":
            print(f"Resultado: {b}")
            return False,b
                    
        else:
            print(f"Recibido: {b}")
            return True,b
    else:
        return True,""
    
      
def reiniciar():
    ser.write(b"00008\n")
    bucle = True
