import tkinter as tk
import socket
from tkinter import *
from VotingPage import votingPg
from PIL import Image, ImageTk

def establish_connection():
    host = socket.gethostname()
    port = 4001
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(client_socket)
    message = client_socket.recv(1024)
    if message.decode() == "Connection Established":
        return client_socket
    else:
        return 'Failed'

def failed_return(root, frame1, client_socket, message):
    for widget in frame1.winfo_children():
        widget.destroy()
    
    # Set background image
    try:
        bg_image = Image.open("img/bg.png")
        bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = Label(frame1, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print(f"Background image error: {e}")
        frame1.config(bg='lightgray')
    
    # Calculate positions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    laptop_center_x = screen_width // 2
    laptop_center_y = screen_height // 2 - 100

    # HOME BUTTON (reduced size)
    home_btn = Button(frame1, text="🏠 Home", font=('Helvetica', 12, 'bold'), 
                     command=lambda: __import__('homePage').Home(root, frame1, Frame(root)),
                     bg='lightblue', fg='black', relief='raised', bd=2, 
                     width=10, height=1, cursor='hand2')
    home_btn.place(x=20, y=20)

    message = message + "... \nTry again..."
    Label(frame1, text=message, font=('Helvetica', 16, 'bold'), bg='black', fg='white').place(x=laptop_center_x, y=laptop_center_y, anchor='center')
    client_socket.close()

def log_server(root, frame1, client_socket, voter_ID, password):
    message = voter_ID + " " + password
    client_socket.send(message.encode())
    message = client_socket.recv(1024)
    message = message.decode()

    if message == "Authenticate":
        votingPg(root, frame1, client_socket)
    elif message == "VoteCasted":
        message = "Vote has Already been Cast"
        failed_return(root, frame1, client_socket, message)
    elif message == "InvalidVoter":
        message = "Invalid Voter"
        failed_return(root, frame1, client_socket, message)
    else:
        message = "Server Error"
        failed_return(root, frame1, client_socket, message)

def voterLogin(root, frame1):
    client_socket = establish_connection()
    if client_socket == 'Failed':
        message = "Connection failed"
        failed_return(root, frame1, client_socket, message)

    root.title("Voter Login")
    for widget in frame1.winfo_children():
        widget.destroy()

    # Set background image
    try:
        bg_image = Image.open("img/bg.png")
        bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = Label(frame1, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print(f"Background image error: {e}")
        frame1.config(bg='lightgray')

    # Calculate positions for laptop DISPLAY area
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    laptop_center_x = screen_width // 2
    laptop_center_y = screen_height // 2 - 100

    # HOME BUTTON (reduced size)
    home_btn = Button(frame1, text="🏠 Home", font=('Helvetica', 12, 'bold'), 
                     command=lambda: __import__('homePage').Home(root, frame1, Frame(root)),
                     bg='lightblue', fg='black', relief='raised', bd=2, 
                     width=10, height=1, cursor='hand2')
    home_btn.place(x=20, y=20)

    # Title positioned at top of laptop DISPLAY
    title_label = Label(frame1, text="Voter Login", font=('Helvetica', 28, 'bold'), 
                       bg='black', fg='white', bd=0)
    title_label.place(x=laptop_center_x, y=laptop_center_y - 100, anchor='center')

    # Form positioned inside laptop DISPLAY
    form_start_y = laptop_center_y - 20
    label_x = laptop_center_x - 100
    entry_x = laptop_center_x + 50
    spacing = 60

    # Labels and entries positioned inside laptop DISPLAY
    Label(frame1, text="Voter ID:", font=('Helvetica', 16, 'bold'), bg='black', fg='white').place(x=label_x, y=form_start_y, anchor='e')
    Label(frame1, text="Password:", font=('Helvetica', 16, 'bold'), bg='black', fg='white').place(x=label_x, y=form_start_y + spacing, anchor='e')

    voter_ID = tk.StringVar()
    password = tk.StringVar()

    e1 = Entry(frame1, textvariable=voter_ID, font=('Helvetica', 14), width=18, bd=2, relief='sunken')
    e1.place(x=entry_x, y=form_start_y, anchor='center')
    e3 = Entry(frame1, textvariable=password, show='*', font=('Helvetica', 14), width=18, bd=2, relief='sunken')
    e3.place(x=entry_x, y=form_start_y + spacing, anchor='center')

    def perform_voter_login():
        log_server(root, frame1, client_socket, voter_ID.get(), password.get())

    # Login button (reduced size)
    sub = Button(frame1, text="Login", width=12, height=1, font=('Helvetica', 16, 'bold'),
                command=perform_voter_login, bg='#4CAF50', fg='white', relief='raised', bd=3, cursor='hand2')
    sub.place(x=laptop_center_x, y=form_start_y + spacing*2, anchor='center')

    root.bind('<Return>', lambda event: perform_voter_login())
    e1.bind('<Return>', lambda event: perform_voter_login())
    e3.bind('<Return>', lambda event: perform_voter_login())

    frame1.pack(fill=BOTH, expand=True)
    root.mainloop()