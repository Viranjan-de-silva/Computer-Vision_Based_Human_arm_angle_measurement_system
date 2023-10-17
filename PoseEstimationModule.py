import cv2
import mediapipe as mp
import time


class poseDetector:

    def __init__(self, mode=False, modelComplexity=1, smLm=True, enaSeg=False, smSeg=True, minDetectConfi=0.5,
                 minTrackConfi=0.5):
        self.static_image_mode = mode
        self.model_complexity = modelComplexity
        self.smooth_landmarks = smLm
        self.enable_segmentation = enaSeg
        self.smooth_segmentation = smSeg

        self.min_detection_confidence = minDetectConfi
        self.min_tracking_confidence = minTrackConfi

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.static_image_mode, self.model_complexity, self.smooth_landmarks,
                                     self.enable_segmentation, self.smooth_segmentation, self.min_detection_confidence,
                                     self.min_tracking_confidence)

    def findPose(self, img, draw=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img

    def findPosition(self, img, draw=True):
        lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return lmList


def main():
    cap = cv2.VideoCapture(0)
    pTime = 0

    detector = poseDetector()

    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        lmList = detector.findPosition(img, draw=False)

        if len(lmList) > 16:
            print(lmList[12], lmList[14], lmList[16])  # 12- shoulder, 14- elbow, 16- hand
            cv2.circle(img, (lmList[12][1], lmList[12][2]), 5, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (lmList[14][1], lmList[14][2]), 5, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (lmList[16][1], lmList[16][2]), 5, (255, 0, 0), cv2.FILLED)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        cv2.imshow("WebCam", cv2.flip(img, 1))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == "__main__":  # running this file it runs main function, if just calling another function it will not run main part
    main()
