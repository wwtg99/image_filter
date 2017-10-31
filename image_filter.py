import argparse
import os
from PIL import Image
import filters


NAME = 'Image Filter'
DESR = 'Collection of image filters.'
VERSION = '0.1.0'
FILTERS = {
    'rgb': 'Rgb',
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
    return {'input': inp, 'output': output, 'output_type': output_type, 'param': p, 'width': args.width,
            'height': args.height}


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
    # output
    if os.path.isdir(output):
        fout = output + name + '.' + outtype
        im2.save(fout)
        print('Output to %s' % fout)
    else:
        fout = output
        im2.save(output)
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


def main():
    arg = argparse.ArgumentParser(description=DESR)
    arg.add_argument('-v', '--version', action='version', version=NAME + ' ' + VERSION)
    arg.add_argument('-l', '--list', action='store_true', help='List Filters.')
    arg.add_argument('-f', '--filter', help='Filter name or a list of names.', nargs='+')
    arg.add_argument('--all-filters', help='Use all filters, disregard --filter option if exists', action='store_true')
    arg.add_argument('-i', '--input', help='Input images path.')
    arg.add_argument('-o', '--output', help='Output image path or directory (for multi filters).')
    arg.add_argument('-t', '--type', help='Output image type used for directory output')
    arg.add_argument('-a', '--param', help='Filter parameters', action='append')
    arg.add_argument('--width', help='Image width (height can be calculated), can be used to create thumbnail', type=int)
    arg.add_argument('--height', help='Image height (width can be calculated), can be used to create thumbnail', type=int)
    parser = arg.parse_args()
    if parser.list:
        show_filters()
        exit()
    else:
        run(parser)


if __name__ == '__main__':
    main()
