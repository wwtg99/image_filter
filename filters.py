from PIL import Image
import numpy as np
from PIL import ImageFilter


class Filter:

    def __init__(self, image) -> None:
        super().__init__()
        self.image = image

    def filter(self, **kwargs) -> Image:
        """
        Filter image
        :param kwargs:
        :return: Image
        """
        pass


class Rgb(Filter):
    """
    RGB 原图
    """
    def filter(self, **kwargs) -> Image:
        return self.image.convert('RGB')


class Greyscale(Filter):
    """
    灰度
    """
    def filter(self, **kwargs) -> Image:
        return self.image.convert('L')


class HandDrawn(Filter):
    """
    手绘风格
    """
    def filter(self, **kwargs) -> Image:
        a = np.asarray(self.image.convert('L')).astype('float')

        depth = 10.  # (0-100)
        grad = np.gradient(a)  # 取图像灰度的梯度值
        grad_x, grad_y = grad  # 分别取横纵图像梯度值
        grad_x = grad_x * depth / 100.
        grad_y = grad_y * depth / 100.
        A = np.sqrt(grad_x ** 2 + grad_y ** 2 + 1.)
        uni_x = grad_x / A
        uni_y = grad_y / A
        uni_z = 1. / A

        vec_el = np.pi / 2.2  # 光源的俯视角度，弧度值
        vec_az = np.pi / 4.  # 光源的方位角度，弧度值
        dx = np.cos(vec_el) * np.cos(vec_az)  # 光源对x 轴的影响
        dy = np.cos(vec_el) * np.sin(vec_az)  # 光源对y 轴的影响
        dz = np.sin(vec_el)  # 光源对z 轴的影响

        b = 255 * (dx * uni_x + dy * uni_y + dz * uni_z)  # 光源归一化
        b = b.clip(0, 255)

        im = Image.fromarray(b.astype('uint8'))  # 重构图像
        return im


class EdgeCurve(Filter):
    """
    边缘
    """
    def filter(self, **kwargs) -> Image:
        return self.image.convert('RGB').filter(ImageFilter.FIND_EDGES)


class Blur(Filter):
    """
    模糊
    """
    def filter(self, **kwargs) -> Image:
        return self.image.convert('RGB').filter(ImageFilter.BLUR)


class Contour(Filter):
    """
    描边
    """
    def filter(self, **kwargs) -> Image:
        return self.image.convert('RGB').filter(ImageFilter.CONTOUR)


class EdgeEnhance(Filter):
    """
    边缘强化

    :param more: 强化更多
    """
    def filter(self, **kwargs) -> Image:
        if 'more' in kwargs:
            return self.image.convert('RGB').filter(ImageFilter.EDGE_ENHANCE_MORE)
        else:
            return self.image.convert('RGB').filter(ImageFilter.EDGE_ENHANCE)


class Emboss(Filter):
    """
    浮雕
    """
    def filter(self, **kwargs) -> Image:
        return self.image.convert('RGB').filter(ImageFilter.EMBOSS)


class Smooth(Filter):
    """
    平滑

    :param more:
    """
    def filter(self, **kwargs) -> Image:
        if 'more' in kwargs:
            return self.image.convert('RGB').filter(ImageFilter.SMOOTH_MORE)
        else:
            return self.image.convert('RGB').filter(ImageFilter.SMOOTH)


class Sharpen(Filter):
    """
    锐化
    """
    def filter(self, **kwargs) -> Image:
        return self.image.convert('RGB').filter(ImageFilter.SHARPEN)


class GaussianBlur(Filter):
    """
    高斯模糊

    :param radius:
    """
    def filter(self, **kwargs) -> Image:
        if 'radius' in kwargs:
            r = int(kwargs['radius'])
        else:
            r = 2
        return self.image.convert('RGB').filter(ImageFilter.GaussianBlur(radius=r))


class MinFilter(Filter):
    """
    最小化

    :param size: 3 or 5
    """
    def filter(self, **kwargs) -> Image:
        if 'size' in kwargs:
            s = int(kwargs['size'])
        else:
            s = 3
        return self.image.convert('RGB').filter(ImageFilter.MinFilter(size=s))


class MedianFilter(Filter):
    """
    中间化

    :param size: 3 or 5
    """
    def filter(self, **kwargs) -> Image:
        if 'size' in kwargs:
            s = int(kwargs['size'])
        else:
            s = 3
        return self.image.convert('RGB').filter(ImageFilter.MedianFilter(size=s))


class MaxFilter(Filter):
    """
    最大化

    :param size: 3 or 5
    """
    def filter(self, **kwargs) -> Image:
        if 'size' in kwargs:
            s = int(kwargs['size'])
        else:
            s = 3
        return self.image.convert('RGB').filter(ImageFilter.MaxFilter(size=s))


class ModeFilter(Filter):
    """
    最高频率化

    :param size: 3 or 5
    """
    def filter(self, **kwargs) -> Image:
        if 'size' in kwargs:
            s = int(kwargs['size'])
        else:
            s = 3
        return self.image.convert('RGB').filter(ImageFilter.ModeFilter(size=s))


class UnsharpMask(Filter):
    """
    锐化遮罩

    :param radius
    :param percent
    :param threshold
    """
    def filter(self, **kwargs) -> Image:
        if 'radius' in kwargs:
            r = int(kwargs['radius'])
        else:
            r = 2
        if 'percent' in kwargs:
            p = int(kwargs['percent'])
        else:
            p = 150
        if 'threshold' in kwargs:
            t = int(kwargs['threshold'])
        else:
            t = 3
        return self.image.convert('RGB').filter(ImageFilter.UnsharpMask(radius=r, percent=p, threshold=t))


class Emboss45d(Filter):
    """
    45 度浮雕
    """
    def filter(self, **kwargs) -> Image:
        class Emboss45DegreeFilter(ImageFilter.BuiltinFilter):
            name = "Emboss_45_degree"
            filterargs = (3, 3), 1, 0, (
                -1, -1, 0,
                -1, 1, 1,
                0, 1, 1
            )
        return self.image.convert('RGB').filter(Emboss45DegreeFilter)


class SharpEdge(Filter):
    """
    边缘锐化
    """
    def filter(self, **kwargs) -> Image:
        class SharpEdgeFilter(ImageFilter.BuiltinFilter):
            name = "Sharp_Edge"
            filterargs = (3, 3), 1, 0, (
                1, 1, 1,
                1, -7, 1,
                1, 1, 1
            )
        return self.image.convert('RGB').filter(SharpEdgeFilter)


class SharpCenter(Filter):
    """
    中心锐化
    """
    def filter(self, **kwargs) -> Image:
        class SharpCenterFilter(ImageFilter.BuiltinFilter):
            name = "Sharp_Center"
            filterargs = (3, 3), -1, 0, (
                1, 1, 1,
                1, -9, 1,
                1, 1, 1
            )
        return self.image.convert('RGB').filter(SharpCenterFilter)


class EmbossAsymmetric(Filter):
    """
    非对称浮雕
    """
    def filter(self, **kwargs) -> Image:
        class EmbossAsymmetricFilter(ImageFilter.BuiltinFilter):
            name = "Emboss_Asymmetric"
            filterargs = (3, 3), 1, 0, (
                2, 0, 0,
                0, -1, 0,
                0, 0, -1
            )
        return self.image.convert('RGB').filter(EmbossAsymmetricFilter)
