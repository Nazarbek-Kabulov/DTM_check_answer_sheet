import numpy as np
import cv2
from .helper import get_rect_cnts, create_contour_mask, show_images


def find_book_number(image):
    # find contours on the document
    gray_doc = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur_doc = cv2.GaussianBlur(gray_doc, (5, 5), 0)
    edge_doc = cv2.Canny(blur_doc, 10, 70)
    contours, _ = cv2.findContours(edge_doc, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # finding approximate contours
    rect_cnts = get_rect_cnts(contours)

    # find book_num_contours
    find_book_num_cnt = rect_cnts[0]

    # Now, use the sorted contours to extract the cut-out regions
    cut_book_number = cv2.bitwise_and(image, image,  mask=create_contour_mask(image.shape, find_book_num_cnt))

    # show_images(['Cut Out findbook number'], [cut_book_number])

    # cooredinates of the biggest contour
    # I added 4 and 10 pixels to x and y, and removed 4 pixels from x_W and y_H to make
    # sure we are inside the contour and not take the border of the biggest contour
    x, y = find_book_num_cnt[0][0][0] + 4, find_book_num_cnt[0][0][1] + 10
    x_w, y_h = find_book_num_cnt[2][0][0] - 4, find_book_num_cnt[2][0][1] - 4

    # Use the adjusted coordinates for cropping the regions
    cut_book_number = cut_book_number[y:y_h, x:x_w]

    # Load the image of the DTM book number
    book_num_img = cut_book_number

    try:
        if not book_num_img.size == 0:
            book_num_img = cv2.resize(book_num_img, (250, 500))
            # Convert the book_num_img to grayscale
            gray_book_num_img = cv2.cvtColor(book_num_img, cv2.COLOR_BGR2GRAY)

            # Apply histogram equalization
            equalized_book_num_img = cv2.equalizeHist(gray_book_num_img)

            # Merge the equalized image back to the original color format
            equalized_book_num_img = cv2.merge([equalized_book_num_img, equalized_book_num_img, equalized_book_num_img])

            # Display the image with detected circles and enhanced contrast
            # cv2.imshow('Equalized Image', equalized_book_num_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            return '0000000'
    except UnboundLocalError:
        return '0000000'

    # Use Hough Circle Transform to detect circles
    circles = cv2.HoughCircles(
        gray_book_num_img,
        cv2.HOUGH_GRADIENT,
        dp=10.5,
        minDist=20,
        param1=50,
        param2=30,
        minRadius=10,
        maxRadius=20
    )

    # save some data
    circle_info = []
    find_y_coords = []

    # Define the y-coordinate threshold
    y_threshold = 70

    # Draw circles on the original image and collect information
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            # Get the coordinates and radius
            center = (i[0], i[1])
            radius = i[2]

            # Check if the circle's center is below the y-coordinate threshold
            if center[1] > y_threshold:
                # Ensure the ROI is within the image boundaries
                roi_top = max(i[1] - radius, 0)
                roi_bottom = min(i[1] + radius, book_num_img.shape[0])
                roi_left = max(i[0] - radius, 0)
                roi_right = min(i[0] + radius, book_num_img.shape[1])

                # Extract the region of interest (ROI) for the current circle
                roi = book_num_img[roi_top:roi_bottom, roi_left:roi_right]

                # Check if the ROI is not empty before calculating the mean
                if roi.size > 0:
                    # Calculate the mean color of the ROI
                    mean_color = np.mean(roi, axis=(0, 1))

                    # Check if the mean color is close to black (adjust the threshold as needed)
                    if mean_color[0] < 100 and mean_color[1] < 100 and mean_color[2] < 100:
                        # Determine the answer option based on the x-coordinate of the center
                        if 80 < center[1] < 120:
                            option = '1'
                        elif 120 < center[1] < 160:
                            option = '2'
                        elif 160 < center[1] < 200:
                            option = '3'
                        elif 200 < center[1] < 245:
                            option = '4'
                        elif 245 < center[1] < 290:
                            option = '5'
                        elif 290 < center[1] < 330:
                            option = '6'
                        elif 330 < center[1] < 370:
                            option = '7'
                        elif 370 < center[1] < 410:
                            option = '8'
                        elif 410 < center[1] < 455:
                            option = '9'
                        elif 455 < center[1] < 500:
                            option = '0'
                        else:
                            option = None

                        # Collect information about the circle and its corresponding answer option
                        circle_info.append({"Center": center, "Radius": radius, "Answer Option": option})
                        # Draw the circle on a copy of the original image
                        cv2.circle(book_num_img, center, radius, (0, 255, 0), 2)  # Green circles
                        cv2.circle(book_num_img, center, 2, (0, 0, 255), 3)  # Red center dots
    # Sort the circle_info based on x-coordinate
    sorted_circle_info = sorted(circle_info, key=lambda x: x['Center'][0])

    book_number = ''
    data = 'No result'
    try:
        for i in range(len(sorted_circle_info)):
            book_number += sorted_circle_info[i]['Answer Option']
        data = book_number
    except:
        return data

    return data

