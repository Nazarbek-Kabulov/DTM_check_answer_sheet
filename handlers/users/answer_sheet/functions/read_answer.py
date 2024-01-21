import numpy as np
import cv2
from imutils.perspective import four_point_transform
from .helper import answers, remove_duplicates, replace_with_asterisk, show_images, get_rect_cnts, create_contour_mask
from .find_book_number import find_book_number


def answer_sheet(image_file):
    try:
        # declare some variables
        height = 800
        width = 600
        green = (0, 255, 0)
        red = (0, 0, 255)
        white = (255, 255, 255)

        # image path
        img_path = f'/home/nazarbek/Portfolio/Check-answer-sheet/{image_file}'

        # image imread and resize
        img = cv2.imread(img_path)
        img = cv2.resize(img, (width, height))

        # convert the image to grayscale and equalize the brightness
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        equalized_img = clahe.apply(gray_img)

        # save 2 sample images
        img_copy = img.copy()

        # to blur the image and detect edges
        blur_img = cv2.GaussianBlur(equalized_img, (5, 5), 0)
        edge_img = cv2.Canny(blur_img, 10, 70)

        # find the contours in the image
        contours, _ = cv2.findContours(edge_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        # draw the contours
        cv2.drawContours(img, contours, -1, green, 1)
        # show_images(['image'], [img])

        rect_cnts = get_rect_cnts(contours)
        # warp perspective to get the top-down view of the document
        document = four_point_transform(img_copy, rect_cnts[0].reshape(4, 2))
        document1 = four_point_transform(img_copy, rect_cnts[2].reshape(4, 2))

        # marked answers and test book number contour pictures
        doc_copy = document.copy()
        book_num_image = document1.copy()

        # find book number
        """
            Through this function we can read the
            'Test Book Number' in the answer sheet.
        """
        find_book_num = find_book_number(book_num_image)
        print(f'Test kitob raqami: {find_book_num}')

        cv2.drawContours(img_copy, rect_cnts, -1, green, 1)
        # show_images(['image', 'document'], [img_copy, document])

        # find contours on the document
        gray_doc = cv2.cvtColor(document, cv2.COLOR_BGR2GRAY)
        blur_doc = cv2.GaussianBlur(gray_doc, (5, 5), 0)
        edge_doc = cv2.Canny(blur_doc, 10, 70)
        contours, _ = cv2.findContours(edge_doc, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # finding approximate contours
        rect_cnts = get_rect_cnts(contours)

        # outline of the biggest
        biggest_cnt = rect_cnts[0]
        # outline of the middle
        middle_cnt = rect_cnts[2]
        # outline of the grade
        grade_cnt = rect_cnts[1]

        # Extract x-coordinates from the contours
        x1 = biggest_cnt[0][0][0]
        x2 = middle_cnt[0][0][0]
        x3 = grade_cnt[0][0][0]

        # Create a list of tuples with the x-coordinates and contours
        contours_with_x = [(x1, biggest_cnt), (x2, middle_cnt), (x3, grade_cnt)]

        # Sort the list based on x-coordinates
        contours_with_x = sorted(contours_with_x, key=lambda x: x[0])

        # Reassign the sorted contours
        biggest_cnt = contours_with_x[0][1]
        middle_cnt = contours_with_x[1][1]
        grade_cnt = contours_with_x[2][1]

        # Now, use the sorted contours to extract the cut-out regions
        cut_out_biggest = cv2.bitwise_and(document, document, mask=create_contour_mask(document.shape, biggest_cnt))
        cut_out_middle = cv2.bitwise_and(document, document, mask=create_contour_mask(document.shape, middle_cnt))
        cut_out_grade = cv2.bitwise_and(document, document, mask=create_contour_mask(document.shape, grade_cnt))

        # Display the cut-out regions separately
        # show_images(['Cut Out Biggest Contour', 'Cut Out Middle Contour', 'Cut Out Grade Contour'],
        #             [cut_out_biggest, cut_out_middle, cut_out_grade])

        # cooredinates of the biggest contour
        # I added 4 and 10 pixels to x and y, and removed 4 pixels from x_W and y_H to make
        # sure we are inside the contour and not take the border of the biggest contour
        x, y = biggest_cnt[0][0][0] + 4, biggest_cnt[0][0][1] + 10
        x_W, y_H = biggest_cnt[2][0][0] - 4, biggest_cnt[2][0][1] - 4

        x1, y1 = middle_cnt[0][0][0] + 4, middle_cnt[0][0][1] + 10
        x_W1, y_H1 = middle_cnt[2][0][0] - 4, middle_cnt[2][0][1] - 4

        x2, y2 = grade_cnt[0][0][0] + 4, grade_cnt[0][0][1] + 10
        x_W2, y_H2 = grade_cnt[2][0][0] - 4, grade_cnt[2][0][1] - 4

        # Use the adjusted coordinates for cropping the regions
        cut_out_biggest = cut_out_biggest[y:y_H, x:x_W]
        cut_out_middle = cut_out_middle[y1:y_H1, x1:x_W1]
        cut_out_grade = cut_out_grade[y2:y_H2, x2:x_W2]

        # Display the cut-out regions separately
        # show_images(['Cut Out Biggest Contour', 'Cut Out Middle Contour', 'Cut Out Grade Contour'],
        #             [cut_out_biggest, cut_out_middle, cut_out_grade])

        # create a black image with the same dimensions as the document
        mask = np.zeros((document.shape[0], document.shape[1]), np.uint8)
        # we create a white rectangle in the region of the biggest contour
        cv2.rectangle(mask, (x, y), (x_W, y_H), white, -1)
        masked = cv2.bitwise_and(doc_copy, doc_copy, mask=mask)

        # take only the region of the biggest contour
        masked = masked[y:y_H, x:x_W]
        # show_images(['document', 'mask', 'masked'], [doc_copy, mask, masked])

        # Load the image of the DTM header
        image_1 = cut_out_biggest
        image_2 = cut_out_middle
        image_3 = cut_out_grade

        all_results = []
        try:
            for image in (image_1, image_2, image_3):

                # resize image
                image = cv2.resize(image, (200, 900))

                # Apply GaussianBlur directly to the color image
                blurred_image = cv2.GaussianBlur(image, (15, 15), 50)

                # Optionally, convert the blurred image to grayscale if needed
                gray_blurred_image = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2GRAY)

                # cv2.imshow('Gray image', gray_blurred_image)
                # cv2.waitKey(0)

                # Use Hough Circle Transform to detect circles
                circles = cv2.HoughCircles(
                    gray_blurred_image,
                    cv2.HOUGH_GRADIENT,
                    dp=4.5,
                    minDist=7,
                    param1=50,
                    param2=30,
                    minRadius=6,
                    maxRadius=18
                )

                # save some data
                circle_info = []

                # Define the y-coordinate threshold
                y_threshold = 50

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
                            roi_bottom = min(i[1] + radius, image.shape[0])
                            roi_left = max(i[0] - radius, 0)
                            roi_right = min(i[0] + radius, image.shape[1])

                            # Extract the region of interest (ROI) for the current circle
                            roi = image[roi_top:roi_bottom, roi_left:roi_right]

                            # Check if the ROI is not empty before calculating the mean
                            if roi.size > 0:
                                # Calculate the mean color of the ROI
                                mean_color = np.mean(roi, axis=(0, 1))

                                # Check if the mean color is close to black (adjust the threshold as needed)
                                if mean_color[0] < 100 and mean_color[1] < 100 and mean_color[2] < 100:
                                    # Determine the answer option based on the x-coordinate of the center
                                    if 40 < center[0] < 75:
                                        option = 'A'
                                    elif 75 < center[0] < 110:
                                        option = 'B'
                                    elif 109 < center[0] < 145:
                                        option = 'C'
                                    elif 145 < center[0] < 175:
                                        option = 'D'
                                    else:
                                        option = None

                                    # Collect information about the circle and its corresponding answer option
                                    circle_info.append({"Center": center, "Radius": radius, "Answer Option": option})
                                    # Draw the circle on a copy of the original image
                                    cv2.circle(image, center, radius, (0, 255, 0), 2)  # Green circles
                                    cv2.circle(image, center, 2, (0, 0, 255), 3)  # Red center dots

                # some save data
                num = 0
                y_info = []
                full_info = []

                # Sort the circle_info based on y-coordinate
                sorted_circle_info = sorted(circle_info, key=lambda x: x['Center'][1])

                # Print and store the information in ascending order of y-coordinate
                for num, info in enumerate(sorted_circle_info):
                    y_info.append(info['Center'][1])
                    data = {'answer': info['Answer Option'], 'y_coords': info['Center'][1]}
                    full_info.append(data)

                # data sorted with coordinate
                sorted_circle_info_y_only = sorted(circle_info, key=lambda x: x['Center'][1])

                # the obtained results sorted by the y coordinate
                result_1 = [{'Center': circle['Center'], 'Radius': circle['Radius'], 'Answer Option': circle['Answer Option']} for
                            circle in sorted_circle_info_y_only]

                # all answers read
                answers_ = answers(result_1)

                # identifying two or more answers to a single question and unmarked questions
                remove_duplicates_ = remove_duplicates(answers_)

                # all results obtained
                data = replace_with_asterisk(remove_duplicates_)

                # Display the image with detected circles
                # cv2.imshow('Detected Circles', image)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()

                all_results.append(data)

        except Exception as e:
            print(f'An error occurred: {e}')
            all_results = 'No result'

        data = all_results
        results = f'{find_book_num}:'

        if data is not 'No result' and find_book_num != '0000000':
            for i in data:
                for j in i:
                    output_str = ', '.join([f"{key}: {value}" for key, value in j.items()])
                    results += output_str[-1]
        else:
            results = data

        return results
    except:
        return 'No result'
