


all_lines = []
with open("agg_data.txt", "r") as f:
    fi_lines = f.readlines()

for line in fi_lines:
    lsan = line.replace('"',"").replace("'","")
    if line not in all_lines:
        all_lines.append(lsan)


with open("agg_data_san.txt", "a+") as f:
    for line in all_lines:
        f.write(line)