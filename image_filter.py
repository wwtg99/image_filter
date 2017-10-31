import argparse
import os
from PIL import Image, ImageDraw, ImageFont
import filters


NAME = 'Image Filter'
DESR = 'Collection of image filters.'
VERSION = '0.1.0'
FILTERS = {
    'rgb': 'Rgb',
    'rgba': 'Rgba',
    'grey': 'Greyscale',
    'hand_drawn': 'HandDrawn',
    'edge_curve': 'EdgeCurve',
    'blur': 'Blur',
    'contour': 'Contour',
    'edge_enhance': 'EdgeEnhance',
    'emboss': 'Emboss',
    'smooth': 'Smooth',
    'sharpen': 'Sharpen',
    'gaussian_blur': 'GaussianBlur',
    'min': 'MinFilter',
    'median': 'MedianFilter',
    'max': 'MaxFilter',
    'mode': 'ModeFilter',
    'unsharp_mask': 'UnsharpMask',
    'emboss_45d': 'Emboss45d',
    'sharp_edge': 'SharpEdge',
    'sharp_center': 'SharpCenter',
    'emboss_asym': 'EmbossAsymmetric',
}


def show_filters():
    [print(x) for x in FILTERS]


def parse_args(args):
    if not args.input or not os.path.exists(args.input):
        print('Invalid input')
        return None
    inp = args.input
    output = args.output
    if not output:
        output = './'
    output_type = args.type
    if not output_type:
        output_type = os.path.splitext(args.input)[1].strip('.')
    if args.param:
        p = dict([k.split('=') for k in args.param])
    else:
        p = {}
    if args.water_mark:
        if not os.path.exists(args.water_mark):
            print('Invalid water mark')
            return None
    if args.font_color:
        fcolor = tuple([int(x) for x in args.font_color.split(',')])
    else:
        fcolor = (0, 0, 0, 255)
    return {'input': inp, 'output': output, 'output_type': output_type, 'param': p, 'width': args.width,
            'height': args.height, 'water_mark': args.water_mark, 'water_mark_text': args.water_mark_text,
            'water_mark_pos': args.water_mark_pos, 'font': args.font, 'font_size': args.font_size,
            'font_color': fcolor}


def run(args):
    a = parse_args(args)
    if a is None:
        return
    image = Image.open(a['input'])
    # filters
    if args.all_filters:
        out = [call_filter(f, image, a) for f in FILTERS]
    else:
        fs = args.filter
        if not fs:
            fs = list(FILTERS.keys())[0:1]
        out = [call_filter(f, image, a) for f in fs if f in FILTERS]


def call_filter(name, image, args):
    print('Filter image by %s' % name)
    # filter
    f = getattr(filters, FILTERS[name])(image)
    params = args['param']
    im2 = f.filter(**params)
    output = args['output']
    outtype = args['output_type']
    # resize
    if args['width'] or args['height']:
        resize(im2, args['width'], args['height'])
    # water mark
    if args['water_mark']:
        im2 = water_mark(im2, args['water_mark'], args['water_mark_pos'])
    elif args['water_mark_text']:
        im2 = text_water_mark(im2, args['water_mark_text'], pos=args['water_mark_pos'], font=args['font'],
                              font_size=args['font_size'], font_color=args['font_color'])
    # output
    if outtype in ['BMP', 'EPS', 'JPEG', 'PCX', 'PPM']:
        im2 = im2.convert('RGB')
    if os.path.isdir(output):
        if outtype == 'JPEG':
            ext = 'jpg'
        else:
            ext = outtype.lower()
        fout = output + name + '.' + ext
        im2.save(fout, outtype)
        print('Output to %s' % fout)
    else:
        fout = output
        im2.save(output, outtype)
        print('Output to %s' % output)
    return fout


def resize(image, width, height):
    print('Resize image')
    if not width:
        width = image.size[0]
    if not height:
        height = image.size[1]
    image.thumbnail((width, height), Image.LANCZOS)
    return image


def water_mark(image, mark, pos='LT'):
    mark_im = Image.open(mark).convert('RGBA')
    bw, bh = image.size
    lw, lh = mark_im.size
    pos = pos.upper()
    if pos == 'LT':  # left top
        size = (0, 0)
    elif pos == 'RT':  # right top
        size = (bw-lw, 0)
    elif pos == 'LB':  # left bottom
        size = (0, bh-lh)
    else:  # right bottom
        size = (bw-lw, bh-lh)
    layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
    layer.paste(mark_im, size)
    image = Image.alpha_composite(image.convert('RGBA'), layer)
    return image


def text_water_mark(image, text, pos, font='Helvetica', font_size=20, font_color=(0, 0, 0, 255)):
    txt = Image.new('RGBA', image.size, (0, 0, 0, 0))
    bw, bh = txt.size
    font = ImageFont.truetype(font, font_size)
    fw, fh = font.getsize(text)
    pos = pos.upper()
    if pos == 'LT':  # left top
        size = (0, 0)
    elif pos == 'RT':  # right top
        size = (bw - fw, 0)
    elif pos == 'LB':  # left bottom
        size = (0, bh - fh)
    else:  # right bottom
        size = (bw - fw, bh - fh)
    d = ImageDraw.Draw(txt, 'RGBA')
    d.text(size, text, fill=font_color, font=font)
    image = Image.alpha_composite(image.convert('RGBA'), txt)
    return image


def main():
    arg = argparse.ArgumentParser(description=DESR)
    arg.add_argument('-v', '--version', action='version', version=NAME + ' ' + VERSION)
    arg.add_argument('-l', '--list', action='store_true', help='List Filters.')
    arg.add_argument('-f', '--filter', help='Filter name or a list of names.', nargs='+')
    arg.add_argument('--all-filters', help='Use all filters, disregard --filter option if exists', action='store_true')
    arg.add_argument('-i', '--input', help='Input images path.')
    arg.add_argument('-o', '--output', help='Output image path or directory (for multi filters).')
    arg.add_argument('-t', '--type',
                     help='Output image type used for directory output, default JPEG, more information please refer '
                          'to http://pillow.readthedocs.io/en/3.3.x/handbook/image-file-formats.html', default='JPEG')
    arg.add_argument('-a', '--param', help='Filter parameters', action='append')
    arg.add_argument('--width', help='Image width (height can be calculated), can be used to create thumbnail', type=int)
    arg.add_argument('--height', help='Image height (width can be calculated), can be used to create thumbnail', type=int)
    arg.add_argument('-m', '--water-mark', help='Add water mark to image, mutually exclusive with --water-mark-text')
    arg.add_argument('-x', '--water-mark-text', help='Add water mark text, mutually exclusive with --water-mark')
    arg.add_argument('-p', '--water-mark-pos', help='Add water mark position: LT(left top, default), RT(right top), LB(left bottom, RB(right bottom)', default='LT')
    arg.add_argument('--font', help='Font for water mark text, default Helvetica', default='Helvetica')
    arg.add_argument('--font-size', help='Font size for water mark text in points, default 20', default=20, type=int)
    arg.add_argument('--font-color', help='Font color for water mark text (4 int), default 0,0,0,255', default='0,0,0,255')
    parser = arg.parse_args()
    if parser.list:
        show_filters()
        exit()
    else:
        run(parser)


if __name__ == '__main__':
    main()
