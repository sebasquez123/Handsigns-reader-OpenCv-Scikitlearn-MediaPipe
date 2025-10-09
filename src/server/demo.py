import cv2
import pandas as pd  


USE_SMOOTHING = True
SMOOTH_ALPHA = 0.3  
_smooth_distance = None  


def demo(mp_drawing,hands,mp_hands,classifier,frame):
    '''Process the input frame to detect hand gestures, and annotate the frame with results.'''
    
    global _smooth_distance
    feature_names = None
    
    # Check if the classifier has feature names
    if classifier is not None and hasattr(classifier, 'feature_names_in_'):
        feature_names = classifier.feature_names_in_

    # Formating frame for processing and analysis
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    # ride through the hand landmarks on the frame if detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw hand landmarks on the frame
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            data = []

            # append the x,y,z coordinates of each landmark to the data list.
            for lm in hand_landmarks.landmark:
                data.extend([lm.x, lm.y, lm.z])
            # Create a DataFrame if feature names are available, else use a simple list.
            if feature_names is not None:
                X = pd.DataFrame([data], columns=feature_names)
            else:
                X = [data]

            # Predict the gesture using the trained classifier if available.
            if classifier is not None:
                pred = classifier.predict(X)[0]
                # Display the predicted gesture on the frame.
                cv2.putText(frame, f"Gesture: {pred}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                # If no classifier loaded, annotate that the model is missing.
                cv2.putText(frame, "Gesture: (no model)", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    return frame
