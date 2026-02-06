# MAIN - this is the main entry point of the application where the video processing loop is implemented. 
# It initializes the person detector, safety analytics, and handles video reading, processing, and output generation.

import cv2
from detector import PersonDetector
from posture import classify_posture
from safety_rules import get_safety_status
from analytics import SafetyAnalytics

VIDEO_PATH = "data/sample_video.mp4"
OUTPUT_VIDEO_PATH = "outputs/processed_video.mp4"


def draw_boxes(frame, boxes): # this function takes a video frame and a list of detected bounding boxes as input.
                             # For each detected person (represented by a bounding box), it classifies the posture and determines the safety status based on predefined rules.
    postures = []
    safety_states = []

    for (x1, y1, x2, y2, conf) in boxes:
        posture = classify_posture(x1, y1, x2, y2)
        safety = get_safety_status(posture)

        postures.append(posture)
        safety_states.append(safety)

        if safety == "SAFE":
            color = (0, 255, 0)
        elif safety == "MONITOR":
            color = (0, 255, 255)
        else:
            color = (0, 0, 255)

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        label = f"{posture} | {safety} | {conf:.2f}"

        cv2.putText(
            frame,
            label,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2
        )

    return postures, safety_states # this function returns two lists: 
                                    # postures and safety_states, which contain the classified posture 
                                    # and safety status for each detected person in the current video frame.


def main(): # this is the main function that orchestrates the video processing workflow.
          #  It initializes the person detector and safety analytics, opens the video file, and processes each frame in a loop.
    detector = PersonDetector()
    analytics = SafetyAnalytics()

    cap = cv2.VideoCapture(VIDEO_PATH)

    if not cap.isOpened():
        print("Error: Cannot open video.")
        return

    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Define codec and create VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(OUTPUT_VIDEO_PATH, fourcc, fps, (width, height))

    print("Processing video...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        boxes = detector.detect_people(frame)

        postures, safety_states = draw_boxes(frame, boxes)

        analytics.update(boxes, postures, safety_states)

        out.write(frame)

        cv2.imshow("Safety Monitoring System", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release() # this will release the video capture object, freeing up any resources associated with it, and out.release() will release the video writer object, ensuring that the output video file is properly saved and closed after processing is complete. Finally, cv2.destroyAllWindows() will close any OpenCV windows that were opened during the video processing, cleaning up the user interface.
    out.release()# this will release the video writer object, ensuring that the output video file is properly saved and closed after processing is complete.
    cv2.destroyAllWindows() # this will close any OpenCV windows that were opened during the video processing, cleaning up the user interface.

    analytics.generate_report()

    print("Processed video saved to:", OUTPUT_VIDEO_PATH) 


if __name__ == "__main__":
    main()

# THANKYOU JI FOR REVIEWING MY CODE HOPING TO CONNECT WITH U FOR THE NEXT ROUND OF INTERVIEW :) SHAKTESH
