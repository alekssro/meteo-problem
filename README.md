# Ejercicios

## 2.1.  Sistema de predicción eólica sencillo

El ejercicio consiste en implementar un sistema de predicción de generación de energía eólicamediante la relación entre la producción de energía de un parque eólico y el viento. Esta relaciónpodrá ser diferente para cada parque eólico, por lo que se necesita un sistema automático para obtenery evaluar la relación para diferentes parques eólicos.

## 2.2.  API HTTP de predicciones

Queremos hacer disponibles las predicciones a través de una API HTTP. La idea es que cualquiercliente se pueda conectar a esa API, y pedir la predicción para una ubicación y una fecha. El protocoloque vamos a utilizar en este caso es HTTP, y las peticiones deben ir en JSON, así como la respuesta.Para pedir predicciones realizaremos una petición POST cuyo contenido sea similar a este:

    {
        "ubicacion": {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [125.6, 10.1]
            },
            "properties": {
                    "name": "Dinagat Islands"
            }
        }
    }
    
La ubicación está en formato GeoJSON. Los datos a devolver serán aleatorios, devolveremos latemperatura máxima para la fecha solicitada y los siguientes 10 días. Ejemplo de respuesta:

    {"ubicacion": {"type": "Feature","geometry": {"type": "Point","coordinates": [125.6, 10.1]},"properties": {"name": "Dinagat Islands"}},"prediccion": [{"fecha": "2019-01-15","Tmax": 22.5},{"fecha": "2019-01-16","Tmax": 22.5},{"fecha": "2019-01-17","Tmax": 22.5},{"fecha": "2019-01-18","Tmax": 22.5},{"fecha": "2019-01-19","Tmax": 22.5},{"fecha": "2019-01-20","Tmax": 22.5},{"fecha": "2019-01-21","Tmax": 22.5},{"fecha": "2019-01-22","Tmax": 22.5},{"fecha": "2019-01-23","Tmax": 22.5},{"fecha": "2019-01-24","Tmax": 22.5}]}

## 2.3.  Construcción económica de vallas

Tenemos algunos bosques por el campo, y queríamos construir una valla alrededor para que noentre ningún pirómano. Cada uno de esos bosques tiene los árboles distribuidos de forma irregular, yqueremos vallarlos de la forma más económica posible, es decir, minimizando la longitud total de lavalla. El ejercicio consiste en hacer un pequeño programa que dada una serie de puntos nos devuelveel polígono que corresponderá a la valla (basta con los vértices de ese polígono). Ejemplo entrada:

    0 0
    0 2
    2 0
    2 2
    1 1

Ejemplo salida:

    0 0
    0 2
    2 2
    2 0

Este programa debe funcionar para entradas aleatorias.Para que puedas comprobar si tu algoritmo está funcionando bien, queremos que hagas una pe-queña visualización del resultado. Para hacer esta visualización utilizaremos la biblioteca CppPlotlyque genera un html que se puede ver en el navegador. 