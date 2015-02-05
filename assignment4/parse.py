import csv
import sys

def readCSV(filename):
    '''Reads the CSV file `filename` and returns a list
    with as many items as the CSV has rows. Each list item 
    is a tuple containing the columns in that row as stings.
    Note that if the CSV has a header, it will be the first
    item in the list.'''
    with open(filename,'r') as f:
        rdr = csv.reader(f)
        lines = list(rdr)
    return(lines)


### enter your code below
def get_avg_latlng(data):
	'''shows the averge latitude and longitiude of
	construction permits in HP'''

	numRows = len(data)
	latsum = 0
	lngsum = 0
	for row in data:
		latsum = float(row[128]) + latsum
		lngsum = float(row[129]) + lngsum
	p = latsum/numRows
	q = lngsum/numRows
	return (p,q)

hppermits = readCSV('permits_hydepark.csv')
print get_avg_latlng(hppermits)

#clean the data (because its really dirty)
cleaned_zip = []
for row in readCSV('permits_hydepark.csv'):
	if row[28] == "":
		pass
	elif len(row[28]) == 6:
		cleaned_zip.append(int(row[28].split('-')[0]))
	else:
		cleaned_zip.append(int(row[28]))
#print cleaned_zip
#was told by Hunter to use Contractor 1 zipcode, 
#and to leave zipcode blank if it is empty if one does not exist
#in that category

#make histogram
import matplotlib.pyplot as plt
import numpy as np

#print np.unique(cleaned_zip, return_counts=True)

def zip_code_barchart(data):
	fig = plt.figure()
	ax = fig.add_subplot(111)
	unique_zip_array = np.unique(data)
	unique_zip = unique_zip_array.tolist()
	zip_counts = np.unique(data, return_counts=True)
	ax.bar(range(len(unique_zip)), zip_counts[1])
	ax.set_title("Hyde Park Zip Code Bar Chart")
	ax.set_xlabel("Zip Codes")
	ax.set_ylabel("Frequency")
	xTickMarks = [str(x) for x in unique_zip]
	ax.set_xticks(np.arange(37) + .5)
	xtickNames = ax.set_xticklabels(xTickMarks)
	plt.setp(xtickNames, rotation = 45, size = 8)
	#plt.show()
	fig.savefig("hist.jpg")

zip_code_barchart(cleaned_zip)


#exectuable program
def zip_code_barchart2(data):
	fig = plt.figure()
	ax = fig.add_subplot(111)
	unique_zip_array = np.unique(data)
	unique_zip = unique_zip_array.tolist()
	zip_counts = np.unique(data, return_counts=True)
	ax.bar(range(len(unique_zip)), zip_counts[1])
	ax.set_title("Hyde Park Zip Code Bar Chart")
	ax.set_xlabel("Zip Codes")
	ax.set_ylabel("Frequency")
	xTickMarks = [str(x) for x in unique_zip]
	ax.set_xticks(np.arange(37) + .5)
	xtickNames = ax.set_xticklabels(xTickMarks)
	plt.setp(xtickNames, rotation = 45, size = 8)
	plt.show()
	#fig.savefig("hist.jpg")

zip_code_barchart2(cleaned_zip)

for arg in sys.argv:
	if arg == "latlng":
		print get_avg_latlng(hppermits)
	elif arg == "hist":
		print zip_code_barchart(cleaned_zip)