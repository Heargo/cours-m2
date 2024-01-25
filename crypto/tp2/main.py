# read args from command line
import argparse
import os
from PIL import Image
from EncodeurDecodeur import EncodeurDecodeur
from Signateur import Signateur
from DiplomeGenerator import DiplomeGenerator


def open_image(image_path):
    image = Image.open(image_path)
    return image


def encode_message_in_image(path, message, encodeur_decodeur):
    img = open_image(path)
    encodeur_decodeur.encode(message)


def decode_message_in_image(path, algorithm):
    img = open_image(path)
    message = encodeur_decodeur.decode()
    print("decoded message is:", message)


if (__name__ == '__main__'):
    parser = argparse.ArgumentParser(description='TP2 - crypto')
    parser.add_argument(
        '-i', '--image', help='Input image (png or ppm format)', required=False)
    parser.add_argument('-m', '--message',
                        help='message to encode', required=False)
    parser.add_argument('-a', '--algorithm', help='Algorithm', required=False)
    parser.add_argument(
        '-d', '--decrypt', help='if not specified, the message will be encrypted', required=False)
    parser.add_argument('-n', '--name', help='name', required=False)
    parser.add_argument('-da', '--date', help='date', required=False)
    parser.add_argument('-me', '--mention', help='mention', required=False)
    parser.add_argument('-o', '--output', help='output file', required=False)
    parser.add_argument('-f', '--function', help='function', required=False)
    parser.add_argument('-vu', '--verification-url',
                        help='url to verify the certificate, example: https://some-university.com/diplome/verify', required=False, default="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    args = parser.parse_args()

    # # check if input file exists
    # if (not os.path.isfile(args.image)):
    #     print('Input file does not exist')
    #     exit(1)

    # # check if algorithm is valid
    # if (args.algorithm not in ['basic', 'sign']):
    #     print('Algorithm not supported')
    #     exit(1)

    algo = None
    diplome_generator = DiplomeGenerator()

    if (args.function == 'generate'):
        error = False
        if (args.name is None):
            print('name is required')
            error = True
        if (args.date is None):
            print('date is required')
            error = True

        if (error):
            exit(1)

        diplome_generator.generate(
            args.output, args.name, args.date, args.mention, args.verification_url)
        exit(0)

    if (args.function == 'stenography'):
        if (args.algorithm == 'basic'):
            encodeur_decodeur = EncodeurDecodeur(args.image)
        elif (args.algorithm == 'sign'):
            encodeur_decodeur = Signateur(args.image)

        if (args.decrypt is None):
            print("encrypting message...")
            encode_message_in_image(
                args.image, args.message, encodeur_decodeur)
        else:
            print("decrypting message...")
            decode_message_in_image(args.image, encodeur_decodeur)
