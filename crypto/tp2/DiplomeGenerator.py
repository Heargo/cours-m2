from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from Signateur import Signateur
import qrcode
import uuid


class DiplomeGenerator:
    def __init__(self):
        self.img = Image.open("diplome-BG.png")

    def generate(self, output="diplome.png", name="John", date="01/01/2018", mention="", verification_url=""):

        if (mention is None):
            mention = ""

        self.add_text_center("Diplôme de Maître Table",
                             150, font="Raleway-medium.ttf", size=48)
        self.add_text_center("Ce diplôme certifie que", 230, size=20)
        self.add_text_center(name, 280, font="Tangerine-Bold.ttf", size=72)
        self.add_text_center(
            "à terminé le programme d'étude et obtenu ce diplôme", 380, size=20)
        self.add_text_center("le "+date, 420, size=20)
        if (mention != ""):
            self.add_text_center(mention, 460, size=24)

        if (verification_url != ""):
            self.add_qrcode(verification_url, name, date)
        # save image
        self.img.save(output)
        self.sign_diplome(
            output, "Diplôme de Maître Table, " + name + ", le "+date + " "+mention)

    def sign_diplome(self,  output, message):
        signer = Signateur(output)
        signer.encode(message, output)

    def add_qrcode(self, base_url, name, date, size=2):
        if (base_url[-1] != '/'):
            base_url += '/'

        # this uuid generation will need to be sync with database in production
        diplome_unique_id = str(uuid.uuid4())

        message = base_url + diplome_unique_id
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=size,
            border=0,
        )
        qr.add_data(message)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # get size of qr code
        w, h = img.size
        # center qr code
        x = (self.img.width - w) / 2
        y = 550

        self.img.paste(img, (int(x), int(y)))

    def add_text(self, text, x, y, font="Raleway-medium.ttf", size=32, color="black"):
        draw = ImageDraw.Draw(self.img)
        font = ImageFont.truetype(font, size)
        draw.text((x, y), text, color, font)

    def add_text_center(self, text, y, font="Raleway-medium.ttf", size=32, color="black"):
        draw = ImageDraw.Draw(self.img)
        font = ImageFont.truetype(font, size)
        bbox = font.getbbox(text)
        w = bbox[2] - bbox[0]
        draw.text(((self.img.width - w) / 2, y), text, color, font)
