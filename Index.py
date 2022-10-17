
from cgitb import text
from doctest import master
import tkinter
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import messagebox, ttk
import Funciones
import Vision
import sqlite3
import cv2
import os
from datetime import datetime


class Principal():
    
    def Conexion():
        #Creacion de bade de datos
        db = sqlite3.connect("Data.db")
        conn = db.cursor()
        #Creacion de la tabla
        conn.execute("CREATE TABLE IF NOT EXISTS Clasificacion (fecha DATETIME, Rojo INTEGER, Verde INTEGER, Azul INTEGER)")
        db.commit()
        
        return db,conn

    def GuardarCSV(self, color):
        
        db,conn = Principal.Conexion()
        
        now = datetime.now()
        fecha = now.strftime("%Y-%m-%d %H:%M:%S")
        
        data = [0, 0, 0]
        if color == "R":
            data[0] = 1
        if color == "G":
            data[1] = 1
        if color == "B":
            data[2] = 1

        conn.execute(f"INSERT INTO Clasificacion VALUES ('{fecha}',{data[0]},{data[1]},{data[2]})")
        db.commit()
        conn.close()
        
    def mostrarDatos():
        global treeview, label_R, label_G, label_B
        
        treeview.delete(*treeview.get_children())
        
        now = datetime.now()
        fecha = now.strftime("%Y-%m-%d")
        
        db,conn = Principal.Conexion()
        
        #Totales
        conn.execute(f"SELECT fecha, SUM (Rojo),SUM(Verde),SUM(Azul) FROM Clasificacion WHERE DATE(fecha)='{fecha}'")
        val = conn.fetchone()
        if val[0]!=None:
            label_R.configure(text=f"{val[1]}")
            label_G.configure(text=f"{val[2]}")
            label_B.configure(text=f"{val[3]}")
        
        #Consulta de datos totales
        conn.execute(f"SELECT * FROM Clasificacion WHERE DATE(fecha)='{fecha}'")
        valores = conn.fetchall()
        if len(valores)>0:
            for dato in reversed(valores):
                treeview.insert("", 'end', text=dato[0], values=(dato[1], dato[2], dato[3]))

        db.close()

    def App(self):
        global treeview, label_R, label_G, label_B, puertos, devices

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        ICONS_DIR = os.path.join(BASE_DIR, 'Resources')

        # Modes: "System" (standard), "Dark", "Light"
        ctk.set_appearance_mode("System")
        # Themes: "blue" (standard), "green", "dark-blue"
        ctk.set_default_color_theme("blue")
        app = ctk.CTk()
        app.resizable(0, 0)

        screen_width = app.winfo_screenwidth()
        screen_height = app.winfo_screenheight()

        window_height = 720
        window_width = 1280

        x_cordinate = (screen_width - window_width)//2
        y_cordinate = (screen_height - window_height)//4

        app.geometry(
            f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")
        app.iconbitmap(default=os.path.join(ICONS_DIR, "Blank.ico"))
        app.title("Brazo clasificador")

        def sizex(x):
            return int((x/100) * window_width)

        def sizey(y):
            return int((y/100) * window_height)

        def on_closing():

            if messagebox.askokcancel("Salir", "¿Esta seguro que quieres salir?"):
                try:
                    Vision.apagar()
                except:
                    pass
                try:
                    Funciones.desconectar()
                except:
                    pass
                app.destroy()

        # -----------------------------------------------------------------
        def cambiarRango(self):
            Vision.distancia = r.get() * 10
            lblDistancia.configure(text=f"Distancia: {r.get() * 10}")
            
        def encender():
            '''
            Enciende la cámara seleccionada
            '''
            if h.get() == 1:
                if len(devices) > 0:
                    switchcam.configure(text="Cámara: ON")
                    Vision.encender(devices[menuCam.get()])
                    messagebox.showinfo("Info", "Camara Encendida")
                    visualizar()
                else:
                    messagebox.showinfo("Info", "No hay opciones disponibles")

            else:
                switchcam.configure(text="Cámara: OFF")
                lblVideo.configure(image=camimg)
                lblVideo.image = camimg
                Vision.apagar()

        def visualizar():
            '''
            Recibe los fotogramas de video
            '''
            try:
                ret, frame = Vision.capturar()
                if ret:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    im = Image.fromarray(frame)
                    img = ImageTk.PhotoImage(image=im)
                    lblVideo.configure(image=img)
                    lblVideo.image = img
                    lblVideo.after(10, visualizar)
                    if Vision.actualizar:
                        Principal.mostrarDatos()
                        Vision.actualizar = False
                else:
                    lblVideo.place_forget()

            except:
                lblVideo.place_forget()

        def BuscarPuertos():
            global puertos
            puertos = Funciones.serial_ports()
            var = list(puertos.keys())
            menubtn.configure(values=var, require_redraw=True)
            if len(var) > 0:
                menubtn.set(var[0])
            else:
                menubtn.set("Seleccione un Puerto")

        def BuscarCamaras():
            global devices
            devices = Vision.listarCamaras()
            var = list(devices.keys())
            menuCam.configure(values=var, require_redraw=True)
            if len(var) > 0:
                menuCam.set(var[0])
            else:
                menuCam.set("Seleccione una Cámara")

        def Conexion():
            global puertos

            if Funciones.verificar():
                Funciones.desconectar()
                messagebox.showinfo("Info", "Desconectado")
                button_C.configure(
                    text="Conectar", fg_color="#ff2c24", hover_color="#08bc64")
            else:
                if len(puertos) > 0:
                    Funciones.conectar(puertos[menubtn.get()])
                    if Funciones.verificar():
                        messagebox.showinfo("Info", "Conexión exitosa")
                        button_C.configure(
                            text="Desconectar", fg_color="green", hover_color="red")
                    else:
                        messagebox.showerror(
                            "Error", "Hubo un problema con la conexión")
                else:
                    messagebox.showinfo("Info", "No hay opciones disponibles")

        h = tkinter.IntVar()
        h.set(0)
        r = tkinter.IntVar()
        r.set(750)

        reloadCamera_image = ImageTk.PhotoImage(Image.open(
            os.path.join(ICONS_DIR, "Reload_CAM.png")).resize((35, 25)))
        reload_image = ImageTk.PhotoImage(Image.open(
            os.path.join(ICONS_DIR, "Reload_COM.png")).resize((50, 25)))

        app.grid_columnconfigure(1, weight=1)
        app.grid_rowconfigure(0, weight=1)

        frameOptions = ctk.CTkFrame(
            master=app,  width=sizex(52), height=sizey(20))
        frameOptions.grid(row=0, column=0, sticky="nswe", padx=20, pady=20)

        frame_right = ctk.CTkFrame(master=app)
        frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        frame_camara = ctk.CTkFrame(master=app, width=sizex(52), height=sizey(72),
                                    corner_radius=0)
        frame_camara.grid(row=1, column=0, sticky="nswe", padx=20, pady=20)

        frame_option = ctk.CTkFrame(master=app)
        frame_option.grid(row=1, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frameOptions ============
        # configure grid layout (1x11)
        # empty row with minsize as spacing
        frameOptions.grid_rowconfigure(0, minsize=10)
        frameOptions.grid_rowconfigure(5, weight=1)  # empty row as spacing
        # empty row with minsize as spacing
        frameOptions.grid_rowconfigure(8, minsize=20)
        # empty row with minsize as spacing
        frameOptions.grid_rowconfigure(11, minsize=10)

        devices = {}
        menuCam = ctk.CTkOptionMenu(frameOptions, width=sizex(22))
        menuCam.place(x=sizex(3), y=sizey(3))
        BuscarCamaras()

        button_RC = ctk.CTkButton(master=frameOptions, image=reloadCamera_image, text="Buscar",
                                  compound="right", command=BuscarCamaras)
        button_RC.place(x=sizex(27), y=sizey(3), width=sizex(9))

        switchcam = ctk.CTkSwitch(master=frameOptions, text='Cámara: OFF',
                                  variable=h, offvalue=0, onvalue=1, command=encender)
        switchcam.place(x=sizex(38), y=sizey(4))

        puertos = {}
        menubtn = ctk.CTkOptionMenu(frameOptions, width=sizex(22))
        menubtn.place(x=sizex(3), y=sizey(10))
        BuscarPuertos()

        button_R = ctk.CTkButton(master=frameOptions, image=reload_image, text="Buscar",
                                 compound="right", command=BuscarPuertos)
        button_R.place(x=sizex(27), y=sizey(10), width=sizex(9))

        button_C = ctk.CTkButton(master=frameOptions,
                                 fg_color="#ff2c24",
                                 hover_color="#08bc64",
                                 text='Conectar', command=Conexion)
        button_C.place(x=sizex(38), y=sizey(10), width=sizex(9))
        
        rangoSlider = ctk.CTkSlider(master=frameOptions,from_=10,to=2000,progress_color='#206ca4',variable=r,command=cambiarRango)
        rangoSlider.place(x=sizex(2.5), y=sizey(16),width=sizex(34),height=sizey(3))
        
        lblDistancia = ctk.CTkLabel(master=frameOptions,text=f"Distancia: {r.get()}")
        lblDistancia.place(x=sizex(37), y=sizey(15))

        camimg = ImageTk.PhotoImage(Image.open(
            os.path.join(ICONS_DIR, "FondoCam.png")))
        lblVideo = ctk.CTkLabel(frame_camara, text="", image=camimg)
        lblVideo.pack(padx=sizex(0.7), pady=sizey(1))

        imgR = ImageTk.PhotoImage(Image.open(os.path.join(
            ICONS_DIR, "ImagenR.png")).resize((75, 100)))
        imgG = ImageTk.PhotoImage(Image.open(os.path.join(
            ICONS_DIR, "ImagenG.png")).resize((75, 100)))
        imgB = ImageTk.PhotoImage(Image.open(os.path.join(
            ICONS_DIR, "ImagenB.png")).resize((75, 100)))

        label_R = ctk.CTkLabel(
            master=frame_right, image=imgR, text="0", text_color="#ff2c24", compound="top")
        label_R.place(x=sizex(2), y=sizey(1))
        label_R.configure(font=("Cambria", 15))
        label_G = ctk.CTkLabel(
            master=frame_right, image=imgG, text="0", text_color="#08bc64", compound="top")
        label_G.place(x=sizex(15), y=sizey(1))
        label_G.configure(font=("Cambria", 15))
        label_B = ctk.CTkLabel(
            master=frame_right, image=imgB, text="0", text_color="#08ace4", compound="top")
        label_B.place(x=sizex(29), y=sizey(1))
        label_B.configure(font=("Cambria", 15))

        style = ttk.Style()
        style.configure("Treeview.Heading", font=(None, 15))
        style.theme_use("clam")
        style.configure("Treeview", font=("Cambria", 12), rowheight=25,
                        background="grey25", foreground="white", fieldbackground="grey25")

        treeview = ttk.Treeview(
            frame_option, selectmode="extended", columns=(1, 2, 3), height=18)
        treeview.place(x=sizex(1), y=sizey(1))

        treeview.column("#0", anchor='c', width=210)
        treeview.column(1, anchor='c', width=100)
        treeview.column(2, anchor='c', width=100)
        treeview.column(3, anchor='c', width=100)

        treeview.heading("#0", text="Fecha", anchor='center')
        treeview.heading(1, text="Rojo", anchor='center')
        treeview.heading(2, text="Verde", anchor='center')
        treeview.heading(3, text="Azul", anchor='center')

        cambiarRango(self)
        Principal.mostrarDatos()

        app.protocol("WM_DELETE_WINDOW", on_closing)
        app.mainloop()


if __name__ == "__main__":
    principal = Principal()
    principal.App()
