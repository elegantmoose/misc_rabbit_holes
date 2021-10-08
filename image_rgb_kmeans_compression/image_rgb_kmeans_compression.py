"""
Reduce an image to its k primary RGB colors using k-means clustering.

@author: elegantmoose
"""

import argparse
import copy
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans


def _get_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'image_fp',
        help='image filepath'
    )

    parser.add_argument(
        '-k',
        action='store',
        default=2,
        type=int,
        dest='k_colors',
        help='number of colors'
    )

    return parser


def main():
    args = _get_argparser().parse_args()
    image = Image.open(args.image_fp)
    image_array = np.array(image)
    
    # stripping alpha (pixel transparency)
    rgb_image_array = np.zeros((int(len(image_array)), int(len(image_array[0])), 3))
    for i in range(len(image_array)):
        for j in range(len(image_array[0])):
            rgb_image_array[i][j] = [image_array[i][j][0],image_array[i][j][1], image_array[i][j][2]]


    # (deterministic order of) rgb vectors
    rgb_vectors = [rgb_image_array[i][j] for i in range(len(rgb_image_array)) for j in range(len(rgb_image_array[0]))]
    assert len(rgb_vectors) == (len(rgb_image_array) * len(rgb_image_array[0]))

    # k-means tansform of image
    kmeans = KMeans(n_clusters=args.k_colors, random_state=0).fit(rgb_vectors)

    # round cluster centers (i.e to rgb color values)
    cluster_centers = np.uint8(kmeans.cluster_centers_)
    
    print(f'RGB k-clusters:\n {cluster_centers}')

    # transform original rgb image array values to k-cluster rbg values
    transf_rgb_image_array = np.zeros((int(len(image_array)), int(len(image_array[0])), 3))
    n = len(rgb_image_array[0])
    for i in range(len(transf_rgb_image_array)):
        for j in range(len(transf_rgb_image_array[0])):
            column_major_index = (i * n) + j
            k_class = kmeans.labels_[column_major_index]
            transf_rgb_image_array[i][j] = cluster_centers[k_class]

    # convert back to rgb array
    transf_image = Image.fromarray((transf_rgb_image_array * 255).astype(np.uint8))
    
    # Dump
    filename, ext = args.image_fp.split('.')
    transf_image.save(f'{filename}_{args.k_colors}colors_transf.{ext}')


if __name__ == '__main__':
    main()
