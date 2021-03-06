import requests
import pymysql

"""
B16010. Educational Attainment and Employment Status by Language Spoken At Home for the Population 25 Years and Over 
B16009. Poverty Status in the Past 12 Months by Age by Language Spoken At Home for the Population 5+ Yrs 
B16008. Citizenship Status by Age by Language Spoken At Home for the Population 5+ Yrs 
B99163. Imputation of Ability to Speak English for the Population 5 Years and Over 
B01001. Sex by Age
B02001. Race
"""
#choose tables
census = ["B01001", "B02001", "B16008", "B16009", "B16010", "B99163"]


#collect table information

def gettableInfo(table_id):
	url="http://api.censusreporter.org/1.0/table/" + table_id
	req=requests.get(url)
	if not req.ok:
		print "error in request"
	data=req.json()
	table_info = []
	for key,value in data["columns"].iteritems():
		table_title = data['table_title']
		denominator = data['denominator_column_id']
		column_title = value["column_title"]
		#print column_title
		col_tag = key
		#print col_tag
		parent_col = value["parent_column_id"]
		"""if parent_col = null:
			parent_col = col_tag
		else:
			parent_col = parent_col"""
		tuple_list = (parent_col, col_tag, column_title, denominator, table_title, table_id)
		#(table_id, table_title, denominator, column_title, col_tag,  parent_col)
		#print tuple_list
		#table_info.append(tuple_list)
		"""initially used the .append line, but table_info displayed the incorrect format
		tuple_list displayed correct format, so the .append line was omitted from the code
		returned tuple_list instead, and the formatting was correct"""
		#print table_info
	#return table_info
	return tuple_list


#run code for table information
table_info_list = []
for table in census:
	table_info_list.append(gettableInfo(table))
#print table_info_list

FIPS_dict = {"Mississippi": "28", "Oklahoma": "40", "Delaware": "10", "Minnesota": "27", "Illinois": "17", "Arkansas": "05", "New Mexico": '35', "Indiana": '18', "Maryland": '24', "Louisiana": '22', "Idaho": '16', "Wyoming": '56', "Tennessee": '47', "Arizona": '04', "Iowa": '19', "Michigan": '26', "Kansas": '20', "Utah": '49', "Virginia": '51', "Oregon": '41', "Connecticut": '09', "Montana": '30', "California": '06', "Massachusetts": '25', "West Virginia": '54', "South Carolina": '45', "New Hampshire": '33', "Wisconsin": '55', "Vermont": '50', "Georgia": '13', "North Dakota": '38', "Pennsylvania": '42', "Florida": '12', "Alaska": "02", "Kentucky": '21', "Hawaii": '15', "Nebraska": '31', "Missouri": '29', "Ohio": '39', "Alabama": "01", "New York": '36', "South Dakota": '46', "Colorado": "08", "New Jersey": '34', "Washington": '53', "North Carolina": '37', "District of Columbia": '11', "Texas": '48', "Nevada": '32', "Maine": '23', "Rhode Island": '44'}
states = FIPS_dict.keys()
FIPSCode = FIPS_dict.values()

#table data
def gettabledata(table_id):
	for code in FIPSCode:
		url = "http://api.censusreporter.org/1.0/data/show/latest?table_ids=" + table_id + "&geo_ids=140|04000US" + code
		req = requests.get(url)
		if not req.ok:
			print "error in request"
		data = req.json()
		table_data = []
		if not data['data']:
			print "BROKEN LINK", url
		else:
			for num in data['data'].keys():
				col_num = data['data'][num].keys()
				#print col_num
				for col in col_num:
					responses = data['data'][num][col]['estimate'].items()
					#print responses
					for (x,y) in responses:
						info = (table_id, code, num, col_num, x, y)
						#print info
						#table_data.append(info)
						#print table_data
		#return table_data
	return info
""".append line had same issue as the gettableInfo, same solution was attempted.
The new problem arose with a timeout error-the connection would be aborted by
the machine."""
#run code to get data from select tables
table_data_list = []
for table in census:
	table_data_list.append(gettabledata(table))
#print table_data_list
"""
#TESTING
#finds the length of the appended list; displays if length greater than 6
for l in table_info_list:
	if len(l) != 6:
	print len(l)

#print len(table_info_list)

#for q in table_data_list:
	#if len(q) != 6:
	#print len(q)
print len(table_data_list)
#print len(table_data_list)
"""
#create MySQL Database
dbname="final"
host="localhost"
user="root"
passwd="Forest14"
db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')

#populate database
cur = db.cursor()

gettableInfo = '''CREATE TABLE IF NOT EXISTS TableInfo (TableId VARCHAR(255), TableTitle VARCHAR(255), Denominator VARCHAR(255), ColumnTitle VARCHAR(255), ColumnId VARCHAR(255), ParentColId VARCHAR(255));'''
gettabledata = '''CREATE TABLE IF NOT EXISTS TableData (TableId VARCHAR(255), FIPSCode INTEGER, ColumnId VARCHAR(255), ResponseCategory VARCHAR(255), Response INTEGER);'''

cur.execute(gettableInfo)
cur.execute(gettabledata)

insertQuery1 = '''insert into TableInfo (TableId, TableTitle, Denominator, ColumnTitle, ColumnId, ParentColId)
values (%s, %s, %s, %s, %s, %s);'''

    
cur.executemany(insertQuery1,table_info_list)

"""Able to populate MySQL table with the data using the ammended code"""

insertQuery2 = '''insert into TableData (TableId, FIPSCode, ColumnId, ResponseCategory, Response)
values (%s, %s, %s, %s, %s);'''

cur.executemany(insertQuery2,table_data_list)

"""Unable to populate MySQL table
attempted to modify code to use only 1 state, still failed"""

db.commit()
cur.close()