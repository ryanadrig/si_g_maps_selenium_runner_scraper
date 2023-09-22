



all_lines = []

files_to_agg = [
    "33-n117-rdata",
    "33-n118-rdata"
]

for fi in files_to_agg:
    with open(fi, "r") as f:
        fi_lines = f.readlines()

    for line in fi_lines:
        if line not in all_lines:
            all_lines.append(line)


with open("agg_data", "a+") as f:
    for line in all_lines:
        f.write(line)
