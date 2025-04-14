
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load and prepare image
img = cv2.imread('./imagens/Aviao.jpeg')
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

# Blur and detect edges
img_blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
edges = cv2.Canny(img_blur, 50, 150)
edges_dilated = cv2.dilate(edges, np.ones((5, 5), np.uint8), iterations=1)

# Find contours
contours, _ = cv2.findContours(edges_dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Outline filtering
img_outlined = img_rgb.copy()
height = img_gray.shape[0]
min_area = 1000
max_bottom_y = int(height * 0.6)  # only contours that end above 60% of the image height

for cnt in contours:
    area = cv2.contourArea(cnt)
    x, y, w, h = cv2.boundingRect(cnt)
    bottom_y = y + h
    if area > min_area and bottom_y < max_bottom_y:
        cv2.drawContours(img_outlined, [cnt], -1, (255, 0, 0), 2)

# Show all stages
titles = ["Original", "Gray", "Blurred", "Canny", "Dilated", "Final Outlined"]
images = [img_rgb, img_gray, img_blur, edges, edges_dilated, img_outlined]
cmaps = [None, 'gray', 'gray', 'gray', 'gray', None]

plt.figure(figsize=(18, 10))
for i in range(len(images)):
    plt.subplot(2, 3, i + 1)
    plt.title(titles[i])
    plt.imshow(images[i], cmap=cmaps[i])
    plt.axis('off')
plt.tight_layout()

plt.savefig('./assets/aviao.png')
final_bgr = cv2.cvtColor(img_outlined, cv2.COLOR_RGB2BGR)
cv2.imwrite('./assets/aviao_final.png', final_bgr)
