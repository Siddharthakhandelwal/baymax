import cv2

# Initialize video capture (use 0 for webcam or a video file path)
cap = cv2.VideoCapture(0)

# Define the bounding box (x, y, width, height)
bbox = (100, 100, 150, 150)  # Initial bounding box

# Create tracker (using CSRT for accuracy)
tracker = cv2.TrackerCSRT_create()
ret, frame = cap.read()
tracker.init(frame, bbox)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Update the tracker
    success, bbox = tracker.update(frame)
    if success:
        x, y, w, h = [int(v) for v in bbox]  # Convert to integers

        # Draw bounding box
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Get frame dimensions
        frame_h, frame_w, _ = frame.shape

        # Check boundary conditions
        status = []
        if x <= 0:
            status.append("Left")
        if x + w >= frame_w:
            status.append("Right")
        if y <= 0:
            status.append("Top")
        if y + h >= frame_h:
            status.append("Bottom")

        # Display status
        status_text = "Out from: " + ", ".join(status) if status else "Inside"
        cv2.putText(frame, status_text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()