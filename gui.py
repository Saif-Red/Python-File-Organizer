import tkinter as tk
import threading
import sys
import os
import subprocess
import ctypes
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from organizer import (
    organize_folder,
    undo_last_organization
)

import history
import theme

def get_resource_path(relative_path):
    """Return the absolute path to a bundled resource."""

    if getattr(sys, "frozen", False):
        base_path = Path(
            getattr(sys, "_MEIPASS", Path(__file__).resolve().parent)
        )
    else:
        base_path = Path(__file__).resolve().parent

    return base_path / relative_path

def apply_windows_titlebar_theme(root):
    """Apply the application's dark theme to the Windows title bar."""

    try:
        hwnd = root.winfo_id()

        dwmapi = ctypes.windll.dwmapi

        #Enable Windows dark mode for the title bar
        dark_mode = ctypes.c_int(1)

        dwmapi.DwmSetWindowAttribute(
            hwnd,
            20,
            ctypes.byref(dark_mode),
            ctypes.sizeof(dark_mode)
        )

        #Windows uses BGR rather than RGB for COLORREF values
        caption_color = ctypes.c_int(0x00170F0F)
        text_color = ctypes.c_int(0x00F8FAFC)

        #Caption background color
        dwmapi.DwmSetWindowAttribute(
            hwnd,
            35,
            ctypes.byref(caption_color),
            ctypes.sizeof(caption_color)
        )

        #Caption text color
        dwmapi.DwmSetWindowAttribute(
            hwnd,
            36,
            ctypes.byref(text_color),
            ctypes.sizeof(text_color)
        )

    except Exception:
        #If Windows does not support these attributes, simply keep the normal title bar
        pass

class FileOrganizerGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Smart File Organizer")
        self.root.geometry("800x650")
        self.root.minsize(700, 550)

        self.root.configure(
            bg = theme.BACKGROUND
        )

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        self.style = ttk.Style()

        self.style.theme_use("clam")

        self.style.configure(
            "Modern.Vertical.TScrollbar",
            background = theme.PANEL_DARK,
            troughcolor = theme.RESULT_BACKGROUND,
            bordercolor = theme.RESULT_BACKGROUND,
            arrowcolor = theme.TEXT_MUTED,
            relief = "flat",
            width = 10
        )

        self.style.configure(
            "Dark.TEntry",
            fieldbackground = theme.INPUT_BACKGROUND,
            foreground = theme.TEXT,
            insertcolor = theme.TEXT,
            bordercolor = theme.BORDER,
            lightcolor = theme.BORDER,
            darkcolor = theme.BORDER,
            padding = 8
        )

        self.style.configure(
            "Action.TButton",
            font = ("Segoe UI", 11, "bold"),
            padding = (18, 10),
            background = theme.ACCENT,
            foreground = theme.TEXT,
            borderwidth = 0,
            relief = "flat"
        )

        self.style.configure(
            "Browse.TButton",
            font = ("Segoe UI", 10, "bold"),
            padding = (14, 8),
            background = theme.PANEL,
            foreground = theme.TEXT,
            borderwidth = 1
        )

        self.style.configure(
            "Dark.Horizontal.TProgressbar",
            troughcolor = theme.PANEL_DARK,
            background = theme.ACCENT,
            bordercolor = theme.BORDER,
            lightcolor = theme.ACCENT,
            darkcolor = theme.ACCENT
        )

        self.style.configure(
            "Clear.TButton",
            font = ("Segoe UI", 9),
            padding = (10, 5),
            background = theme.PANEL_DARK,
            foreground = theme.TEXT
        )

    def create_widgets(self):
        self.create_menu()

        self.header_frame = tk.Frame(
            self.root,
            bg = theme.BACKGROUND
        )

        self.header_frame.pack(
            fill = "x",
            padx = 28,
            pady = (18, 8)
        )

        self.title_label = tk.Label(
            self.header_frame,
            text="SMART FILE ORGANIZER",
            font=("Segoe UI", 24, "bold"),
            bg = theme.BACKGROUND,
            fg = theme.TEXT
        )

        self.title_label.pack(pady = (10, 2))

        self.subtitle_label = tk.Label(
                self.header_frame,
                text="Organize your files quickly and safely",
                font=("Segoe UI", 10),
                bg = theme.BACKGROUND,
                fg = theme.TEXT_SECONDARY
        )
        
        self.subtitle_label.pack(pady = (0, 10))

        self.folder_frame = tk.LabelFrame(
            self.root,
            text = " SELECT FOLDER ",
            padx = 14,
            pady = 14,
            bg = theme.PANEL,
            fg = theme.TEXT,
            bd = 1,
            relief = "solid"
        )

        self.folder_frame.pack(
            fill = "x",
            padx = 20,
            pady = 10
        )

        self.folder_entry = ttk.Entry(
            self.folder_frame,
            style = "Dark.TEntry"
        )

        self.folder_entry.grid(
            row = 0,
            column = 0,
            padx = 5,
            pady = 5,
            sticky = "ew"
        )

        self.browse_button = ttk.Button(
            self.folder_frame,
            text="Browse",
            command=self.browse_folder,
            style = "Browse.TButton"
        )

        self.browse_button.grid(
            row = 0,
            column = 1,
            padx = 5,
            pady = 5
        )

        self.folder_frame.columnconfigure(
            0,
            weight = 1
        )

        self.action_frame = tk.Frame(
            self.root,
            bg = theme.BACKGROUND
        )

        self.action_frame.pack(
            fill = "x",
            padx = 20,
            pady = 10
        )

        self.preview_button = ttk.Button(
            self.action_frame,
            text="Preview Changes",
            command=self.preview_files,
            style = "Action.TButton"
        )

        self.preview_button.pack(
            side = "left",
            expand = True,
            padx = 10,
            pady = 5
        )

        self.organize_button = ttk.Button(
            self.action_frame,
            text="Organize Files",
            command=self.organize_files,
            style = "Action.TButton"
        )

        self.organize_button.pack(
            side = "left",
            expand = True,
            padx = 10,
            pady = 5
        )

        self.status_frame = tk.LabelFrame(
            self.root,
            text = " STATUS ",
            padx = 14,
            pady = 14,
            bg = theme.PANEL,
            fg = theme.TEXT,
            bd = 1,
            relief = "solid"
        )

        self.status_frame.pack(

            fill = "x",
            padx = 20,
            pady = 10
        )

        self.status_label = tk.Label(
            self.status_frame,
            text="● Ready",
            font=("Segoe UI", 11, "bold"),
            anchor = "w",
            bg = theme.PANEL,
            fg = theme.SUCCESS
        )

        self.status_label.pack(
            fill = "x"
        )

        self.progress_bar = ttk.Progressbar(
            self.status_frame,
            orient = "horizontal",
            mode ="determinate",
            style = "Dark.Horizontal.TProgressbar"
        )

        self.progress_bar.pack(
            fill = "x",
            pady = (10, 5)
        )

        self.progress_label = tk.Label(
            self.status_frame,
            text ="0 / 0 files",
            font = ("Segoe UI", 9),
            bg = theme.PANEL,
            fg = theme.TEXT_SECONDARY
        )

        self.progress_label.pack(
            anchor = "e"
        )

        self.result_frame = tk.LabelFrame(
            self.root,
            text = " RESULTS ",
            padx = 14,
            pady = 14,
            bg = theme.PANEL,
            fg = theme.TEXT,
            bd = 1,
            relief = "solid"
        )

        self.result_frame.pack(
            fill = "both",
            expand = True,
            padx = 20,
            pady = 10
        )

        self.clear_button = ttk.Button(
            self.result_frame,
            text = "Clear Results",
            command = self.clear_results,
            style = "Clear.TButton"
        )

        self.clear_button.pack(
            anchor = "e",
            pady = (5,0)
        )

        self.result_container = tk.Frame(
            self.result_frame,
            bg = theme.PANEL
        )

        self.result_container.pack(
            fill = "both",
            expand = True
        )

        self.result_text = tk.Text(
            self.result_container,
            height = 10,
            wrap = "word",
            font = ("Consolas", 10),
            padx = 8,
            pady = 8,
            bg = theme.RESULT_BACKGROUND,
            fg = theme.TEXT,
            insertbackground = theme.TEXT,
            selectbackground = theme.ACCENT,
            selectforeground = theme.TEXT,
            relief = "flat",
            borderwidth = 0
        )

        self.result_scrollbar = ttk.Scrollbar(
            self.result_container,
            orient = "vertical",
            command = self.result_text.yview,
            style = "Modern.Vertical.TScrollbar"
        )

        self.result_text.configure(
            yscrollcommand = self.result_scrollbar.set
        )

        self.result_text.pack(
            side = "left",
            fill = "both",
            expand = True
        )

        self.result_scrollbar.pack(
            side = "right",
            fill = "y"
        )

        self.style.map(
            "Action.TButton",
            background = [
                ("active", theme.ACCENT_HOVER),
                ("pressed", theme.ACCENT_DARK)
            ],
            foreground = [
                ("disabled", theme.TEXT_MUTED)
            ]
        )

        self.style.map(
            "Browse.TButton",
            background = [
                ("active", theme.PANEL),
                ("pressed", theme.ACCENT_DARK)
            ]
        )

        self.root.bind(
            "<Control-z>",
            self.handle_undo_shortcut
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

        if result.get("message"):
            self.status_label.config(
                text = "● " + result["message"]
            )

            self.progress_bar["value"] = 0

            self.progress_label.config(
                text = "0 / 0 files"
            )

            self.show_result(
                result["message"]
            )

            return

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
        if result.get("message"):
            self.status_label.config(
                text ="● " + result["message"]
            )

            self.progress_bar["value"] = 0

            self.progress_label.config(
                text = "0 / 0 files"
            )

            self.show_result(
                result["message"]
            )

            self.organize_button.config(
                state = tk.NORMAL
            )

            self.preview_button.config(
                state = tk.NORMAL
            )

            return
        
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

        self.update_undo_menu()

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

    def clear_results(self):
        self.result_text.delete(
            "1.0",
            tk.END
        )

        self.status_label.config(
            text = "● Ready"
        )

        self.progress_bar["value"] = 0

        self.progress_label.config(
            text = "0 / 0 files"
        )

    def create_menu(self):
        self.menu_bar = tk.Menu(
            self.root,
            bg = "#0B1220",
            fg = "#E5E7EB",
            activebackground = "#2563EB",
            activeforeground ="#FFFFFF",
            tearoff = False
        )

        #FILE MENU

        file_menu = tk.Menu(
            self.menu_bar,
            tearoff = False,
            bg = "#0B1220",
            fg = "#E5E7EB",
            activebackground = "#2563EB",
            activeforeground = "#FFFFFF"
        )

        file_menu.add_command(
            label = "Select Folder",
            command = self.browse_folder
        )

        file_menu.add_command(
            label = "Clear Results",
            command = self.clear_results
        )

        file_menu.add_separator()

        file_menu.add_command(
            label = "Exit",
            command = self.root.destroy
        )

        self.menu_bar.add_cascade(
            label = "File",
            menu = file_menu
        )

        #EDIT MENU

        self.edit_menu = tk.Menu(
            self.menu_bar,
            tearoff = False,
            bg = "#0B1220",
            fg = "#E5E7EB",
            activebackground = "#2563EB",
            activeforeground = "#FFFFFF"
        )

        self.edit_menu.add_command(
            label = "Undo Last Organization",
            accelerator = "Ctrl+Z",
            command = self.undo_last_organization
        )

        self.menu_bar.add_cascade(
            label = "Edit",
            menu = self.edit_menu
        )

        #TOOLS MENU

        tools_menu = tk.Menu(
            self.menu_bar,
            tearoff = False,
            bg = "#0B1220",
            fg = "#E5E7EB",
            activebackground = "#2563EB",
            activeforeground = "#FFFFFF"
        )

        tools_menu.add_command(
            label = "Open Log Folder",
            command = self.open_log_folder
        )

        self.menu_bar.add_cascade(
            label = "Tools",
            menu = tools_menu
        )

        #HELP MENU

        help_menu = tk.Menu(
            self.menu_bar,
            tearoff = False,
            bg = "#0B1220",
            fg = "#E5E7EB",
            activebackground = "#2563EB",
            activeforeground = "#FFFFFF"
        )

        help_menu.add_command(
            label = "How to Use",
            command = self.show_help
        )

        help_menu.add_command(
            label = "About",
            command = self.show_about
        )

        self.menu_bar.add_cascade(
            label = "Help",
            menu = help_menu
        )

        self.root.config(
            menu = self.menu_bar
        )

        self.update_undo_menu()

    def open_log_folder(self):
        log_folder = Path("logs").resolve()

        log_folder.mkdir(
            exist_ok = True
        )

        try:
            os.startfile(log_folder)

        except AttributeError:
            subprocess.Popen(
                ["explorer", str(log_folder)]
            )

    def show_help(self):
        help_text = (
            "SMART FILE ORGANIZER\n\n"

            "How to use:\n\n"

            "1. Click Browse and select a folder.\n\n"

            "2. Click Preview Changes to see what "
            "will happen without moving files\n\n"

            "3. Click Organize Files to actually "
            "organize the files\n\n"

            "4. Files are grouped according to their "
            "extensions.\n\n"

            "5. Existing filenames are protected by "
            "adding a numeric suffix when necessary.\n\n"

            "Example:\n"
            "photo.jpg\n"
            "photo_1.jpg\n"
            "photo_2.jpg\n\n"

            "Use Tools > Open Log Folder to view "
            "operation logs."
        )

        messagebox.showinfo(
            "How to Use",
            help_text
        )

    def show_about(self):
        about_text = (
            "Smart File Organizer\n\n"
            "A Python-based Windows desktop application "
            "for automatically organizing files into "
            "category folders.\n\n"
            "Features:\n"
            "• File categorization\n"
            "• Preview mode\n"
            "• Duplicate handling\n"
            "• Progress tracking\n"
            "• Error handling\n"
            "• Activity logging\n\n"
            "Built with Python and Tkinter."
        )

        messagebox.showinfo(
            "About Smart File Organizer",
            about_text
        )

    def update_undo_menu(self):
        if history.has_history():
            self.edit_menu.entryconfig(
                "Undo Last Organization",
                state = tk.NORMAL
            )

        else:
            self.edit_menu.entryconfig(
                "Undo Last Organization",
                state = tk.DISABLED
            )

    def undo_last_organization(self):
        if not history.has_history():
            self.status_label.config(
                text = "Status: Nothing to undo"
            )

            self.show_result(
                "There is no organization operation to undo."
            )

            return

        confirmed = messagebox.askyesno(
            "Undo Organization",
            "Undo the most recent organization?\n\n"
            "The files will be moved back to their original locations."
        )

        if not confirmed:
            self.status_label.config(
                text = "Status: Undo cancelled"
            )

            self.show_result(
                "Undo cancelled.\n\n"
                "No files were moved."
            )

            return

        self.status_label.config(
            text = "Status: Undoing organization..."
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

        self.edit_menu.entryconfig(
            "Undo Last Organization",
            state = tk.DISABLED
        )

        thread = threading.Thread(
            target = self.undo_worker,
            daemon = True
        )

        thread.start()

    def undo_worker(self):
        result = undo_last_organization(
            progress_callback = self.update_progress
        )

        self.root.after(
            0,
            lambda: self.undo_complete(result)
        )

    def undo_complete(self, result):
        self.organize_button.config(
            state = tk.NORMAL
        )

        self.preview_button.config(
            state = tk.NORMAL
        )

        if not result["success"]:
            self.status_label.config(
                text = "Status: Undo failed"
            )

            self.show_result(
                result.get(
                    "message",
                    "Unable to undo the last organization."
                )
            )

            self.update_undo_menu()

            return

        output = "UNDO ORGANIZATION\n"
        output += "=" * 50
        output += "\n\n"

        for detail in result["details"]:
            output += detail + "\n"

        output += "\n"
        output += "=" * 50
        output += "\n"

        output += (
            f"Files restored: "
            f"{result['files_restored']}\n"
        )

        output += (
            f"Files failed: "
            f"{result['files_failed']}\n"
        )

        if result["files_failed"] == 0:
            self.status_label.config(
                text = "Status: Undo complete"
            )

        else:
            self.status_label.config(
                text = "Status: Undo completed with errors"
            )

        self.show_result(output)

        self.update_undo_menu()

    def handle_undo_shortcut(self, event = None):
        self.undo_last_organization()

def main():

    root = tk.Tk()

    icon_path = get_resource_path(
        "assets/icon.ico"
    )

    root.iconbitmap(icon_path)

    apply_windows_titlebar_theme(root)

    app = FileOrganizerGUI(root)

    root.mainloop()


if __name__ == "__main__":
    main()