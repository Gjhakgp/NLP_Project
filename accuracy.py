from parser import xml_parser
import redis
import json

def InitConfusionMatrix():
	dct={"true_positive":0.0,"false_positive":0.0,"true_negative":0.0,"false_negative":0.0}
	return dct

def Precision(confusion_matrix):
	p=confusion_matrix["true_positive"]*1.0/(confusion_matrix["true_positive"]+confusion_matrix["false_positive"])
	return p

def Recall(confusion_matrix):
	r=confusion_matrix["true_positive"]*1.0/(confusion_matrix["true_positive"]+confusion_matrix["false_negative"])
	return r

def FScore(confusion_matrix):
	p=Precision(confusion_matrix)
	r=Recall(confusion_matrix)
	if (p+r)==0:
		return 0
	f=2*p*r/(p+r)
	return f

def createRedisConnection():
	r = redis.StrictRedis('localhost')
	return r

def SubStringMatch(A,B):
	alphabet=list(map(chr, range(97, 123)))
	Alphabet=[x.upper() for x in alphabet]
	others=["an","the","An","The"]
	if A in alphabet or B in alphabet or A in Alphabet or B in Alphabet:
		return False
	if A in others or B in others:
		return False
	if A in B or B in A:
		return True
	return False

def StringInArray(key,array):
	for a in array:
		if SubStringMatch(key,a):
			return True
	return False

def Parameters(parameter,w_parameter,result,doc):
	tp=0.0
	fn=0.0
	fp=0.0
	tn=0.0
	for x in doc:
		if SubStringMatch(parameter,x[0]) and StringInArray(x[1],result[w_parameter]):
			tp=tp+1
		elif SubStringMatch(parameter,x[0]) and not StringInArray(x[1],result[w_parameter]):
			fn=fn+1
		elif not SubStringMatch(parameter,x[0]) and StringInArray(x[1],result[w_parameter]):
			fp=fp+1
		else:
			tn=tn+1
	dct={"true_positive":tp,"false_positive":fp,"true_negative":tn,"false_negative":fn}
	return dct

def update_cf(cf1,cf2):
	cf1["true_positive"]=cf1["true_positive"]+cf2["true_positive"]
	cf1["false_positive"]=cf1["false_positive"]+cf2["false_positive"]
	cf1["true_negative"]=cf1["true_negative"]+cf2["true_negative"]
	cf1["false_negative"]=cf1["false_negative"]+cf2["false_negative"]


doc,a,b=xml_parser("/home/gaurav/apoorvanlp/data/English/Train/")
r=createRedisConnection()
PLACE=InitConfusionMatrix()
TIME=InitConfusionMatrix()
REASON=InitConfusionMatrix()
count=0
place_acc=0
time_acc=0
reason_acc=0
for file,d in doc.items():
	data = r.get(file)
	result = json.loads(data)
	count=count+1
	place_temp=Parameters("PLACE","where",result,d)
	time_temp=Parameters("TIME","when",result,d)
	reason_temp=Parameters("REASON","why",result,d)
	if(place_temp["true_positive"]>0):
		place_acc=place_acc+1
	if(time_temp["true_positive"]>0):
		time_acc=time_acc+1
	if(reason_temp["true_positive"]>0):
		reason_acc=reason_acc+1
	update_cf(PLACE,place_temp)
	update_cf(TIME,time_temp)
	update_cf(REASON,reason_temp)

	if count%50==0:
		temp_place_acc=place_acc*1.0/count
		temp_time_acc=time_acc*1.0/count
		temp_reason_acc=time_acc*1.0/count
		print("After {}".format(count))
		print("Accuracy for place {}".format(temp_place_acc))
		print("Precision for Place is {}".format(Precision(PLACE)))
		print("Recall for Place is {}".format(Recall(PLACE)))
		print("FScore for Place is {}".format(FScore(PLACE)))
		
		print("Accuracy for Time {}".format(temp_time_acc))
		print("Precision for Time is {}".format(Precision(TIME)))
		print("Recall for Time is {}".format(Recall(TIME)))
		print("FScore for Time is {}".format(FScore(TIME)))

		print("Accuracy for Reason {}".format(temp_reason_acc))
		print("Precision for Reason is {}".format(Precision(REASON)))
		print("Recall for Reason is {}".format(Recall(REASON)))
		print("FScore for Reason is {}".format(FScore(REASON)))

		