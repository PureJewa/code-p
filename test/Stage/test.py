import cv2

def webcam_object_detection():
    # Laad de afbeelding die je wilt detecteren
    template = cv2.imread(r"C:\Users\Jelle\PycharmProjects\pythonProject\knappejonge.png", cv2.IMREAD_GRAYSCALE)
    if template is None:
        print("Kon de template-afbeelding niet laden.")
        return

    # Open de webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Kon de webcam niet openen.")
        return

    while True:
        # Lees een frame van de webcam
        ret, frame = cap.read()
        if not ret:
            print("Kon het frame niet lezen.")
            break

        # Converteer het frame naar grijswaarden
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Pas template matching toe
        result = cv2.matchTemplate(gray_frame, template, cv2.TM_CCOEFF_NORMED)

        # Zoek naar de locatie van de beste match
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Stel een drempel in voor een "match"
        threshold = 0.8  # Pas aan op basis van je situatie
        if max_val >= threshold:
            top_left = max_loc
            h, w = template.shape
            bottom_right = (top_left[0] + w, top_left[1] + h)

            # Teken een rechthoek rond het gedetecteerde object
            cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
            print("Object gevonden")
        else:
            print("niet gevonden")
        # Toon het resultaat

        cv2.imshow("Webcam Object Detection", frame)

        # Breek de lus af bij het indrukken van de 'q'-toets
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Ruim op
    cap.release()
    cv2.destroyAllWindows()

