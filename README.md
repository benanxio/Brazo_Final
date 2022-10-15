# Sistema de vision para un brazo robótico
Una interfaz de control desarrollada utilizando *Tkinter* y *[customTkinter][3]* para controlar un brazo robótico clasificador de objetos por colores con Arduino.
# Interfaz
![](Resources/Index.png)
| _`Index.py` Interfaz de control del brazo_

# Librería de listado de cámaras
Un inconveniete de trabajar con Python y **OpenCV** es que no se cuenta con una API para enumerar los dispositvos de captura de video, pero este inconveniente fue solucionado gracias al aporte de [yushulx][0] con su proyecto [python-capture-device-list][1]. 

## Environment   
* [Microsoft C++ Build Tools][2]
* Python 3.6 o superior
* requirements.txt

[0]:https://github.com/yushulx
[1]:https://github.com/yushulx/python-capture-device-list
[2]:https://visualstudio.microsoft.com/es/downloads/
[3]:https://github.com/TomSchimansky/CustomTkinter