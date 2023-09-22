

fi_lines = []
with open("agg_data_san.txt", "r") as f:
    fi_lines = f.readlines()

sites = []
rd_lines = []
for line in fi_lines:
    site = line.split(",")[1]
    if site not in sites:
        sites.append(site)
        rd_lines.append(line)


with open("agg_data_san_rd.txt", "a+") as f:
    for line in rd_lines:
        f.write(line)