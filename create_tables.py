import pandas as pd
import os
import re
import datetime


def create_table(filename, schema, col_size):
    DEFAULT_DATATYPE = "[varchar](" + str(col_size) + ")"

    filename = filename.upper()
    # speed up using only first 5 rows
    read_file = pd.read_csv(filename, nrows=0)
    read_file = str(read_file).split(";")
    # print(read_file)

    total_col = list(read_file).count
    sql_text = " "

    table = "[" + filename.replace(".csv", "") + "]"

    sql_text = sql_text + (f"\nCREATE TABLE [{schema}].{table} ( \n")

    for i, line in enumerate(list(read_file)):
        # add columns number
        line = line + "_" + str(i)
        # print(f'"{filename}", {i+1}, "{line}"')
        # fix column name in SQL format
        line = line.rstrip().lstrip()  # Remove front and end blank
        # line = line.replace("__", "_")
        line = line.replace("/", "_")
        line = line.replace(".", "_")
        line = line.replace(" ", "_")

        sql_text = sql_text + f"       [{line}] {DEFAULT_DATATYPE}  NULL,"

    sql_text = sql_text + r"END"

    return sql_text


def bulk_inserts(filename, schema):
    filename = filename.upper()
    table_only = filename.replace(".csv", "")

    sql_text = (
        f"\nBULK INSERT [{schema}].[{table_only}] FROM 'H:\SAP\{table_only}.csv' WITH"
    )
    sql_text = (
        sql_text + r" (FIRSTROW=2, FIELDTERMINATOR=';', ROWTERMINATOR = '\n') GO "
    )

    return sql_text


def drop_tables(filename, schema):
    filename = filename.upper()
    table_only = filename.replace(".XLSX", "")

    sql_text = f"\nDROP TABLE IF EXISTS [{schema}].[{table_only}] \nGO\n"

    return sql_text


def main(source_path):
    os.chdir(source_path)

    print(f"Start..", end=" ")
    print()
    mode = input("Enter Mode (d=Database or s=Schema Only): ")
    now = datetime.datetime.now()
    if mode == "d":  # With Database
        p1 = input("Enter Database Name: ")
        p2 = input("Enter Schema Name: ")
        schema = p1 + "].[" + p2
    else:
        schema = now.strftime("%Y%m%d")  # input("Enter Schema: ")

    default_size = 200  # input("Enter default column size: ")

    all_sql_text = "USE [Sandbox] \nGO\n" + f"\nCREATE SCHEMA [{schema}] \nGO\n"
    bulk_ins = "USE [Sandbox] \nGO\n\n "
    drop_text = "USE [Sandbox] \nGO\n" + f"\nDROP SCHEMA [{schema}] \nGO\n"

    for x in os.listdir():
        x = x.upper()  # lower case
        if x.endswith(".CSV"):
            print(f"Generate SQL for {x}")
            all_sql_text = all_sql_text + create_table(x, schema, default_size)
            # fix Text
            all_sql_text = all_sql_text.replace("[Empty_DataFrame", " ")
            all_sql_text = all_sql_text.replace("Columns:_", " ")
            # all_sql_text = all_sql_text.replace("Index:_[]] ", " ")
            bulk_ins = bulk_ins + bulk_inserts(x, schema)
            drop_text = drop_text + drop_tables(x, schema)

    # run once
    file_name_suffix = r".sql"
    # write a file
    create_file = (
        schema.replace("].[", "_")
        + "_step_1_"
        # + x.replace(".XLSX", "")
        + "create"
        + file_name_suffix
    )
    # fix file 1
    print("Fix create table file 1")
    # all_sql_text = re.sub("  ", " ", all_sql_text)
    all_sql_text = re.sub("\s", " ", all_sql_text)
    all_sql_text = re.sub(",END", ") ON [PRIMARY] \nGO\n", all_sql_text)
    all_sql_text = re.sub(" GO ", "\nGO\n", all_sql_text)
    all_sql_text = re.sub(r".CSV", "", all_sql_text)
    all_sql_text = re.sub(r",", ",\n", all_sql_text)
    all_sql_text = re.sub(r"\] Index:_\[\]_", "_", all_sql_text)
    # remove double empty space
    all_sql_text = re.sub(r"  ", " ", all_sql_text)
    all_sql_text = re.sub(r"  ", " ", all_sql_text)
    all_sql_text = re.sub(r"  ", " ", all_sql_text)
    all_sql_text = re.sub(r"  ", " ", all_sql_text)
    all_sql_text = re.sub(r"  ", " ", all_sql_text)
    all_sql_text = re.sub(r"__", "_", all_sql_text)

    # write file  1 CREATE TABLE
    with open(create_file, "w") as f:
        f.write(all_sql_text + "\n")

    # write file  2 BULK INSERT
    insert_file = (
        schema.replace("].[", "_")
        + "_step_2_"
        # + x.replace(".XLSX", "")
        + "insert"
        + file_name_suffix
    )

    # fix file 2 BULK INSERT
    print("Fix BULK INSERT file 2")
    bulk_ins = re.sub(r".CSV", "", bulk_ins)
    bulk_ins = re.sub(" GO ", "\nGO\n", bulk_ins)

    with open(insert_file, "w") as i:
        i.write(bulk_ins)

    # write file  3 DROP TABLE
    drop_file = (
        schema.replace("].[", "_")
        + "_step_3_"
        # + x.replace(".XLSX", "")
        + "drop"
        + file_name_suffix
    )

    print("Fix DROP file 3")
    drop_text = re.sub(r".CSV", "", drop_text)
    drop_text = re.sub(" GO ", "\nGO\n", drop_text)

    with open(drop_file, "w") as d:
        d.write(drop_text)

    print(f"Files create successfully!")


if __name__ == "__main__":
    pass
