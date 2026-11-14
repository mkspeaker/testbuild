import sonutils

def run(query):
	sect = 0
	mint = 0
	hourt = 0
	k = 0
	query=sonutils.list2nums(query)
	for item in query:
		if type(item)==str:
			if "секунд" in item: 
				sect=int(query[k-1])
				query.remove(query[k-1])
				query.remove(item)

			if "минут" in item: 
				mint=int(query[k-1])
				query.remove(query[k-1])
				query.remove(item)

			if "час" in item: 
				hourt=int(query[k-1])
				query.remove(query[k-1])
				query.remove(item)
		k+=1

	sonutils.logger.info(query)
	if "через" in query:
		query.remove("через")
		try:
			query.remove("что")
		except: None
		message = " ".join(query)
		sonutils.scheduler("timer",[hourt,mint,sect], "opt.alarm", message)
	else:
		message = " ".join(query)
		sonutils.scheduler("scheduler", [hourt,mint,sect], "opt.alarm", message)

