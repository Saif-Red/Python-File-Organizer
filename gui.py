import tkinter as tk
import threading
from tkinter import filedialog, messagebox, ttk

from organizer import organize_folder


class FileOrganizerGUI:

    def __init__(self, root):
        self.root = root

        self.root.title("Smart File Organizer")
        self.root.geometry("700x500")

        self.create_widgets()

    def create_widgets(self):

        self.header_frame = tk.Frame(
            self.root
        )

        self.header_frame.pack(
            fill = "x",
            padx = 20,
            pady = 10
        )

        self.title_label = tk.Label(
            self.header_frame,
            text="SMART FILE ORGANIZER",
            font=("Arial", 22, "bold")
        )

        self.subtitle_label = tk.Label(
                self.header_frame,
                text="Organize your files quickly and safely",
                font=("Arial", 11)
        )
        
        self.subtitle_label.pack()

        self.title_label.pack(pady=30)

        self.folder_frame = tk.LabelFrame(
            self.root,
            text = " Select Folder ",
            padx = 10,
            pady = 10
        )

        self.folder_frame.pack(
            fill = "x",
            padx = 20,
            pady = 10
        )

        self.folder_entry = tk.Entry(
            self.folder_frame,
            width=55
        )

        self.folder_entry.grid(
            row = 0,
            column = 0,
            padx = 5,
            pady=5,
            sticky = "ew"
        )

        self.browse_button = tk.Button(
            self.folder_frame,
            text="Browse",
            command=self.browse_folder
        )

        self.browse_button.grid(
            row = 0,
            column = 1,
            padx = 5,
            pady=5
        )

        self.folder_frame.columnconfigure(
            0,
            weight = 1
        )

        self.action_frame = tk.Frame(
            self.root
        )

        self.action_frame.pack(
            fill = "x",
            padx = 20,
            pady = 10
        )

        self.preview_button = tk.Button(
            self.action_frame,
            text="Preview Changes",
            width=20,
            command=self.preview_files
        )

        self.preview_button.pack(
            side = "left",
            expand = True,
            padx = 10,
            pady = 5
        )

        self.organize_button = tk.Button(
            self.action_frame,
            text="Organize Files",
            width=20,
            command=self.organize_files
        )

        self.organize_button.pack(
            side = "left",
            expand = True,
            padx = 10,
            pady=5
        )

        self.status_frame = tk.LabelFrame(
            self.root,
            text = " Status ",
            padx = 10,
            pady = 10
        )

        self.status_frame.pack(

            fill = "x",
            padx = 20,
            pady = 10
        )

        self.status_label = tk.Label(
            self.status_frame,
            text="Status: Ready",
            font=("Arial", 12)
        )

        self.status_label.pack(
            anchor = "w"
        )

        self.progress_bar = ttk.Progressbar(
            self.status_frame,
            orient = "horizontal",
            length = 500,
            mode ="determinate"
        )

        self.progress_bar.pack(
            fill = "x",
            pady = 10
        )

        self.progress_label = tk.Label(
            self.status_frame,
            text ="0 / 0 files"
        )

        self.progress_label.pack()

        self.result_frame = tk.LabelFrame(
            self.root,
            text = " Results ",
            padx = 10,
            pady = 10
        )

        self.result_frame.pack(
            fill = "both",
            expand = True,
            padx = 20,
            pady = 10
        )

        self.result_text = tk.Text(
            self.result_frame,
            height=10,
            width=75
        )

        self.result_text.pack(
            fill = "both",
            expand = True
        )

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

        self.progress_bar["value"] = 0

        self.progress_label.config(
            text = "0 / 0 files"
        )

        self.organize_button.config(
            state = tk.DISABLED
        )

        self.preview_button.config(
            state = tk.DISABLED
        )

        thread = threading.Thread(
            target = self.organize_worker,
            args = (folder,),
            daemon = True
        )

        thread.start()

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

    def organize_worker(self, folder):
        result = organize_folder(
            folder,
            dry_run = False,
            progress_callback = self.update_progress
        )

        self.root.after(
            0,
            lambda: self.organization_complete(result)
        )

    def organization_complete(self, result):
        if not result["success"]:
            self.status_label.config(
                text = "Status: Error"
            )

            self.show_result(
                result["error"]
            )

            self.organize_button.config(
                state = tk.NORMAL
            )

            self.preview_button.config(
                state = tk.NORMAL
            )

            return

        output = "ORGANIZATION COMPLETE\n"
        output += "=" * 50
        output += "\n\n"

        for detail in result["details"]:
            output += detail + "\n"

        output += (
            f"Files moved: "
            f"{result['files_moved']}\n"
        )

        output += (
            f"Files failed: "
            f"{result['files_failed']}\n"
        )

        self.status_label.config(
            text = "Status: Organization complete"
        )

        self.show_result(output)

        self.organize_button.config(
            state = tk.NORMAL
        )

        self.preview_button.config(
            state = tk.NORMAL
        )

    def update_progress(self, processed, total):
        self.root.after(
            0,
            lambda: self.update_progress_gui(
                processed,
                total
            )
        )

    def update_progress_gui(self, processed, total):
        if total == 0:
            self.progress_bar["value"] =0
            self.progress_label.config(
                text = "0 / 0 files"
            )
            return

        percentage = (
            processed / total
        ) * 100

        self.progress_bar["value"] = percentage
        self.progress_label.config(
            text = f"{processed} / {total} files"
        )


def main():

    root = tk.Tk()

    app = FileOrganizerGUI(root)

    root.mainloop()


if __name__ == "__main__":
    main()