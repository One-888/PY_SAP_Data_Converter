from convert_sap_to_csv import remove_border_keep_header
import os
import glob
import zipfile as z
from merge_all_multiple_csv_to_single_csv import merge_to_csv, read_header
from create_tables import main
import shutil
import subprocess

# This is the main program


def convert_to_csv(source_path):
    # change working directory
    os.chdir(source_path)

    print(f"Starting..")

    file_filter = "*"
    file_txt = file_filter + ".txt"
    print(file_txt)
    file_csv = file_filter + ".csv"

    for i, file_name in enumerate(glob.glob(f"**\{file_filter}.txt", recursive=True)):
        print(f"Converting {file_name} to csv")
        remove_border_keep_header(file_name)
        # keep_data_header(file_name)

    # print(f"Success!")


def merge_to_one_csv(destination_path, cols_list):
    os.chdir(destination_path)
    print()
    rows = int(input("Enter number of rows: "))
    # separator = input("Enter Separator (SAP Default ; ): ")
    # esc_char = input("Enter Escape (Default / ): ")

    merge_to_csv(
        selected_columns=cols_list,
        file_name=f"*.csv",
        top_rows=rows,  # 10_000_000
        output_file="_output",
        # sep_in=separator,
        # esc_in=esc_char,
    )


def zip_files(source, destination):
    os.chdir(destination)
    shutil.make_archive("sap_data", "zip", source)


def delete_files(source, file_type):
    for i, file_name in enumerate(
        glob.glob(f"{source}\*.{file_type}", recursive=False)
    ):
        print(f"Remove file: {file_name}")
        os.remove(file_name)


def move_files(source, destination):
    make_folder(source, destination)

    src_csv = source + "\\" + "_output.csv"
    dest_csv = destination + "\\" + "_output.csv"
    # print(file_name)
    shutil.move(src_csv, destination)

    for i, file_name in enumerate(glob.glob(f"{source}\*step*.sql", recursive=False)):
        src_sql = source + "\\" + file_name
        # dest_sql = destination + "\\" + file_name
        print(file_name)
        shutil.move(src_sql, destination)


def open_explorer(dir_to_open):
    try:
        print(f"Open Folder: {dir_to_open}")
        os.chdir(dir_to_open)
        os.system("explorer.exe .")
    except FileNotFoundError:
        print(f"No Folder: {dir_to_open}")


def make_folder(source, destination):
    print(f"Make Folder {destination}")
    shutil.rmtree(destination, ignore_errors=True)
    # os.chdir("H:")
    os.mkdir(r"H:\SAP")
    os.chdir(source)


def copy_files(source, destination):
    print(f"Unloading from {source} to {destination}")
    os.chdir(source)
    shutil.copytree(source, destination, dirs_exist_ok=True)


def copy_a_zip_file(source, destination):
    zip_file = source + "\\sap_data.zip"
    print()
    print(f"Unloading a Zip from {zip_file} to {destination}. Please wait...")
    os.chdir(source)
    shutil.copy(zip_file, destination)


def display_menu():
    print(
        """
c: Remove | borders and convert to csv files
h: Show header columns from csv file
m: Merge all text files into a single csv file
d: Delete Files
e: Show Windows Explorer
t: Create SQL tables for BULK
f: Make a upload folder on server only
u: Make a folder then upload to share on SQL Server 
z: Make a folder then zip file | removing unneeded files first such txt files
          """
    )


def start_program(src, dst):
    display_menu()
    enter_mode = input("Enter Mode (c,h,m,d,e,t,f,u,z): ")

    os.chdir(source_directory)

    if enter_mode == "c":  # Remove border and convert
        convert_to_csv(source_directory)
    elif enter_mode == "t":  # Create Tables
        main(source_directory)
    elif enter_mode == "e":  # Create Tables
        open_explorer(source_directory)
        open_explorer(dest_dir)
    elif enter_mode == "d":  # Delete Files
        delete_files(source_directory, "txt")
    elif enter_mode == "h":  # Show header
        hd = input("Enter file name (.csv): ")
        read_header(hd)
        print()
    elif enter_mode == "m":  # Merge
        # Change column names here
        print()
        selected_columns = input("Enter column name separated by ; : ")
        print()
        print(f"COL: {selected_columns}")
        # merge_to_one_csv(input("Enter Merge Directory: "))
        merge_to_one_csv(source_directory, selected_columns)
    elif enter_mode == "u":  # upload to H
        make_folder(source_directory, dest_dir)
        up = input(
            "Click any keys to continue. Depend on how large the file is. Upload time may vary. "
        )
        copy_files(source_directory, dest_dir)
    elif enter_mode == "f":  # make folder on H
        make_folder(source_directory, dest_dir)
    elif enter_mode == "z":  # make a zip file
        make_folder(source_directory, dest_dir)
        u1 = input(
            "Click any keys to continue. Depend on how large the file is. Upload time may vary. "
        )
        zip_files(source_directory, dest_dir)
        # copy_a_zip_file(source_directory, dest_dir)


print(
    """
Welcome to SAP Data Converter v0.03
      """
)
source_directory = input("Enter Source Folder txt (Ctrl+V here): ")
dest_dir = r"H:\SAP"  #  input("Enter Destination Folder on SQL Server: ")
while True:
    start_program(source_directory, dest_dir)
