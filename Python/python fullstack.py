import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect("Fullstack_DB")
cursor = conn.cursor()

# Creación de las tablas
cursor.execute("""
CREATE TABLE IF NOT EXISTS Usuario (
    id_usuario INTEGER PRIMARY KEY,
    nombre_usuario TEXT,
    contraseña TEXT,
    email TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Administrador (
    id_administrador INTEGER PRIMARY KEY,
    nombre TEXT,
    contraseña TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Cliente (
    id_cliente INTEGER PRIMARY KEY,
    id_usuario INTEGER,
    contraseña TEXT,
    email TEXT,
    telefono TEXT,
    direccion TEXT,
    pais TEXT,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Carrito (
    id_carrito INTEGER PRIMARY KEY,
    id_usuario INTEGER,
    id_producto INTEGER,
    cantidad_producto INTEGER,
    precio_total REAL,
    fecha_agregado DATE,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Producto (
    id_producto INTEGER PRIMARY KEY,
    nombre TEXT,
    descripcion TEXT,
    precio REAL,
    stock INTEGER,
    imagen TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Invitado (
    id_invitado INTEGER PRIMARY KEY,
    registro TEXT
)
""")

conn.commit()
conn.close()

# Ahora definiremos las clases

class Usuario:
    def __init__(self, db_name="Fullstack_DB"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def registrarse(self, nombre_usuario, contraseña, email):
        try:
            # Verificar si el usuario ya existe
            self.cursor.execute("SELECT id_usuario FROM Usuario WHERE nombre_usuario = ?", (nombre_usuario,))
            usuario_existente = self.cursor.fetchone()

            if usuario_existente:
                return "El nombre de usuario ya está en uso."

            # Insertar nuevo usuario
            self.cursor.execute("INSERT INTO Usuario (nombre_usuario, contraseña, email) VALUES (?, ?, ?)",
                                (nombre_usuario, contraseña, email))
            self.conn.commit()
            return "Registro exitoso."

        except Exception as e:
            return str(e)

    def login(self, nombre_usuario, contraseña):
        try:
            # Verificar las credenciales de inicio de sesión
            self.cursor.execute("SELECT id_usuario FROM Usuario WHERE nombre_usuario = ? AND contraseña = ?",
                                (nombre_usuario, contraseña))
            usuario = self.cursor.fetchone()

            if usuario:
                return "Inicio de sesión exitoso."
            else:
                return "Credenciales incorrectas."

        except Exception as e:
            return str(e)

    def editar_perfil(self, id_usuario, nuevo_nombre, nueva_contraseña, nuevo_email):
        try:
            # Actualizar los datos del usuario
            self.cursor.execute("UPDATE Usuario SET nombre_usuario = ?, contraseña = ?, email = ? WHERE id_usuario = ?",
                                (nuevo_nombre, nueva_contraseña, nuevo_email, id_usuario))
            self.conn.commit()
            return "Perfil actualizado correctamente."

        except Exception as e:
            return str(e)

    def contraseña_olvidada(self, nombre_usuario, nuevo_contraseña):
        try:
            # Actualizar la contraseña del usuario
            self.cursor.execute("UPDATE Usuario SET contraseña = ? WHERE nombre_usuario = ?",
                                (nuevo_contraseña, nombre_usuario))
            self.conn.commit()
            return "Contraseña actualizada correctamente."

        except Exception as e:
            return str(e)

    def cerrar_conexion(self):
        self.conn.close()

class Administrador(Usuario):
    def __init__(self, db_name="Fullstack_DB"):
        super().__init__(db_name)

    def ver_productos(self):
        try:
            # Consultar la lista de productos
            self.cursor.execute("SELECT * FROM Producto")
            productos = self.cursor.fetchall()
            return productos

        except Exception as e:
            return str(e)

    def agregar_producto(self, nombre, descripcion, precio, stock, imagen):
        try:
            # Insertar un nuevo producto
            self.cursor.execute("INSERT INTO Producto (nombre, descripcion, precio, stock, imagen) VALUES (?, ?, ?, ?, ?)",
                                (nombre, descripcion, precio, stock, imagen))
            self.conn.commit()
            return "Producto agregado correctamente."

        except Exception as e:
            return str(e)

    def eliminar_producto(self, id_producto):
        try:
            # Eliminar un producto por su ID
            self.cursor.execute("DELETE FROM Producto WHERE id_producto = ?", (id_producto,))
            self.conn.commit()
            return "Producto eliminado correctamente."

        except Exception as e:
            return str(e)

    def modificar_producto(self, id_producto, nuevo_nombre, nueva_descripcion, nuevo_precio, nuevo_stock, nueva_imagen):
        try:
            # Modificar los datos de un producto
            self.cursor.execute("UPDATE Producto SET nombre = ?, descripcion = ?, precio = ?, stock = ?, imagen = ? WHERE id_producto = ?",
                                (nuevo_nombre, nueva_descripcion, nuevo_precio, nuevo_stock, nueva_imagen, id_producto))
            self.conn.commit()
            return "Producto modificado correctamente."

        except Exception as e:
            return str(e)

class Cliente(Usuario):
    def __init__(self, db_name="Fullstack_DB"):
        super().__init__(db_name)

    def comprar_producto(self, id_producto, cantidad):
        try:
            # Verificar si el producto existe y tiene suficiente stock
            self.cursor.execute("SELECT nombre, stock, precio FROM Producto WHERE id_producto = ?", (id_producto,))
            producto = self.cursor.fetchone()

            if not producto:
                return "El producto no existe."

            nombre_producto, stock_producto, precio_producto = producto

            if stock_producto < cantidad:
                return "No hay suficiente stock disponible para este producto."

            # Calcular el precio total de la compra
            precio_total = precio_producto * cantidad

            # Registrar la compra en la tabla Carrito
            self.cursor.execute("INSERT INTO Carrito (id_usuario, id_producto, cantidad_producto, precio_total, fecha_agregado) "
                                "VALUES (?, ?, ?, ?, date('now'))",
                                (self.id_usuario, id_producto, cantidad, precio_total))
            self.conn.commit()

            # Actualizar el stock del producto
            self.cursor.execute("UPDATE Producto SET stock = stock - ? WHERE id_producto = ?", (cantidad, id_producto))
            self.conn.commit()

            return f"Compra de {cantidad} {nombre_producto}(s) realizada con éxito. Precio total: ${precio_total}"

        except Exception as e:
            return str(e)

    def ver_producto(self, id_producto):
        try:
            # Consultar los detalles de un producto por su ID
            self.cursor.execute("SELECT * FROM Producto WHERE id_producto = ?", (id_producto,))
            producto = self.cursor.fetchone()
            return producto

        except Exception as e:
            return str(e)

    def añadir_al_carrito(self, id_producto, cantidad):
        try:
            # Verificar si el producto existe y tiene suficiente stock
            self.cursor.execute("SELECT nombre, stock, precio FROM Producto WHERE id_producto = ?", (id_producto,))
            producto = self.cursor.fetchone()

            if not producto:
                return "El producto no existe."

            nombre_producto, stock_producto, precio_producto = producto

            if stock_producto < cantidad:
                return "No hay suficiente stock disponible para este producto."

            # Calcular el precio total de los productos a añadir al carrito
            precio_total = precio_producto * cantidad

            # Verificar si ya hay un carrito activo para el usuario
            self.cursor.execute("SELECT id_carrito FROM Carrito WHERE id_usuario = ? AND fecha_agregado IS NULL", (self.id_usuario,))
            carrito_existente = self.cursor.fetchone()

            if carrito_existente:
                id_carrito = carrito_existente[0]
                # Verificar si el producto ya está en el carrito y actualizar la cantidad
                self.cursor.execute("SELECT id_carrito FROM Carrito WHERE id_carrito = ? AND id_producto = ?",
                                    (id_carrito, id_producto))
                producto_en_carrito = self.cursor.fetchone()
                if producto_en_carrito:
                    # El producto ya está en el carrito, actualizar la cantidad
                    self.cursor.execute("UPDATE Carrito SET cantidad_producto = cantidad_producto + ? WHERE id_carrito = ? AND id_producto = ?",
                                        (cantidad, id_carrito, id_producto))
                else:
                    # El producto no está en el carrito, agregarlo
                    self.cursor.execute("INSERT INTO Carrito (id_usuario, id_producto, cantidad_producto, precio_total, fecha_agregado) "
                                        "VALUES (?, ?, ?, ?, NULL)",
                                        (self.id_usuario, id_producto, cantidad, precio_total))
            else:
                # Crear un nuevo carrito
                self.cursor.execute("INSERT INTO Carrito (id_usuario, id_producto, cantidad_producto, precio_total, fecha_agregado) "
                                    "VALUES (?, ?, ?, ?, NULL)",
                                    (self.id_usuario, id_producto, cantidad, precio_total))

            self.conn.commit()
            return f"{cantidad} {nombre_producto}(s) añadidos al carrito. Precio total en el carrito: ${precio_total}"

        except Exception as e:
            return str(e)

    def borrar_del_carrito(self, id_producto):
        try:
            # Verificar si el producto está en el carrito
            self.cursor.execute("SELECT id_carrito FROM Carrito WHERE id_usuario = ? AND id_producto = ? AND fecha_agregado IS NULL",
                                (self.id_usuario, id_producto))
            carrito_existente = self.cursor.fetchone()

            if carrito_existente:
                id_carrito = carrito_existente[0]
                # Eliminar el producto del carrito
                self.cursor.execute("DELETE FROM Carrito WHERE id_carrito = ? AND id_producto = ?", (id_carrito, id_producto))
                self.conn.commit()
                return "Producto eliminado del carrito."
            else:
                return "El producto no está en el carrito."

        except Exception as e:
            return str(e)

    def hacer_pago(self):
        try:
            # Calcular el precio total del carrito
            self.cursor.execute("SELECT SUM(precio_total) FROM Carrito WHERE id_usuario = ? AND fecha_agregado IS NULL", (self.id_usuario,))
            precio_total = self.cursor.fetchone()[0]

            if precio_total:
                # Registrar el pago (simulado) y vaciar el carrito
                self.cursor.execute("UPDATE Carrito SET fecha_agregado = date('now') WHERE id_usuario = ? AND fecha_agregado IS NULL", (self.id_usuario,))
                self.conn.commit()
                return f"Pago realizado con éxito. Total a pagar: ${precio_total}"
            else:
                return "No hay productos en el carrito."

        except Exception as e:
            return str(e)

# Clase para la gestión del carrito
class Carrito:
    def __init__(self, db_name="Fullstack_DB"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def ver_carrito(self, id_usuario):
        try:
            # Consultar los productos en el carrito del usuario
            self.cursor.execute("SELECT C.id_carrito, P.nombre, C.cantidad_producto, C.precio_total FROM Carrito AS C "
                                "INNER JOIN Producto AS P ON C.id_producto = P.id_producto "
                                "WHERE C.id_usuario = ? AND C.fecha_agregado IS NULL", (id_usuario,))
            carrito = self.cursor.fetchall()
            return carrito

        except Exception as e:
            return str(e)

    def cerrar_conexion(self):
        self.conn.close()


