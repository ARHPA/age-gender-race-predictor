import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image

import torch
import torchvision

name = []


def select_image():
    # Open the file dialog to select an image
    image_path = filedialog.askopenfilename(initialdir='/', title='Select an Image',
                                            filetypes=(('Image Files', '*.png *.jpg *.jpeg'), ('All Files', '*.*')))
    name.append(image_path)
    if image_path:
        # Display the selected image
        image = Image.open(image_path)
        image.thumbnail((300, 300))  # Resize image to fit the GUI
        image = ImageTk.PhotoImage(image)
        image_label.configure(image=image)
        image_label.image = image


def analyze_image():
    gender = find_gender()
    race = find_race()
    age = find_age()
    label_gender.config(text=f'Gender: {gender}')
    label_race.config(text=f'Race: {race}')
    label_age.config(text=f'Age: between {age * 10} and {age * 10 + 10}')


def find_gender():
    gender = {0: "male", 1: "female"}
    img_path = name[len(name) - 1]
    img = Image.open(img_path)
    gender_model = torch.load('gender/gender_estimation.pth', map_location=torch.device('cpu'))
    tensor = torchvision.transforms.functional.to_tensor(img)
    tensor = tensor.unsqueeze(dim=0)
    out = gender_model(tensor)
    _, predicted_label = torch.max(out, 1)
    return gender[predicted_label.item()]


def find_race():
    race = {0: "White", 1: "Black", 2: "Asian", 3: "Indian", 4: "Others"}
    img_path = name[len(name) - 1]
    img = Image.open(img_path)
    race_model = torch.load('race/race_estimation.pth', map_location=torch.device('cpu'))
    tensor = torchvision.transforms.functional.to_tensor(img)
    tensor = tensor.unsqueeze(dim=0)
    out = race_model(tensor)
    _, predicted_label = torch.max(out, 1)
    return race[predicted_label.item()]


def find_age():
    img_path = name[len(name) - 1]
    img = Image.open(img_path)
    race_model = torch.load('age/age_estimation.pth', map_location=torch.device('cpu'))
    tensor = torchvision.transforms.functional.to_tensor(img)
    tensor = tensor.unsqueeze(dim=0)
    out = race_model(tensor)
    _, predicted_label = torch.max(out, 1)
    return predicted_label.item()


# find_gender()
# Create the GUI
root = tk.Tk()
root.title('Image Analyzer')

# Configure the window size and background color
root.geometry('600x600')
root.configure(bg='#F4F4F4')

# Add text label above the Select Image button
label_select = tk.Label(root, text='Select an Image:', font=('Arial', 14, 'bold'), bg='#F4F4F4')
label_select.pack(pady=10)

# Create a frame for the image display
frame_image = tk.Frame(root, bg='#F4F4F4')
frame_image.pack(pady=20)

# Add label to display the selected image
image_label = tk.Label(frame_image, bg='white')
image_label.pack()

# Create a frame for the buttons
frame_buttons = tk.Frame(root, bg='#F4F4F4')
frame_buttons.pack(pady=10)

# Add button to select image
button_select = tk.Button(frame_buttons, text='Select Image', command=select_image, width=20)
button_select.grid(row=0, column=0, padx=10)

# Add button to analyze image
button_analyze = tk.Button(frame_buttons, text='Analyze Image', command=analyze_image, width=20)
button_analyze.grid(row=0, column=1, padx=10)

# Create a frame for the labels
frame_labels = tk.Frame(root, bg='#F4F4F4')
frame_labels.pack(pady=10)

# Add labels for gender, and race
label_gender = tk.Label(frame_labels, text='Gender:', font=('Arial', 14), bg='#F4F4F4')
label_gender.grid(row=0, column=0, padx=5)

label_race = tk.Label(frame_labels, text='Race:', font=('Arial', 14), bg='#F4F4F4')
label_race.grid(row=1, column=0, padx=5)

label_age = tk.Label(frame_labels, text='Age:', font=('Arial', 14), bg='#F4F4F4')
label_age.grid(row=2, column=0, padx=5)

root.mainloop()
