#!/usr/bin/python
# -*- coding: utf-8 -*-

"""argparse script for trivector"""

import os
import argparse
import sys

from trivector.trivector import trivector, DiagonalStyle


def get_parser():
    """Create and return the argparser for trivector"""
    parser = argparse.ArgumentParser(
        description="Convert an image into a ``.svg`` vector image composed "
                    "of triangles"
    )
    parser.add_argument("image", help="Path to the image to trivector")

    group = parser.add_argument_group("Image Generation Options")
    group.add_argument("-o", "--output", default=os.path.join(
                       ".", "<image_name>_tri_<cut_size>.svg"),
                       help="Path to output the trivectored image "
                            "(default: %(default)s)")
    group.add_argument("-c", "--cut-size", dest="cut_size", type=int,
                       required=True,
                       help="Size in pixels for each triangle sector "
                            "(smaller==more triangles)")
    group.add_argument("-d", "--diagonal-style", dest="diagonal_style",
                       type=DiagonalStyle, choices=list(DiagonalStyle),
                       default=DiagonalStyle.alternating.value,
                       help="Styling on how to arrange the triangle "
                            "sectors diagonals (default: %(default)s)")
    return parser


def main(argv=sys.argv[1:]):
    """argparse function for trivector"""
    parser = get_parser()
    args = parser.parse_args(argv)

    # generate or get the output image name
    image_name = os.path.basename(args.image)
    image_name, _ = os.path.splitext(image_name)
    if not args.output:
        output_path = os.path.join(
            os.getcwd(),
            "{}_tri_{}.svg".format(args.image, args.cut_size)
        )
    else:
        output_path = args.output

    trivector(
        image_path=args.image,
        cut_size=args.cut_size,
        output_path=output_path,
        diagonal_style=args.diagonal_style
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
