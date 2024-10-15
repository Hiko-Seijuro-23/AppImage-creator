 ![Texto alternativo](https://raw.githubusercontent.com/Hiko-Seijuro-23/AppImage-creator/d2d25dca7b9b5f8bf12f32be658bb2a99019e3bc/src/icono.png)
# AppImage-creator

**AppImage Creator** es una herramienta gráfica para generar paquetes AppImage de forma sencilla en Linux. Este programa permite a los usuarios crear un AppImage a partir de un directorio de origen, ejecutable e icono, generando automáticamente los archivos y estructura necesarios para que la aplicación sea empaquetada en formato AppImage.

## Funcionalidades

- **Selección de Directorio de Origen**: Permite elegir el directorio donde se encuentra el código fuente de la aplicación y otros archivos necesarios.
- **Selección del Ejecutable**: Escoge el archivo ejecutable de la aplicación que será incluido en el paquete.
- **Selección del Icono**: El usuario puede seleccionar un icono en formato `.png` o `.svg` para la aplicación.
- **Configuración de la Aplicación**: Permite ingresar el nombre, la descripción y seleccionar la categoría a la que pertenece la aplicación.
- **Generación de Estructura AppDir**: Crea automáticamente la estructura de carpetas necesaria, incluyendo el archivo `AppRun` y un archivo `.desktop` que permite integrar la aplicación con el escritorio de Linux.
- **Preparación del Directorio de Fuentes**: Copia el ejecutable, el icono y todos los archivos necesarios en la estructura de directorios correcta.
- **Generación Automática de Archivos `.desktop` y `AppRun`**: Estos archivos son esenciales para el funcionamiento de la AppImage y se generan de manera automática a partir de la información proporcionada por el usuario.

## Requisitos

- **Python 3.x**
- **appstream**
  
## Instrucciones de Uso

1. **Ejecutar el Programa**:
   Para ejecutar el programa, simplemente ejecuta el script principal:
   ```bash
   ./appimage-creator.sh
   ```

2. **Preparar la Fuente**:
   - Selecciona el directorio de origen donde se encuentra tu aplicación.
   - Selecciona el ejecutable que será empaquetado.
   - Elige un icono (en formato `.png` o `.svg`) para la aplicación.
   - Ingresa el nombre de la aplicación, una breve descripción y selecciona la categoría adecuada.
   - Haz clic en el botón "Preparar Fuente" para generar la estructura de archivos necesaria.

3. **Crear AppImage**:
   Al pulsar el boton de **Crear AppImage** el programa solicitara el directorio de salida donde se guardara el appimage generado.

## Estructura de Archivos Generada

Cuando se hace clic en "Preparar Fuente", el programa genera la siguiente estructura dentro del directorio de origen:

```
app_name.AppDir/
│
├── AppRun
├── usr/
│   ├── bin/
│   ├── share/
│       ├── icons/
│       │   └── hicolor/256x256/apps/icon.png
│       ├── ejecutable
│       └── otros archivos copiados desde el directorio de origen
├── app_name.desktop
├── icon.png
```

