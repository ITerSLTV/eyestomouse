import cv2
import mediapipe as mp
import numpy as np
import time
import threading
import pyautogui, sys
import autopy

mp_drawing = mp.solutions.drawing_utils
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)

LEFT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
RIGHT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
LEFT_IRIS = [474, 475, 476, 477]
RIGHT_IRIS = [469, 470, 471, 472]

bli_leftx = []
bli_lefty = []
bli_rightx =[]
bli_righty =[]

def get_frame_global():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    global check_stop, nose_location, count_left_eye, count_right_eye
    global frame_itf, frame_left_eye, frame_right_eye, frame_nose
    check_stop = True
    while True:
        ret, frame = cap.read()
        frame_itf = frame
        frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
        frame_mapping = cv2.resize(frame, (1920, 1080))
        frame_mapping.flags.writeable = False
        frame.flags.writeable = False
        results = face_mesh.process(frame)
        results_mapping = face_mesh.process(frame_mapping)
        frame_mapping.flags.writeable = True
        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame_mapping = cv2.cvtColor(frame_mapping, cv2.COLOR_RGB2BGR)

        img_h, img_w, img_c = frame.shape
        img_h_m, img_w_m, img_c_m = frame_mapping.shape
        face_3d = []
        face_2d = []

        if results_mapping.multi_face_landmarks:
            for face_landmarks in results_mapping.multi_face_landmarks:
                for idx, lm in enumerate(face_landmarks.landmark):
                    if idx == 1:
                        nose_location = (int(lm.x * img_w_m), int(lm.y * img_h_m))
                        break
            cv2.circle(frame_mapping, nose_location, 5, (0, 255, 0), 1, cv2.LINE_AA)

        if results.multi_face_landmarks:
            mesh_points = np.array([np.multiply([p.x, p.y], [img_w, img_h]).astype(int) for p in results.multi_face_landmarks[0].landmark])
            (l_cx, l_cy), l_radius = cv2.minEnclosingCircle(mesh_points[LEFT_IRIS])
            (r_cx, r_cy), r_radius = cv2.minEnclosingCircle(mesh_points[RIGHT_IRIS])
            center_left = np.array([l_cx, l_cy], dtype=np.int32)
            center_right = np.array([r_cx, r_cy], dtype=np.int32)
            cv2.circle(frame, center_left, 2, (255, 0, 255), 1, cv2.LINE_AA)
            cv2.circle(frame, center_right, 2, (255, 0, 255), 1, cv2.LINE_AA)

            for face_landmarks in results.multi_face_landmarks:
                for idx, lm in enumerate(face_landmarks.landmark):
                    if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                        if idx == 1:
                            nose_2d = (lm.x * img_w, lm.y * img_h)

                        x, y = int(lm.x * img_w), int(lm.y * img_h)

                        face_2d.append([x, y])
                        face_3d.append([x, y, lm.z])

                    if idx == 225:
                        eye_left = (int(lm.x * img_w), int(lm.y * img_h))
                        cv2.circle(frame, (int(lm.x * img_w), int(lm.y * img_h)), 3, (255, 0, 255))
                    if idx == 228:
                        eye_left1 = (int(lm.x * img_w), int(lm.y * img_h))
                        cv2.circle(frame, (int(lm.x * img_w), int(lm.y * img_h)), 3, (255, 0, 255))
                    if idx == 128:
                        eye_left2 = (int(lm.x * img_w), int(lm.y * img_h))
                        cv2.circle(frame, (int(lm.x * img_w), int(lm.y * img_h)), 3, (255, 0, 255))
                    if idx == 221:
                        eye_left3 = (int(lm.x * img_w), int(lm.y * img_h))
                        cv2.circle(frame, (int(lm.x * img_w), int(lm.y * img_h)), 3, (255, 0, 255))

                    if idx == 441:
                        eye_right = (int(lm.x * img_w), int(lm.y * img_h))
                        cv2.circle(frame, (int(lm.x * img_w), int(lm.y * img_h)), 3, (255, 0, 255))
                    if idx == 445:
                        eye_right1 = (int(lm.x * img_w), int(lm.y * img_h))
                        cv2.circle(frame, (int(lm.x * img_w), int(lm.y * img_h)), 3, (255, 0, 255))
                    if idx == 448:
                        eye_right2 = (int(lm.x * img_w), int(lm.y * img_h))
                        cv2.circle(frame, (int(lm.x * img_w), int(lm.y * img_h)), 3, (255, 0, 255))
                    if idx == 412:
                        eye_right3 = (int(lm.x * img_w), int(lm.y * img_h))
                        cv2.circle(frame, (int(lm.x * img_w), int(lm.y * img_h)), 3, (255, 0, 255))
                    if idx in LEFT_IRIS:
                        bli_leftx.append((int(lm.x * img_w)))
                        bli_lefty.append((int(lm.y * img_h)))
                    if idx in RIGHT_IRIS:
                        bli_rightx.append((int(lm.x * img_w)))
                        bli_righty.append((int(lm.y * img_h)))

                face_2d = np.array(face_2d, dtype=np.float64)
                face_3d = np.array(face_3d, dtype=np.float64)

                focal_length = 1 * img_w

                cam_matrix = np.array([[focal_length, 0, img_h / 2],
                                       [0, focal_length, img_w / 2],
                                       [0, 0, 1]])

                dist_matrix = np.zeros((4, 1), dtype=np.float64)
                success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)
                rmat, jac = cv2.Rodrigues(rot_vec)
                angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3((rmat))

                x = angles[0] * 360
                y = angles[1] * 360
                z = angles[2] * 360

                p1 = (int(nose_2d[0]), int(nose_2d[1]))
                p2 = (int(nose_2d[0] + y * 10), int(nose_2d[1] - x * 10))

                cv2.circle(frame, p1, 3, (255, 0, 255))
                cv2.line(frame, (0, p1[1]), (640, p1[1]), (255, 0, 0), 1)
                cv2.line(frame, (p1[0], 0), (p1[0], 480), (255, 0, 0), 1)
                cv2.line(frame, (0, center_right[1]), (640, center_right[1]), (0, 255, 0), 1)
                cv2.line(frame, (center_right[0], 0), (center_right[0], 480), (0, 255, 0), 1)
                cv2.line(frame, (0, center_left[1]), (640, center_left[1]), (0, 255, 0), 1)
                cv2.line(frame, (center_left[0], 0), (center_left[0], 480), (0, 255, 0), 1)

#--------------------------------------put on interface--------------------------------------
                frame_left_eye = frame[eye_left[1] - 20 : eye_left[1] + eye_left1[1] - eye_left[1],
                           eye_left[0]: eye_left[0] + eye_left3[0] - eye_left[0]]
                frame_right_eye = frame[eye_right[1] - 20 : eye_right3[1], eye_right[0] : eye_right1[0]]
                frame_nose = frame[p1[1] - 25 : p1[1] + 25, p1[0] - 25 : p1[0] + 25]
#-------------------------------------------------------

                count_left_eye = frame[min(bli_lefty): max(bli_lefty), min(bli_leftx): max(bli_leftx)]
                count_right_eye = frame[min(bli_righty) + 3: max(bli_righty),
                                  min(bli_rightx): max(bli_rightx)]

                bli_lefty.clear()
                bli_leftx.clear()
                bli_rightx.clear()
                bli_righty.clear()

                # mp_drawing.draw_landmarks(image=frame,
                #                         landmark_list=face_landmarks,
                #                         connections=mp_face_mesh.FACEMESH_CONTOURS,
                #                         landmark_drawing_spec=drawing_spec,
                #                         connection_drawing_spec=drawing_spec)

        frame_mapping = cv2.rectangle(frame_mapping, (800, 500), (1000, 600), (0, 255, 0), 3)
        #cv2.imshow('Camera', count_left_eye)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            check_stop = False
            break

    cap.release()
    cv2.destroyAllWindows()

def blinking():
    time.sleep(1)
    global check_stop, count_left_eye, count_right_eye

    check_count_l = False
    check_count_r = False
    check_eye_left = False
    check_eye_right = False
    past_time = time.time()
    count_l = 0
    count_r = 0

    while True:
        left_02 = cv2.cvtColor(count_left_eye, cv2.COLOR_BGR2GRAY)
        _, left_02 = cv2.threshold(left_02, 30, 255, cv2.THRESH_BINARY)
        right_02 = cv2.cvtColor(count_right_eye, cv2.COLOR_BGR2GRAY)
        _, right_02 = cv2.threshold(right_02, 30, 255, cv2.THRESH_BINARY)

        current_right = np.mean(left_02)
        current_left = np.mean(right_02)

        if check_count_r == False:
            if current_left > 200 and check_eye_left == False and check_count_l == False:
                check_eye_left = True
                print("-------------")
            elif current_left < 190 and check_eye_left == True and check_count_l == False:
                print("-------------------Blinking Left--------------------------")
                check_eye_left = False
                check_count_l = True
                past_time = time.time()
            if time.time() - past_time <= 1 and check_count_l == True:
                if current_left > 200 and check_eye_left == False and check_count_l == True:
                    check_eye_left = True
                elif current_left < 190 and check_eye_left == True and check_count_l == True:
                    print("-------------------COUNT--------------------------")
                    check_eye_left = False
                    count_l += 1
            elif count_l == 0 and check_count_l == True:
                print("Click")
                pyautogui.click(button='left')
                check_count_l = False
                count_l = 0
            elif count_l == 1 and check_count_l == True:
                print("DouClick")
                pyautogui.doubleClick()
                check_count_l = False
                count = 0
            elif count_l == 2 and check_count_l == True:
                print("Scolling Up")
                pyautogui.scroll(500)
                check_count_l = False
                count_l = 0
            else:
                check_count_l = False
                count_l = 0

        if check_count_l == False:
            if current_right > 210 and check_eye_right == False and check_count_r == False:
                check_eye_right = True
                print("-------------")
            if current_right < 190 and check_eye_right == True and check_count_r == False:
                print("-------------------Blinking Right--------------------------")
                check_eye_right = False
                check_count_r = True
                past_time = time.time()
            if time.time() - past_time <= 1.5 and check_count_r == True:
                if current_right > 200 and check_eye_right == False and check_count_r == True:
                    check_eye_right = True
                elif current_right < 190 and check_eye_right == True and check_count_r == True:
                    print("-------------------COUNT--------------------------")
                    check_eye_right = False
                    count_r += 1
            elif count_r == 0 and check_count_r == True:
                print("Click_Right")
                pyautogui.click(button='right')
                check_count_r = False
                count_r = 0
            elif count_r == 1 and check_count_r == True:
                print("Copy")
                pyautogui.keyDown('shift')
                pyautogui.click(button='left')
                pyautogui.keyUp('shift')

                pyautogui.keyDown('ctrl')
                pyautogui.press('c')
                pyautogui.keyUp('ctrl')

                check_count_r = False
                count_r = 0
            elif count_r == 2 and check_count_r == True:
                print("Scolling Down")
                pyautogui.scroll(-500)
                check_count_r = False
                count_r = 0
            else:
                check_count_r = False
                count_r = 0

        if check_stop == False:
            break

def mapping_screen():
    time.sleep(1)
    global check_stop, nose_location
    global clocX, clocY
    wScr, hScr = pyautogui.size()
    smoothening = 10
    plocX, plocY = 0, 0
    clocX, clocY = 0, 0

    sum_x, sum_y = 0, 0
    ave_x, ave_y = 0, 0
    count, coef_ave = 0, 5

    while True:
        count += 1
        sum_x += nose_location[0]
        sum_y += nose_location[1]
        if count == coef_ave:
            ave_x = int(sum_x / coef_ave)
            ave_y = int(sum_y / coef_ave)
            sum_x, sum_y, count = 0, 0, 0

            xScr = np.interp(ave_x, (800, 1000), (0, wScr))  # (900,500), (1100, 600)
            yScr = np.interp(ave_y, (500, 600), (0, hScr))
            clocX = plocX + (xScr - plocX) / smoothening
            clocY = plocY + (yScr - plocY) / smoothening
            pyautogui.moveTo(clocX, clocY, 0.1)
            plocX, plocY = clocX, clocY

        if check_stop == False:
            break

if __name__ == '__main__':
    x = threading.Thread(target=get_frame_global)
    x.start()
    y = threading.Thread(target=mapping_screen)
    y.start()
    z = threading.Thread(target=blinking)
    z.start()