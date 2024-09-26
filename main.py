import cv2
import threading
import speech_recognition as sr
import pyttsx3
from ultralytics import YOLO

# Load the YOLOv8 model (use the 'n' version for fast performance)
model = YOLO('yolov8n.pt')

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Set up speech recognizer
recognizer = sr.Recognizer()

# Thread lock for shared resources
lock = threading.Lock()

# Function to handle text-to-speech
def speak(text):
    with lock:
        engine.say(text)
        engine.runAndWait()

# Function to handle speech recognition
def recognize_speech():
    with sr.Microphone() as source:
        print("Listening for commands...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"Command: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
            return None

# Function to process the recognized speech command
def process_command(command):
    if "what is" in command:
        speak("Let me analyze the scene.")
        # Optionally add logic to respond based on detected objects

# Function for object detection and showing bounding boxes
def object_detection():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Failed to grab frame.")
            break

        # Run YOLOv8 inference
        results = model(frame)

        # Display results (bounding boxes)
        annotated_frame = results[0].plot()

        # Display the video with bounding boxes
        cv2.imshow('AR Assistant - Object Detection', annotated_frame)

        # Capture keyboard input for exiting
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Thread for handling real-time voice commands
def voice_command_thread():
    while True:
        command = recognize_speech()
        if command:
            process_command(command)

if __name__ == "__main__":
    # Start the object detection and voice command processes simultaneously
    speak("Hello! I'm your Augmented Reality AI Assistant.")

    # Create a thread for speech recognition
    voice_thread = threading.Thread(target=voice_command_thread)
    voice_thread.daemon = True
    voice_thread.start()

    # Run object detection in the main thread
    object_detection()
