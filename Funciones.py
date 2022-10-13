from time import sleep
import serial
from serial.tools import list_ports_windows

ser = serial.Serial()

def serial_ports():
    '''
    Regresa un diccionario con los puertos COM disponibles
    '''
    global ports
    ports = list_ports_windows.comports()
    puertos = []
    p = {}
    for pos,puerto in enumerate(ports):
        puertos.append(puerto)
        p.update({str(puerto):pos})
        
    return p


def conectar(option):
    '''
    Realiza la conexión con el puerto COM seleccionado
    '''
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
    '''
    Se desconecta del puerto COM
    '''
    global ser
    ser.close()


def verificar():
    '''
    Verifica si la conexion al puerto COM aun persiste
    '''
    global ser
    if ser.isOpen():
        return True
    else:
        return False

def enviar(x,y):
    global ser
    cad = f"{x},{y},\n"
    ser.write(cad.encode('ascii'))
    
def enviarColor(x,y,c):
    '''
    Envía la posición del objeto y el color a clasificar
    '''
    global ser
    cad = ""
    if len(c) > 0:    
        cad = f"{x},{y},ClassColor{c}\n"
        ser.write(cad.encode('ascii'))
        return True
    else:
        return False
    
def recibirConfirmacion():
    '''
    Espera una respuesta despues de que el brazo termina de clasificar
    '''
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