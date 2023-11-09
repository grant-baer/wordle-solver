import tkinter as tk
from tkinter import messagebox

# Create a tkinter window
root = tk.Tk()
root.geometry("500x500")
root.title("Wordle Game")

label = tk.Label(root, text="Wordle AI", font=('Times New Roman', 24))
label.pack(padx=20, pady=20)


# Create a frame to hold the black boxes
box_frame = tk.Frame(root)
box_frame.pack()

# Create 30 empty black boxes in a 5x6 pattern
white_boxes = []
for row in range(6):
    row_boxes = []
    for col in range(5):
        white_box = tk.Label(box_frame, width=6, height=3, bg="white", borderwidth=1, relief="solid")
        white_box.grid(row=row, column=col, padx=5, pady=5)
        row_boxes.append(white_box)
    white_boxes.append(row_boxes)


# Function to label a specific box with a letter
def label_box_with_letter(row, col, letter):
    if 0 <= row < 6 and 0 <= col < 5:
        white_boxes[row][col].config(text=letter)

# Button to label a specific box with a letter
label_button = tk.Button(root, text="Label Box", command=lambda: label_box_with_letter(1, 2, "X"))
label_button.pack(pady=10)

root.mainloop()