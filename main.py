from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json



# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)


    new_password_letter = [random.choice(letters) for _ in range(nr_letters)]

    new_password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]

    new_password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]


    password_list = new_password_letter + new_password_symbols + new_password_numbers

    random.shuffle(password_list)

    password = "".join(password_list)

    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():

    website = website_entry.get()
    email_username = email_or_username_entry.get()
    user_password = password_entry.get()
    new_data = {
        website.title(): {
            "email": email_username,
            "password": user_password
        }
    }
    if len(website) == 0 or len(user_password) == 0:
        response = messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
        if response == "ok":
             return

    else:
        try:
            with open("data.json", "r") as data_file:
                #reading json
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as file:
                json.dump(new_data, file, indent=4)
        except json.JSONDecodeError:
            with open("data.json", "w") as file:
                json.dump(new_data, file, indent=4)
        else:
            with open("data.json", "w") as file:
                # updating json
                data.update(new_data)
                json.dump(data, file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)

# ---------------------------- SEARCH PASSWORD ------------------------ #
def search():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
            website_name = (website_entry.get()).strip().title()

            if website_name in data:
                response = data[website_name]
                email = response["email"]
                password = response["password"]
                messagebox.showinfo(title=website_name, message=f"Email: {email}\n Password: {password}")
            else:
                messagebox.showinfo(title="Not Found", message=f"No Password Information found{ ' for '+website_name+'!' if len(website_name) != 0 else '!'}")
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

canvas = Canvas(width=200, height=200)
password_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=password_img)
canvas.grid(row=0, column=1)

website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
website_label.focus()

website_entry = Entry(width=21)
website_entry.grid(row=1, column=1)


search_entry = Button(text="Search", bg="blue", command=search)
search_entry.grid(row=1, column=2)

email_or_username = Label(text="Email/Username:")
email_or_username.grid(row=2, column=0)

email_or_username_entry = Entry(width=35)
email_or_username_entry.grid(row=2, column=1, columnspan=2)
email_or_username_entry.insert(0, "gideon@gmail.com")


password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

password_entry = Entry(width=21)
password_entry.grid(row=3, column=1)


generate_btn = Button(text="Generate Password", cursor="hand2", command=generate_password)
generate_btn.grid(row=3, column=2)


add_btn = Button(text="Add", width=36, cursor="hand2", command=save)
add_btn.grid(row=4, column=1, columnspan=2)






window.mainloop()