import time
import threading
import httpServer
import cv2
from PoseEstimationModule import poseDetector
import controller
import queue
# import graph

req = None


def get_requests():
    global req
    while True:
        if not httpServer.request_queue.empty():
            request = httpServer.request_queue.get()
            # print("Received request:", request)
            req = request
        time.sleep(1)  # be careful


def pose_identifier(queue):
    global req
    print('post_detector_started')

    cap = cv2.VideoCapture(0)
    pTime = 0

    detector = poseDetector()
    update_queue = False

    while True:

        if req == 'start':
            update_queue = True
        success, img = cap.read()
        img = detector.findPose(img)
        lmList = detector.findPosition(img, draw=False)

        if len(lmList) > 0:
            # print(lmList[12], lmList[14], lmList[16])  # 12- shoulder, 14- elbow, 16- hand
            cv2.circle(img, (lmList[12][1], lmList[12][2]), 5, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (lmList[14][1], lmList[14][2]), 5, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (lmList[16][1], lmList[16][2]), 5, (255, 0, 0), cv2.FILLED)
            if update_queue:
                queue.put([lmList[12], lmList[14], lmList[16]])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (580, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow("WebCam", cv2.flip(img, 1))

        #----------------------------------------------------------------------------------------------------------10/17
        if req == 'stop':
            update_queue = False
            break
        #---------------------------------------------------------------------------------------------------------------

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def main():
    # Your main program logic here
    global req
    print("Main program started.")

    # Start the print_requests function in a separate thread
    request_thread = threading.Thread(target=get_requests, daemon=True)
    request_thread.daemon = True
    request_thread.start()

    shared_queue = queue.Queue()

    pose_thread = threading.Thread(target=pose_identifier, args=(shared_queue,))
    controller_thread = threading.Thread(target=controller.controller, daemon=True, args=(shared_queue,))
    #graph_thread = threading.Thread(target=graph.plot, daemon=True, args=(controller.angle_queue,))          #optional Thread ....

    # graph_thread.start()                          ....
    pose_thread.start()
    controller_thread.start()


if __name__ == '__main__':
    main()
