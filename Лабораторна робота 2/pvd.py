import math
from PIL import Image
import os


RANGE_TABLE = [
    (0, 7), (8, 15), (16, 31),
    (32, 63), (64, 127), (128, 255)
]

INPUT_DIR = "download"
OUTPUT_DIR = "result"

def get_interval(diff):
    abs_diff = abs(diff)
    for low, high in RANGE_TABLE:
        if low <= abs_diff <= high:
            return low, high
    return None, None

def is_png_file(path):
    return path.lower().endswith(".png")

def clamp_value(val):
    return max(0, min(255, val))

def compute_capacity(image):
    pixels = image.load()
    width, height = image.size

    capacity_bits = 0

    for y in range(height):
        for x in range(0, width - 1, 2):
            _, _, b1 = pixels[x, y]
            _, _, b2 = pixels[x + 1, y]

            diff = b2 - b1
            low, high = get_interval(diff)

            if low is None:
                continue

            capacity_bits += int(math.log2(high - low + 1))

    return capacity_bits

def encode_image(input_path, output_path, message):
    if not is_png_file(input_path):
        print("Only PNG files are supported")
        return

    img = Image.open(input_path).convert("RGB")
    pixels = img.load()
    width, height = img.size

    binary_message = ''.join(format(ord(c), '08b') for c in message) + '00000000'

    capacity = compute_capacity(img)

    if len(binary_message) > capacity:
        print("Message is too large for this image")
        return

    index = 0

    for y in range(height):
        for x in range(0, width - 1, 2):

            if index >= len(binary_message):
                img.save(output_path)
                print("Encoding finished")
                return

            r1, g1, b1 = pixels[x, y]
            r2, g2, b2 = pixels[x + 1, y]

            diff = b2 - b1
            low, high = get_interval(diff)

            if low is None:
                continue

            n_bits = int(math.log2(high - low + 1))

            chunk = binary_message[index:index + n_bits].ljust(n_bits, '0')
            value = int(chunk, 2)

            new_diff = low + value
            m = new_diff - abs(diff)

            if diff >= 0:
                b1_new = b1 - m // 2
                b2_new = b2 + (m - m // 2)
            else:
                b1_new = b1 + m // 2
                b2_new = b2 - (m - m // 2)

            b1_new = clamp_value(b1_new)
            b2_new = clamp_value(b2_new)

            pixels[x, y] = (r1, g1, b1_new)
            pixels[x + 1, y] = (r2, g2, b2_new)

            index += n_bits

    img.save(output_path)
    print("File saved\n")

def decode_image(input_path):
    if not is_png_file(input_path):
        print("Only PNG files are supported")
        return

    img = Image.open(input_path).convert("RGB")
    pixels = img.load()
    width, height = img.size

    bitstream = ""

    for y in range(height):
        for x in range(0, width - 1, 2):

            _, _, b1 = pixels[x, y]
            _, _, b2 = pixels[x + 1, y]

            diff = b2 - b1
            low, high = get_interval(diff)

            if low is None:
                continue

            n_bits = int(math.log2(high - low + 1))
            value = abs(diff) - low

            bitstream += format(value, f'0{n_bits}b')

    message = ""

    for i in range(0, len(bitstream), 8):
        byte = bitstream[i:i + 8]
        if byte == "00000000":
            break
        message += chr(int(byte, 2))

    print(message)

if __name__ == "__main__":
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    while True:
        mode = input("Select mode:\n1 - Encode\n2 - Decode\n0 - Exit\n> ")
    
        if mode == "1":
            file_name = input("Input file name: ")
            text = input("Message: ")

            encode_image(
                os.path.join(INPUT_DIR, file_name),
                os.path.join(OUTPUT_DIR, "encoded_" + file_name),
                text
            )

        elif mode == "2":
            file_name = input("File name: ")

            decode_image(
                os.path.join(OUTPUT_DIR, file_name)
            )
        else:
            break;