import csv
import base64
filename="multidb.csv"

records=[]
fields=[]

f=open(filename, 'r')
cf=csv.reader(f)

for each in cf:
	if len(each) < 1 : continue
	records.append(each)
	print(each)


#cf.close()
f.close()

user = input("What is Username: ")
cred = input("What is Password: ")
url = input("What is Url: ")

key=base64.b64encode((user+":"+cred).encode()).decode("ascii")
record=[key,user,cred,url]
records.append(record)

f=open(filename, 'w')
cf=csv.writer(f)
cf.writerows(records)

#cf.close()
f.close()



