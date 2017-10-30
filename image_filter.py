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


def run(args):
    if not args.input or not os.path.exists(args.input):
        print('Invalid input')
        return
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
    image = Image.open(args.input)
    # filters
    if args.all_filters:
        out = [call_filter(f, image, output, output_type, p) for f in FILTERS]
    else:
        fs = args.filter
        if not fs:
            fs = list(FILTERS.keys())[0:1]
        out = [call_filter(f, image, output, output_type, p) for f in fs if f in FILTERS]


def call_filter(name, image, output, outtype='jpg', params={}):
    print('Filter image by %s' % name)
    filter = getattr(filters, FILTERS[name])(image)
    im2 = filter.filter(**params)
    if os.path.isdir(output):
        fout = output + name + '.' + outtype
        im2.save(fout)
        print('Output to %s' % fout)
    else:
        fout = output
        im2.save(output)
        print('Output to %s' % output)
    return fout


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
    parser = arg.parse_args()
    if parser.list:
        show_filters()
        exit()
    else:
        run(parser)


if __name__ == '__main__':
    main()
