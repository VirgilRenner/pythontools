""" https://zhuanlan.zhihu.com/p/43907816 """

from PIL import Image
import numpy as np
import math
import time

def getColor(data, r, point, weight):
	# r 模糊半径
	c_x, c_y = point
	min_x = c_x - r
	max_x = c_x + r + 1
	min_y = c_y - r
	max_y = c_y + r + 1
	color = np.array([0, 0, 0])
	for y in range(min_y, max_y):
		for x in range(min_x, max_x):
			now_x = x
			now_y = y
			# 边缘处理
			if y < 0:
				now_y = -y
			if x < 0: 
				now_x = -x
			if y > height - 1:
				now_y = 2*c_y - y
			if x > width - 1:
				now_x = 2*c_x - x
			w = weight[x - min_x][y - min_y]
			point = data[now_x, now_y] * w
			color = color + point
	return color.tolist()


def gaussian(x, y):
    # np.exp 返回自然常数 e
    # sigma σ 控制"钟形"的宽度 现在设为 2
    sigma = 2
    return 1 / (2 * math.pi * sigma ** 2) * np.exp(-(x ** 2 + y ** 2) / (2 * sigma ** 2))


def getGaussianWeight(r):
	l = r * 2 + 1
	weight = np.zeros((l, l))
	for y in range(l):
		for x in range(l):
			bias_x = x - r
			bias_y = y - r
			weight[x][y] = gaussian(bias_x, bias_y)
	sum = np.sum(weight)
	weight = weight / sum
	return weight


if __name__ == '__main__':
	t1 = time.time()
	image = Image.open("test.jpg")
	width, height = image.size
	total = width * height
	count, r = 0, 5
	data = np.array(image)
	weight = getGaussianWeight(r)
	for y in range(height):
		for x in range(width):
			data[x][y] = getColor(data, r, (x, y), weight)
			count += 1
			print('point %i/%i' % (count, total), end='\r')
	res = Image.fromarray(data)
	res.save("gaussianblur-result.jpg")
	t2 = time.time()
	print('\ntime:%is' % (t2 - t1))
