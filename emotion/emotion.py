import cv2
from deepface import DeepFace
from retinaface import RetinaFace
import time
from collections import Counter

# Start capturing video
cap = cv2.VideoCapture(0)

# Initialize variables for averaging emotions
emotion_list = []
start_time = time.time()
window_duration = 5  # Time window in seconds
min_face_size = 50  # Minimum size of the detected face

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture video frame.")
        break

    # Detect faces using RetinaFace
    faces = RetinaFace.detect_faces(frame)

    if isinstance(faces, dict):  # Check if any faces are detected
        for face_key, face_data in faces.items():
            confidence = face_data["score"]
            facial_area = face_data["facial_area"]
            x1, y1, x2, y2 = facial_area

            # Filter detections by confidence and face size
            if confidence > 0.9 and (x2 - x1) > min_face_size and (y2 - y1) > min_face_size:
                # Extract face ROI
                face_roi = frame[y1:y2, x1:x2]

                try:
                    # Perform emotion analysis on the face ROI
                    result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)

                    # Determine the dominant emotion
                    emotion = result[0]['dominant_emotion']
                    emotion_list.append(emotion)

                    # Draw rectangle around face and label with predicted emotion
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, emotion, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                except Exception as e:
                    print(f"Error analyzing emotion: {e}")

    # Display the resulting frame
    cv2.imshow('Real-time Emotion Detection', frame)

    # Calculate average emotion every 5 seconds
    elapsed_time = time.time() - start_time
    if elapsed_time >= window_duration:
        if emotion_list:
            # Count the frequency of each emotion and find the most common one
            emotion_counter = Counter(emotion_list)
            avg_emotion = emotion_counter.most_common(1)[0][0]
            print(f"Average Emotion in Last {window_duration} Seconds: {avg_emotion}")
        else:
            print("No emotions detected in the last 5 seconds.")

        # Reset for the next window
        emotion_list = []
        start_time = time.time()

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close all windows
cap.release()
cv2.destroyAllWindows()
