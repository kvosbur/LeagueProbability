import statistics
import sys

def partialfactorial(original, lower):
	'''gives an amount for a partial factorial from the orginal number , orignal, and lower numbers less than it. example partialfactorial(5,2)  = 5 * 4 '''
	print("original ", original, " lower ", lower)
	total = 1
	original = original
	for i in range(lower):
		total = total * original
		original = original - 1
	return total


def twolettercombo(teams):
	''' Creates a list possible that contains all of the possible 2 letter combinations given a list of letters teams  '''
	possible=[]
	length = len(teams)
	for i in range(length):    #loop through all possible starting characters
		start = teams[i]
		for j in range(length):    #loop through all possible second characters
			second = teams[j]
			if start != second: #catches incase both letters are same.
				possible.append(start + second)
	return possible
	
def sortletter(t, teams):
	'''  This takes a list t of possible 2 letter combinations and arranges them into a masterlist where each sub list contains combinations that have
	been sorted for the purpose of this program. All of the combos with a's are in the first sublist and all of the ones with b's in the next. There is also
	no overlap between sections so a 2 letter combination only belongs in the first sublist it is assigned to.'''
	masterlist=[]
	length = len(teams)
	for i in range(length - 1):
		another=[]   #temporarily contains two letter combinations until appended to masterlist 
		for items in t:
			if teams[i] in items: 
				another.append(items)
		for item in another:  #removes the items just put in masterlist from the starting list so they can't be chosen next time
			t.remove(item)
		masterlist.append(another)
	return masterlist

	
def chooseuniquegames(choosing, choices):
	'''this chooses games for the league for one team given the possible choices and the amount of games to choose. It does this by starting with an emptylist and 
	then inserting in the last position of the list '''
	totalchoices = len(choices)
	subsequent = len(choices)-1  #use later on (skipped fisrt one because of the first for loop)
	totalcombos= partialfactorial(totalchoices, choosing)  
	total = totalcombos//totalchoices
	previous = totalcombos//subsequent  #tracks the last amount

	combos = []        #contains the game combos for the given team.
	for i in range(totalcombos):#totalcombos):
		combos.append("")
		
	print("length of combos ", totalcombos)
		
	accumulator = 0
	for j in range(totalchoices):    #makes the first additions to the master list combos
		for i in range(total):
			combos[accumulator] = choices[j]
			accumulator += 1
			
	print("choosing", choosing)
			
	for games in range(choosing-1):
		accumulator = 0
		print("subsequent", subsequent)
		total = total//subsequent
		while accumulator < totalcombos:
			for twoletters in range(totalchoices):
				current = choices[twoletters]
				if accumulator == totalcombos:
					pass
				elif current not in combos[accumulator]:
					if current[1] + current[0] not in combos[accumulator]:   
						for i in range(total):
							combos[accumulator] = combos[accumulator] + current
							accumulator += 1
					else:
						for i in range(total):
							r = combos.pop(accumulator)
							totalcombos = totalcombos - 1
		subsequent = subsequent - 1
		
	return combos

def early_away_parameter(combos, teams, test_against, index):
	'''used to test early if a combo does not follow away parameter
	combos = combos per team,  teams= list of the teams , test_against = tells how many home or away games it would take to make it break away parameter
	index = index of current team testing for'''
	new_combos = []
	for games in combos:
		count = [0,0]   # first = away  second = home
		accumulator = 0
		n = 0
		while n == 0:
			#this evaluates where to add to for the count list
			pairs = games[accumulator]
			location = pairs.find(teams[index])
			accumulator += 1
			if location == 0:
				count[0] += 1
			else:
				count[1] += 1
			#this part will decide whether to end the loop or not
			if test_against in count:
				n = ''
			elif accumulator == len(games):
				n = games
		if n == '':
			pass
		else:
			new_combos.append(games)
	
	return new_combos
		
			
	
	
def weed_early(combos, teams, index):
	''' this checks all of the possiblities in combos to see if any can be ruled out by the away parameter here instead of having to go through it later'''
	
	if len(teams) % 2 == 1: #odd amount of teams
		test_against = (len(teams)-1) // 2 + 1
		if len(combos) >= test_against:
			result = early_away_parameter(combos, teams, test_against, index)
		else:
			result = combos
	else: #even amount of teams
		test_against = (len(teams)-1) // 2 + 2
		if len(combos) >= test_against:  #tests whether their are enough items in combos to see if there are enough to go against the away parameter
			result = early_away_parameter(combos, teams, test_against, index)
		else: 
			result = combos
	
	return result
	
def possible_games(masterlist, teams):
	games = []
	accumulator = len(teams) - 1
	for items in range(len(masterlist)):
		print("choosing accumulator ", accumulator)
		combos = chooseuniquegames(accumulator, masterlist[items])    # not issue
		filtered = weed_early(combos, teams, items)
		#games.append(filtered)
		games.append(combos)
		accumulator = accumulator -1
		print(len(combos))
	return games
	
def sort_by_away_odd(masterlist, teams):
	''' given a possible league list for an odd amount of teams in the league it will return nothing if it does not fit within the parameters
	and returns the league if it is ok.  '''
	away= {} #dictionary is created to keep track of the amount of away games of each team with teams in order 

	for items in teams:   #sets dictionary values for each team to 0 to initiate it.
		away[items] = 0
		
	n = 0
	accumulator = 0
	home_away = (len(teams)-1) // 2
	while n == 0:
		away[masterlist[accumulator][0]] += 1
		accumulator += 1
		if home_away + 1 in away.values():
			n = ''
		elif accumulator == len(masterlist):
			n = masterlist
	return n
	
def sort_by_away_even(masterlist, teams):
	''' given a possible league list for an even amount of teams in the league it will return nothing if it does not fit within the parameters
	and returns the league if it is ok.  '''
	away= {} #dictionary is created to keep track of the amount of away games of each team with teams in order 

	for items in teams:   #sets dictionary values for each team to 0 to initiate it.
		away[items] = 0
		
	n = 0
	accumulator = 0
	home_away = (len(teams)-1) // 2
	while n == 0:
		away[masterlist[accumulator][0]] += 1
		accumulator += 1
		if home_away + 2 in away.values():
			n = ''
		elif accumulator == len(masterlist):
			n = masterlist

	return n
	
def parameter_away(league, teams):
	'''given the overall list of leagues to this point it loops through all leagues and applies the sort_by_away function to see which
	meet the parameter of having the right amount of home and away games. It returns a list of the remaining possible leagues that meet 
	the requirements.'''
	if len(teams) % 2 == 1:
		result = sort_by_away_odd(league,teams)
	else:
		result = sort_by_away_even(league,teams)
	
	return result

	
def possibilities(masterlist):
	'''Takes a list of sublists and counts the amount of items within the sublists
	returns total, the total amount of ways the items can be combined     lengths, a list that stores each length of the sublist in order'''
	total = 1
	lengths = []
	for i in range(len(masterlist)):
		length = len(masterlist[i])
		total = total * length
		lengths.append(length)
	return total, lengths
	
def subsequent(masterlist):
	''' This function will create a list of the max amount of times each part part of the team_sort needs to be cycled through(really hard to explain)  
	argument is team_sort and uses possibilities function'''
	total , lengths = possibilities(masterlist)
	change_total = total  #creates a variable i can change the value of as i still need the total amount to return
	max = []
	for items in lengths:
		max.append(change_total // items)
		change_total = change_total // items
	return total, lengths, max


distances = {'ab': 13, 'ac': 8, 'ad': 21, 'ae': 17, 'bc':23, 'bd':11, 'be': 6, 'cd': 14, 'ce':20, 'de': 18,'af': 19 , 'bf': 7, 'cf': 25, 'df':12 ,'ef': 9}
def parameter_distance(league,teams, values):
	'''this is a function that takes the windled down amount of choices and chooses from those the one that is best based on the lowest standard deviation
	of travel distance between the teams in that possible league.  mean(), stdev()'''
	keys = distances.keys()
	for game in league:
		for pairs in keys:
			if game[0] in pairs and game[1] in pairs:
				values[game[0]] += distances[pairs]
	deviation = statistics.stdev(values.values())
	
	return deviation

	

def choose_unique_league(masterlist, teams):
	''' this function creates all of the comibinations of the possible leagues
	eventually will check away and home and will write data to files in order to use with more teams without running into ram issues'''
	total, lengths, max = subsequent(masterlist)
	indexs = []
	counts = []
	amount = len(masterlist)
	print("total length " + str(total))
	for items in range(amount):
		indexs.append(0)
		counts.append(0)
	
	###  This is setup for the standard deviation parameter as not all parts must be calculated each time ###
	best_so_far_value = 10000000
	best_so_far_league = []
	values = {}
	for a in teams:
		values[a] = 0
	
	#leagues = []
	accumulator = 0
	while accumulator < total:  #loops through all of the possible combinations
		if(accumulator % 100000 == 0):
			print(accumulator)
		league = ""
		# this next while loop if statements will catch when to change the indexs list and when to reset portions of the counts list as well
		for items in range(amount):
			if counts[items] == max[items]:
				counts[items] = 0
				indexs[items] += 1
			else:
				pass
			if indexs[items] >= lengths[items]:
				indexs[items] = 0
		
		for team in range(amount): # this goes through and puts together the league using the indexs list as a reference
			current_index = indexs[team]
			league = league + masterlist[team][current_index]
		for i in range(len(counts)):
			counts[i] += 1
		accumulator += 1
		
		r = parameter_away(league, teams)
		
		if r == '':
			pass
		else: #this is the point in which i need to test for standard deviations to tell which is higher
			deviation = parameter_distance(league,teams,values)
			if deviation < best_so_far_value:
				best_so_far_value = deviation
				best_so_far_league = league
	return 'best so far league', best_so_far_league, 'best_so_far_value', best_so_far_value	
	
	
def main():
	teams = ('a','b','c','d','e','f')
	sorted = sortletter(twolettercombo(teams),teams)
	print(sorted)
	total_games = possible_games(sorted, teams)
	final = choose_unique_league(total_games, teams)
	print(total_games)
	

	
			
	
main()