import re
import os


def remove_border_no_header(file_name):
    file_name_output = file_name.replace(".txt", ".csv")

    with open(file_name, "r") as f:
        lines = f.readlines()
        lines = lines[3:]  # top tree line
        lines = lines[:-1]  # bottom line
        # print(lines)

        with open(file_name_output, "w") as wf:
            # iterate each line
            for number, line in enumerate(lines):
                # remove header first two rows
                if number not in [0, 1]:
                    # Replace last character with empty string
                    line = re.sub(r".$", "", line)
                    line = line.lstrip("|")  # remove first | on the left
                    line = line.replace("|", ";")  # change delimeters
                    wf.write(line)


def remove_border_keep_header(file_name):
    file_name_output = file_name.replace(".txt", ".csv")
    print(f"Remove {file_name_output}")
    try:
        os.remove(file_name_output)
    except FileNotFoundError:
        # pass
        print(f"No File {file_name_output}")

    with open(file_name, "r") as f:
        lines = f.readlines()
        lines = lines[3:]  # top tree line
        lines = lines[:-1]  # bottom line
        # print(lines)

        with open(file_name_output, "w") as wf:
            # iterate each line
            for number, line in enumerate(lines):
                # remove header first two rows
                if number not in [1]:  # remove '------------------'
                    # Replace last character with empty string
                    line = re.sub(r".$", "", line)  # remove right border
                    line = re.sub(
                        r"  ", "", line
                    )  # remove 2 space in a row into 1 space
                    line = line.lstrip("|")  # remove left border
                    line = line.replace("|", ";")  # change | => ; delimeters
                    line = re.sub(" ;", ";", line)  # remove space ; to just ;
                    line = re.sub("; ", ";", line)  # remove space ; to just ;
                    line = re.sub(",", "", line)  # remove comma ;
                    wf.write(line)


if __name__ == "__main__":
    pass
