import xml.etree.ElementTree as ET
import requests
import pandas as pd


class CurrencyParser:

	
	def __init__(self, filename):
		self.__filename = filename
		self.__url = f'https://www.cbr.ru/scripts/XML_daily.asp?date_req=02'
		self.convert_currencies = None
		self.dataframe = pd.read_csv(filename)
		self.__data = None
		self.min_date = self.dataframe['published_at'].min()
		self.max_date = self.dataframe['published_at'].max()
	
	def receive_line(self, month, year):
		try:
			my_month = ('0' + str(month))[-2:]
			link = f'{self.__url}/{my_month}/{year}'
			print(link)
			res = requests.get(link)
			dic = ET.fromstring(res.content)
			line = [f'{year}-{my_month}']		
			for cur in self.convert_currencies:
				if cur == 'RUR':
					line.append(1)
					continue			
				found = False
				for curr in dic:
					if curr[1].text == cur:
						line.append(round(float(curr[4].text.replace(',', '.'))
														 / float(curr[2].text.replace(',', '.')), 6))
						found = True
						break
				
				if not found:
					line.append(None)
			
			return line
		except Exception as e:
			print(e)
			return None
	def export_to_csv(self, start, end):
		month_st = int(start[5:7])
		year_st = int(start[:4])
		month_end = int(end[5:7])
		year_end = int(end[:4])
		my_frame = pd.DataFrame(columns=['date'] + self.convert_currencies)
		for y in range(year_st, year_end + 1):
			for month in range(1, 13):
				if (y == year_end and month > month_end) or (y == year_st and month < month_st):
					continue		
				line = self.receive_line(str(month), str(y))
				if (line is None):
					continue			
				my_frame.loc[len(my_frame.index)] = line
		
		self.__data = my_frame
		my_frame.to_csv('data.csv')
	
	def receive_values(self, n=5000):
		return_value = []
		values = self.dataframe['salary_currency'].value_counts()
		for cur, val in values.items():
			if (val > n):
				return_value.append(cur)
		self.convert_currencies = return_value
		return return_value
	


parser = CurrencyParser('../../../vacancies_dif_currencies.csv')
parser.receive_values()
parser.export_to_csv(parser.min_date, parser.max_date)