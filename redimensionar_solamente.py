import os
from PIL import Image

def resize_image(image_path, output_path, target_width, target_height):
    """
    Redimensiona una imagen manteniendo las proporciones.
    """
    # Abrir la imagen con PIL para el procesamiento
    img = Image.open(image_path).convert("RGBA")

    # Calcular la relación de aspecto
    target_ratio = target_width / target_height
    img_ratio = img.width / img.height

    # Determinar nuevas dimensiones manteniendo la proporción
    if img_ratio > target_ratio:
        new_width = target_width
        new_height = int(target_width / img_ratio)
    else:
        new_width = int(target_height * img_ratio)
        new_height = target_height

    # Redimensionar la imagen
    img_resized = img.resize((new_width, new_height), Image.LANCZOS)

    # Crear un lienzo del tamaño objetivo y centrar la imagen redimensionada
    new_img = Image.new("RGBA", (target_width, target_height), (255, 255, 255, 255))
    paste_x = (target_width - new_width) // 2
    paste_y = (target_height - new_height) // 2
    new_img.paste(img_resized, (paste_x, paste_y), img_resized)

    # Guardar la imagen redimensionada
    new_img.save(output_path)
    return True

def process_images_in_folder(input_folder, output_folder, target_width, target_height):
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            image_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            try:
                success = resize_image(
                    image_path, 
                    output_path, 
                    target_width, 
                    target_height
                )
                if success:
                    print(f"Procesada: {filename}")
                else:
                    print(f"No se pudo procesar: {filename}")
            except Exception as e:
                print(f"Error procesando {filename}: {e}")

# Configuración
input_folder = r"C:\Users\jtrujillo\Desktop\X7 imagenes"
output_folder = os.path.join(input_folder, "Procesadas")  # Carpeta de salida dentro de la carpeta de entrada
target_width = 1000
target_height = 1100

process_images_in_folder(input_folder, output_folder, target_width, target_height)