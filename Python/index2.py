from tkinter import ttk
from tkinter import *
from tkinter import messagebox

import sqlite3

class Producto:

    db_name = 'BaseDatos.db'

    def __init__(self, window):
        self.wind = window
        self.wind.title('Registro de Productos')

        # Crear un contenedor
        frame = LabelFrame(self.wind, text='Registro de Producto')
        frame.grid(row=0, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")

        # Ingresar nombre
        Label(frame, text='Nombre').grid(row=2, column=0, sticky="w")
        self.Nombre = Entry(frame)
        self.Nombre.grid(row=2, column=1, sticky="w")

        # Ingresar Precio
        Label(frame, text='Precio').grid(row=3, column=0, sticky="w")
        self.Precio = Entry(frame)
        self.Precio.grid(row=3, column=1, sticky="w")

        # Crear botones para guardar, eliminar y actualizar
        ttk.Button(frame, text='Guardar Producto', command=self.agregar_producto).grid(row=4, columnspan=2, sticky="w")
        ttk.Button(frame, text='Eliminar Producto', command=self.eliminar_producto).grid(row=5, column=0, sticky="w")
        ttk.Button(frame, text='Actualizar Producto', command=self.confirmar_actualizar_producto).grid(row=5, column=1, sticky="w")

        # Crear una tabla
        self.tree = ttk.Treeview(height=10, columns=2)
        self.tree.grid(row=6, column=0, columnspan=2, sticky="nsew")
        self.tree.heading('#0', text='Nombre', anchor=CENTER)
        self.tree.heading('#1', text='Precio', anchor=CENTER)

        # Configurar expansión automática de columnas y filas
        self.wind.grid_columnconfigure(0, weight=1)
        self.wind.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(6, weight=1)

        self.get_Productos()

    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def get_Productos(self):
        # Limpiar la tabla
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        # Consultar la tabla
        query = 'SELECT * FROM Productos ORDER BY Nombre DESC'
        db_rows = self.run_query(query)

        # Rellenar los datos
        for row in db_rows:
            self.tree.insert('', 'end', text=row[1], values=(row[2]))

    def validacion(self):
        return len(self.Nombre.get()) != 0 and len(self.Precio.get()) != 0

    def agregar_producto(self):
        if self.validacion():
            query = 'INSERT INTO Productos VALUES(NULL, ?, ?)'
            parameters = (self.Nombre.get(), self.Precio.get())
            self.run_query(query, parameters)
            self.get_Productos()
            self.Nombre.delete(0, END)
            self.Precio.delete(0, END)
        else:
            print('Nombre y precio requeridos')

    def eliminar_producto(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_text = self.tree.item(selected_item)['text']

            # Mostrar cuadro de diálogo de confirmación
            confirmacion = messagebox.askyesno("Confirmar eliminación", f"¿Está seguro de que desea eliminar el producto '{item_text}'?")

            if confirmacion:
                query = 'DELETE FROM Productos WHERE Nombre = ?'
                self.run_query(query, (item_text,))
                self.get_Productos()
        else:
            messagebox.showerror('Error', 'Seleccione un producto para eliminar')

    def confirmar_actualizar_producto(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_text = self.tree.item(selected_item)['text']
            new_price = self.Precio.get()
            new_name = self.Nombre.get()

            # Mostrar cuadro de diálogo de confirmación
            confirmacion = messagebox.askyesno("Confirmar actualización", f"¿Está seguro de que desea actualizar el precio del producto '{item_text}'?")

            if confirmacion:
                query = 'UPDATE Productos SET Precio = ? WHERE Nombre = ?'
                self.run_query(query, (new_price, item_text,new_name))
                self.get_Productos()
        else:
            print('Seleccione un producto para actualizar')

if __name__ == '__main__':
    window = Tk()
    application = Producto(window)
    window.mainloop()
