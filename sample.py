import cv2
import numpy as np

# Load the image
image = cv2.imread('sample.jpg')
if image is None:
    raise Exception("Image not found. Please make sure the path is correct.")

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Perform Canny edge detection
edges = cv2.Canny(blurred, 50, 150)

# Find contours in the edges image
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Create a copy of the original image to draw contours on
contour_image = image.copy()

# Draw contours
cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)

# Display the images
cv2.imshow('Original Image', image)
cv2.imshow('Grayscale Image', gray)
cv2.imshow('Blurred Image', blurred)
cv2.imshow('Edges', edges)
cv2.imshow('Contours', contour_image)

# Wait for a key press and close the image windows
cv2.waitKey(0)
cv2.destroyAllWindows()
