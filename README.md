# Lane Detection
This code captures video from a file called "car2.mp4", crops the frame, applies various filters on the image, detects lines using HoughLinesP, calculates the mean of the left and right lines, and draws them on the original frame. The final output is displayed using cv2.imshow(). The while loop continues until the 'q' key is pressed.
# In-script Image
![Screenshot_2](https://user-images.githubusercontent.com/68299931/213160030-6f399dee-ffe4-47d5-bf04-b142fa1f6ea3.png)

# Dependencies
opencv-python  
numpy  
# Usage
Copy code
```
python lane_detection.py
```
# Code Explanation
1. The video is captured using cv2.VideoCapture() and stored in the variable 'cam'.  
2. The frame is cropped using the function 'crop_matris()' which creates a polygon to be used as a mask.  
3. The polygon is applied as a mask on the frame using the function 'crop_image()'.  
4. Various filters are applied on the image using the function 'filt()' to improve the detection of lines.  
5. The lines are detected in the image using cv2.HoughLinesP().  
6. The mean of the left and right lines is calculated using the function 'line_mean()'.  
7. The final output is displayed using cv2.imshow() and the while loop continues until the 'q' key is pressed.  
# Note
You can change the video file name that you want to use for processing in the line "cam = cv2.VideoCapture("car2.mp4")"  

# Conclusion
This code can be used as a basic lane detection system, but it may not work well in all scenarios and may require further tuning and optimization for specific use cases.
