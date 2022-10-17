import cv2
import numpy as np
import time
import Funciones
from threading import Thread
from Index import Principal

clasificar = False
detectado = False
inicio, previo = 0, 0  # Para contar los segundos de espera
tDetect = 3  # Tiempo de espera antes de la clasificacion
clascolor = ""
actualizar = False  # Se accede desde el archivo Index para actualizar los datos recibidos
clasificando = False
distancia = 0


azul = np.array([[90, 100, 20],
                [120, 255, 255]], np.uint8)

verde = np.array([[25, 52, 72],
                  [102, 255, 255]], np.uint8)

rojo1 = np.array([[0, 100, 20],
                  [8, 255, 255]], np.uint8)

rojo2 = np.array([[170, 100, 20],
                  [179, 255, 255]], np.uint8)


colores = {"Rojo": (0, 0, 255),
           "Verde": (0, 255, 0),
           "Azul": (255, 0, 0)}

font = cv2.FONT_HERSHEY_SIMPLEX


def listarCamaras():
    import device
    
    dispositivos = {}
    device_list = device.getDeviceList()

    for index, camera in enumerate(device_list):
        dispositivos.update({str(camera[0]): index})

    return dispositivos


def pError(val, error=0.01):
    return [val - int(val * error), val + int(val * error)]


def cRango(val, valE):
    if val > valE[0] and val < valE[1]:
        return True
    else:
        return False


def dibujar(mask, color):

    global x, y, erx, ery, detectado

    contornos, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contornos:
        area = cv2.contourArea(c)
        if area > distancia:
            detectado = True
            M = cv2.moments(c)
            if (M["m00"] == 0):
                M["m00"] = 1
            x = int(M["m10"]/M["m00"])
            y = int(M['m01']/M['m00'])
            cv2.circle(frame, (x, y), 7, (0, 0, 255), -1)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, '{},{}'.format(x, y), (x + 10, y), font, 1.2, (0, 0, 255), 2, cv2.LINE_AA)
            nuevoContorno = cv2.convexHull(c)
            cv2.drawContours(frame, [nuevoContorno], 0, color, 3)
            if Funciones.verificar() and clasificando == False:
                # Funciones.enviar(x,y)
                clasificacion(color)

def Confirmacion(val):
    global actualizar,clasificar,previo,detectado,clasificando
    
    while val:
        val, c = Funciones.recibirConfirmacion()
        if val == False:
            Principal.GuardarDB(Principal, c)
            actualizar = True
    clasificar = False
    previo = 0
    detectado = False
    clasificando = False

def clasificacion(color, Draw=True):

    global clasificar, inicio, erx, ery, previo, detectado, frame, clascolor, actualizar,clasificando

    if detectado and clasificar == False:
        clasificar = True
        inicio = time.time()
        erx = pError(x, 0.05)
        ery = pError(y, 0.05)

    elif detectado and clasificar:
        actual = int(time.time() - inicio)
        if Draw:
            # Muestra el margen de error de x,y
            cv2.rectangle(frame, (5, 5), (190, 50), (50, 50, 50), -1)
            cv2.putText(frame, f'Error en x: {erx[0]} <=> {erx[1]}', (
                10, 20), font, .4, (255, 255, 225), 1, cv2.LINE_AA)
            cv2.putText(frame, f'Error en y: {ery[0]} <=> {ery[1]}', (
                10, 40), font, .4, (255, 255, 225), 1, cv2.LINE_AA)

        if previo < actual:
            previo = actual

            if previo == tDetect and cRango(x, erx) and cRango(y, ery):

                val = Funciones.enviarColor(x, y, clascolor)
                clasificando = True
                t1 = Thread(target = Confirmacion,args=(val,))
                #t1.setDaemon(True)
                t1.start()
                
            elif previo < tDetect and cRango(x, erx) and cRango(y, ery):
                pass

            elif previo < tDetect and cRango(x, erx) == False and cRango(y, ery) == False:
                previo = 0
                clasificar = False
                detectado = False
            else:
                previo = 0
                clasificar = False
        # Dibuja el tiempo restante y cuando empieza a clasificar
        elif previo < tDetect and cRango(x, erx) and cRango(y, ery):

            actual = time.time() - inicio
            centro = (frame.shape[1]//2, frame.shape[0]//2)

            if actual < tDetect-0.2:
                cv2.putText(frame, f"{tDetect - previo}",
                            centro, font, 1.0, color, 2, cv2.LINE_AA)
            else:
                cv2.putText(
                    frame, 'Clasificando', (centro[0]-120, centro[1]), font, 1.5, (15, 15, 15), 3, cv2.LINE_AA)
        else:
            pass
    else:
        pass


def capturar():
    global cap, clascolor, frame
    ret, frame = cap.read()
    if ret:
        #frame = cv2.flip(frame, 1)

        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        maskRed1 = cv2.inRange(frameHSV, rojo1[0], rojo1[1])
        maskRed2 = cv2.inRange(frameHSV, rojo2[0], rojo2[1])
        
        maskRed = cv2.add(maskRed1, maskRed2)
        maskAzul = cv2.inRange(frameHSV, azul[0], azul[1])
        maskGreen = cv2.inRange(frameHSV, verde[0], verde[1])
        
        if maskRed[maskRed >= 255].shape[0] > distancia:
            clascolor = "R"
            dibujar(maskRed1, colores["Rojo"])
        elif maskGreen[maskGreen >= 255].shape[0] > distancia:
            clascolor = "G"
            dibujar(maskGreen, colores["Verde"])
        elif maskAzul[maskAzul >= 255].shape[0] > distancia:
            dibujar(maskAzul, colores["Azul"])
            clascolor = "B"
        
        if clasificando:
                centro = (frame.shape[1]//2, frame.shape[0]//2)
                cv2.putText(frame, 'Clasificando', (centro[0]-120, centro[1]), font, 1.5, (15, 15, 15), 3, cv2.LINE_AA)

    return ret, frame


def encender(cam):
    global cap
    cap = cv2.VideoCapture(cam)


def apagar():
    global cap
    cap.release()