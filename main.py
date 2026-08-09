from organizer import organize_folder


def main():
    print("================================")
    print("       SMART FILE ORGANIZER")
    print("================================")

    folder_path = input("Enter the folder path: ")

    print("\nChoose an option:")
    print("1. Preview changes")
    print("2. Organize files")

    choice = input("Enter your choice (1/2): ")

    if choice == "1":
        organize_folder(folder_path, dry_run=True)

    elif choice == "2":
        confirmation = input("\nThis will move files in the selected folder.\n"
                             "Do you want to continue? (y/n): ")
        if confirmation.lower() == "y":
            organize_folder(folder_path, dry_run=False)
        else:
            print("Operation cancelled.")

    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()