import cv2
import numpy as np

cap = cv2.VideoCapture(0)
def webcam_contours():
    # Open de webcam (standaard camera is index 0)

    # Controleer of de camera goed opent
    if not cap.isOpened():
        print("Kan de webcam niet openen.")
        exit()

    # Begin de loop om beelden van de camera te lezen
    while True:
        # Lees een frame van de camera
        low_array = np.array([90,90,90])
        high_array = np.array([255,250,250])
        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (9, 9), 0)
        edges = cv2.Canny(blurred, 0, 150)
        countours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)
        output = frame.copy()
        cv2.drawContours(output, countours, -1, (0, 255, 0), 2)

        cv2.imshow("Origineel", frame)
        cv2.imshow("Randen", edges)
        cv2.imshow("Contouren", output)

        """

        ret, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(frame,low_array ,high_array )

        edge = cv2.Canny(gray, 30, 200)
        canny_output = cv2.Canny(gray, 100, 150)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        img_2 = cv2.drawContours(thresh, contours, -1, (100, 100, 100), 2)
       # result = cv2.bitwise_and(canny_output, frame, mask=mask)
        drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
        for i in range(len(contours)):
            color = (rng.randint(0, 256), rng.randint(0, 256), rng.randint(0, 256))
            cv2.drawContours(drawing, contours, 1, (100,100,100), 2, cv2.LINE_8, hierarchy, 0)
        # Show in a window
        cv2.imshow('Contours', drawing)

        # Als het frame succesvol is gelezen
        if not ret:
            print("Kan frame niet lezen.")
            break

        # Toon het frame in een window
        cv2.imshow("HSV", img_2)
        # cv2.imshow('Webcam Feed', frame)
       # cv2.imshow('Threshold', thresh)
        cv2.imshow("edge", edge)
        """

        output_path = r'C:\Users\Jelle\PycharmProjects\pythonProject\wanted.png'
        # Wacht op een toets (bijv. 'q' om te stoppen)
        if cv2.waitKey(1) & 0xFF == ord('q'):
          break
        if cv2.waitKey(1) & 0xFF == ord("x"):
            cv2.imwrite(output_path, frame)
    # Bevrijd de camera en sluit alle OpenCV vensters
    cap.release()
    cv2.destroyAllWindows()
