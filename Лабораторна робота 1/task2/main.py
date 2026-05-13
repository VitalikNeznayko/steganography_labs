from PIL import Image
import numpy as np

def text_to_binary(text):
    return ''.join(format(ord(c), '08b') for c in text)

def binary_to_text(binary):
    chars = []
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        chars.append(chr(int(byte, 2)))
    return ''.join(chars)

def hide_text(image_path, text, output_path):
    image = Image.open(image_path)
    image = image.convert("RGB")
    pixels = np.array(image)

    binary_text = text_to_binary(text) + "1111111111111110"  

    flat_pixels = pixels.flatten()

    if len(binary_text) > len(flat_pixels):
        print("Текст занадто великий для цього зображення")
        return

    for i in range(len(binary_text)):
        flat_pixels[i] = (flat_pixels[i] & 254) | int(binary_text[i])

    new_pixels = flat_pixels.reshape(pixels.shape)

    new_image = Image.fromarray(new_pixels.astype('uint8'), 'RGB')
    new_image.save(output_path)

    print("Текст успішно приховано у:", output_path)

def extract_text(image_path):
    image = Image.open(image_path)
    pixels = np.array(image)

    flat_pixels = pixels.flatten()

    binary_data = ""

    for pixel in flat_pixels:
        binary_data += str(pixel & 1)

    end_marker = "1111111111111110"

    index = binary_data.find(end_marker)

    if index != -1:
        binary_data = binary_data[:index]

    text = binary_to_text(binary_data)

    return text

def compare_images(original_path, stego_path):
    img1 = Image.open(original_path).convert("RGB")
    img2 = Image.open(stego_path).convert("RGB")

    img1 = np.array(img1)
    img2 = np.array(img2)

    difference = np.sum(img1 != img2)

    print("Кількість змінених значень пікселів:", difference)

def main():
    while True:
        print("\n1 - Приховати текст")
        print("2 - Витягнути текст")
        print("3 - Порівняти зображення")
        print("0 - Вийти")

        choice = input("Ваш вибір: ")

        if choice == "1":
            image_path = input("Шлях до зображення (PNG/BMP): ")
            text = input("Введіть текст для приховування: ")
            output = input("Назва нового файлу: ")

            hide_text(image_path, text, output)

        elif choice == "2":
            image_path = input("Шлях до зображення: ")

            text = extract_text(image_path)

            print("Прихований текст:")
            print(text)

        elif choice == "3":
            original = input("Оригінальне зображення: ")
            stego = input("Зображення з текстом: ")

            compare_images(original, stego)

        elif choice == "0":
            break

        else:
            print("Невірний вибір")

if __name__ == "__main__":
    main()