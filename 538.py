import csv
from urllib import request
from contextlib import closing
import random

'''
Ricky Jacobson's solution to FiveThirtyEight's Riddler Express 10/12.
See https://fivethirtyeight.com/features/so-you-want-to-tether-your-goat-now-what/
for problem statement.

The most important part of this problem is acknowledging that birthdays are
not in fact evenly distributed. For example, babies in America are most rarely
born on major US holidays, such as Christmas Day (2/25), Christmas Eve (2/24),
New Years Day (1/1) and the Fourth of July (7/4).

This script uses birth data from FiveThirtyEight's Friday the 13th project,
which can be found here:
https://github.com/fivethirtyeight/data/tree/master/births
'''

class DateLoader():
	def __init__(self):
		self.births_by_date = {}
		self.total_births = 0

	# Loads the birthdate data from FiveThirtyEight's Friday the 13th project
	def load(self):
		# Load data from CDC and NCHS for 1994-2003
		url = "https://raw.githubusercontent.com/fivethirtyeight/data/master/births/US_births_1994-2003_CDC_NCHS.csv"
		with closing(request.urlopen(url)) as r:
			c= csv.DictReader(r.read().decode('utf-8').split('\r'))
			for row in c:
				date =  (int(row['month']), int(row['date_of_month']))
				births = int(row['births'])
				if date not in self.births_by_date:
					self.births_by_date[date] = births
				else:
					self.births_by_date[date] += births
				self.total_births += births

		# Load from Social Security Administration for 2004-2013
		# Data from 2000-2003 & 2014 are ignored
		# so that leap day data are handled properly
		url = "https://raw.githubusercontent.com/fivethirtyeight/data/master/births/US_births_2000-2014_SSA.csv"
		with closing(request.urlopen(url)) as r:
			c= csv.DictReader(r.read().decode('utf-8').split('\r'))
			for row in c:
				# Ignore data for years earlier
				if int(row['year']) <= 2003 or int(row['year']) == 2014:
					continue
				date =  (int(row['month']), int(row['date_of_month']))
				births = int(row['births'])
				if date not in self.births_by_date:
					self.births_by_date[date] = births
				else:
					self.births_by_date[date] += births
				self.total_births += births

	# Returns the probability of being born on a given date
	def probability(self, date):
		return self.births_by_date[date]/self.total_births

	# Returns the expected number of failed trials until a success
	# where each trial has probability, self.probability(date)
	def expected_number_of_trials(self, date):
		# The expected number of trials until success is simply
		# 1/probability of success. The proof is left as an exercise
		# to the reader.
		return 1/self.probability(date) - 1

# Simulates singing the Unbirthday Song
# to random people until it is unwarrented,
# 'iterations' times.
# 
# Returns the average number of people sung to 
def simulate(date_loader, iterations):
	total = 0
	for i in range(iterations):
		# Choose random date
		date = random.sample(date_loader.births_by_date.keys(),1)[0]
		# Only allow leap years 1 in 4 times 
		while date == (2,29) and random.randrange(4) != 0:
			date = random.sample(date_loader.births_by_date.keys(), 1)[0]
		count = 0
		p = date_loader.probability(date)
		while random.random() > p:
			count += 1
		total += count

	return total/iterations

def main():
	loader = DateLoader()
	loader.load()

	# Calculate expected value numerically
	expected_value = 0
	for date in loader.births_by_date:
		# The probability that 'date' is today (accounting for leap days) 
		prob = (1 if date == (2,29) else 4)/(365*4+1)
		expected_value += prob*loader.expected_number_of_trials(date)

	# Expected Value = ~366.253
	print(expected_value)

	# Simulate and return average
	print(simulate(loader, iterations = 100000))

main()
