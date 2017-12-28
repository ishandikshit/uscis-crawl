import re
import csv
import sys
import time
from mechanize import Browser

count_received = 0
count_mailed = 0
count_cardgenerated = 0
count_other = 0
record ={}
global_receipt_number = ""
br = Browser()
for i in range (250,450):	
	br.open("https://egov.uscis.gov/casestatus/landing.do")
	br.select_form(name="caseStatusForm")
	receipt_number="YSC18900"+str(sys.argv[1])+str("%03d" % i)
	global_receipt_number = receipt_number
	print receipt_number
	br.form["appReceiptNum"]= receipt_number
	response = br.submit()
	output = str(response.read())
	if "Case Was Received" in output:
		print "Case Was Received"
		count_received=count_received+1
		record[receipt_number] = "Case Was Received"
	elif "New Card Is Being Produced" in output:
		print "New Card Is Being Produced"
		count_cardgenerated=count_cardgenerated+1
		record[receipt_number] = "New Card Is Being Produced"
	elif "Card Was Mailed To Me" in output:
		print "Card Was Mailed To Me"
		count_mailed=count_mailed+1
		record[receipt_number] = "Card Was Mailed To Me"
	else:
		print "Other Status"
		count_other=count_other+1
		record[receipt_number] = "Other Status"

with open("uscis-"+str(global_receipt_number)+"-"+str(time.strftime("%d-%m-%Y"))+str(time.strftime("%H-%M-%S"))+'.csv', 'wb') as f:
    w = csv.writer(f)
    w.writerows(record.items())

print "Approved+Completed: "+str((count_mailed+count_cardgenerated)*100/(count_mailed+count_cardgenerated+count_received))+"%"
print "Received: ",count_received
print "Other: ", count_other
print "Mailed: ", count_mailed
print "Card Generated: ", count_cardgenerated