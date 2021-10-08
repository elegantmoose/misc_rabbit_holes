# Image RGB - K-means Compression

## Operation

- Loads an image file
- Converts to RGB (if not)
- Runs k-means on the RGB vectors for specified k
- Converts cluster centers to approximate RGB pixel value
- Tansforms image pixels to image pixel of it cluster center
- Writes file


## Usage

```sh
python image_rgb_kmeans_compression.py <image file> -k <>
```

## Example

**k=2**

![k2](./imiages/git_push_2colors_transf.png)

**k=4**

**k=10**

**k=100**

**k=1000**
