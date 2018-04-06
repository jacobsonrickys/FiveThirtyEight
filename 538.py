# Author: Ricky Jacobson
# File: 538.py
# Description: This script solves the FiveThirtyEight Riddler Express puzzle for 4/6/2018

def main():
	DAYS_PER_MONTH = {month:(28 if month==2 else (30 if month in (4,6,9,11) else 31)) for month in range(1,13)} # Stores the number of days in each month
	years = [0 for i in range(1,100)] # Stores the number of occurrences in each year

	for month in range(1,13): # For each month in the year
		for day in range(1, DAYS_PER_MONTH[month]+1): # For each day
			if month*day<=99:
				years[month*day-1] += 1 # Add 1 to that year

	## NOTE: 2/29 is NOT counted because 2*29=58 and 2058 is not a leap year.
	
	mx = max(years)
	mn = min(years)
	total = sum(years)

	maxyears = [str(i+1) for i in range(len(years)) if years[i] == mx]
	minyears = [str(i+1) for i in range(len(years)) if years[i] == mn]

	print("Total number of occurrences: %s"%total)
	print("Years with most occurrences (%s): 20%s"%(mx, ", '".join(maxyears)))
	print("Years with fewest occurrences (%s): 20%s"%(mn, ", '".join(minyears)))

	## Find longest stretch
	
	assert mn == 0 # Make sure there are years without attacks. This should be at least be true for prime numbered years greater than 31.

	minyears = [int(year) for year in minyears] # convert to ints

	gaps = []
	index = 1

	# Break minyears into groups of consecutive years
	while index < len(minyears):
		if minyears[index] - minyears[index-1] > 1:
			gaps.append(minyears[:index])
			minyears = minyears[index:]
			index = 1
		else:
			index += 1
	gaps.append(minyears)

	maxsize = max((len(gap) for gap in gaps)) # find the maximum gap size
	gaps = [gap for gap in gaps if len(gap) == maxsize] # filter out all but the largest gaps
	
	boundaries = {} # Stores the date boundaries of each gap and their associated length
	
	# For each gap, calculate the number of days between occurrences
	for gap in gaps:
		days = 0

		# First add all the full years
		for year in gap:
			days += 366 if year%4==0 else 365 # accounts for leap years

		# Next, add all the days from the last occurrence to the end of the year
		startyear = gap[0]-1
		startmonth = 12
		# Count backward from the end of the year until an occurrence is found
		while startyear%startmonth!=0: 
			days += DAYS_PER_MONTH[startmonth] # Add all the days in each month without an occurrence
			startmonth -= 1
		days += DAYS_PER_MONTH[startmonth]-startyear//startmonth

		# Don't forget about the leap day
		if startyear%4==0 and startmonth <= 2:
			days += 1 # leap day

		# Finally, add all the days from the start of the next year to the next occurrence
		endyear = gap[-1]+1
		endmonth = 1
		# Count forward from the beginning of the year until an occurrence is found
		while endyear%endmonth!=0 or endyear//endmonth>DAYS_PER_MONTH[endmonth]:
			days += DAYS_PER_MONTH[endmonth] # Add all the days in each month without an occurrence
			endmonth += 1
		days += endyear//endmonth

		# Don't forget about the leap day again
		if endyear%4==0 and endmonth>2:
			days += 1

		# Save the dates to 'boundaries' based on their length (days)
		if days in boundaries:
			boundaries[days].append("%s/%s/20%s – %s/%s/20%s"%(startmonth,startyear//startmonth,startyear,endmonth,endyear//endmonth,endyear)) # in case multiple boundaries have the same length
		else:
			boundaries[days] = ["%s/%s/20%s – %s/%s/20%s"%(startmonth,startyear//startmonth,startyear,endmonth,endyear//endmonth,endyear)]

	# Find the longest stretch
	longest = max(boundaries.keys())
	print("The longest stretch between attacks is %s days, which occurs %s."%(longest," and ".join(boundaries[longest])))


main()