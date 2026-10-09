# Instructivo para lanzar el experimento oTree (Dilemas_SEA2)

Guía paso a paso para correr el experimento en un PC con Windows, con los
estudiantes conectados al mismo router. Todos los comandos son para
**PowerShell**.

> En los comandos, `<CARPETA>` es la ruta donde está clonado este
> repositorio. Ejemplo:
> `C:\Users\lujoc\OneDrive\Desktop\Cristian Trabajo\ExperimentoOtreeDanielVillar`

---

## Paso 0. Instalar oTree (solo una vez)

Hacerlo la primera vez, o si se borra o se vuelve a clonar la carpeta.
Pegar uno por uno:

```powershell
cd "<CARPETA>\Dilemas_SEA2"
py -3.13 -m venv venv
.\venv\Scripts\python -m pip install otree==5.11.5
$env:PATH = "$PWD\venv\Scripts;$env:PATH"
otree resetdb
```

- `resetdb` prepara la base de datos. Pregunta si desea continuar: responder `y`.
- **`resetdb` BORRA los datos guardados.** Solo se usa al instalar o cuando
  un cambio del código agrega columnas nuevas. **Nunca después de una sesión real.**
- Localmente se usa Python 3.13 con oTree 5.11.5, porque oTree 5.10.4 (el de
  `requirements.txt`) no funciona con Python 3.13.

---

## Paso 1. Conectar el PC al router

- Prender el router D-Link y dejarlo conectado a la corriente.
- Conectar el **Wi-Fi del PC** a: `dlink_DWR-932C_313C`

Si el PC no está en la red del router, los teléfonos de los estudiantes
se quedan cargando sin fin.

---

## Paso 2. Prender el servidor

```powershell
cd "<CARPETA>\Dilemas_SEA2"
$env:PATH = "$PWD\venv\Scripts;$env:PATH"
otree prodserver 8000
```

El servidor **ya está listo** cuando la ventana muestra estas dos líneas y
se queda quieta:

```
Running prodserver
timeoutworker is listening for messages through DB
```

- **No cerrar esta ventana** mientras dure la sesión.
- Usar `prodserver` y no `devserver`: `devserver` guarda los datos en
  memoria y se pierden si la ventana se cierra.

---

## Paso 3. Ver la IP del PC

En **otra** ventana de PowerShell:

```powershell
ipconfig
```

Buscar **"Adaptador de LAN inalámbrica Wi-Fi"** (la que tiene puerta de
enlace `192.168.0.1`) y anotar la **Dirección IPv4**. Ejemplo: `192.168.0.23`.
Puede cambiar de un día a otro, revisarla siempre.

---

## Paso 4. Crear la sesión en la sala "Dilemas" (recomendado)

La sala tiene una **dirección fija** que no cambia entre sesiones:

```
http://<IP>:8000/room/dilemas
```

Las etiquetas de los computadores son `pc1` a `pc32`
(archivo `Dilemas_SEA2/_rooms/dilemas.txt`).

1. En el navegador del PC abrir: `http://localhost:8000/rooms`
2. Clic en **Dilemas**.
3. En *Session Config* elegir **debate_conflict**.
4. Poner el número de participantes.
   **SIEMPRE MÚLTIPLO DE 4** (4, 8, 12, 16...). Con menos de 4 o con un
   número que no sea múltiplo de 4, el experimento falla.
5. Clic en **Create**.

### Enlaces para los estudiantes
- **Enlace general:** `http://<IP>:8000/room/dilemas`. El estudiante
  escribe la etiqueta de su computador (`pc1`, `pc2`...).
- **Enlace por computador** (no hay que escribir nada):
  `http://<IP>:8000/room/dilemas/?participant_label=pc1`.
  En la página de la sala aparecen todos en *Participant-specific URLs*.

### Alternativa sin sala
En `http://localhost:8000/sessions` → **Create new session** →
pestaña **Links** → copiar el *Session-wide link* y cambiar `localhost`
por la IP. Este enlace cambia en cada sesión.

**No abrir los enlaces "para probar": cada visita ocupa un cupo.**

---

## Paso 5. Los estudiantes

- Conectarse al Wi-Fi `dlink_DWR-932C_313C`.
- **Apagar los datos móviles.**
- Abrir el enlace escribiendo `http://` al inicio.

---

## Paso 6. Durante y al final

- Seguir el avance en la pestaña **Monitor** de la sesión.
- Si una pantalla dice "Por favor espere", es normal: espera a que la
  pareja o todos los participantes lleguen a ese punto.
- Al terminar, descargar los resultados en la pestaña **Data**
  (formato ancho o Excel) y guardarlos aparte.

### Dónde se guardan los datos
En el archivo `Dilemas_SEA2\db.sqlite3`. **No borrarlo.**

---

## Modo local: probar en el mismo PC (sin estudiantes)

```powershell
cd "<CARPETA>\Dilemas_SEA2"
$env:PATH = "$PWD\venv\Scripts;$env:PATH"
otree devserver 0.0.0.0:8000
```

1. Abrir `http://localhost:8000/demo` y dar clic en **debate_conflict**
   (crea una prueba con 4 participantes).
2. Abrir cada uno de los 4 enlaces en una pestaña distinta. Parejas: P1 con
   P2 y P3 con P4. Cuando una pestaña diga "Por favor espere", avanzar otra.
3. Para probar desde un teléfono: mismo Wi-Fi que el PC, datos móviles
   apagados, y cambiar `localhost` por la IP del PC en el enlace.

En `devserver` los datos se borran al cerrar la ventana: **solo para pruebas.**

---

## Apagar todo

En la ventana del servidor presionar **Ctrl + C**.

## Problemas comunes

| Síntoma | Causa | Solución |
|---|---|---|
| El teléfono se queda cargando | El PC no está en el Wi-Fi del router | Paso 1 y revisar la IP (Paso 3) |
| La página no carga en el teléfono | Datos móviles encendidos o falta `http://` | Apagar datos y escribir `http://` |
| "Session is full" | Se acabaron los cupos de la sesión | Crear otra sesión con más participantes |
| Error en "Instrucciones generales" | La sesión no es múltiplo de 4 | Crear la sesión con 4, 8, 12... |
| Errores después de traer cambios del código | El cambio agregó columnas nuevas a los datos | `otree resetdb` (borra los datos guardados) |
