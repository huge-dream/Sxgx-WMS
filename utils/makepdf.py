import traceback

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from barcode.codex import Code128
from barcode.writer import ImageWriter
from io import BytesIO
import os
from django.conf import settings
from greaterwms.celery import app
from traceback import format_exc

data = [{
    'id': 1,
    'patch_number': 'WH21-Z-2225-1',
    'brand': 'MADE IN CHINA',
    'barcode': '876e09fb76428b0beede86fbefe3a866',
    'total': 5,
    'goods_code': 'AT-68',
    'address': 'EA',
    'country': 'US',
},{
    'id': 2,
    'patch_number': 'WH21-Z-3333-5',
    'brand': 'MADE IN CHINA',
    'barcode': '12d81a624d62d77e1eb057c118c95141',
    'total': 10,
    'goods_code': 'AT-50',
    'address': 'BO',
    'country': 'AS',
},
]

base_dir = settings.BASE_DIR

class DrawImg:

    def __init__(self, img_fp=None):
        self.img_fp = img_fp
        self.draw = None
        self.size_x, self.size_y = None, None
        self.font_path = os.path.join(base_dir, 'media/asn_label/arial.ttf')
        self.goods = {}
        self.folder = ''

    def get_font(self, size):
        return ImageFont.truetype(font=self.font_path, size=size)

    def draw_patch(self, text):
        font = self.get_font(80)
        text_width, text_height = font.getbbox(text)[2:]
        char_width = int(text_width / len(text))
        start_x = int((self.size_x - text_width) / 2)
        start_y = 150
        self.draw.text(xy=(start_x, start_y), text=text, fill=(0, 0, 0), font=font)

    def draw_pk(self, text):
        font = self.get_font(100)
        text_width, text_height = font.getbbox(text)[2:]
        char_width = int(text_width / len(text))
        start_x = int((self.size_x - text_width) / 2)
        start_y = 28
        self.draw.text(xy=(start_x, start_y), text=text, fill=(255, 255, 255), font=font)

    def draw_address(self, text):
        font = self.get_font(90)
        text_width, text_height = font.getbbox(text)[2:]
        char_width = int(text_width / len(text))
        start_x = 750
        start_y = 30
        self.draw.text(xy=(start_x, start_y), text=text, fill=(0, 0, 0), font=font)

    def draw_country(self, text):
        font = self.get_font(90)
        text_width, text_height = font.getbbox(text)[2:]
        char_width = int(text_width / len(text))
        start_x = 120
        start_y = 30
        self.draw.text(xy=(start_x, start_y), text=text, fill=(0, 0, 0), font=font)
    
    def draw_prefix(self, text):
        font = self.get_font(50)
        text_width, text_height = font.getbbox(text)[2:]
        char_width = int(text_width / len(text))
        start_x = 20
        start_y = 520
        self.draw.text(xy=(start_x, start_y), text=text, fill=(0, 0, 0), font=font)
    
    def draw_madeinchina(self, text):
        font = self.get_font(50)
        text_width, text_height = font.getbbox(text)[2:]
        char_width = int(text_width / len(text))
        start_x = 600
        start_y = 520
        self.draw.text(xy=(start_x, start_y), text=text, fill=(0, 0, 0), font=font)

    def draw_sku(self, text):
        font = ImageFont.truetype(font=self.font_path, size=80)
        text_width, text_height = font.getbbox(text)[2:]
        char_width = int(text_width / len(text))
        start_x = int((self.size_x - text_width) / 2)
        start_y = 420
        self.draw.text(xy=(start_x, start_y), text=text, fill=(0, 0, 0), font=font)

    def draw_barcode(self, code, patch):
        self.check_folder()
        bc = Code128(code, writer=ImageWriter())
        ph = os.path.join(base_dir, f'media/asn_label/{patch}/{code}')
        opt = {'write_text': False, 'quiet_zone': 2, 'text_distance': 10}
        bc.save(ph, opt)
        codeimg = Image.open(ph+'.png')
        out = codeimg.resize((750,180))
        self.img_fp.paste(out, (int((self.size_x - 750) / 2), 240))

    def check_folder(self):
        if self.goods['patch_number'] not in os.listdir(os.path.join(base_dir, 'media/asn_label/')):
            os.mkdir(self.folder)

    def save(self, i=None):
        filename = os.path.join(self.folder, f'{self.goods["goods_code"]}{"" if i is None else f"-{i}"}.jpg')
        self.img_fp.save(filename)
    
    def make(self, data):
        self.goods = data
        self.folder = os.path.join(base_dir, f'media/asn_label/{self.goods["patch_number"]}/')
        label_file_list = []
        for i in range(data['total']):
            self.img_fp = Image.open(os.path.join(base_dir, 'media/asn_label/base_label.jpg'))
            self.draw = ImageDraw.Draw(self.img_fp)
            self.size_x, self.size_y = self.img_fp.size
            self.draw_patch(data['patch_number'])
            self.draw_pk(str(data['id']))
            self.draw_address(data['address'])
            self.draw_country(data['country'])
            self.draw_prefix(f'{i+1}/{data["total"]}')
            self.draw_madeinchina(data['brand'])
            self.draw_sku(data['goods_code'])
            # self.draw_barcode(data['barcode'], data['patch_number'])
            self.draw_barcode(data['goods_code'], data['patch_number'])
            self.save(i+1)
            label_file_list.append(os.path.join(self.folder, f'{self.goods["goods_code"]}-{i+1}.jpg'))
        return label_file_list


def generate_label_files(data):
    draw = DrawImg()
    patch_file_list = list()
    for i in data:
        patch_file_list.append(draw.make(i))
    return patch_file_list

# @app.task
import funboost
@funboost.boost('makepdf', broker_kind=funboost.BrokerEnum.PERSISTQUEUE, log_level=21)
def generate_pdf(data, patch):
    try:
        patch_file_list = generate_label_files(data)
        images = []
        output = None
        for i in patch_file_list:
            # print('the list length is', len(i))
            if output is None:
                output = Image.open(i[0])
            for j in i:
                # print(j)
                img = Image.open(j)
                images.append(img)
            # print('next list')
        # print('all imgs have', len(images))
        # print('generate pdf start, file is', f'media/asn_label/{patch}/{patch}.pdf')
        output.save(
            os.path.join(base_dir, f'media/asn_label/{patch}/{patch}.pdf'),
            'pdf', save_all=True, append_images=images[1:]
        )
        # print('generate pdf end')
    except:
        print(traceback.format_exc())

