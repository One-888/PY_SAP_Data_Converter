import pandas as pd
import glob
import csv


def merge_to_csv(selected_columns, file_name, top_rows, output_file):
    print(f"Starting merge_to_csv..")
    dfs = []

    selected_columns = selected_columns.split(";")

    for i, file in enumerate(glob.glob(f"**/{file_name}", recursive=True)):  # **/
        print(f"Read file {i:02d}: {file}")
        try:
            df = pd.read_csv(
                file,
                sep=";",
                usecols=selected_columns,
                nrows=top_rows,
            )

            # Add file name columns
            df["file_name"] = file

            print(df)
            df.drop_duplicates()
            dfs.append(df)

        except:
            print(f"Error Read {file}")

    concat_df = pd.concat(dfs)
    concat_df = concat_df.drop_duplicates()

    output_filename = output_file + ".csv"
    # make csv
    print(f"Merging into one {output_filename}")
    print()
    concat_df.to_csv(
        output_filename,
        index=None,
        header=True,
        sep=";",
        quoting=csv.QUOTE_NONE,
        escapechar="/",
    )
    print(f"Success!")


def read_header(file_name):
    print()
    print("Sample header to copy")
    header = pd.read_csv(
        file_name,
        sep=";",
        # usecols=selected_columns,
        nrows=0,
    )
    for hd in header:
        print(f"{hd}", end=";")
    print()


if __name__ == "__main__":
    pass
