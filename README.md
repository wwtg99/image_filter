Image Filter
============

# Dependency
- Python3
- Numpy
- Pillow

# Usage
Show Help
```
python image_filter.py -h
```

List filters
```
python image_filter.py -l
```

Filter image
```
python image_filter.py -f grey -i images/test.jpg -o images/
```

Some filters need parameters

```
python image_filter.py -f gaussian_blur -i images/test.jpg -o images/ -a radius=3
```

# Filters
- rgb: RGB image
- grey: Grayscale
- hand_drawn: Hand drawn
- edge_curve: Find edges
- blur: Blur
- contour: Contour
- edge_enhance: Enhance edge
    - more: More enhancement
- emboss: Emboss
- smooth: Smooth
    - more: More smooth
- sharpen: Sharpen
- gaussian_blur: Gaussian blur
    - radius: Blur radius
- min: Picks the lowest pixel value in a window with the given size
    - size: 3 or 5, default 3
- median: Picks the median pixel value in a window with the given size
    - size: 3 or 5, default 3
- max: Picks the largest pixel value in a window with the given size
    - size: 3 or 5, default 3
- mode: Picks the most frequent pixel value in a box with the given size. Pixel values that occur only once or twice are ignored; if no pixel value occurs more than twice, the original pixel value is preserved
    - size: 3 or 5, default 3
- unsharp_mask: Unsharp mask
    - radius: Blur Radius, default 2
    - percent: Unsharp strength, in percent, default 150
    - threshold: Threshold controls the minimum brightness change that will be sharpened, default 3
- emboss_45d: Emboss from 45 degree
- sharp_edge: sharp edge
- sharp_center: sharp center
- emboss_asym: Asymmetric emboss

# Example

Origin 原图

![Origin](https://github.com/wwtg99/image_filter/blob/master/images/test.jpg)

---

RGB

![RGB](https://github.com/wwtg99/image_filter/blob/master/images/rgb.jpg)

---

Grayscale 灰度图

![Grayscale](https://github.com/wwtg99/image_filter/blob/master/images/grey.jpg)

---

Hand drawn 手绘图

![Hand drawn](https://github.com/wwtg99/image_filter/blob/master/images/hand_drawn.jpg)

---

Find edges 边缘线

![Find edges](https://github.com/wwtg99/image_filter/blob/master/images/edge_curve.jpg)

---

Blur 模糊

![Blur](https://github.com/wwtg99/image_filter/blob/master/images/blur.jpg)

---

Contour 描边

![Contour](https://github.com/wwtg99/image_filter/blob/master/images/contour.jpg)

---

Edge Enhance 边缘强化

![Edge Enhance](https://github.com/wwtg99/image_filter/blob/master/images/edge_enhance.jpg)

---

Emboss 浮雕

![Emboss](https://github.com/wwtg99/image_filter/blob/master/images/emboss.jpg)

---

Smooth 平滑

![Smooth](https://github.com/wwtg99/image_filter/blob/master/images/smooth.jpg)

---

Sharpen 锐化

![Sharpen](https://github.com/wwtg99/image_filter/blob/master/images/sharpen.jpg)

---

Gaussian Blur 高斯模糊

![Gaussian Blur](https://github.com/wwtg99/image_filter/blob/master/images/gaussian_blur.jpg)

---

Min Filter

![Min Filter](https://github.com/wwtg99/image_filter/blob/master/images/min.jpg)

---

Median Filter

![Median Filter](https://github.com/wwtg99/image_filter/blob/master/images/median.jpg)

---

Max Filter

![Max Filter](https://github.com/wwtg99/image_filter/blob/master/images/max.jpg)

---

Mode Filter

![Mode Filter](https://github.com/wwtg99/image_filter/blob/master/images/mode.jpg)

---

Unsharp Mask 锐化遮罩

![Unsharp Mask](https://github.com/wwtg99/image_filter/blob/master/images/unsharp_mask.jpg)

---

Emboss 45d 45 度浮雕

![Emboss 45d](https://github.com/wwtg99/image_filter/blob/master/images/emboss_45d.jpg)

---

Sharp Edge 边缘锐化

![Sharp Edge](https://github.com/wwtg99/image_filter/blob/master/images/sharp_edge.jpg)

---

Sharp Center 中心锐化

![Sharp Center](https://github.com/wwtg99/image_filter/blob/master/images/sharp_center.jpg)

---

Emboss Asymmetric 非对称浮雕

![Emboss Asymmetric](https://github.com/wwtg99/image_filter/blob/master/images/emboss_asym.jpg)
