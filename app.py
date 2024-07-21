import cv2
import requests
from tkinter import Tk, Label, Button, Frame
from PIL import Image, ImageTk

# Function to capture and process the image
def capture_and_send():
    global cap, result_label

    ret, frame = cap.read()
    if ret:
        filename = 'screenshot.jpg'
        cv2.imwrite(filename, frame)
        result = send_screenshot(filename)
        update_gui(result)

# Function to send the screenshot and get the response
def send_screenshot(file_path):
    url = "https://renderapp-h819.onrender.com/identify-lateral-flow-test/"
    with open(file_path, 'rb') as file:
        response = requests.post(url, files={'file': file})
    return response.json().get("result")

# Function to update the GUI with the result
def update_gui(result):
    global result_label
    result_label.config(text=f"Result: {result}")

# Function to update the video stream
def update_stream():
    global cap, video_label, video_width, video_height
    
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (video_width, video_height))
        img = Image.fromarray(frame)
        img = ImageTk.PhotoImage(img)
        video_label.config(image=img)
        video_label.image = img
    root.after(10, update_stream)

# Initialize the main application window
root = Tk()
root.title("Real-Time Camera Stream")
root.geometry("375x667")

# Set video dimensions
video_width = 360
video_height = 480

# Create a frame for the video stream
video_frame = Frame(root, width=video_width, height=video_height)
video_frame.pack(pady=10)
video_frame.pack_propagate(False)  # Prevent the frame from resizing to fit the content

# Initialize the camera
cap = cv2.VideoCapture(0)

# Create a label to display the video stream
video_label = Label(video_frame)
video_label.pack()

# Create a label to display the result
result_label = Label(root, text="Result: ", font=("Arial", 18))
result_label.pack(pady=10)

# Create a button to capture and process the image
capture_button = Button(root, text="Take Image", command=capture_and_send)
capture_button.pack(pady=10)

# Start the video stream
update_stream()

# Start the main loop
root.mainloop()

# Release the camera when the application is closed
cap.release()