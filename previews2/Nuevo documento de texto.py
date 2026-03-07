import os
from PIL import Image

def procesar_y_limpiar():
    # Dimensiones deseadas
    TARGET_W, TARGET_H = 480, 270
    extensiones_validas = ('.jpg', '.jpeg', '.png', '.bmp', '.webp', '.tiff')
    
    # Obtener lista de imágenes en la carpeta actual
    archivos = [f for f in os.listdir('.') if f.lower().endswith(extensiones_validas)]
    
    if not archivos:
        print("No se encontraron imágenes en esta carpeta.")
        return

    print(f"--- Iniciando procesamiento de {len(archivos)} imágenes ---")

    for archivo in archivos:
        try:
            ruta_original = archivo
            nombre_sin_ext = os.path.splitext(archivo)[0]
            ruta_final = f"{nombre_sin_ext}.png"

            with Image.open(ruta_original) as img:
                # 1. Convertir a RGBA para manejar transparencias si existen
                img = img.convert("RGBA")
                
                # 2. Crear lienzo negro de 480x270
                # Usamos "RGB" al final para que pese menos (el PNG no necesita canal alfa si el fondo es negro)
                fondo = Image.new("RGB", (TARGET_W, TARGET_H), (0, 0, 0))
                
                # 3. Redimensionar manteniendo proporción (evita que se vea estirada)
                img.thumbnail((TARGET_W, TARGET_H), Image.Resampling.LANCZOS)
                
                # 4. Centrar la imagen sobre el fondo negro
                offset = (
                    (TARGET_W - img.size[0]) // 2,
                    (TARGET_H - img.size[1]) // 2
                )
                
                # Pegar (usamos la propia imagen como máscara por si tiene transparencias)
                fondo.paste(img, offset, mask=img)
                
                # 5. Guardado temporal si es el mismo nombre, o directo si cambia
                # Para evitar errores de "archivo abierto", guardamos con optimización
                fondo.save(ruta_final, "PNG", optimize=True)

            # --- GESTIÓN DE ARCHIVOS (No crear copias) ---
            # Si el archivo original NO era .png, lo borramos.
            if ruta_original.lower() != ruta_final.lower():
                os.remove(ruta_original)
                print(f"[CONVERTIDO] {ruta_original} -> {ruta_final}")
            else:
                print(f"[REESCRITO] {ruta_final} (Ya era PNG, ahora tiene el tamaño correcto)")

        except Exception as e:
            print(f"Error con {archivo}: {e}")

    print("\n--- ¡Listo! Todas las imágenes son ahora 480x270 PNG ---")

if __name__ == "__main__":
    procesar_y_limpiar()