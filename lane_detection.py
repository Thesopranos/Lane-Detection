# import necessary libraries
import cv2
import numpy as np

# initialize the video capture
cam = cv2.VideoCapture("car2.mp4")

# set a variable for cropping the frame
sapma = 100

# create a kernel for morphological operations
kernel = np.ones((3,3), dtype = np.uint8)

# function to create a polygon for cropping the frame
def crop_matris(img):
    x,y = img.shape[:2]
    # create a polygon with four points to crop the image
    value = np.array([
        [(sapma,x-sapma),
        (int((y*3.2)/8),int(x*0.6)),
        (int((y*5)/8),int(x*0.6)),
        (y,x-sapma)
        ]],np.int32)
    return value

# function to apply the polygon as a mask on the image
def crop_image(img, matris):
    x,y = img.shape[:2]
    # create a black image with the same shape as the original
    mask = np.zeros(shape = (x,y), dtype = np.uint8)
    # fill the polygon on the black image
    mask = cv2.fillPoly(mask, matris, 255)
    # apply the mask on the original image
    mask = cv2.bitwise_and(img, img, mask = mask)
    return mask

# function to apply filters on the image
def filt(img):
    # convert the image to grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # apply thresholding to keep only bright pixels
    img = cv2.inRange(img, 150, 255)
    # apply morphological operations to remove noise
    img = cv2.erode(img, kernel)
    img = cv2.dilate(img, kernel)
    # apply median blur to smooth the image
    img = cv2.medianBlur(img, 9)
    # apply Canny edge detection
    img = cv2.Canny(img, 80, 200)
    return img

# function to find the mean of the lines
def line_mean(lines):
    left = []
    right = []
    # iterate over all the lines
    for line in lines:
        for x1, y1, x2, y2, in line:
            # calculate the slope of the line
            m = (y2- y1)/(x2-x1)
            # calculate the y-intercept of the line
            fonks_b = y1 - m*x1
            # set a point to calculate the line's x-value
            fonks_x_left = 10000
            fonks_x_right = 1
            # if the slope is negative, it's a right line
            if m < -0.2: 
                fonks = m*fonks_x_right + fonks_b
                right.append((x1,y1,fonks_x_right,fonks)) 
            elif m > 0.2:
                fonks = m*fonks_x_left + fonks_b
                left.append((x1,y1,fonks_x_left,fonks)) 
            
    # calculate the mean of the right and left lines
    right_mean = np.mean(right, axis=0)
    left_mean = np.mean(left, axis=0)
    # check if either mean is None
    if not isinstance(right_mean, type(np.nan)):
        if not isinstance(left_mean, type(np.nan)):
                return right_mean, left_mean
        else:
            return right_mean, None
    else:
        if not isinstance(left_mean, type(np.nan)):
                return None, left_mean
        else:
            return None, None
        
# function to draw the lines on the image
def draw_line(img, line):
    line = np.int32(np.around(line))
    x1, y1, x2, y2 = line
    cv2.line(img, (x1, y1), (x2, y2), (0,0,255), 20)
    return img
    
# main loop to read frames and apply the functions
while cam.isOpened():
    ret, frame = cam.read()
    if not ret:
        break
    frame_org = frame.copy()
    
    # create the polygon for cropping
    matris = crop_matris(frame)
    
    # apply the polygon as a mask on the image
    img = crop_image(frame, matris)
    
    # apply filters on the image
    img = filt(img)
    
    # apply HoughLinesP to find lines in the image
    lines = cv2.HoughLinesP(img, 1, np.pi/180, 50, minLineLength = 5, maxLineGap = 100)
    
    # check if any lines were found
    if lines is not None:
        # find the mean of the lines
        right_line, left_line = line_mean(lines)
        
        # check if a right line was found and draw it
        if right_line is not None:
            frame = draw_line(frame, right_line)
        
        # check if a left line was found and draw it
        if left_line is not None:
            frame = draw_line(frame, left_line)
    
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()