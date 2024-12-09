import os
from PIL import Image
import cv2

def crop_and_center_with_detection(image_path, output_path, crop_width, crop_height):
    """
    Recorta una imagen a las dimensiones especificadas, centrando el carro detectado.

    :param image_path: Ruta de la imagen de entrada.
    :param output_path: Ruta para guardar la imagen recortada.
    :param crop_width: Ancho del recorte.
    :param crop_height: Altura del recorte.
    """
    # Cargar la imagen con OpenCV
    img = cv2.imread(image_path)
    if img is None:
        print(f"No se pudo cargar la imagen: {image_path}")
        return False

    # Cargar el clasificador Haar preentrenado para carros
    car_cascade = cv2.CascadeClassifier('modelos/haarcascade_car.xml')

    # Convertir a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detectar carros en la imagen
    cars = car_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=2)
    if len(cars) == 0:
        print(f"No se detectaron carros en la imagen: {image_path}")
        return False

    # Tomar el primer carro detectado (puedes modificar para tomar el más grande)
    x, y, w, h = cars[0]

    # Calcular el centro del objeto detectado
    center_x = x + w // 2
    center_y = y + h // 2

    # Leer la imagen original con Pillow
    img_pil = Image.open(image_path)

    # Calcular las coordenadas del recorte
    left = max(0, center_x - crop_width // 2)
    top = max(0, center_y - crop_height // 2)
    right = min(img_pil.width, center_x + crop_width // 2)
    bottom = min(img_pil.height, center_y + crop_height // 2)

    # Ajustar si el recorte se sale de los límites
    if right - left < crop_width:
        diff = crop_width - (right - left)
        left = max(0, left - diff // 2)
        right = min(img_pil.width, right + diff // 2)
    if bottom - top < crop_height:
        diff = crop_height - (bottom - top)
        top = max(0, top - diff // 2)
        bottom = min(img_pil.height, bottom + diff // 2)

    # Recortar y guardar la imagen
    cropped_img = img_pil.crop((left, top, right, bottom))
    cropped_img.save(output_path)
    return True

def process_images_in_folder(input_folder, output_folder, crop_width, crop_height):
    """
    Procesa todas las imágenes en una carpeta y guarda las imágenes recortadas en una carpeta de salida.

    :param input_folder: Carpeta de entrada con las imágenes.
    :param output_folder: Carpeta de salida para guardar las imágenes procesadas.
    :param crop_width: Ancho del recorte.
    :param crop_height: Altura del recorte.
    """
    # Crear la carpeta de salida si no existe
    os.makedirs(output_folder, exist_ok=True)

    # Obtener una lista de archivos en la carpeta de entrada
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        if os.path.isfile(file_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            # Generar la ruta de salida
            output_path = os.path.join(output_folder, filename)

            # Procesar la imagen
            success = crop_and_center_with_detection(file_path, output_path, crop_width, crop_height)
            if success:
                print(f"Procesada: {filename}")
            else:
                print(f"No se pudo procesar: {filename}")

# Configuración
input_folder = r"C:\Users\Bradl\OneDrive\Escritorio\Imagenes carros\Imagenes"  # Carpeta de entrada con las imágenes
output_folder = os.path.join(input_folder, "Procesadas")  # Carpeta de salida dentro de la carpeta de entrada
crop_width = 1000  # Ancho del recorte
crop_height = 1100  # Altura del recorte

process_images_in_folder(input_folder, output_folder, crop_width, crop_height)
