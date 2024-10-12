import sys
import os

# Importar Tkinter directamente desde el sistema
from tkinter import (
    Tk, Label, Entry, Button, filedialog, messagebox, StringVar
)

# Añadir la carpeta 'dependencias' al sys.path solo para importar Pillow
script_dir = os.path.dirname(os.path.abspath(__file__))
deps_dir = os.path.join(script_dir, 'dependencias')

if os.path.isdir(deps_dir):
    sys.path.insert(0, deps_dir)
    print(f"Carpeta de dependencias añadida al sys.path: {deps_dir}")
else:
    print(f"Carpeta de dependencias no encontrada: {deps_dir}")
    sys.exit(1)

try:
    from PIL import Image, ImageTk  # Pillow está instalado en 'dependencias'
except ImportError as e:
    print(f"Error al importar Pillow: {e}")
    sys.exit(1)

import shutil
import subprocess
import traceback

class AppImageCreator:
    def __init__(self, master):
        self.master = master
        master.title("Creador de AppImage")

        # Establecer icono personalizado de la ventana
        try:
            icon_path = os.path.join(script_dir, "icono.png")
            if os.path.exists(icon_path):
                img = Image.open(icon_path)
                photo = ImageTk.PhotoImage(img)
                master.iconphoto(False, photo)
                print(f"Icono de ventana establecido desde: {icon_path}")
            else:
                print("Icono personalizado no encontrado. Se usará el icono por defecto.")
        except Exception as e:
            print(f"Error al cargar el icono: {e}")

        # Variables para almacenar las rutas y datos ingresados
        self.source_dir = StringVar()
        self.icon_path = StringVar()
        self.exec_path = StringVar()
        self.app_name = StringVar()
        self.app_description = StringVar()
        self.categories = StringVar()

        # Configuración de los widgets de la interfaz
        padding_options = {'padx': 10, 'pady': 5}

        # Campo para seleccionar el Directorio de Origen
        Label(master, text="Directorio de Origen:").grid(row=0, column=0, sticky="e", **padding_options)
        Button(master, text="Seleccionar", command=self.select_source).grid(row=0, column=2, **padding_options)
        Entry(master, textvariable=self.source_dir, width=50).grid(row=0, column=1, **padding_options)

        # Campo para seleccionar el Icono
        Label(master, text="Icono (.png o .svg):").grid(row=1, column=0, sticky="e", **padding_options)
        Button(master, text="Seleccionar", command=self.select_icon).grid(row=1, column=2, **padding_options)
        Entry(master, textvariable=self.icon_path, width=50).grid(row=1, column=1, **padding_options)

        # Campo para seleccionar el Archivo Ejecutable
        Label(master, text="Archivo Ejecutable:").grid(row=2, column=0, sticky="e", **padding_options)
        Button(master, text="Seleccionar", command=self.select_exec).grid(row=2, column=2, **padding_options)
        Entry(master, textvariable=self.exec_path, width=50).grid(row=2, column=1, **padding_options)

        # Campo para ingresar el Nombre de la App
        Label(master, text="Nombre de la App:").grid(row=3, column=0, sticky="e", **padding_options)
        Entry(master, textvariable=self.app_name, width=50).grid(row=3, column=1, **padding_options)

        # Campo para ingresar la Descripción de la App
        Label(master, text="Descripción:").grid(row=4, column=0, sticky="e", **padding_options)
        Entry(master, textvariable=self.app_description, width=50).grid(row=4, column=1, **padding_options)

        # Campo para ingresar las Categorías de la App
        Label(master, text="Categorías:").grid(row=5, column=0, sticky="e", **padding_options)
        Label(master, text="(separadas por ';')").grid(row=5, column=2, sticky="e", **padding_options)
        Entry(master, textvariable=self.categories, width=50).grid(row=5, column=1, **padding_options)
        
        Label(text="Audio, Video, Development, Education, Game").grid(row=6,column=1)
        Label(text="Graphics, Network, Office, Science, Settings, System, Utility").grid(row=7,column=1)

        # Botones para preparar la fuente y crear el AppImage
        Button(master, text="Preparar Fuente", command=self.prepare_source).grid(row=8, column=0, pady=10)
        Button(master, text="Crear AppImage", command=self.create_appimage).grid(row=8, column=1, pady=10)

    def select_source(self):
        directory = filedialog.askdirectory()
        if directory:
            self.source_dir.set(directory)
            print(f"Directorio de origen seleccionado: {directory}")

    def select_icon(self):
        filetypes = [("Image Files", "*.png *.svg")]
        filepath = filedialog.askopenfilename(filetypes=filetypes)
        if filepath:
            self.icon_path.set(filepath)
            print(f"Icono seleccionado: {filepath}")

    def select_exec(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            self.exec_path.set(filepath)
            print(f"Archivo ejecutable seleccionado: {filepath}")

    def prepare_source(self):
        # Validar que todos los campos necesarios estén completos
        if not all([
            self.source_dir.get(),
            self.exec_path.get(),
            self.app_name.get(),
            self.app_description.get(),
            self.categories.get()
        ]):
            messagebox.showerror("Error", "Por favor, completa todos los campos necesarios para preparar la fuente.")
            print("Error: Campos incompletos.")
            return

        exec_name = os.path.basename(self.exec_path.get())
        appdir_name = f"{self.app_name.get()}.AppDir"
        appdir_path = os.path.join(self.source_dir.get(), appdir_name)

        print(f"Preparando fuente en: {appdir_path}")

        if os.path.exists(appdir_path):
            messagebox.showerror("Error", f"El directorio '{appdir_name}' ya existe en el directorio de origen.")
            print(f"Error: El directorio '{appdir_name}' ya existe.")
            return

        try:
            # Crear la estructura de directorios
            os.makedirs(os.path.join(appdir_path, "usr", "bin"), exist_ok=True)
            os.makedirs(os.path.join(appdir_path, "usr", "share", "icons", "hicolor", "256x256", "apps"), exist_ok=True)
            os.makedirs(os.path.join(appdir_path, "usr", "share"), exist_ok=True)
            print("Estructura de directorios creada.")

            # Copiar el ejecutable a usr/share/
            exec_dst_path = os.path.join(appdir_path, "usr", "share", exec_name)
            shutil.copy2(self.exec_path.get(), exec_dst_path)
            print(f"Ejecutable copiado a: {exec_dst_path}")

            # Copiar el icono a AppDir/icon.png
            icon_dst_path_appdir = os.path.join(appdir_path, "icon.png")
            shutil.copy2(self.icon_path.get(), icon_dst_path_appdir)
            print(f"Icono copiado a: {icon_dst_path_appdir}")

            # Copiar el icono a usr/share/icons/hicolor/256x256/apps/icon.png
            icon_dst_path_icons = os.path.join(appdir_path, "usr", "share", "icons", "hicolor", "256x256", "apps", "icon.png")
            os.makedirs(os.path.dirname(icon_dst_path_icons), exist_ok=True)  # Asegurar que el directorio existe
            shutil.copy2(self.icon_path.get(), icon_dst_path_icons)
            print(f"Icono copiado a: {icon_dst_path_icons}")

            # Crear el archivo 'AppRun' en AppDir apuntando al ejecutable en usr/bin/
            apprun_content = f"""#! /bin/bash
cd "$(dirname "$0")"
exec ./usr/bin/{exec_name}
"""
            apprun_path = os.path.join(appdir_path, "AppRun")
            with open(apprun_path, "w") as f:
                f.write(apprun_content)
            os.chmod(apprun_path, 0o755)  # Asegurar permisos de ejecución
            print(f"Archivo 'AppRun' creado en: {apprun_path}")

            # Crear un enlace simbólico del ejecutable en usr/bin/ apuntando a ../share/executable
            symlink_path = os.path.join(appdir_path, "usr", "bin", exec_name)
            target_path = os.path.join("..", "share", exec_name)
            os.symlink(target_path, symlink_path)
            print(f"Enlace simbólico creado en: {symlink_path} apuntando a {target_path}")

            # Copiar todos los demás archivos del directorio de origen a usr/share/
            source_files = [
                f for f in os.listdir(self.source_dir.get()) 
                if f not in [exec_name, "AppRun", f"{self.app_name.get()}.desktop", appdir_name, "icono.png"]
            ]
            for file in source_files:
                src_path = os.path.join(self.source_dir.get(), file)
                dest_path = os.path.join(appdir_path, "usr", "share", file)
                if os.path.isdir(src_path):
                    shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
                    print(f"Directorio copiado a: {dest_path}")
                else:
                    shutil.copy2(src_path, dest_path)
                    print(f"Archivo copiado a: {dest_path}")

            # Crear el archivo '.desktop' en AppDir/usr/
            desktop_entry = f"""[Desktop Entry]
Name={self.app_name.get()}
Exec=AppRun
Icon=icon
Type=Application
Categories={self.categories.get()}
Comment={self.app_description.get()}
"""
            desktop_path = os.path.join(appdir_path, "usr", f"{self.app_name.get()}.desktop")
            with open(desktop_path, "w") as f:
                f.write(desktop_entry)
            os.chmod(desktop_path, 0o644)
            print(f"Archivo '.desktop' creado en: {desktop_path}")

            # ===== NUEVO: Copiar el archivo '.desktop' al directorio raíz de AppDir =====
            desktop_dst_path_root = os.path.join(appdir_path, f"{self.app_name.get()}.desktop")
            shutil.copy2(desktop_path, desktop_dst_path_root)
            print(f"Archivo '.desktop' copiado a: {desktop_dst_path_root}")
            # ===========================================================================

            messagebox.showinfo("Éxito", "Fuente preparada exitosamente.")

        except Exception as e:
            error_trace = traceback.format_exc()
            print(f"Error al preparar la fuente: {e}\n{error_trace}")
            messagebox.showerror("Error", f"No se pudo preparar la fuente: {e}")

    def create_appimage(self):
        # Validar que todos los campos necesarios estén completos
        if not all([
            self.source_dir.get(),
            self.icon_path.get(),
            self.exec_path.get(),
            self.app_name.get(),
            self.app_description.get(),
            self.categories.get()
        ]):
            messagebox.showerror("Error", "Por favor, completa todos los campos necesarios.")
            print("Error: Campos incompletos.")
            return

        # Verificar que las herramientas están en la carpeta 'tools/'
        tools_dir = os.path.join(script_dir, "tools")
        appimagetool_path = os.path.join(tools_dir, "appimagetool-x86_64.AppImage")
        runtime_path = os.path.join(tools_dir, "runtime-x86_64")

        missing_tools = []
        for tool, path in [("appimagetool-x86_64.AppImage", appimagetool_path), 
                           ("runtime-x86_64", runtime_path)]:
            if not os.path.exists(path):
                missing_tools.append(tool)
                print(f"Error: Herramienta faltante: {tool} en {path}")
            elif not os.access(path, os.X_OK):
                try:
                    os.chmod(path, 0o755)
                    print(f"Permisos de ejecución asignados a: {path}")
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudieron cambiar los permisos de '{tool}': {e}")
                    print(f"Error al cambiar permisos de {path}: {e}")
                    return

        if missing_tools:
            messagebox.showerror("Error", f"No se encontraron las siguientes herramientas en 'tools/': {', '.join(missing_tools)}")
            print(f"Error: Herramientas faltantes: {', '.join(missing_tools)}")
            return

        # Verificar si appstreamcli está en /usr/bin/
        appstreamcli_system = "/usr/bin/appstreamcli"
        if not os.path.exists(appstreamcli_system):
            messagebox.showerror("Error", "No se encontró 'appstreamcli' en '/usr/bin/'. Por favor, instala el paquete 'appstream'.")
            print("Error: 'appstreamcli' no encontrado en '/usr/bin/'.")
            return

        # Configurar el entorno para subprocess.run, asegurando que /usr/bin esté en PATH
        env = os.environ.copy()
        # Priorizar /usr/bin en PATH para que appstreamcli del sistema sea usada
        env["PATH"] = "/usr/bin" + os.pathsep + tools_dir + os.pathsep + env.get("PATH", "")
        # Agregar la variable de entorno ARCH
        env["ARCH"] = "x86_64"

        # Depuración: Imprimir el PATH para verificar
        print(f"PATH para subprocess.run: {env['PATH']}")

        try:
            # Identificar el directorio AppDir creado por "Preparar Fuente"
            appdir_name = f"{self.app_name.get()}.AppDir"
            appdir_path = os.path.join(self.source_dir.get(), appdir_name)

            if not os.path.exists(appdir_path):
                messagebox.showerror("Error", f"No se encontró el directorio '{appdir_name}'. Por favor, ejecuta 'Preparar Fuente' primero.")
                print(f"Error: El directorio '{appdir_name}' no existe.")
                return

            # Comprobar que 'AppRun' existe en AppDir
            apprun_path = os.path.join(appdir_path, "AppRun")
            if not os.path.exists(apprun_path):
                messagebox.showerror("Error", f"No se encontró 'AppRun' en {appdir_path}. Por favor, ejecuta 'Preparar Fuente' primero.")
                print(f"Error: 'AppRun' no encontrado en {appdir_path}.")
                return

            # Solicitar al usuario el directorio de salida para el AppImage
            output_dir = filedialog.askdirectory(title="Selecciona el directorio de salida para AppImage")
            if not output_dir:
                messagebox.showerror("Error", "No se seleccionó ningún directorio de salida.")
                print("Error: No se seleccionó ningún directorio de salida.")
                return

            appimage_name = f"{self.app_name.get()}.AppImage"
            output_path = os.path.join(output_dir, appimage_name)

            # Ejecutar appimagetool con ARCH=x86_64
            command = [
                appimagetool_path,
                appdir_path,
                output_path
            ]

            print(f"Ejecutando comando: ARCH=x86_64 {' '.join(command)}")

            # Ejecutar el comando con el entorno configurado
            result = subprocess.run(
                command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=env
            )

            print("Salida de appimagetool:")
            print(result.stdout)
            if result.stderr:
                print("Errores de appimagetool:")
                print(result.stderr)

            messagebox.showinfo("Éxito", f"AppImage creado exitosamente en: {output_path}")
            print(f"AppImage creado exitosamente en: {output_path}")

        except subprocess.CalledProcessError as e:
            error_message = (
                f"Error al ejecutar el comando: {' '.join(e.cmd)}\n"
                f"Código de retorno: {e.returncode}\n"
                f"Salida: {e.stdout}\n"
                f"Error: {e.stderr}"
            )
            print(error_message)
            messagebox.showerror("Error", error_message)
        except Exception as e:
            error_trace = traceback.format_exc()
            print(f"Ocurrió un error inesperado:\n{error_trace}")
            messagebox.showerror("Error", f"Ocurrió un error inesperado:\n{e}")

def main():
    root = Tk()
    app = AppImageCreator(root)
    root.mainloop()

if __name__ == "__main__":
    main()

