import cv2
import mediapipe as mp
import numpy as np
import time
import threading

mp_drawing = mp.solutions.drawing_utils
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)

LEFT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
RIGHT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
LEFT_IRIS = [474, 475, 476, 477]
RIGHT_IRIS = [469, 470, 471, 472]

current_eye = []
past_eye = []
current_nose =[]
past_nose = []

def get_frame_global():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    global center_right, check_stop, frame_left_eye, frame_right_eye, frame_nose
    check_stop = True
    while True:
        ret, framee = cap.read()
        frame = cv2.resize(framee, (1840, 1380))
        frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
        frame.flags.writeable = False
        results = face_mesh.process(frame)
        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        img_h, img_w, img_c = frame.shape
        face_3d = []
        face_2d = []
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
                            nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 3000)

                        x, y = int(lm.x * img_w), int(lm.y * img_h)

                        face_2d.append([x, y])
                        face_3d.append([x, y, lm.z])

                    if idx == 225:
                        eye_left = (int(lm.x * img_w), int(lm.y * img_h))
                        cv2.circle(frame, (int(lm.x * img_w), int(lm.y * img_h)), 3, (255, 0, 255))
                        # frame_cp = frame_cp[int(lm.y * img_h) - 10 : int(lm.y * img_h) + 30, int(lm.x * img_w) - 10 : int(lm.x * img_w) + 50]
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

                frame_left_eye = frame[eye_left[1] - 20 : eye_left[1] + eye_left1[1] - eye_left[1],
                           eye_left[0]: eye_left[0] + eye_left3[0] - eye_left[0]]
                frame_right_eye = frame[eye_right[1] - 20 : eye_right3[1], eye_right[0] : eye_right1[0]]
                frame_nose = frame[p1[1] - 25 : p1[1] + 25, p1[0] - 25 : p1[0] + 25]

                # mp_drawing.draw_landmarks(image=frame,
                #                         landmark_list=face_landmarks,
                #                         connections=mp_face_mesh.FACEMESH_CONTOURS,
                #                         landmark_drawing_spec=drawing_spec,
                #                         connection_drawing_spec=drawing_spec)

        cv2.imshow('Camera', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            check_stop = False
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    get_frame_global()