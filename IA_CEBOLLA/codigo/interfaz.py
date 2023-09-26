import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import time
from generador_imagenes import main_generar

imagen_actual = None
generating_event = threading.Event()

def generar():
    global imagen_actual
    
    # Obtener el dato seleccionado en el menú de Tiempo
    dato_tiempo = menu_desplegable_tiempo.get()
    # Obtener el dato seleccionado en el menú de Terreno
    dato_terreno = menu_desplegable_terreno.get()
    
    # Deshabilitar el botón mientras se genera la imagen
    boton.config(state="disabled")
    
    # Mostrar una barra de progreso
    progreso = ttk.Progressbar(panel_inferior, mode="indeterminate")
    progreso.pack(fill=tk.BOTH, expand=False)
    progreso.start()
    
    # Función para generar la imagen en segundo plano
    def generar_imagen():
        imagen_generada = main_generar(dato_terreno, dato_tiempo)
        
        # Redimensionar la imagen para que tenga un tamaño deseado
        nuevo_ancho = 500  # Cambia el ancho deseado
        nuevo_alto = 400   # Cambia el alto deseado
        imagen_generada = imagen_generada.resize((nuevo_ancho, nuevo_alto), Image.ANTIALIAS)
        
        # Convertir la imagen PIL a una imagen Tkinter PhotoImage
        imagen_generada_tk = ImageTk.PhotoImage(imagen_generada)
        
        # Actualizar la imagen en el panel inferior
        ventana.after(0, lambda: actualizar_imagen(imagen_generada_tk))
        
        # Habilitar el botón nuevamente
        boton.config(state="normal")
        
        # Detener y ocultar la barra de progreso
        progreso.stop()
        progreso.pack_forget()
        
        # Indicar que la generación ha terminado
        generating_event.clear()
    
    def actualizar_imagen(imagen_tk):
        global imagen_actual
        if imagen_actual:
            imagen_actual.destroy()  # Elimina la imagen anterior si existe
        
        imagen_actual = tk.Label(panel_inferior, image=imagen_tk)
        imagen_actual.photo = imagen_tk  # Evita que la imagen sea eliminada por el recolector de basura
        imagen_actual.pack(fill=tk.BOTH, expand=False)
    
    # Verificar si la generación ya está en progreso
    if not generating_event.is_set():
        # Crear un hilo para generar la imagen en segundo plano
        hilo_generar = threading.Thread(target=generar_imagen)
        hilo_generar.start()
        
        # Indicar que la generación está en progreso
        generating_event.set()

# Crear una instancia de la ventana
ventana = tk.Tk()
ventana.title("Scallion IA")
ancho_ventana = 500
alto_ventana = 700
ventana.configure(bg="#49D975")
ventana.minsize(ancho_ventana, alto_ventana)
ventana.resizable(width=False, height=False)
ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla = ventana.winfo_screenheight()
x_pos = int((ancho_pantalla/2) - (ancho_ventana/2))
y_pos = int((alto_pantalla/2) - (alto_ventana/2))
ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x_pos}+{y_pos}")

# Panel superior
panel_superior = tk.Frame(ventana, bg="#49D975")
panel_superior.pack(fill=tk.BOTH, expand=False)  # No expandir el panel superior

# Cargar una imagen y redimensionarla
imagen_original = Image.open("archivos/logo_scallion.png")
ancho_deseado = 120  # Cambia el ancho deseado de la imagen
alto_deseado = 40  # Cambia el alto deseado de la imagen
imagen_redimensionada = imagen_original.resize((ancho_deseado, alto_deseado), Image.ANTIALIAS)
imagen = ImageTk.PhotoImage(imagen_redimensionada)

# Mostrar la imagen en un Label
label_imagen = tk.Label(panel_superior, image=imagen, bg="#49D975")
label_imagen.photo = imagen  # Evita que la imagen sea eliminada por el recolector de basura
label_imagen.pack(pady=20)

# Texto arriba del primer menú desplegable (Tiempo)
label_texto_input_clima = tk.Label(panel_superior, text="Seleccione los meses que han pasado desde su cultivo:", bg="#49D975")
label_texto_input_clima.pack(pady=5)

# Menú desplegable Tiempo
opciones_tiempo = ["1", "2", "3", "4", "5", "6"]
menu_desplegable_tiempo = ttk.Combobox(panel_superior, values=opciones_tiempo, state="readonly")
menu_desplegable_tiempo.pack(padx=10, pady=5)

# Texto arriba del segundo menú desplegable (Terreno)
label_texto_input_terreno = tk.Label(panel_superior, text="Seleccione el tipo de terreno:", bg="#49D975")
label_texto_input_terreno.pack(pady=5)

# Menú desplegable Terreno
opciones_terreno = ["seco", "húmedo", "rocoso", "arenoso"]
menu_desplegable_terreno = ttk.Combobox(panel_superior, values=opciones_terreno, state="readonly")
menu_desplegable_terreno.pack(padx=10, pady=5)

# Botón
boton = tk.Button(panel_superior, text="Generar", bg="#49D975", command=generar)
boton.pack(pady=10)

# Espaciado entre los paneles
espaciado = tk.Frame(ventana, height=2, bg="black")
espaciado.pack(fill=tk.BOTH, expand=False)

# Panel inferior
panel_inferior = tk.Frame(ventana, bg="#76F19C")
panel_inferior.pack(fill=tk.BOTH, expand=True)  # Expandir el panel inferior para llenar el espacio

ventana.mainloop()
