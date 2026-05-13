import os
import re

def text_to_binary(text):
    return ''.join(format(ord(c), '08b') for c in text)

def binary_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(c, 2)) for c in chars if len(c) == 8)

ZW0 = '\u200b'
ZW1 = '\u200c'

def hide_zero_width(container, secret):
    binary = text_to_binary(secret)
    length = format(len(binary), '016b')
    full = length + binary

    result = container
    for bit in full:
        result += ZW1 if bit == '1' else ZW0

    return result

def extract_zero_width(text):
    binary = ''
    for c in text:
        if c == ZW0:
            binary += '0'
        elif c == ZW1:
            binary += '1'

    if len(binary) < 16:
        return "Error: no hidden data found"

    length = int(binary[:16], 2)
    data = binary[16:16+length]

    return binary_to_text(data)


def hide_case(container, secret):
    binary = text_to_binary(secret)

    result = list(container)
    j = 0

    for i in range(len(result)):
        if result[i].isalpha() and j < len(binary):
            result[i] = result[i].upper() if binary[j] == '1' else result[i].lower()
            j += 1

    if j < len(binary):
        raise Exception("Not enough letters in container text!")

    return ''.join(result)

def extract_case(text):
    binary = ''

    for c in text:
        if c.isalpha():
            binary += '1' if c.isupper() else '0'

    return binary_to_text(binary)


def hide_spaces(container, secret):
    binary = text_to_binary(secret)
    words = container.split()

    if len(binary) > len(words) - 1:
        raise Exception("Not enough spaces!")

    result = '' 

    for i, word in enumerate(words):
        result += word
        if i < len(binary):
            result += '  ' if binary[i] == '1' else ' '
        elif i < len(words) - 1:
            result += ' '

    return result

def extract_spaces(text):
    binary = ''
    i = 0

    while i < len(text) - 1:
        if text[i] == ' ':
            if text[i+1] == ' ':
                binary += '1'
                i += 2
            else:
                binary += '0'
                i += 1
        else:
            i += 1

    return binary_to_text(binary)


def hide_color(container, secret):
    binary = text_to_binary(secret)

    result = ""
    for i, c in enumerate(container):
        if i < len(binary):
            color = "red" if binary[i] == '1' else "black"
            result += f'<span style="color:{color}">{c}</span>'
        else:
            result += c

    return result

def extract_color(html):
    matches = re.findall(r'color:(red|black)', html)
    binary = ''.join('1' if m == 'red' else '0' for m in matches)
    return binary_to_text(binary)


def save_file(filename, text):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)

def load_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def caesar_encrypt(text, shift=3):
    return ''.join(chr(ord(c) + shift) for c in text)

def caesar_decrypt(text, shift=3):
    result = ""
    for c in text:
        result += chr((ord(c) - shift) % 0x110000)
    return result


def menu():
    while True:
        print("\n1. Hide message")
        print("2. Extract message")
        print("0. Exit")

        choice = input("Your choice: ")

        if choice == '1':
            container = input("Enter container text: ")
            secret = input("Enter secret message: ")

            enc = input("Encrypt message? (y/n): ")
            if enc == 'y':
                secret = caesar_encrypt(secret)

            print("\nChoose method:")
            print("1 - Zero Width")
            print("2 - Case")
            print("3 - Spaces")
            print("4 - Color")

            method = input("Method: ")

            try:
                if method == '1':
                    result = hide_zero_width(container, secret)
                elif method == '2':
                    result = hide_case(container, secret)
                elif method == '3':
                    result = hide_spaces(container, secret)
                elif method == '4':
                    result = hide_color(container, secret)
                else:
                    continue

                print("\nStego text:")
                print(result)

                save = input("Save to file? (y/n): ")
                if save == 'y':
                    filename = input("Enter filename: ")
                    save_file(filename, result)

            except Exception as e:
                print("Error:", e)

        elif choice == '2':
            load = input("Load from file? (y/n): ")

            if load == 'y':
                filename = input("Enter filename: ")
                text = load_file(filename)
            else:
                text = input("Paste stego text: ")

            print("\nChoose method:")
            print("1 - Zero Width")
            print("2 - Case")
            print("3 - Spaces")
            print("4 - Color")

            method = input("Method: ")

            if method == '1':
                secret = extract_zero_width(text)
            elif method == '2':
                secret = extract_case(text)
            elif method == '3':
                secret = extract_spaces(text)
            elif method == '4':
                secret = extract_color(text)
            else:
                continue

            dec = input("Decrypt message? (y/n): ")
            if dec == 'y':
                secret = caesar_decrypt(secret)

            print("\nExtracted message:")
            print(secret)

        elif choice == '0':
            break


if __name__ == "__main__":
    menu()