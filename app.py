from PIL import Image
import numpy as np


def dct2(block):
    return np.fft.fft2(block)


def idct2(block):
    return np.fft.ifft2(block)


def embed_bit(value, bit):
    return (value & ~1) | bit


def embed_data(image, data, key):
    global passw
    passw = key
    data = np.unpackbits(np.array(list(data), dtype=np.uint8))
    data_len = len(data)
    width, height = image.size
    image_array = np.array(image)

    if data_len > width * height:
        raise ValueError("Insufficient space in the image to embed the data")

    flat_image = image_array.flatten()
    for i in range(data_len):
        flat_image[i] = embed_bit(flat_image[i], data[i])

    embedded_image_array = flat_image.reshape(image_array.shape)
    embedded_image = Image.fromarray(embedded_image_array)
    return embedded_image


def extract_data(image, data_len):
    image_array = np.array(image)
    flat_image = image_array.flatten()[:data_len]
    extracted_data = [pixel & 1 for pixel in flat_image]
    extracted_bytes = np.packbits(extracted_data)[:data_len]
    return extracted_bytes


if __name__ == "__main__":
    # Embedding
    cover_image = Image.open("cover_image.jpg")
    secret_key = input("Secret_key")
    secret_data = input("Enter the secret message: ")
    secret_data = bytes(secret_data, "utf-8")
    stego_image = embed_data(cover_image, secret_data, secret_key)
    stego_image.save("stego_image.jpg")

    # Extraction
    secret_key = input("Secret_key")
    if secret_key == passw:
        extracted_data = extract_data(stego_image, len(secret_data) * 8)
        decoded_data = extracted_data.tobytes().decode()
        print("Extracted data:", decoded_data)
    else:
        print("invalid key")
