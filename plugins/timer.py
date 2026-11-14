import sonutils

def run(query):
	query=sonutils.list2nums(query)
	sonutils.logger.debug(query)
	sect = 0
	mint = 0
	hourt = 0
	k = 0

	for item in query:
		if type(item)==str:
			if "секунд" in item: sect=int(query[k-1])
			if "минут" in item: mint=int(query[k-1])
			if "час" in item: hourt=int(query[k-1])
		k+=1

	sonutils.logger.debug(sect)
	sonutils.scheduler("timer",[hourt,mint,sect], "opt.alarm")
