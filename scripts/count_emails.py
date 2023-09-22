# import ast
import json

rdl = []
with open("../rdata/hyd_email_list_data_rd", "r") as f:
    rdl = f.readlines()


def textToList(hashtags):
    return hashtags.strip('[]').replace('\'', '').replace(' ', '').split(',')



ne_ct = 0
for line in rdl:
    print("count line ~ " + line)
    lst = textToList(line.split(",")[3])
    print("lst " + str(lst))
    if (lst[0] != "\n"):
        ne_ct +=1



print ("ne ct ~ " + str(ne_ct))

