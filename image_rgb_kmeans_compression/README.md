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

**Original Image**

![orig](./images/git_push.png)

**k=2**

![k2](./images/git_push_2colors_transf.png)

**k=4**

![k4](./images/git_push_4colors_transf.png)

**k=10**

![k10](./images/git_push_10colors_transf.png)


**k=100**

![k100](./images/git_push_100colors_transf.png)


**k=1000**
