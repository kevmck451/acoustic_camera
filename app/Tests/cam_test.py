# import cv2
#
# cap = cv2.VideoCapture(0)  # Use the appropriate camera index
# if not cap.isOpened():
#     print("Cannot open camera")
#     exit()
# while True:
#     ret, frame = cap.read()
#     if not ret:
#         print("Can't receive frame (stream end?). Exiting ...")
#         break
#     cv2.imshow('frame', frame)
#     if cv2.waitKey(1) == ord('q'):
#         break
# cap.release()
# cv2.destroyAllWindows()


# import cv2
# import tkinter as tk
# from PIL import Image, ImageTk
# import customtkinter as ctk
#
# def update_frame():
#     _, frame = cap.read()
#     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     frame = Image.fromarray(frame)
#     frame = ImageTk.PhotoImage(frame)
#     video_label.configure(image=frame)
#     video_label.image = frame
#     video_label.after(10, update_frame)
#
# cap = cv2.VideoCapture(0)  # Use 0 for the first webcam
#
# root = ctk.CTk()  # This initializes your main CustomTkinter window
# video_label = ctk.CTkLabel(root)  # Use CTkLabel for a CustomTkinter Label
# video_label.pack()
#
# update_frame()  # Start the frame update loop
#
# root.mainloop()



import cv2

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
ret, frame = cap.read()
if ret:
    cv2.imshow('Camera', frame)
    cv2.waitKey(0)
else:
    print("Can't receive frame (stream end?). Exiting ...")
cap.release()
cv2.destroyAllWindows()
