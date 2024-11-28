import pandas as pd
from datetime import datetime

# Inicialización de tablas
tabla_miembros = pd.DataFrame(columns=["ID_Usuario", "Nombre", "Apellido", "Número de Documento", "Fecha de Nacimiento", "Teléfono", "Domicilio"])
tabla_pagos = pd.DataFrame(columns=["ID_Pago", "ID_Usuario", "Monto", "Fecha"])

def guardar_tablas():
    """Guarda las tablas en archivos CSV."""
    tabla_miembros.to_csv("tabla_miembros.csv", index=False)
    tabla_pagos.to_csv("tabla_pagos.csv", index=False)
    print("Tablas guardadas exitosamente.")

def cargar_tablas():
    """Carga las tablas desde archivos CSV, si existen."""
    global tabla_miembros, tabla_pagos
    try:
        tabla_miembros = pd.read_csv("tabla_miembros.csv")
        tabla_pagos = pd.read_csv("tabla_pagos.csv")
        print("Tablas cargadas exitosamente.")
    except FileNotFoundError:
        print("No se encontraron archivos de tablas. Se iniciará con tablas vacías.")

def validar_fecha(fecha):
    """Valida si una fecha tiene formato válido (YYYY-MM-DD)."""
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def es_numero_entero(valor):
    """Verifica si el valor es un número entero."""
    return valor.isdigit()

def es_mayor_de_edad(fecha_nacimiento):
    """Verifica si alguien es mayor de 18 años basado en la fecha de nacimiento."""
    fecha_nac = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
    hoy = datetime.now()
    edad = hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
    return edad >= 18

def es_nombre_valido(nombre):
    """Valida que el nombre o apellido contenga solo letras."""
    return nombre.isalpha()

def agregar_miembro():
    global tabla_miembros
    print("\n--- Agregar nuevo miembro ---")
    
    # Validar ID único
    id_usuario = input("ID de Usuario: ")
    while not es_numero_entero(id_usuario) or id_usuario in tabla_miembros["ID_Usuario"].astype(str).tolist():
        if not es_numero_entero(id_usuario):
            print("Error: El ID debe ser un número entero. Intenta de nuevo.")
        else:
            print("Error: El ID ya existe. Ingresa un ID único.")
        id_usuario = input("ID de Usuario: ")

    # Validar Nombre
    nombre = input("Nombre: ")
    while not es_nombre_valido(nombre):
        print("Error: El nombre debe contener solo letras. Intenta de nuevo.")
        nombre = input("Nombre: ")

    # Validar Apellido
    apellido = input("Apellido: ")
    while not es_nombre_valido(apellido):
        print("Error: El apellido debe contener solo letras. Intenta de nuevo.")
        apellido = input("Apellido: ")
    
    # Validar número de documento
    numero_documento = input("Número de documento: ")
    while not es_numero_entero(numero_documento):
        print("Error: El número de documento debe contener solo dígitos. Intenta de nuevo.")
        numero_documento = input("Número de documento: ")

    # Validar fecha de nacimiento
    fecha_nacimiento = input("Fecha de nacimiento (YYYY-MM-DD): ")
    while not validar_fecha(fecha_nacimiento):
        print("Error: Formato de fecha inválido. Intenta de nuevo.")
        fecha_nacimiento = input("Fecha de nacimiento (YYYY-MM-DD): ")
    while not es_mayor_de_edad(fecha_nacimiento):
        print("Error: Debes tener al menos 18 años para registrarte.")
        fecha_nacimiento = input("Fecha de nacimiento (YYYY-MM-DD): ")

    telefono = input("Teléfono: ")
    while not es_numero_entero(telefono):
        print("Error: El número de teléfono debe contener solo dígitos. Intenta de nuevo.")
        telefono = input("Teléfono: ")

    domicilio = input("Domicilio: ")

    # Agregar datos a la tabla
    tabla_miembros = pd.concat([tabla_miembros, pd.DataFrame([{
        "ID_Usuario": id_usuario,
        "Nombre": nombre,
        "Apellido": apellido,
        "Número de Documento": numero_documento,
        "Fecha de Nacimiento": fecha_nacimiento,
        "Teléfono": telefono,
        "Domicilio": domicilio
    }])], ignore_index=True)
    print("Miembro agregado exitosamente.")

def agregar_pago():
    global tabla_pagos, tabla_miembros
    print("\n--- Agregar nuevo pago ---")
    
    id_pago = input("ID del pago: ")
    while id_pago in tabla_pagos["ID_Pago"].astype(str).tolist():
        print("Error: El ID de pago ya existe. Ingresa un ID único.")
        id_pago = input("ID del pago: ")

    id_usuario = input("ID de Usuario: ")
    while id_usuario not in tabla_miembros["ID_Usuario"].astype(str).tolist():
        print("Error: El ID de usuario no existe. Intenta de nuevo.")
        id_usuario = input("ID de Usuario: ")

    monto = input("Monto: ")
    while not monto.replace('.', '', 1).isdigit():
        print("Error: El monto debe ser un valor numérico. Intenta de nuevo.")
        monto = input("Monto: ")

    fecha = input("Fecha (YYYY-MM-DD): ")
    while not validar_fecha(fecha):
        print("Error: Formato de fecha inválido. Intenta de nuevo.")
        fecha = input("Fecha (YYYY-MM-DD): ")

    tabla_pagos = pd.concat([tabla_pagos, pd.DataFrame([{
        "ID_Pago": id_pago,
        "ID_Usuario": id_usuario,
        "Monto": float(monto),
        "Fecha": fecha
    }])], ignore_index=True)
    print("Pago agregado exitosamente.")
def consultar_tablas():
    print("\n--- Consultar datos ---")
    print("1. Tabla Miembros")
    print("2. Tabla Pagos")
    print("3. Tabla combinada (Miembros + Pagos)")
    opcion = input("Selecciona una opción: ")
    if opcion == "1":
        print("\nTabla de Miembros:")
        print(tabla_miembros.to_string(index=False))
    elif opcion == "2":
        print("\nTabla de Pagos:")
        print(tabla_pagos.to_string(index=False))
    elif opcion == "3":
        tabla_combinada = pd.merge(tabla_miembros, tabla_pagos, on="ID_Usuario", how="inner")
        print("\nTabla combinada (Miembros + Pagos):")
        print(tabla_combinada.to_string(index=False))
    else:
        print("Opción no válida.")

def mostrar_ordenado():
    global tabla_miembros
    print("\n--- Mostrar tabla Miembros ordenada ---")
    print("1. Por Nombre")
    print("2. Por Apellido")
    print("3. Por Fecha de Nacimiento")
    opcion = input("Selecciona una opción: ")
    if opcion == "1":
        print(tabla_miembros.sort_values(by="Nombre").to_string(index=False))
    elif opcion == "2":
        print(tabla_miembros.sort_values(by="Apellido").to_string(index=False))
    elif opcion == "3":
        print(tabla_miembros.sort_values(by="Fecha de Nacimiento").to_string(index=False))
    else:
        print("Opción no válida.")

def eliminar_datos():
    global tabla_miembros, tabla_pagos
    print("\n--- Eliminar datos ---")
    print("1. Eliminar un miembro")
    print("2. Eliminar un pago")
    opcion = input("Selecciona una opción: ")
    if opcion == "1":
        id_usuario = input("ID del usuario a eliminar: ")
        tabla_miembros = tabla_miembros[tabla_miembros["ID_Usuario"] != id_usuario]
        tabla_pagos = tabla_pagos[tabla_pagos["ID_Usuario"] != id_usuario]
        print("Miembro eliminado exitosamente.")
    elif opcion == "2":
        id_pago = input("ID del pago a eliminar: ")
        tabla_pagos = tabla_pagos[tabla_pagos["ID_Pago"] != id_pago]
        print("Pago eliminado exitosamente.")
    else:
        print("Opción no válida.")


# Menú principal
def menu():
    cargar_tablas()
    while True:
        print("\n--- Menú Principal ---")
        print("1. Agregar miembro")
        print("2. Agregar pago")
        print("3. Consultar datos")
        print("4. Eliminar datos")
        print("5. Mostrar datos ordenados")
        print("6. Buscar persona")
        print("7. Guardar y salir")
        
        opcion = input("Selecciona una opción: ")
        if opcion == "1":
            agregar_miembro()
        elif opcion == "2":
            agregar_pago()
        elif opcion == "3":
            consultar_tablas()
        elif opcion == "4":
            eliminar_datos()
        elif opcion == "5":
            mostrar_ordenado()
        elif opcion == "6":
            buscar_persona()
        elif opcion == "7":
            guardar_tablas()
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

menu()