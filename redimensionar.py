import os
from PIL import Image
import cv2

def resize_and_pad(image_path, output_path, target_width, target_height, add_background=True, background_color=(255, 255, 255, 255)):
    """
    Ajusta el tamaño de una imagen para que encaje en un área objetivo.
    Si add_background es True: redimensiona y centra en un lienzo del tamaño objetivo
    Si add_background es False: solo redimensiona manteniendo proporciones
    """
    # Detectar el carro primero
    img_cv2 = cv2.imread(image_path)
    if img_cv2 is None:
        print(f"No se pudo cargar la imagen: {image_path}")
        return False

    # Cargar el clasificador Haar
    car_cascade = cv2.CascadeClassifier('modelos/haarcascade_car.xml')
    gray = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2GRAY)
    cars = car_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=2)

    # Abrir la imagen con PIL para el procesamiento
    img = Image.open(image_path).convert("RGBA")
    
    if len(cars) > 0:
        # Si se detectó un carro, calcular el centro
        x, y, w, h = cars[0]
        center_x = x + w // 2
        center_y = y + h // 2
        
        # Calcular las coordenadas de recorte centradas en el carro
        crop_left = max(0, center_x - target_width // 2)
        crop_top = max(0, center_y - target_height // 2)
        crop_right = min(img.width, center_x + target_width // 2)
        crop_bottom = min(img.height, center_y + target_height // 2)
        
        # Ajustar si el recorte se sale de los límites
        if crop_right - crop_left < target_width:
            diff = target_width - (crop_right - crop_left)
            crop_left = max(0, crop_left - diff // 2)
            crop_right = min(img.width, crop_right + diff // 2)
        if crop_bottom - crop_top < target_height:
            diff = target_height - (crop_bottom - crop_top)
            crop_top = max(0, crop_top - diff // 2)
            crop_bottom = min(img.height, crop_bottom + diff // 2)
        
        # Recortar la imagen centrada en el carro
        img = img.crop((crop_left, crop_top, crop_right, crop_bottom))

    # Continuar con el redimensionamiento
    target_ratio = target_width / target_height
    img_ratio = img.width / img.height

    if img_ratio > target_ratio:
        new_width = target_width
        new_height = int(target_width / img_ratio)
    else:
        new_width = int(target_height * img_ratio)
        new_height = target_height

    img_resized = img.resize((new_width, new_height), Image.LANCZOS)

    if add_background:
        # Crear lienzo con fondo y centrar la imagen
        new_img = Image.new("RGBA", (target_width, target_height), background_color)
        paste_x = (target_width - new_width) // 2
        paste_y = (target_height - new_height) // 2
        new_img.paste(img_resized, (paste_x, paste_y), img_resized)
    else:
        # Solo redimensionar la imagen original manteniendo su transparencia
        new_img = img_resized
        # La imagen resultante será de tamaño (new_width x new_height), 
        # que podría ser menor que target_width x target_height

    new_img.save(output_path)
    return True

def process_images_in_folder(input_folder, output_folder, target_width, target_height, add_background=True, background_color=(255, 255, 255, 255)):
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            image_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            try:
                success = resize_and_pad(
                    image_path, 
                    output_path, 
                    target_width, 
                    target_height, 
                    add_background,
                    background_color
                )
                if success:
                    print(f"Procesada: {filename}")
                else:
                    print(f"No se pudo procesar: {filename}")
            except Exception as e:
                print(f"Error procesando {filename}: {e}")

# Configuración
input_folder = r"C:\Users\Bradl\OneDrive\Escritorio\Imagenes carros\Imagenes"
output_folder = os.path.join(input_folder, "Procesadas")  # Carpeta de salida dentro de la carpeta de entrada
target_width = 1000
target_height = 1100
add_background = True  # Nueva opción: True para agregar fondo, False para mantener transparencia
background_color = (255, 255, 255, 255)  # Fondo blanco sólido (RGBA)

process_images_in_folder(input_folder, output_folder, target_width, target_height, add_background, background_color)
