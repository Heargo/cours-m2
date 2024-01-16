from PIL import Image
import os


class EncodeurDecodeur:
    END_MESSAGE = "######"

    def __init__(self, image):
        self.image = Image.open(image)

    def encode(self, message, output="output.png"):
        return self.write_message(message, output)

    def decode(self):
        return self.read()

    def write(self, message, output="output.png"):
        # convert to rgb
        img = self.image.convert('RGB')
        pixels = img.load()
        width, height = img.size

        # convert message to binary
        encoded_message = message + self.END_MESSAGE
        binary_message = ''.join(
            format(ord(i), '08b') for i in encoded_message)
        for j in range(height):
            for i in range(width):
                r, g, b = pixels[i, j]
                numberPixel = j * width + i
                if numberPixel < len(binary_message):
                    # change least significant bit of red same as binary message
                    val = int(binary_message[numberPixel])
                    r = (r & ~1) | val
                    pixels[i, j] = (r, g, b)
                    # update image with new pixel
                    img.putpixel((i, j), (r, g, b))
        img.save('output.png')
        return img

    def read(self):
        # convert to rgb
        img = self.image.convert('RGB')
        pixels = img.load()
        width, height = img.size

        decoded_message_binary = ''
        for j in range(height):
            for i in range(width):
                r, g, b = pixels[i, j]
                if r % 2 == 0:
                    decoded_message_binary += '0'
                else:
                    decoded_message_binary += '1'

        # convert binary to string
        decoded_message = ''
        for i in range(0, len(decoded_message_binary), 8):
            decoded_message += chr(int(decoded_message_binary[i:i+8], 2))
        return decoded_message.split(self.END_MESSAGE)[0]
