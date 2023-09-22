

old_lines = []
with open("data_old", "r") as f:
    old_lines = f.readlines()

rem_lines = []
for line in old_lines:
    if line not in rem_lines:
        rem_lines.append(line)

with open("new_data", "a+") as f:
    for line in rem_lines:
        f.write(line)


