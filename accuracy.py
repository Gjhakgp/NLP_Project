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

def Accuracy(confusion_matrix):
	tp=confusion_matrix["true_positive"]
	tn=confusion_matrix["true_negative"]
	fp=confusion_matrix["false_positive"]
	fn=confusion_matrix["false_negative"]
	acc=(tp+tn)*1.0/(tp+tn+fp+fn)
	return acc

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

def Contain(doc,parameter):
	for x in doc:
		if SubStringMatch(x[0],parameter):
			return True
	return False


doc,a,b=xml_parser("/home/gaurav/apoorvanlp/data/English/Train/")
r=createRedisConnection()
PLACE=InitConfusionMatrix()
TIME=InitConfusionMatrix()
REASON=InitConfusionMatrix()
PARTICIPANT=InitConfusionMatrix()
CASUALTIES=InitConfusionMatrix()
AFTER_EFFECTS=InitConfusionMatrix()

count=0
place_count=0
place_acc=0

time_count=0
time_acc=0

reason_count=0
reason_acc=0

participant_count=0
participant_acc=0

casualties_count=0
casualties_acc=0

after_effects_count=0
after_effects_acc=0

for file,d in doc.items():
	data = r.get(file)
	result = json.loads(data)
	count=count+1

	if Contain(d,"PLACE"):
		place_count=place_count+1
		place_temp=Parameters("PLACE","where",result,d)
		if(place_temp["true_positive"]>0):
			place_acc=place_acc+1
		update_cf(PLACE,place_temp)

	if Contain(d,"TIME"):
		time_count=time_count+1
		time_temp=Parameters("TIME","when",result,d)
		if(time_temp["true_positive"]>0):
			time_acc=time_acc+1
		update_cf(TIME,time_temp)

	if Contain(d,"REASON"):
		reason_count=reason_count+1
		reason_temp=Parameters("REASON","why",result,d)
		if(reason_temp["true_positive"]>0):
			reason_acc=reason_acc+1
		update_cf(REASON,reason_temp)

	if Contain(d,"PARTICIPANT"):
		participant_count=participant_count+1
		participant_temp=Parameters("PARTICIPANT","who",result,d)
		if(participant_temp["true_positive"]>0):
			participant_acc=participant_acc+1
		update_cf(PARTICIPANT,participant_temp)

	if Contain(d,"CASUALTIES"):
		casualties_count=casualties_count+1
		casualties_temp=Parameters("CASUALTIES","what",result,d)
		if(casualties_temp["true_positive"]>0):
			casualties_acc=casualties_acc+1
		update_cf(CASUALTIES,casualties_temp)

	if Contain(d,"AFTER_EFFECTS"):
		after_effects_count=after_effects_count+1
		after_effects_temp=Parameters("AFTER_EFFECTS","what",result,d)
		if after_effects_temp["true_positive"]>0 :
			after_effects_acc=after_effects_acc+1
		update_cf(AFTER_EFFECTS,after_effects_temp)


	if count%50==0:
		temp_place_acc=place_acc*1.0/place_count
		temp_time_acc=time_acc*1.0/time_count
		temp_reason_acc=reason_acc*1.0/reason_count
		temp_participant_acc=participant_acc*1.0/participant_count
		temp_casualties_acc=casualties_acc*1.0/casualties_count
		temp_after_effects_acc=after_effects_acc*1.0/after_effects_count

		print("After {}".format(count))
		print("Accuracy for place {}".format(temp_place_acc))
		print("Precision for Place is {}".format(Precision(PLACE)))
		print("Recall for Place is {}".format(Recall(PLACE)))
		print("FScore for Place is {}".format(FScore(PLACE)))
		print("Accuracy2 for Place is {}".format(Accuracy(PLACE)))
		print("\n")
		
		print("Accuracy for Time {}".format(temp_time_acc))
		print("Precision for Time is {}".format(Precision(TIME)))
		print("Recall for Time is {}".format(Recall(TIME)))
		print("FScore for Time is {}".format(FScore(TIME)))
		print("Accuracy2 for Time is {}".format(Accuracy(TIME)))
		print("\n")

		print("Accuracy for Reason {}".format(temp_reason_acc))
		print("Precision for Reason is {}".format(Precision(REASON)))
		print("Recall for Reason is {}".format(Recall(REASON)))
		print("FScore for Reason is {}".format(FScore(REASON)))
		print("Accuracy2 for Reason is {}".format(Accuracy(REASON)))
		print("\n")

		print("Accuracy for Participant {}".format(temp_participant_acc))
		print("Precision for Participant is {}".format(Precision(PARTICIPANT)))
		print("Recall for Participant is {}".format(Recall(PARTICIPANT)))
		print("FScore for Participant is {}".format(FScore(PARTICIPANT)))
		print("Accuracy2 for Participant is {}".format(Accuracy(PARTICIPANT)))
		print("\n")

		print("Accuracy for Casualties {}".format(temp_casualties_acc))
		print("Precision for Casualtie   is {}".format(Precision(CASUALTIES)))
		print("Recall for Casualties  is {}".format(Recall(CASUALTIES)))
		print("FScore for Casualties  is {}".format(FScore(CASUALTIES)))
		print("Accuracy2 for Casualties is {}".format(Accuracy(CASUALTIES)))
		print("\n")

		print("Accuracy for  After-effects {}".format(temp_after_effects_acc))
		print("Precision for  After-effects is {}".format(Precision(AFTER_EFFECTS)))
		print("Recall for  After-effects is {}".format(Recall(AFTER_EFFECTS)))
		print("FScore for  After-effects is {}".format(FScore(AFTER_EFFECTS)))
		print("Accuracy2 for After-effects is {}".format(Accuracy(AFTER_EFFECTS)))
		print("\n")
		print("---------------------------------------------------------------------")

		