# conexión.py

import happybase
import pandas as pd
from datetime import datetime

# Bloque principal de ejecución
try:
    # 1. Establecer conexión con HBase
    connection = happybase.Connection('localhost')
    print("\nConexión establecida con HBase")

    # 2. Crear la tabla con las familias de columnas
    table_name = 'morbilidad_cancer'
    families = {
        'diagnostico': dict(),  # Información del diagnóstico
        'paciente': dict(),     # Información del paciente
        'registro': dict()      # Información del registro
    }

    # Eliminar la tabla si ya existe
    if table_name.encode() in connection.tables():
        print(f"\nEliminando tabla existente - {table_name}")
        connection.delete_table(table_name, disable=True)

    # Crear nueva tabla
    connection.create_table(table_name, families)
    table = connection.table(table_name)
    print("\nTabla 'morbilidad_cancer' creada exitosamente")

    # 3. Cargar datos del CSV
    url = 'https://www.datos.gov.co/resource/utgq-6fdm.csv'
    data = pd.read_csv(url)

    # Iterar sobre el DataFrame usando el índice
    for index, row in data.iterrows():
        # Generar row key basado en el índice
        row_key = f'diagnostico_{index}'.encode()

        # Organizar los datos en familias de columnas
        datos = {
            b'diagnostico:nombre': str(row['nombre_diagnostico']).encode(),
            b'diagnostico:codigo': str(row['codigo_diagnostico']).encode(),
            b'paciente:edad': str(row['edad']).encode(),
            b'paciente:sexo': str(row['sexo']).encode(),
            b'paciente:zona': str(row['zona']).encode(),
            b'paciente:regimen': str(row['regimen']).encode(),
            b'registro:ano': str(row['a_o']).encode()
        }

        # Insertar los datos en la tabla
        table.put(row_key, datos)

    print("\nDatos cargados exitosamente")

    # 4. Consultas y Análisis

    # 4.1 Contar el número total de diagnósticos
    count = 0
    for key, data in table.scan():
        count += 1
    print(f"\nTotal de diagnósticos: {count}")

    # 4.2 Obtener diagnósticos por año
    diagnosticos_por_ano = {}
    for key, data in table.scan():
        ano = data[b'registro:ano'].decode()
        diagnosticos_por_ano[ano] = diagnosticos_por_ano.get(ano, 0) + 1

    print("\nDiagnósticos por año:")
    for ano, count in diagnosticos_por_ano.items():
        print(f"Año {ano}: {count} diagnósticos")

    # 4.3 Obtener diagnósticos por sexo
    diagnosticos_por_sexo = {}
    for key, data in table.scan():
        sexo = data[b'paciente:sexo'].decode()
        diagnosticos_por_sexo[sexo] = diagnosticos_por_sexo.get(sexo, 0) + 1

    print("\nDiagnósticos por sexo:")
    for sexo, count in diagnosticos_por_sexo.items():
        print(f"Sexo {sexo}: {count} diagnósticos")

    # 4.4 Obtener diagnósticos por zona geográfica
    diagnosticos_por_zona = {}
    for key, data in table.scan():
        zona = data[b'paciente:zona'].decode()
        diagnosticos_por_zona[zona] = diagnosticos_por_zona.get(zona, 0) + 1

    print("\nDiagnósticos por zona geográfica:")
    for zona, count in diagnosticos_por_zona.items():
        print(f"Zona {zona}: {count} diagnósticos")

    # 4.5 Top 5 diagnósticos más frecuentes
    diagnosticos_frecuentes = {}
    for key, data in table.scan():
        diagnostico = data[b'diagnostico:nombre'].decode()
        diagnosticos_frecuentes[diagnostico] = diagnosticos_frecuentes.get(diagnostico, 0) + 1

    top_5_diagnosticos = sorted(diagnosticos_frecuentes.items(), key=lambda x: x[1], reverse=True)[:5]

    print("\nTop 5 diagnósticos más frecuentes:")
    for diagnostico, count in top_5_diagnosticos:
        print(f"{diagnostico}: {count} casos")

    # 4.6 Cantidad de casos por diagnóstico
    print("\nCantidad de casos por diagnóstico:")
    for diagnostico, count in diagnosticos_frecuentes.items():
        print(f"{diagnostico}: {count} casos")

    # 4.7 Agrupar diagnósticos por edad
    diagnosticos_por_edad = {}
    for key, data in table.scan():
        edad = int(data[b'paciente:edad'].decode())
        diagnostico = data[b'diagnostico:nombre'].decode()

        # Agrupar por rango de edad (Ejemplo: 0-10, 11-20, etc.)
        rango_edad = f"{(edad // 10) * 10}-{(edad // 10) * 10 + 9}"
        if rango_edad not in diagnosticos_por_edad:
            diagnosticos_por_edad[rango_edad] = {}

        diagnosticos_por_edad[rango_edad][diagnostico] = diagnosticos_por_edad[rango_edad].get(diagnostico, 0) + 1

    print("\nDiagnósticos más frecuentes por rango de edad:")
    for rango, diagnos in diagnosticos_por_edad.items():
        print(f"\nRango de edad: {rango}")
        for diagnostico, count in diagnos.items():
            print(f"{diagnostico}: {count} casos")

    # 4.8 Ejemplo de actualización (simulado con otro campo, como 'edad')
    car_to_update = 'diagnostico_0'  # Ejemplo de ID
    new_age = 35  # Actualizando edad
    table.put(car_to_update.encode(), {b'paciente:edad': str(new_age).encode()})
    print(f"\nEdad actualizada para el diagnóstico ID: {car_to_update}")

except Exception as e:
    print(f"Error: {str(e)}")
finally:
    # Cerrar la conexión
    connection.close()
