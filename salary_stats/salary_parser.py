import pandas as pd


class SalaryParser:
	def __init__(self, file_name):
		self.__currencies = pd.read_csv('../currency.csv')
		self.__available = list(self.__currencies.keys()[2:])
		self.__filename = file_name
		
	def get_payments(self):
		payments = []
		to_delete = []
		my_frame = pd.read_csv(self.__filename)		
		for job in my_frame.itertuples():
			endInd = str(job[3])			
			startInd = str(job[2])
			if (startInd != 'nan' and endInd != 'nan'):
				salary = float(startInd) + float(endInd)
			elif startInd != 'nan' and endInd == 'nan':
				salary = float(startInd)
			elif startInd == 'nan' and endInd != 'nan':
				salary = float(endInd)
			else:
				to_delete.append(int(job[0]))
				continue
				
			if job[4] == 'nan' or job[4] not in self.__available:
				to_delete.append(int(job[0]))
				continue
				
			if job[4] != 'RUR':
				date = job[6][:7]
				coefficient = self.__currencies[self.__currencies['date'] == date][job[4]].iat[0]
				salary *= coefficient
				
			payments.append(salary)
			
		my_frame.drop(labels=to_delete, axis=0, inplace=True)
		my_frame.drop(labels=['salary_to', 'salary_from', 'salary_currency'], axis=1, inplace=True)
		my_frame['salary'] = payments
		my_frame.head(100).to_csv('100.csv')


SalaryParser('/vacancies_dif_currencies.csv').get_payments()