from organizer import organize_folder


def main():
    print("================================")
    print("       SMART FILE ORGANIZER")
    print("================================")

    folder_path = input("Enter the folder path: ")

    organize_folder(folder_path)


if __name__ == "__main__":
    main()