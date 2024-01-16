# read args from command line
import argparse
import os
from Crypto.Cipher import AES
from PIL import Image


END_MESSAGE = "######"


def open_image(image_path):
    image = Image.open(image_path)
    return image


def basic_encrypt_encode(img, message):
    # convert to rgb
    img = img.convert('RGB')
    pixels = img.load()
    width, height = img.size

    # convert message to binary
    encoded_message = message + END_MESSAGE
    binary_message = ''.join(
        format(ord(i), '08b') for i in encoded_message)
    for i in range(width):
        for j in range(height):
            r, g, b = pixels[i, j]
            numberPixel = i * width + j
            if numberPixel < len(binary_message):
                # change least significant bit of red same as binary message
                val = int(binary_message[numberPixel])
                r = (r & ~1) | val
                pixels[i, j] = (r, g, b)
                # update image with new pixel
                img.putpixel((i, j), (r, g, b))
    return img


def basic_decrypt_decode(img):
    # convert to rgb
    img = img.convert('RGB')
    pixels = img.load()
    width, height = img.size

    decoded_message_binary = ''
    for i in range(width):
        for j in range(height):
            r, g, b = pixels[i, j]
            if r % 2 == 0:
                decoded_message_binary += '0'
            else:
                decoded_message_binary += '1'

    # convert binary to string
    # print("binary is", decoded_message_binary)
    decoded_message = ''
    for i in range(0, len(decoded_message_binary), 8):
        decoded_message += chr(int(decoded_message_binary[i:i+8], 2))
        # if (i <= 30):
        #     print(decoded_message_binary[i:i+8], "is ", int(
        #         decoded_message_binary[i:i+8], 2), "is", chr(int(decoded_message_binary[i:i+8], 2)))
    return decoded_message


def encode_message_in_image(path, message, algorithm):
    print('Encoding message in image...')
    img = open_image(path)
    new_img = algorithm(img, message)
    new_img.save('output.png')


def decode_message_in_image(path, algorithm):
    print('Decoding message in image...')
    img = open_image(path)
    message = algorithm(img)
    clean_msg = message.split(END_MESSAGE)[0]
    print("decoded message is:", clean_msg)


if (__name__ == '__main__'):
    parser = argparse.ArgumentParser(description='TP2 - Criptografia')
    parser.add_argument(
        '-i', '--image', help='Input image (png or ppm format)', required=True)
    parser.add_argument('-m', '--message',
                        help='message to encode', required=False)
    parser.add_argument('-a', '--algorithm', help='Algorithm', required=True)
    parser.add_argument(
        '-d', '--decrypt', help='if not specified, the message will be encrypted', required=False)
    args = parser.parse_args()

    print('Input file: ', args.image)
    print('Message: ', args.message)
    print('Algorithm: ', args.algorithm)
    print('Decrypt: ', args.decrypt)

    # check if input file exists
    if (not os.path.isfile(args.image)):
        print('Input file does not exist')
        exit(1)

    # check if it's decrypt or encrypt
    if (args.decrypt != ''):
        print('you will decrypt')

    # check if algorithm is valid
    if (args.algorithm not in ['basic']):
        print('Algorithm not supported')
        exit(1)

    algo = None

    if (args.algorithm == 'basic'):
        if (args.decrypt is None):
            algorithm = basic_encrypt_encode
        else:
            algorithm = basic_decrypt_decode

    if (args.decrypt is None):
        print("encrypting message...")
        encode_message_in_image(args.image, args.message, algorithm)
    else:
        print("decrypting message...")
        decode_message_in_image(args.image, algorithm)
