import tkinter as tk

def popup_window(message):
    popup = tk.Tk()
    popup.title("ScanScreen")
    label = tk.Label(popup, text=message)
    label.pack(side="top", fill="x", pady=10)
    ok_button = tk.Button(popup, text="OK", command=popup.destroy)
    ok_button.pack()
    popup.update_idletasks()
    width = popup.winfo_width()
    height = popup.winfo_height()
    x = (popup.winfo_screenwidth() // 2) - (width // 2)
    y = (popup.winfo_screenheight() // 2) - (height // 2)
    popup.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    popup.mainloop()

def test_popup_window():
    message = "This is a test message"
    popup_window(message)

# Call the test function
test_popup_window()