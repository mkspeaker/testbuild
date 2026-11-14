import sonutils

def run(query):
	import operator

	mathWords = {
	    "add":["плюс","прибавить","сложить"],
	    "sub":["минус","вычесть"],
	    "mul":["умножить"],
	    "truediv":["разделить"],
	    "pow":["степень"]
	}
	operators = {
		"add":operator.add,
	    "sub":operator.sub,
	    "mul":operator.mul,
	    "truediv":operator.truediv,
	    "pow":operator.pow
	}

	pipeline_dict=sonutils.tir(query, mathWords)
	print(pipeline_dict)
	nums=[]
	funcname=""
	for elem in pipeline_dict['pipeline']:
		if type(elem)==int: nums.append(elem)
		elif type(elem)==str: funcname=elem

	if funcname!="":
		print(operators[funcname](nums[0], nums[1]))
	