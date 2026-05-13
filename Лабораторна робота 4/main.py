import wave
import numpy as np
import matplotlib.pyplot as plt

def embed_message(input_wav: str, output_wav: str, message: str):

    message += chr(0)

    bits = ''.join(f'{ord(char):08b}' for char in message)

    with wave.open(input_wav, 'rb') as wav:
        params = wav.getparams()
        frames = wav.readframes(params.nframes)

    samples = np.frombuffer(frames, dtype=np.int16)

    if len(bits) > len(samples):
        raise ValueError("Повідомлення занадто довге для цього WAV-файлу")

    modified_samples = samples.copy()

    for i, bit in enumerate(bits):
        modified_samples[i] = (modified_samples[i] & ~1) | int(bit)

    with wave.open(output_wav, 'wb') as wav:
        wav.setparams(params)
        wav.writeframes(modified_samples.tobytes())

    print(f"\nПовідомлення успішно приховано у файл: {output_wav}")

def extract_message(stego_wav: str) -> str:

    with wave.open(stego_wav, 'rb') as wav:
        frames = wav.readframes(wav.getnframes())

    samples = np.frombuffer(frames, dtype=np.int16)

    bits = ''.join(str(sample & 1) for sample in samples)

    chars = [
        chr(int(bits[i:i + 8], 2))
        for i in range(0, len(bits), 8)
    ]

    message = ''.join(chars).split(chr(0))[0]

    return message

def plot_waveforms(wav1: str, wav2: str):

    def read_wav(path):
        with wave.open(path, 'rb') as wav:
            sample_rate = wav.getframerate()
            frames = wav.readframes(wav.getnframes())

        data = np.frombuffer(frames, dtype=np.int16)

        time = np.linspace(
            0,
            len(data) / sample_rate,
            num=len(data)
        )

        return time, data

    t1, s1 = read_wav(wav1)
    t2, s2 = read_wav(wav2)

    plt.figure(figsize=(12, 6))

    plt.subplot(2, 1, 1)
    plt.plot(t1, s1)
    plt.title("Оригінальний WAV")
    plt.xlabel("Час (с)")
    plt.ylabel("Амплітуда")

    plt.subplot(2, 1, 2)
    plt.plot(t2, s2, linestyle='--')
    plt.title("WAV із прихованим повідомленням")
    plt.xlabel("Час (с)")
    plt.ylabel("Амплітуда")

    plt.tight_layout()
    plt.show()

def main():

    while True:

        print("\n====== Стеганографія WAV (LSB) ======")
        print("1. Приховати повідомлення")
        print("2. Вилучити повідомлення")
        print("3. Порівняти графіки WAV")
        print("4. Вихід")

        choice = input("Оберіть опцію: ")

        if choice == '1':

            input_wav = input("Шлях до оригінального WAV: ")
            output_wav = input("Шлях для збереження стего WAV: ")
            message = input("Введіть повідомлення: ")

            try:
                embed_message(input_wav, output_wav, message)
            except Exception as e:
                print("Помилка:", e)

        elif choice == '2':

            stego_wav = input("Шлях до стего WAV: ")

            try:
                message = extract_message(stego_wav)

                print("\nВилучене повідомлення:")
                print(message)

            except Exception as e:
                print("Помилка:", e)

        elif choice == '3':

            wav1 = input("Шлях до оригінального WAV: ")
            wav2 = input("Шлях до стего WAV: ")

            try:
                plot_waveforms(wav1, wav2)
            except Exception as e:
                print("Помилка:", e)

        elif choice == '4':

            print("Програму завершено.")
            break

        else:
            print("Невірна опція!")


if __name__ == "__main__":
    main()