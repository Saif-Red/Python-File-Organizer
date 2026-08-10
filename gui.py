import tkinter as tk
from tkinter import filedialog, messagebox

from organizer import organize_folder


class FileOrganizerGUI:

    def __init__(self, root):
        self.root = root

        self.root.title("Smart File Organizer")
        self.root.geometry("700x500")

        self.create_widgets()

    def create_widgets(self):

        self.title_label = tk.Label(
            self.root,
            text="SMART FILE ORGANIZER",
            font=("Arial", 22, "bold")
        )

        self.title_label.pack(pady=30)

        self.folder_entry = tk.Entry(
            self.root,
            width=55
        )

        self.folder_entry.pack(pady=10)

        self.browse_button = tk.Button(
            self.root,
            text="Browse",
            command=self.browse_folder
        )

        self.browse_button.pack(pady=10)

        self.preview_button = tk.Button(
            self.root,
            text="Preview Changes",
            width=20,
            command=self.preview_files
        )

        self.preview_button.pack(pady=10)

        self.organize_button = tk.Button(
            self.root,
            text="Organize Files",
            width=20,
            command=self.organize_files
        )

        self.organize_button.pack(pady=10)

        self.status_label = tk.Label(
            self.root,
            text="Status: Ready",
            font=("Arial", 12)
        )

        self.status_label.pack(pady=20)

        self.result_text = tk.Text(
            self.root,
            height=10,
            width=75
        )

        self.result_text.pack(pady=10)

    def organize_files(self):

        folder = self.folder_entry.get().strip()

        if not folder:

            self.status_label.config(
                text="Status: Please select a folder"
            )

            self.show_result(
                "Please select a folder before organizing."
            )

            return

        confirmed = messagebox.askyesno(
            "Confirm Organization",
            "Are you sure you want to organize the files in this folder?"
        )

        if not confirmed:

            self.status_label.config(
                text="Status: Organization cancelled"
            )

            self.show_result(
                "Organization cancelled.\n\n"
                "No files were moved."
            )

            return

        self.status_label.config(
            text="Status: Organizing files..."
        )

        result = organize_folder(
            folder,
            dry_run=False
        )

        if not result["success"]:

            self.status_label.config(
                text="Status: Error"
            )

            self.show_result(
                result["error"]
            )

            return

        output = "ORGANIZATION COMPLETE\n"
        output += "=" * 50
        output += "\n\n"

        for detail in result["details"]:
            output += detail + "\n"

        output += "\n"
        output += "=" * 50
        output += "\n"

        output += (
            f"Files moved: "
            f"{result['files_moved']}\n"
        )

        output += (
            f"Files failed: "
            f"{result['files_failed']}\n"
        )

        self.status_label.config(
            text="Status: Organization complete"
        )

        self.show_result(output)

    def browse_folder(self):

        folder = filedialog.askdirectory()

        if folder:

            self.folder_entry.delete(
                0,
                tk.END
            )

            self.folder_entry.insert(
                0,
                folder
            )

    def show_result(self, message):

        self.result_text.delete(
            "1.0",
            tk.END
        )

        self.result_text.insert(
            tk.END,
            message
        )

    def preview_files(self):

        folder = self.folder_entry.get().strip()

        if not folder:

            self.status_label.config(
                text="Status: Please select a folder"
            )

            self.show_result(
                "Please select a folder before previewing."
            )

            return

        self.status_label.config(
            text="Status: Creating preview..."
        )

        result = organize_folder(
            folder,
            dry_run=True
        )

        if not result["success"]:

            self.status_label.config(
                text="Status: Error"
            )

            self.show_result(
                result["error"]
            )

            return

        output = "PREVIEW\n"
        output += "=" * 50
        output += "\n\n"

        for detail in result["details"]:
            output += detail + "\n"

        output += "\n"
        output += "=" * 50
        output += "\n"

        output += (
            f"Files that would be moved: "
            f"{result['files_moved']}\n"
        )

        output += (
            f"Files that failed: "
            f"{result['files_failed']}\n"
        )

        output += "\nNo files were moved."

        self.status_label.config(
            text="Status: Preview complete"
        )

        self.show_result(output)


def main():

    root = tk.Tk()

    app = FileOrganizerGUI(root)

    root.mainloop()


if __name__ == "__main__":
    main()