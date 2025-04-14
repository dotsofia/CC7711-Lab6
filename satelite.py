import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load and prepare image
img = cv2.imread('./imagens/Satelite.jpeg')
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

# Apply blackhat morphology to highlight dark features
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4))
blackhat = cv2.morphologyEx(img_gray, cv2.MORPH_BLACKHAT, kernel)

# Preprocessing
img_blur = cv2.GaussianBlur(blackhat, (5, 5), 0)
edges = cv2.Canny(img_blur, 70, 150)
edges_dilated = cv2.dilate(edges, np.ones((3, 3), np.uint8), iterations=1)

# Contour detection and filtering
contours, _ = cv2.findContours(edges_dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
img_outlined = img_rgb.copy()
height, width = img_gray.shape

for cnt in contours:
    area = cv2.contourArea(cnt)
    x, y, w, h = cv2.boundingRect(cnt)
    bottom_y = y + h
    aspect_ratio = w / float(h)
    
    if (
        1000 < area < 20000 and
        w < 300 and h < 300 and  # avoid large moon-like objects
        y > 50 and bottom_y < height * 0.95 and
        0.3 < aspect_ratio < 3
    ):
        cv2.drawContours(img_outlined, [cnt], -1, (255, 0, 0), 2)

# Plot stages
titles = ["Original", "Gray", "Blackhat", "Blurred", "Canny", "Outlined"]
images = [img_rgb, img_gray, blackhat, img_blur, edges, img_outlined]
cmaps = [None, 'gray', 'gray', 'gray', 'gray', None]

plt.figure(figsize=(18, 10))
for i in range(len(images)):
    plt.subplot(2, 3, i + 1)
    plt.title(titles[i])
    plt.imshow(images[i], cmap=cmaps[i])
    plt.axis('off')
plt.tight_layout()

plt.savefig('./assets/satelite.png')
final_bgr = cv2.cvtColor(img_outlined, cv2.COLOR_RGB2BGR)
cv2.imwrite('./assets/satelite_final.png', final_bgr)