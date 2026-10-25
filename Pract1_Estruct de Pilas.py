class Pila:

  def __init__(self, capacidad=8):
    self.capacidad = capacidad
    self.elementos = [None] * capacidad
    self.tope = 0  

  def insertar(self, item):
    if self.tope >= self.capacidad:
      print(
          f"Error! Desbordamiento (Overflow): No se puede insertar '{item}', la"
          " pila está llena."
      )
    else:
      self.tope += 1
      self.elementos[self.tope - 1] = item
      print(
          f"Insertar('{item}'): Pila = {self.elementos[:self.tope]}, TOPE ="
          f" {self.tope}"
      )

  def eliminar(self, nombre_var):
    if self.tope == 0:
      print(
          f"Error! Subdesbordamiento (Underflow): No se puede eliminar a"
          f" '{nombre_var}', la pila esta vacia."
      )
    else:
      item_eliminado = self.elementos[self.tope - 1]
      self.elementos[self.tope - 1] = None
      self.tope -= 1
      print(
          f"Eliminar('{nombre_var}') [Salio {item_eliminado}]: Pila ="
          f" {self.elementos[:self.tope]}, TOPE = {self.tope}"
      )


# --- Simulación del problema ---
print("=== INICIO DE LA SIMULACION DE LA PILA ===")
pila = Pila(capacidad=8)
print(f"Estado inicial -> Pila vacia, TOPE = {pila.tope}\n")

print("--- Operaciones ---")
pila.insertar("X")  
pila.insertar("Y")  
pila.eliminar("Z")  
pila.eliminar("T")  
pila.eliminar("U")  
pila.insertar("V")  
pila.insertar("W")  
pila.eliminar("p")  
pila.insertar("R")  

print("\n=== RESULTADO FINAL ===")
print(f"Elementos restantes en la pila: {pila.tope}")
print(f"Contenido final de la pila: {pila.elementos[:pila.tope]}")

"""
Preguntas:
¿Con cuántos elementos quedó la pila?
	R: Quedaron dos elementos en la pila

¿Hubo algún caso de error (desbordamiento o subdesbordamiento)? Si ocurrió algún error, explícalo.
	R: Si, hubo un error de subdesbordamiento, debido a que se intento eliminar tres elementos de la pila
	cuando solo habían dos elementos al momento de querer eliminar provocando ese fallo
"""
