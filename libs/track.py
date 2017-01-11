import cv2
import numpy as np
import copy


class Meanshife:
    def __init__(self, initial_rect, image):
        self._rect = initial_rect
        self._image = image
        x, y, w, h = self._rect
        roi = image[y:y+h, x:x+w]
        hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_roi, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
        self._roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])
        self._term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

    def track(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv], [0], self._roi_hist, [0, 180], 1)
        _, self._rect = cv2.meanShift(dst, self._rect, self._term_crit)
        return self._rect


def draw_circle(event,x,y,flags,param):
    global ix, iy, drawing, mode, tracker
    mode = True
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    elif event == cv2.EVENT_MOUSEMOVE and flags == 33:
        if drawing is True:
            if mode is True:
                temp = copy.copy(frame)
                cv2.rectangle(temp, (ix, iy), (x, y), (0, 255, 0), 2)
                cv2.imshow('frame', temp)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        tracker = Meanshife((min(ix, x), min(iy, y), abs(ix-x), abs(iy - y)), frame)


def region2point(region):
    point1 = (region[0],region[1])
    point2 = (region[0] + region[2],region[1] + region[3])
    return point1, point2

if __name__ == "__main__":
    cap =cv2.VideoCapture('/home/cpk/inputcar.avi')
    cv2.namedWindow('frame')
    cv2.setMouseCallback('frame', draw_circle)
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    cv2.waitKey(0)

    while True:
        ret, frame = cap.read()
        if cv2.waitKey(20) & 0xFF == ord('q') or ret is False:
            break
        region = tracker.track(frame)
        point1, point2 = region2point(region)
        cv2.rectangle(frame, point1, point2, (0, 255, 0), 2)
        cv2.imshow('frame', frame)
