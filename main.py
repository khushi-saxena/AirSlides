import cv2
import os
import numpy as np
from HandTracker import HandDetector
from dottedline import drawrect

# ── Config ────────────────────────────────────────────────────────────────
width, height = 1280, 720
frames_folder = "Images"
slide_num = 0

# size of the small camera inset
hs, ws = int(120 * 1.2), int(213 * 1.2)

# gesture-zone (upper-right) for slide controls
ge_thresh_y = 400
ge_thresh_x = 750

# debounce & annotation state
gest_done = False
gest_counter = 0
delay = 15

annotations = [[]]
annot_num = 0
annot_start = False

# ── Load slides ───────────────────────────────────────────────────────────
path_imgs = sorted(os.listdir(frames_folder), key=len)
print("Slides:", path_imgs)

# ── Camera & detector setup ───────────────────────────────────────────────
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

detector = HandDetector(detectionCon=0.8, maxHands=1)

# ── Main loop ─────────────────────────────────────────────────────────────
while True:
    success, frame = cap.read()
    if not success:
        break
    frame = cv2.flip(frame, 1)

    # load & resize current slide
    slide_path = os.path.join(frames_folder, path_imgs[slide_num])
    slide = cv2.imread(slide_path)
    slide = cv2.resize(slide, (width, height))
    h, w, _ = slide.shape

    # draw the gesture-zone box on the camera feed
    drawrect(frame, (width, 0), (ge_thresh_x, ge_thresh_y), (0, 255, 0), 5, 'dotted')

    # detect hands & landmarks
    hands, frame = detector.findHands(frame)

    if hands:
        hand = hands[0]
        cx, cy = hand["center"]
        lm_list = hand["lmList"]
        fingers = detector.fingersUp(hand)

        # map the index-finger tip into slide coords
        x_val = int(np.interp(lm_list[8][0], [width//2, w], [0, width]))
        y_val = int(np.interp(lm_list[8][1], [150, height-150], [0, height]))
        index_fing = (x_val, y_val)

        # ── SLIDE CONTROLS (only in upper-right zone) ─────────────
        if not gest_done and cy < ge_thresh_y and cx > ge_thresh_x:
            # Next Slide: Palm (all 5 fingers up)
            if fingers == [1, 1, 1, 1, 1]:
                if slide_num < len(path_imgs) - 1:
                    gest_done = True
                    slide_num += 1
                    annotations = [[]]
                    annot_num = 0

            # Previous Slide: Thumb up only
            elif fingers == [1, 0, 0, 0, 0]:
                if slide_num > 0:
                    gest_done = True
                    slide_num -= 1
                    annotations = [[]]
                    annot_num = 0

            # Clear/Undo: C-Sign ([0,1,1,1,1])
            elif fingers == [0, 1, 1, 1, 1]:
                if len(annotations) > 0:
                    gest_done = True
                    annotations.pop()
                    annot_num = max(annot_num - 1, 0)

        # ── POINTER MODE (anywhere): L-Sign (thumb+index)
        if fingers == [1, 1, 0, 0, 0]:
            cv2.circle(slide, index_fing, 6, (0, 0, 255), cv2.FILLED)
            annot_start = False

        # ── DRAW MODE (anywhere): Index up only
        elif fingers == [0, 1, 0, 0, 0]:
            if not annot_start:
                annot_start = True
                annot_num += 1
                annotations.append([])
            annotations[annot_num].append(index_fing)
            cv2.circle(slide, index_fing, 6, (0, 0, 255), cv2.FILLED)
        else:
            annot_start = False

    # debounce slide gestures
    if gest_done:
        gest_counter += 1
        if gest_counter > delay:
            gest_done = False
            gest_counter = 0

    # draw all annotations on the slide
    for stroke in annotations:
        for i in range(1, len(stroke)):
            cv2.line(slide, stroke[i-1], stroke[i], (0, 0, 255), 6)

    # overlay camera feed in bottom-right
    cam_small = cv2.resize(frame, (ws, hs))
    slide[h-hs:h, w-ws:w] = cam_small

    cv2.imshow("Slides", slide)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# clean up
cap.release()
cv2.destroyAllWindows()
