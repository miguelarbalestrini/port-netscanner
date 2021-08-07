# Final 2.1

## Descripción

En esta carpeta se encuentra el archivo main y en src los 3 módulos utilizados para el escaneo.
Además está el archivo data.json, generado en una corrida utilizando 192.168.0.105/32 como input.

## Uso

`
python3 main.py -i <interfaz>
`
Ejemplo:
`
python3 main.py -i 192.168.0.105/32
`

## Detalle

Desarrollé la herramienta intentando usar lo menos posible librerías y módulos de 3ros, por lo que el resultado final no es eficiente, la complejidad algoritmica del escaneo de redes y puertos hace que el proceso sea muy lento para grandes cantidades de hosts y puertos.

## Código

En main realicé un parseo del input ingresado por consola, llamadas a los 3 módulos utilizados, la post request y por último la generación del json (dando el feedback correspondiente por consola).
En el json se guarda cada dirección ip encontrada y cada una tiene los 2 listas, la primera es de los puertos tcp abiertos y la segunda es de los puertos udp.
La salida del archivo json se guarda en la carpeta output.

### Módulos

Generé 3 módulos encargados de el escaneo de cada parte, intentando mantener un nivel de acoplamiento bajo y con el objetivo de poder ser reemplazados por mejores implementaciones.

#### network_scanner

Este módulo es el encargado de realizar el escaneo de red usando la técnica conocida como ping sweep, la cual consiste en realizar ping a todos los hosts disponibles.
Además guarda en una lista cada dirección que encuentra "viva" en una lista, para considerarse viva se debe poder recibir un paquete al realizar el ping.
Este módulo además puede comprobar sobre qué plataforma se está ejecutando y cambiar el comando ping en funcipon de eso.
Otro detalle a mencionar es que utilicé la librería ipaddress para obtener los hosts disponobles a partir de la netmask en notación cdir (quería evitar usarla pero al final no se me ocurrió una forma simpĺe y efectiva).
Al ser una clase, voy actualizando los atributos cuando es necesario y por eso mismo mantuve una sola instancia en el main.

#### tcp_scanner

Aquí se realiza el escaneo al puerto indicado, guardandolo en una lista en caso de estar "vivo".
Utilicé sockets para aprovechar el saludo de 3 vías de tcp y así poder diagnosticar fácilmente.

#### udp_scanner

Aquí se realiza el escaneo al puerto indicado, guardandolo en una lista en caso de estar "vivo".
También utilicé sockets pero me encontré con la dificultad de que udp, al no ser orientado a conexión, no garantiza la misma. 
Así que me resultó de lo más engorroso e investigando dí con una solución que me pareció intesante, la cual consiste en enviar paquetes DNS, como DNS funciona con puertos udp, se puede conseguir un poco más de claridad de si el puerto está abierto o no.

## Conclusión

En términos generales, como mencionaba anteriormente, no es una solución eficiente y es muy lenta, por lo que no sería aplicable para un escenario real.
Para una implementación mucho más optimizada se podría usar la librería de python-nmap o scapy, las cuales tienen funcionalidades para realizar este tipo de escaneo de forma mucho más simple y rápida.
Si se quisiera utilizar de todas formas algo similar a lo que implementé pero más eficiente, se podría recurrir a la programación concurrente y hacerla multi hilos.
También se podría mejorar el acoplamiento que tiene main separarndo mejor las funcionalidades y chequeando mejor los inputs.
Como mencioné anteriormente, decidí evitar usarlas para poder practicar y entender más sobre la idea de crear herramientas propias, por lo mismo opté por mantenerlo simple y evitar implementar concurrencia.
