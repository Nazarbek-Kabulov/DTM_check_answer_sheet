import cv2
import numpy as np


# finding approximate contours
def get_rect_cnts(contours):
    rect_cnts = []
    for cnt in contours:
        # approximate the contour
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
        # if the approximated contour is a rectangle ...
        if len(approx) == 4:
            # append it to our list
            rect_cnts.append(approx)
    # sort the contours from biggest to smallest
    rect_cnts = sorted(rect_cnts, key=cv2.contourArea, reverse=True)

    return rect_cnts


white = (255, 255, 255)


# Define a function to create a mask for a given contour
def create_contour_mask(image_shape, contour):
        mask = np.zeros(image_shape[:2], dtype=np.uint8)
        cv2.drawContours(mask, [contour], -1, white, -1)
        return mask


# the function to view the results of the read image
def show_images(titles, images, wait=True):
    """Display multiple images with one line of code"""

    for (title, image) in zip(titles, images):
        cv2.imshow(title, image)

    if wait:
        cv2.waitKey(0)
        cv2.destroyAllWindows()


# Sort the read answers by y coordinate from 1-30
def answers(find_y_coords):
    find_answer_numbers = []
    for find_y_coord in find_y_coords:
        if 60 < find_y_coord['Center'][1] < 80:
            answer = {1: find_y_coord['Answer Option']}
            find_answer_numbers.append(answer)
        elif 85 < find_y_coord['Center'][1] < 110:
            answer = {2: find_y_coord['Answer Option']}
            find_answer_numbers.append(answer)
        elif 115 < find_y_coord['Center'][1] < 135:
            answer = {3: find_y_coord['Answer Option']}
            find_answer_numbers.append(answer)
        elif 140 < find_y_coord['Center'][1] < 160:
            answer = {4: find_y_coord['Answer Option']}
            find_answer_numbers.append(answer)
        elif 170 < find_y_coord['Center'][1] < 190:
            answer = {5: find_y_coord['Answer Option']}
            find_answer_numbers.append(answer)
        elif 195 < find_y_coord['Center'][1] < 220:
            answer = {6: find_y_coord['Answer Option']}
            find_answer_numbers.append(answer)
        elif 225 < find_y_coord['Center'][1] < 245:
            answer = {7: find_y_coord['Answer Option']}
            find_answer_numbers.append(answer)
        elif 250 < find_y_coord['Center'][1] < 270:
            answer = {8: find_y_coord['Answer Option']}
            find_answer_numbers.append(answer)
        elif 275 < find_y_coord['Center'][1] < 305:
            answer = {9: find_y_coord['Answer Option']}
            find_answer_numbers.append(answer)
        elif 310 < find_y_coord['Center'][1] < 335:
            answer = {10: find_y_coord['Answer Option']}
            find_answer_numbers.append(answer)
        elif 335 < find_y_coord['Center'][1] < 360:
            answer = {11: find_y_coord['Answer Option']}
            find_answer_numbers.append(answer)
        elif 365 < find_y_coord['Center'][1] < 390:
            answer = {12: find_y_coord['Answer Option']}
            find_answer_numbers.append(answer)
        elif 390 < find_y_coord['Center'][1] < 415:
            answer = {13: find_y_coord['Answer Option']}
            find_answer_numbers.append(answer)
        elif 420 < find_y_coord['Center'][1] < 445:
            answer = {14: find_y_coord['Answer Option']}
            find_answer_numbers.append(answer)
        elif 450 < find_y_coord['Center'][1] < 475:
            answer = {15: find_y_coord['Answer Option']}
            find_answer_numbers.append(answer)
        elif 475 < find_y_coord['Center'][1] < 500:
            answer = {16: find_y_coord['Answer Option']}
            find_answer_numbers.append(answer)
        elif 505 < find_y_coord['Center'][1] < 525:
            answer = {17: find_y_coord['Answer Option']}
            find_answer_numbers.append(answer)
        elif 530 < find_y_coord['Center'][1] < 555:
            answer = {18: find_y_coord['Answer Option']}
            find_answer_numbers.append(answer)
        elif 555 < find_y_coord['Center'][1] < 580:
            answer = {19: find_y_coord['Answer Option']}
            find_answer_numbers.append(answer)
        elif 585 < find_y_coord['Center'][1] < 615:
            answer = {20: find_y_coord['Answer Option']}
            find_answer_numbers.append(answer)
        elif 615 < find_y_coord['Center'][1] < 640:
            answer = {21: find_y_coord['Answer Option']}
            find_answer_numbers.append(answer)
        elif 645 < find_y_coord['Center'][1] < 665:
            answer = {22: find_y_coord['Answer Option']}
            find_answer_numbers.append(answer)
        elif 670 < find_y_coord['Center'][1] < 695:
            answer = {23: find_y_coord['Answer Option']}
            find_answer_numbers.append(answer)
        elif 700 < find_y_coord['Center'][1] < 725:
            answer = {24: find_y_coord['Answer Option']}
            find_answer_numbers.append(answer)
        elif 725 < find_y_coord['Center'][1] < 755:
            answer = {25: find_y_coord['Answer Option']}
            find_answer_numbers.append(answer)
        elif 755 < find_y_coord['Center'][1] < 780:
            answer = {26: find_y_coord['Answer Option']}
            find_answer_numbers.append(answer)
        elif 785 < find_y_coord['Center'][1] < 815:
            answer = {27: find_y_coord['Answer Option']}
            find_answer_numbers.append(answer)
        elif 815 < find_y_coord['Center'][1] < 840:
            answer = {28: find_y_coord['Answer Option']}
            find_answer_numbers.append(answer)
        elif 840 < find_y_coord['Center'][1] < 865:
            answer = {29: find_y_coord['Answer Option']}
            find_answer_numbers.append(answer)
        elif 865 < find_y_coord['Center'][1] < 900:
            answer = {30: find_y_coord['Answer Option']}
            find_answer_numbers.append(answer)
        else:
            find_answer_numbers.append(' * ')
    return find_answer_numbers


# put * for answers not found and broken answers
def replace_with_asterisk(answers_):
    all_numbers = set(range(1, 31))

    answered_numbers = {list(answer.keys())[0] for answer in answers_}

    missing_numbers = all_numbers - answered_numbers

    for num in missing_numbers:
        answers_.append({num: '*'})

    sorted_answers = sorted(answers_, key=lambda x: list(x.keys())[0])
    return sorted_answers


# delete if multiple answers are marked for one question
def remove_duplicates(sorted_answers):
    duplicated_keys = [list(answer.keys())[0] for answer in sorted_answers]
    unique_keys = set(key for key in duplicated_keys if duplicated_keys.count(key) > 1)

    unique_answers = [answer for answer in sorted_answers if list(answer.keys())[0] not in unique_keys]

    return unique_answers
