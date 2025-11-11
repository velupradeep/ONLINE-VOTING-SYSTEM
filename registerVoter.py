import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import dframe as df

def registerVoter(root, frame1):
    # Clear existing widgets
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

    # Screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    laptop_center_x = screen_width // 2
    
    # Position for laptop screen area (above keyboard)
    screen_area_top = screen_height * 0.20
    screen_area_bottom = screen_height * 0.60

    # Home and Admin buttons
    home_btn = Button(frame1, text="🏠 Home", font=('Helvetica', 12, 'bold'),
                     command=lambda: __import__('homePage').Home(root, frame1, Frame(root)),
                     bg='lightblue', fg='black', relief='raised', bd=2,
                     width=10, height=1, cursor='hand2')
    home_btn.place(x=20, y=20)

    admin_btn = Button(frame1, text="👨‍💼 Admin", font=('Helvetica', 12, 'bold'),
                      command=lambda: __import__('Admin').AdminHome(root, frame1, Frame(root)),
                      bg='lightgreen', fg='black', relief='raised', bd=2,
                      width=10, height=1, cursor='hand2')
    admin_btn.place(x=140, y=20)

    # Calculate available height for form
    available_height = screen_area_bottom - screen_area_top
    form_start_y = screen_area_top + (available_height * 0.1)

    # Title
    Label(frame1, text="Register Voter", font=('Helvetica', 20, 'bold'),
          bg='black', fg='white').place(x=laptop_center_x, y=form_start_y, anchor='center')

    # Form fields
    fields = [
        ("Name:", form_start_y + 40),
        ("Sex:", form_start_y + 75),
        ("Zone:", form_start_y + 110),
        ("City:", form_start_y + 145),
        ("Password:", form_start_y + 180)
    ]

    # Create labels and entries
    for label_text, y_pos in fields:
        Label(frame1, text=label_text, font=('Helvetica', 14, 'bold'),
              bg='black', fg='white').place(x=laptop_center_x - 120, y=y_pos, anchor='e')

    # Entry fields
    name_entry = Entry(frame1, font=('Helvetica', 12), relief='sunken', bd=2)
    name_entry.place(x=laptop_center_x - 100, y=form_start_y + 40, anchor='w', width=200)

    sex_var = StringVar()
    sex_combo = ttk.Combobox(frame1, textvariable=sex_var, font=('Helvetica', 12), 
                            values=["Male", "Female", "Other"], state="readonly", width=18)
    sex_combo.place(x=laptop_center_x - 100, y=form_start_y + 75, anchor='w')
    sex_combo.set("Select Sex")

    zone_entry = Entry(frame1, font=('Helvetica', 12), relief='sunken', bd=2)
    zone_entry.place(x=laptop_center_x - 100, y=form_start_y + 110, anchor='w', width=200)

    city_entry = Entry(frame1, font=('Helvetica', 12), relief='sunken', bd=2)
    city_entry.place(x=laptop_center_x - 100, y=form_start_y + 145, anchor='w', width=200)

    password_entry = Entry(frame1, font=('Helvetica', 12), relief='sunken', bd=2, show="*")
    password_entry.place(x=laptop_center_x - 100, y=form_start_y + 180, anchor='w', width=200)

    # Register button function
    def register():
        name_val = name_entry.get().strip()
        sex_val = sex_var.get()
        zone_val = zone_entry.get().strip()
        city_val = city_entry.get().strip()
        password_val = password_entry.get().strip()

        # Validation
        if not name_val:
            show_message("Please enter Name!", "red")
            return
        if sex_val == "Select Sex" or not sex_val:
            show_message("Please select Sex!", "red")
            return
        if not zone_val:
            show_message("Please enter Zone!", "red")
            return
        if not city_val:
            show_message("Please enter City!", "red")
            return
        if not password_val:
            show_message("Please enter Password!", "red")
            return

        try:
            if hasattr(df, 'taking_data_voter'):
                result = df.taking_data_voter(name_val, sex_val, zone_val, city_val, password_val)
                if result:
                    show_message("Voter Registered Successfully!", "green")
                    # Clear all fields
                    name_entry.delete(0, END)
                    sex_combo.set("Select Sex")
                    zone_entry.delete(0, END)
                    city_entry.delete(0, END)
                    password_entry.delete(0, END)
                else:
                    show_message("Registration Failed! Voter may already exist.", "red")
            else:
                show_message("Voter Registered Successfully! (Demo Mode)", "green")
                name_entry.delete(0, END)
                sex_combo.set("Select Sex")
                zone_entry.delete(0, END)
                city_entry.delete(0, END)
                password_entry.delete(0, END)
                
        except Exception as e:
            error_msg = f"Registration Error: {str(e)}"
            show_message(error_msg, "red")

    def show_message(text, color):
        for widget in frame1.winfo_children():
            if isinstance(widget, Message):
                widget.destroy()
        
        msg = Message(frame1, text=text, width=300, font=('Helvetica', 12), 
                     bg=color, fg='white', relief='raised', bd=2)
        msg.place(x=laptop_center_x, y=form_start_y + 250, anchor='center')
        frame1.after(3000, msg.destroy)

    # Register button - MORE SPACE from last field
    register_btn = Button(frame1, text="Register", font=('Helvetica', 14, 'bold'),
                         command=register, bg='#4CAF50', fg='white', 
                         width=12, height=1, relief='raised', bd=3, cursor='hand2')
    register_btn.place(x=laptop_center_x, y=form_start_y + 225, anchor='center')

    frame1.pack(fill=BOTH, expand=True)

# For direct testing
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Voter Registration")
    root.state('zoomed')
    
    frame1 = Frame(root)
    registerVoter(root, frame1)
    root.mainloop()