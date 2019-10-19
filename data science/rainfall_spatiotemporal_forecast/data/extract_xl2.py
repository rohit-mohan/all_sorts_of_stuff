import xlrd
import numpy
import cPickle

book = xlrd.open_workbook('area_weighted_montly.xls')
sheet = book.sheet_by_index(0)
nrows = sheet.nrows


yearWise = []
data = []

for i in range(1, nrows):
	rowVal = sheet.row_values(i)[1:]
	data.append(rowVal)

	if i % 36 == 0:
		datanp = numpy.array(data)
		print i, datanp.shape
		yearWise.append(datanp)
		data = []


Data = yearWise[0]
#print Data.shape

for i in range(1, len(yearWise)):
	temp = yearWise[i]
#	print temp.shape
	Data = numpy.hstack([Data, temp])

print Data.shape
		
pFile = open('india_rainfall.pickle', 'wb')
cPickle.dump(Data, pFile)
pFile.close()
