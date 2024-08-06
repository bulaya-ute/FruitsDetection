import cv2
import numpy as np
from sklearn.cluster import DBSCAN


def mean_position_of_color(image, lower_bound, upper_bound):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
    y_indices, x_indices = np.where(mask > 0)

    if len(x_indices) == 0 or len(y_indices) == 0:
        return None, mask

    mean_x = np.mean(x_indices)
    mean_y = np.mean(y_indices)

    return (int(mean_x), int(mean_y)), mask


def capture_color_range(frame, center, radius):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    center_x, center_y = center
    sample_area = hsv_frame[center_y - radius:center_y + radius, center_x - radius:center_x + radius]
    lower_bound = np.min(sample_area, axis=(0, 1))
    upper_bound = np.max(sample_area, axis=(0, 1))

    return lower_bound, upper_bound


def draw_bounding_box(frame, mask, color, label):
    y_indices, x_indices = np.where(mask > 0)
    if len(x_indices) == 0 or len(y_indices) == 0:
        return frame

    points = np.column_stack((x_indices, y_indices))
    db = DBSCAN(eps=10, min_samples=10).fit(points)
    labels = db.labels_

    unique_labels, counts = np.unique(labels, return_counts=True)
    largest_cluster_label = unique_labels[np.argmax(counts)]

    if largest_cluster_label == -1:
        return frame

    largest_cluster_points = points[labels == largest_cluster_label]
    x_min, y_min = np.min(largest_cluster_points, axis=0)
    x_max, y_max = np.max(largest_cluster_points, axis=0)
    cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), color, 2)

    label_position = (x_min, y_min - 10)
    cv2.putText(frame, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    return frame


def mean_color(lower_bound, upper_bound):
    mean_hsv = (lower_bound + upper_bound) // 2
    mean_hsv = np.uint8([[mean_hsv]])
    mean_bgr = cv2.cvtColor(mean_hsv, cv2.COLOR_HSV2BGR)[0][0]
    return tuple(int(c) for c in mean_bgr)


def hsv_to_rgb(hsv_color):
    hsv_color = np.uint8([[hsv_color]])
    rgb_color = cv2.cvtColor(hsv_color, cv2.COLOR_HSV2BGR)[0][0]
    return rgb_color


mode = 'capture'
center = (320, 240)
radius = 10
colors = [
    (np.array([0, 100, 100]), np.array([10, 255, 255]), 'Red fruit'),
    (np.array([35, 100, 100]), np.array([85, 255, 255]), 'Green fruit'),
    (np.array([25, 100, 100]), np.array([35, 255, 255]), 'Yellow fruit')
]

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    if mode == 'capture':
        cv2.circle(frame, center, radius, (255, 0, 0), 2)
        if cv2.waitKey(1) & 0xFF == ord('c'):
            lower_bound, upper_bound = capture_color_range(frame, center, radius)
            label = input("Enter label for the captured color: ")
            colors.append((lower_bound, upper_bound, label))

            # Print the captured color in HSV and RGB format
            print(f"Captured color '{label}':")
            print(f"Lower Bound HSV: {lower_bound}")
            print(f"Upper Bound HSV: {upper_bound}")
            lower_rgb = hsv_to_rgb(lower_bound)
            upper_rgb = hsv_to_rgb(upper_bound)
            print(f"Lower Bound RGB: {lower_rgb}")
            print(f"Upper Bound RGB: {upper_rgb}")

    elif mode == 'track':
        for lower_bound, upper_bound, label in colors:
            mean_position, mask = mean_position_of_color(frame, lower_bound, upper_bound)
            color = mean_color(lower_bound, upper_bound)
            frame = draw_bounding_box(frame, mask, color, label)

    cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    elif cv2.waitKey(1) & 0xFF == ord('t'):
        mode = 'track'

cap.release()
cv2.destroyAllWindows()
