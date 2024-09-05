import cv2
import pickle
import cvzone
import numpy as np

# Video Feed
cap = cv2.VideoCapture('carPark.mp4')
width, height = 107, 48  # width and height of rectangle

def checkParkingSpace(imgPro):  # This function will help us in checking the parking space
    for pos in posList:  # This crop function helps us in seeing all things happening in our rectangle, each car is a separate image and each of these must be drawn later on after crop to avoid purple region
        x, y = pos
        imgCrop = imgPro[y:y + height, x:x + width]
        # cv2.imshow(str(x * y), imgCrop) #this function hows th croppped images 
        count = cv2.countNonZero(imgCrop)  # It counts the number of non-zero or white pixels in a particular cropped video

        if count<800: #space present
            color=(0,255,0)
            thickness=5
        else: #space absent 
            color=(0,0,255)
            thickness=2
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness) #change the color according to avaliablity
        cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1, thickness=2, offset=0)  # in the image in a rectangle show the count in string format and specify its position in x axis and y axis and to scale them down to 0.2, thickness is 1 and offset is 0.
        # From the video one can easily infer that empty space has a value in hundreds while occupied spaces are in thousands. The gap is big, so now we can put all of them and find min and max value and find the median value.

with open('CarParkPos', 'rb') as f:  # check whether an object is present or not
    posList = pickle.load(f)  # if CarParkPos file is present then assign its value in posList array

while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):  # if the current frame equals the total number of frames in the video then we shall set the frame back to initial or reset the frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, img = cap.read()  # capture each frame of the video and store it in image, it runs by default at 30fps
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)  # dimension of kernel (3, 3) and sigma x as 1 (hit and try)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)  # image blur with maximum value 255 and the method as adaptive threshold gaussian c along with a binary inverse and block size

    imgMedian = cv2.medianBlur(imgThreshold, 5)  # higher kernel value has a bigger impact
    kernel = np.ones((3, 3), np.uint8)  # numpy array of ones which is a square matrix of 3x3 and are unsigned integers
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)  # too many iterations will make it too thick and then this image is to be sent to checkParkingSpace function in line 28

    checkParkingSpace(imgDilate)  # Check parking spaces

    # for pos in posList:
    #     cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

    cv2.imshow("Image", img)  # Display the array of images
    # cv2.imshow("ImageBlur", imgBlur)  # Display the array of images
    # cv2.imshow("ImageThresh", imgThreshold)  # Display the threshold image
    # cv2.imshow("Median Blur", imgMedian)  # Display the median blur image
    # cv2.imshow("Dilate", imgDilate)  # Display the dilated image

    cv2.waitKey(10)  # This method is used to delay the number of frames per millisecond
