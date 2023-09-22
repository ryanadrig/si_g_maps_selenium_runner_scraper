

fi_lines = []
with open("agg_data_san.txt", "r") as f:
    fi_lines = f.readlines()

ccounts = []
for line in fi_lines:
    ccount = 0
    for char in line:
        if char == ",":
            ccount+=1
    ccounts.append(ccount)


ccl = 0
for cc in ccounts:
    if cc !=2:
        print("not 2 on line ~ " + str(ccl))
    ccl +=1