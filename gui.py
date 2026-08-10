import tkinter as tk
from tkinter import filedialog
class FileOrganizerGUI:
    def __init__(self, root):
        self.root =root
        self.root.title("Smart File Organizer")
        self.root.geometry("700x500")
        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(
            self.root,
            text = "SMART FILE ORGANIZER",
            font = ("Arial", 22, "bold")
        )
        self.title_label.pack(pady = 30)
        self.folder_entry = tk.Entry(
            self.root,
            width = 55
        )

        self.folder_entry.pack(pady = 10)

        self.browse_button = tk.Button(
            self.root,
            text = "Browse",
            command = self.browse_folder
        )

        self.browse_button.pack(pady = 10)

        self.preview_button = tk.Button(
            self.root,
            text = "Preview Changes",
            width = 20
        )
        self.preview_button.pack(pady = 10)

        self.organize_button = tk.Button(
            self.root,
            text = "Organize Files",
            width = 20
        )
        self.organize_button.pack(pady = 10)

        self.status_label = tk.Label(
            self.root,
            text = "Status: Ready",
            font = ("Arial", 12)
        )
        self.status_label.pack(pady = 20)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder)

def main():
    root = tk.Tk()

    app = FileOrganizerGUI(root)

    root.mainloop()

if __name__ == "__main__":
    main()