import tkinter as tk
from tkinter import ttk
import serial
import time
import serial.tools.list_ports
from ttkthemes import ThemedTk

ventana = ThemedTk(theme="adapta")
ventana.geometry("350x400")
ventana.title("Control de LED")

# Crear notebook
pestañas = ttk.Notebook(ventana)

# Crear las pestañas
p1 = ttk.Frame(pestañas)
p2 = ttk.Frame(pestañas)
p3 = ttk.Frame(pestañas)

# Agregar las pestañas
pestañas.add(p1, text='SETUP')
pestañas.add(p2, text='MENÚ')
pestañas.add(p3, text='AUTORES')

# Configuración del puerto serie
arduino = None  # Inicializar como None

def listar_puertos():
    """Lista los puertos COM disponibles."""
    puertos = serial.tools.list_ports.comports()
    return [port.device for port in puertos]

def conectar():
    global arduino
    port = COM_var.get()
    baudrate = int(COM_vel.get())
    try:
        arduino = serial.Serial(port, baudrate, timeout=.1)
        time.sleep(2)  # Espera a que se establezca la conexión
        consultar_estado()  # Consultar el estado al conectar
        ESTADO_LED.config(text="Conectado", foreground="green")
    except serial.SerialException as e:
        ESTADO_LED.config(text=f"Error: {str(e)}", foreground="red")
        arduino = None  # Asegurarse de que arduino sea None si hay un error

def LED_encendido(pwm_value=None):
    if arduino:
        if pwm_value is not None:
            arduino.write(f'{pwm_value}\n'.encode())  # Enviar valor PWM
        else:
            arduino.write(b'1\n')  # Enviar comando para encender el LED
        time.sleep(0.2)  # Pausa breve para evitar comandos rápidos
        consultar_estado()  # Actualiza el estado del LED en la GUI

def LED_apagado():
    if arduino:
        arduino.write(b'0\n')  # Enviar comando para apagar el LED
        time.sleep(0.2)  # Pausa breve para evitar comandos rápidos
        consultar_estado()  # Actualiza el estado del LED en la GUI

def VALOR_PWM():
    if arduino:
        spin = valor_PWM.get()
        try:
            pwm_value = int(spin)
            if 0 <= pwm_value <= 255:
                LED_encendido(pwm_value)  # Enciende el LED con el valor de PWM
        except ValueError:
            print("Valor no válido")

def consultar_estado():
    """Consulta el estado actual del LED en el Arduino"""
    if arduino:
        arduino.write(b'?')  # Envía un comando para consultar el estado actual
        time.sleep(0.1)
        response = arduino.readline().decode('utf-8').strip()
        if "ENCENDIDO" in response:
            ESTADO_LED.config(text="ENCENDIDO", foreground="green")
        elif "APAGADO" in response:
            ESTADO_LED.config(text="APAGADO", foreground="red")
    else:
        ESTADO_LED.config(text="ESTADO DESCONOCIDO")

# PESTAÑA SETUP

# OptionMenu para elegir puerto
etiqueta_puerto = ttk.Label(p1, text="Elige el puerto")
etiqueta_puerto.pack()
COM_var = tk.StringVar(p1)
COM_lista = ttk.OptionMenu(p1, COM_var, *listar_puertos())  # Lista de puertos
COM_lista.pack()

# Combobox para elegir velocidad del puerto
etiqueta_vel = ttk.Label(p1, text="Elige la velocidad del puerto")
etiqueta_vel.pack()

velocidades = [9600, 19200, 38400, 115200]
COM_vel = ttk.Combobox(p1, state="readonly", values=velocidades)
COM_vel.current(3)  # Velocidad por defecto (115200)
COM_vel.pack()

# Botón para conectar
boton_conectar = ttk.Button(p1, text="Conectar", command=conectar)
boton_conectar.pack(pady=10)

# Botones para encender y apagar el LED
B_encendido = ttk.Button(p1, text="ENCENDER LED", command=lambda: LED_encendido(255))  # Enciende a brillo máximo
B_encendido.place(x=30, y=250)

B_apagado = ttk.Button(p1, text="APAGAR LED", command=LED_apagado)
B_apagado.place(x=200, y=250)

ETIQUETA_ESTADO = ttk.Label(p1, text="ESTADO DEL LED: ")
ETIQUETA_ESTADO.place(x=60, y=310)

ESTADO_LED = ttk.Label(p1)
ESTADO_LED.place(x=190, y=310)

# PESTAÑA MENÚ (p2)

def ajustar_resistencia():
    """Ajusta el PWM en función de la resistencia seleccionada."""
    resistencia = resistencia_var.get()
    pwm_value = 0
    if resistencia == "100 Ohms":
        pwm_value = 255
    elif resistencia == "200 Ohms":
        pwm_value = 150
    elif resistencia == "300 Ohms":
        pwm_value = 50
    LED_encendido(pwm_value)  # Ajusta el PWM en función de la resistencia seleccionada

# Crear las opciones de selección
modo_var = tk.StringVar(value="PWM")  # Variable para el modo seleccionado (PWM o Resistencia)

# Radiobutton para seleccionar modo de control
modo_pwm = ttk.Radiobutton(p2, text="Controlar con PWM", variable=modo_var, value="PWM")
modo_resistencia = ttk.Radiobutton(p2, text="Controlar con Resistencia", variable=modo_var, value="Resistencia")
modo_pwm.pack()
modo_resistencia.pack()

# Sección para control con PWM
etiqueta_PWM = ttk.Label(p2, text="Intensidad del LED (PWM)", state="normal")
etiqueta_PWM.pack()

valor_PWM = ttk.Spinbox(p2, from_=0, to=255, increment=1, state="normal")  # Ajustar el rango de 0 a 255
valor_PWM.pack()

# Botón para ajustar el brillo del LED con PWM
boton_intensidad = ttk.Button(p2, text="Ajustar Brillo", command=VALOR_PWM, state="normal")
boton_intensidad.pack(pady=10)

# Sección para control con resistencia
etiqueta_resistencia = ttk.Label(p2, text="Seleccionar Resistencia", state="disabled")
etiqueta_resistencia.pack()

resistencia_var = tk.StringVar()
opciones_resistencia = ["100 Ohms", "200 Ohms", "300 Ohms"]
menu_resistencia = ttk.Combobox(p2, state="disabled", values=opciones_resistencia, textvariable=resistencia_var)
menu_resistencia.pack()

# Botón para ajustar el brillo del LED con Resistencia
boton_resistencia = ttk.Button(p2, text="Ajustar con Resistencia", command=ajustar_resistencia, state="disabled")
boton_resistencia.pack(pady=10)

# Función para habilitar/deshabilitar las opciones según el modo seleccionado
def actualizar_modo():
    if modo_var.get() == "PWM":
        etiqueta_PWM.config(state="normal")
        valor_PWM.config(state="normal")
        boton_intensidad.config(state="normal")
        etiqueta_resistencia.config(state="disabled")
        menu_resistencia.config(state="disabled")
        boton_resistencia.config(state="disabled")
    else:
        etiqueta_PWM.config(state="disabled")
        valor_PWM.config(state="disabled")
        boton_intensidad.config(state="disabled")
        etiqueta_resistencia.config(state="normal")
        menu_resistencia.config(state="normal")
        boton_resistencia.config(state="normal")

# Llama a actualizar_modo() cuando cambia el modo seleccionado
modo_var.trace("w", lambda *args: actualizar_modo())

# Llama a actualizar_modo para ajustar el estado inicial
actualizar_modo()

# PESTAÑA AUTORES
etiqueta_nombre = ttk.Label(p3, text="Ojeda Murillo Manuel Alejandro", font=("Arial", 14))
etiqueta_nombre.pack(pady=10)
etiqueta_matricula = ttk.Label(p3, text="202151013", font=("Arial", 14))
etiqueta_matricula.pack(pady=10)
etiqueta_nombre2 = ttk.Label(p3, text="Troncoso López Cristof Emmanuel", font=("Arial", 14))
etiqueta_nombre2.pack(pady=10)
etiqueta_matricula2 = ttk.Label(p3, text="202163496", font=("Arial", 14))
etiqueta_matricula2.pack(pady=10)
etiqueta_nombre3 = ttk.Label(p3, text="Uribe Velázquez Emmanuel", font=("Arial", 14))
etiqueta_nombre3.pack(pady=10)
etiqueta_matricula3 = ttk.Label(p3, text="202163715", font=("Arial", 14))
etiqueta_matricula3.pack(pady=10)
consultar_estado()
# Empaquetar el contenedor de pestañas
pestañas.pack(expand=1, fill='both')

ventana.mainloop()
