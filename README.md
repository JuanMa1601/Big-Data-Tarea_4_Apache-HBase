# Proyecto de Análisis de Datos - Diagnósticos de Salud

Este proyecto tiene como objetivo analizar los datos de diagnósticos de salud de un dataset proporcionado. Se realiza una serie de análisis sobre los diagnósticos más frecuentes, casos por diagnóstico, y se agrupan los diagnósticos según la edad de los pacientes.

## Descripción

El dataset utilizado contiene información sobre diagnósticos médicos, pacientes y su edad, entre otros datos relacionados. El análisis realizado en este proyecto incluye:
- Identificación de los diagnósticos más frecuentes.
- Cálculo de la cantidad de casos por diagnóstico.
- Agrupación de los diagnósticos más frecuentes por edad.

## Funcionalidades

- **Top 5 diagnósticos más frecuentes**: Se listan los cinco diagnósticos más comunes.
- **Cantidad de casos por diagnóstico**: Se muestra cuántos casos existen para cada diagnóstico.
- **Agrupar diagnósticos por edad**: Se agrupan los diagnósticos más frecuentes por la edad de los pacientes.

## Requisitos

Asegúrate de tener las siguientes bibliotecas instaladas:

- `pandas`
- `happybase`
- `hbase`
- `datetime`

Puedes instalar las dependencias usando `pip`:

```bash
pip install pandas happybase
