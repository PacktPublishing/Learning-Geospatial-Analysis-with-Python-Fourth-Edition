"""Simple distance measurement using the Pythagorean Theorem"""
import math
x1 = 456456.23
y1 = 1279721.06
x2 = 576628.34
y2 = 1071740.33
x_dist = x1 - x2
y_dist = y1 - y2
dist_sq = x_dist**2 + y_dist**2
distance = math.sqrt(dist_sq)
print(distance)
