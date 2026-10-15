import tkinter as tk
from tkinter import messagebox

class PilaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Pila (Stack)")
        self.root.geometry("400x500")
        self.root.config(bg="#f0f2f5")

        self.pila = []
        self.max_elementos = 6 # Límite visual para que no desborde la ventana

        # Título
        titulo = tk.Label(root, text="Estructura de Datos: Pila (LIFO)", font=("Arial", 14, "bold"), bg="#f0f2f5", fg="#333")
        titulo.pack(pady=15)

        # Entrada de texto para nuevos elementos
        self.entry_valor = tk.Entry(root, font=("Arial", 12), justify="center")
        self.entry_valor.pack(pady=5)
        self.entry_valor.focus()
        self.entry_valor.bind("<Return>", lambda event: self.push()) # Permitir Enter

        # Botones de acción
        frame_botones = tk.Frame(root, bg="#f0f2f5")
        frame_botones.pack(pady=10)

        btn_push = tk.Button(frame_botones, text="Push (Apilar)", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), width=12, command=self.push)
        btn_push.grid(row=0, column=0, padx=5)

        btn_pop = tk.Button(frame_botones, text="Pop (Desapilar)", bg="#f44336", fg="white", font=("Arial", 10, "bold"), width=12, command=self.pop)
        btn_pop.grid(row=0, column=1, padx=5)

        # Contenedor gráfico de la Pila (Canvas)
        self.canvas = tk.Canvas(root, width=220, height=280, bg="white", highlightthickness=2, highlightbackground="#ccc")
        self.canvas.pack(pady=10)

    def push(self):
        valor = self.entry_valor.get().strip()
        if not valor:
            messagebox.showwarning("Advertencia", "Ingresa un valor para la pila.")
            return
        
        if len(self.pila) >= self.max_elementos:
            messagebox.showerror("Error", "¡La pila está llena (Overflow)! Saca elementos antes de meter más.")
            return

        self.pila.append(valor)
        self.entry_valor.delete(0, tk.END)
        self.actualizar_dibujo()

    def pop(self):
        if not self.pila:
            messagebox.showerror("Error", "¡La pila está vacía (Underflow)! No hay nada que desapilar.")
            return

        self.pila.pop()
        self.actualizar_dibujo()

    def actualizar_dibujo(self):
        self.canvas.delete("all")
        
        # Dibujar la estructura abierta por arriba (forma de U invertida o caja sin tapa)
        # Base y paredes laterales
        self.canvas.create_line(60, 20, 60, 260, width=4, fill="#333") # Pared izquierda
        self.canvas.create_line(160, 20, 160, 260, width=4, fill="#333") # Pared derecha
        self.canvas.create_line(60, 260, 160, 260, width=4, fill="#333") # Base

        # Dibujar los elementos de la pila desde abajo hacia arriba
        y_inicial = 240
        altura_caja = 35
        espacio = 5

        for i, elemento in enumerate(self.pila):
            y1 = y_inicial - (i * (altura_caja + espacio))
            y0 = y1 - altura_caja
            
            # Si es el último elemento (el tope), pintarlo de un color diferente para destacarlo
            color = "#2196F3" if i == len(self.pila) - 1 else "#90CAF9"

            # Dibujar caja del elemento
            self.canvas.create_rectangle(65, y0, 155, y1, fill=color, outline="#0d47a1", width=2)
            # Texto dentro de la caja
            self.canvas.create_text(110, (y0 + y1) / 2, text=elemento, font=("Arial", 11, "bold"), fill="white")

        # Indicador de la cima (TOP) si hay elementos
        if self.pila:
            top_y = y_inicial - ((len(self.pila) - 1) * (altura_caja + espacio)) - (altura_caja / 2)
            self.canvas.create_text(30, top_y, text="TOP", font=("Arial", 9, "bold"), fill="#f44336")
            self.canvas.create_line(45, top_y, 60, top_y, arrow=tk.LAST, fill="#f44336", width=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = PilaApp(root)
    root.mainloop()