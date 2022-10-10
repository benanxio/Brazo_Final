import cv2
import numpy as np
import time
import Funciones
import device
from Index import Principal

clasificar = False
detectado = False
inicio, previo = 0, 0 #Para contar los segundos de espera
tDetect = 5 #Tiempo de espera antes de la clasificacion
clascolor = ""
actualizar = False #Se accede desde el archivo Index para actualizar los datos recibidos


azul = np.array([[100, 100, 20],
                 [125, 255, 255]], np.uint8)

verde = np.array([[25,52,72],
                    [102,255,255]], np.uint8)

rojo1 = np.array([[0, 100, 20],
                  [8, 255, 255]], np.uint8)

rojo2 = np.array([[170,100,20],
                  [179,255,255]], np.uint8)


colores = {"Rojo":(0, 0, 255),
         "Verde":(0, 255, 0),
         "Azul":(255, 0, 0)}

switch_guardar_datos = {
	"R": "Rojo",
	"G": "Verde",
	"B": "Azul",
}

font = cv2.FONT_HERSHEY_SIMPLEX

def listarCamaras():

    global devices
    devices = {}
    
    device_list = device.getDeviceList()
    if len(device_list) > 1:
      deviceP = device_list[0]
      device_list[0] = device_list[1]
      device_list[1] = deviceP

    for index,camera in enumerate(device_list):
      devices.update({str(camera[0]):index})
      
    return devices


def pError(val, error=0.01):
    return [val - int(val * error),val + int(val * error)]


def cRango(val,valE):
    if val > valE[0] and val < valE[1]:
        return True
    else:
        return False
    
    

def dibujar(mask, color):

    global x,y, erx,ery, detectado

    contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contornos:
        area = cv2.contourArea(c)
        if area > 6000:
            detectado = True
            M = cv2.moments(c)
            if (M["m00"] == 0):
                M["m00"] = 1
            x = int(M["m10"]/M["m00"])
            y = int(M['m01']/M['m00'])
            cv2.circle(frame, (x, y), 7, (0, 0, 255), -1)
            cv2.putText(frame, f'{x},{y}', (x+10, y), font, 1.2, (0, 0, 255), 2, cv2.LINE_AA)
            nuevoContorno = cv2.convexHull(c)
            cv2.drawContours(frame, [nuevoContorno], 0, color, 3)
            if Funciones.verificar():
                Funciones.enviar(x,y)
                clasificacion()

def clasificacion(Draw=True):
    
    global x, clasificar, inicio, erx,ery, previo,detectado,frame,clascolor,actualizar
    
    if detectado and clasificar == False:
        clasificar = True
        inicio = time.time()
        erx = pError(x,0.05)
        ery = pError(y,0.05)
        
    elif detectado and clasificar:
        actual = int(time.time() - inicio)
        #Muestra el marge de error de x,y
        if Draw:
            cv2.putText(frame, f'Error en x: {erx[0]} <=> {erx[1]}', (10, 20),font, .4, (15, 15, 15), 1, cv2.LINE_AA)
            cv2.putText(frame, f'Error en y: {erx[0]} <=> {erx[1]}', (10, 40),font, .4, (15, 15, 15), 1, cv2.LINE_AA)
        
        if previo < actual:
            previo = actual
                
            if previo == tDetect and cRango(x,erx) and cRango(y,ery):
                                
                val = Funciones.enviarColor(x,y,clascolor)
                
                while val:
                    val,c = Funciones.recibirConfirmacion()
                    if val == False:
                        Principal.GuardarCSV(Principal,c)
                        actualizar = True
                
                clasificar = False        
                #Fin del movimiento
                previo = 0
                #clasificar = False
                detectado = False
            elif previo < tDetect and cRango(x,erx)  and cRango(y,ery):
                print(f"Verificando: {tDetect - previo} -> {clascolor}")    
                
            elif previo < tDetect and cRango(x,erx) == False  and cRango(y,ery) == False:
                print(f"Termino, valor incial de contador => {previo}")
                previo = 0
                clasificar = False
                detectado = False
            else:
                previo = 0
                clasificar = False
        else:
            pass     
    else:
        pass

def capturar():
    global cap,clascolor,frame
    ret, frame = cap.read()
    if ret:
        frame = cv2.flip(frame, 1)
        
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        maskRed1 = cv2.inRange(frameHSV, rojo1[0], rojo1[1])
        maskRed2 = cv2.inRange(frameHSV,rojo2[0], rojo2[1])
        maskRed = cv2.add(maskRed1,maskRed2)
        
        maskAzul = cv2.inRange(frameHSV, azul[0], azul[1])
        maskGreen = cv2.inRange(frameHSV, verde[0], verde[1])
        
        if maskRed[maskRed >= 255].shape[0] > 10000:
            clascolor = "R"
            dibujar(maskRed1, colores["Rojo"])
        elif maskGreen[maskGreen >= 255].shape[0] > 10000:
            clascolor = "G"
            dibujar(maskGreen, colores["Verde"])
        elif maskAzul[maskAzul >= 255].shape[0] > 10000:
            dibujar(maskAzul,colores["Azul"])
            clascolor = "B"
           
    return ret,frame


def encender(cam):
    global cap
    cap = cv2.VideoCapture(cam)
    
def apagar():
    global cap
    cap.release()