Data Format:
	small.csv
		10x10 grid world (100 states)
		4 actions (1-left, 2-right, 3-up, 4-down)
		Discount factor 0.95
	medium.csv
		State measurements: integers for 500 possible positions, 100 velocity values (50,000 states) (1+pos+500*vel gives state integer)
		Actions: 7 different accelerations
		No discount factor, ends when goal (the flag) is reached
		NOTE: discrete state measurements calculated after simulation, data in medium.csv does not satisfy Markov property
	large.csv
		States: 312020 states
		Actions: 9 actions
		Discount factor 0.95
		NOTE: details secret, lots of hidden structure, look at transitions and rewards carefully
		
Output Format
	Same name as data file with ".policy" extension
	Action for every possible state in the problem
		i-th row contains action taken from the i-th state