import cv2
import numpy as np
import cv.camera as camera
import cv.cv_utils as cv_utils
import cv.constants as constants
import cv.geometry_utils as geometry_utils
import cv.input_generator as input_generator
import cv.image_background_remove as image_background_remove

camera = camera.Camera()
imageBackgroundRemover = None
camera.start_recording()

while camera.is_recording():
    frame = camera.get_current_frame()
    frame = cv_utils.smooth_frame(frame)
    cv2.rectangle(frame, (int(constants.ROI_X_BEGIN * frame.shape[1]), 0),
                  (frame.shape[1], int(constants.ROI_Y_END * frame.shape[0])), (255, 0, 0), 2)
    cv_utils.show_frame(frame, "camera")
    if imageBackgroundRemover is not None and imageBackgroundRemover.calibrated:
        img = imageBackgroundRemover.remove_background_from_image(frame)
        img = cv_utils.crop_frame(img,
                                  (0 , int(constants.ROI_Y_END * img.shape[0])),
                                  (int(constants.ROI_X_BEGIN * img.shape[1]), img.shape[1]))
        cv_utils.show_frame(img, "mask")
        gray = cv_utils.convert_frame_to_gray_scale(img)
        blur = cv_utils.perform_gaussian_blur(gray, constants.GAUSSIAN_BLUR_VAL)
        low_blur = cv_utils.perform_gaussian_blur(gray, constants.GAUSSIAN_BLUR_FINGERS_COUNT)
        _, thresh = cv2.threshold(blur, constants.BINARY_THRESHOLD, 255, cv2.THRESH_BINARY)
        _, thresh2 = cv2.threshold(low_blur, constants.BINARY_THRESHOLD, 255, cv2.THRESH_BINARY)
        cv_utils.show_frame(thresh, "filtered")
        contours = cv_utils.extract_contours_from_image(thresh)
        contours_fingers = cv_utils.extract_contours_from_image(thresh2)
        external_contour = geometry_utils.select_external_contour(contours)
        external_contour_fingers = geometry_utils.select_external_contour(contours_fingers)
        external_without_blur_contour = geometry_utils.select_external_contour(contours)
        hull = cv_utils.get_convex_hull(external_contour)
        # hull = external_contour
        hull = geometry_utils.validate_convex_hull(hull, (img.shape[0], img.shape[1]))

        if hull is not None:
            offset = (int(constants.ROI_X_BEGIN * frame.shape[1]), 0 )
            polygon_angles = geometry_utils.get_polygon_angles(hull)
            for i in range(len(polygon_angles)):
                cv_utils.draw_text(frame, tuple(map(sum, zip(hull[i][0], offset))), str(i) + ': ' +str(polygon_angles[i]))
            center1 = cv_utils.get_polygon_center(external_contour)
            center2 = cv_utils.get_polygon_center(hull)
            cv_utils.draw_point(frame, tuple(map(sum, zip(center1, offset))))
            cv_utils.draw_point(frame, tuple(map(sum, zip(center2, offset))))
            cv2.drawContours(frame, [external_contour],  0, (0, 255, 0), 2, offset = offset)
            cv2.drawContours(frame, [hull], 0, (0, 0, 255), 3, offset = offset)
            input = input_generator.generate_input(center1, hull, polygon_angles, img.shape)
            if input is not None:
                cv_utils.draw_point(frame, tuple(map(sum, zip(input, offset))))
                command = str(geometry_utils.get_vector_direction(input - np.array(center1)))
                cv_utils.draw_text(frame, (40, 40), command)
            else:
                external_contour_fingers
        cv2.imshow('output', frame)

    k = cv2.waitKey(10)
    if k == 27:  # press ESC to exit
        if camera is not None and camera.is_recording():
            camera.stop_recording()
        break
    elif k == ord('b'):  # press 'b' to capture the background
        imageBackgroundRemover = image_background_remove.ImageBackgroundRemover()
        print('calibrated')
