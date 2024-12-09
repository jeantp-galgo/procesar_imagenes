import os
from PIL import Image

"""
CARROS USADOS
"""

def resize_and_crop(image_path, output_path, target_width, target_height):
    """
    Redimensiona y recorta la imagen para llenar completamente el área objetivo.
    """
    # Cargar la imagen con PIL
    img = Image.open(image_path).convert("RGBA")
    
    # Convertir a escala de grises y encontrar los bordes
    gray = img.convert("L")
    bbox = gray.getbbox()
    
    if bbox:
        # Recortar la imagen para eliminar el fondo blanco
        img = img.crop(bbox)

    # Calcular las proporciones
    target_ratio = target_width / target_height
    img_ratio = img.width / img.height

    if img_ratio > target_ratio:
        # La imagen es más ancha, recortar los lados
        new_height = target_height
        new_width = int(target_height * img_ratio)
        img_resized = img.resize((new_width, new_height), Image.LANCZOS)
        left = (new_width - target_width) / 2
        img_cropped = img_resized.crop((left, 0, left + target_width, target_height))
    else:
        # La imagen es más alta, recortar la parte superior e inferior
        new_width = target_width
        new_height = int(target_width / img_ratio)
        img_resized = img.resize((new_width, new_height), Image.LANCZOS)
        top = (new_height - target_height) / 2
        img_cropped = img_resized.crop((0, top, target_width, top + target_height))

    img_cropped.save(output_path)
    return True

def process_images_in_folder(input_folder, output_folder, target_width, target_height):
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.avif')):
            image_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            # Verificar si el nombre del archivo contiene "lifestyle"
            if "lifestyle" in filename.lower():
                specific_width = 1000
                specific_height = 700
            else:
                specific_width = target_width
                specific_height = target_height

            try:
                success = resize_and_crop(
                    image_path, 
                    output_path, 
                    specific_width, 
                    specific_height
                )
                if success:
                    print(f"Procesada: {filename}")
                else:
                    print(f"No se pudo procesar: {filename}")
            except Exception as e:
                print(f"Error procesando {filename}: {e}")

# Configuración
input_folder = r"C:\Users\jtrujillo\Desktop\Archivo actualizaciones\Imagenes recolectadas\06-12-2024\dfsk 500 1.5 luxury mt 5p 2022"
output_folder = os.path.join(input_folder, "Procesadas_usados")  # Carpeta de salida dentro de la carpeta de entrada
target_width = 1000
target_height = 1100

process_images_in_folder(input_folder, output_folder, target_width, target_height)
