from Giveme5W1H.extractor.document import Document
from Giveme5W1H.extractor.extractor import MasterExtractor
from parser import xml_parser
import redis
import json

# def createRedisConnection():
# 	r = redis.StrictRedis('localhost')
# 	return r
# def RedisSave(conn,key_name,value):
# 	conn.set(key_name,value)

# def getFiveValue(y):
# 	temp=[]
# 	for t in y:
# 		temp.append(t.get_parts_as_text())
# 	if len(temp)>5:
# 		temp=temp[:5]
# 	return temp

# date_publish = '1997-11-10 07:44:00'
# conn=createRedisConnection()
# extractor = MasterExtractor()
# doc,a,b=xml_parser("/home/gaurav/apoorvanlp/data/English/Train/")
# event=[]
# for e in b:
# 	event.append(e)
# print(event)
# result=[]
# total_count=0
# count=0
# for file_name,d in doc.items():
# 	total_count=total_count+1
# 	text=""
# 	for x in d:
# 		text=text+" "+x[1]
# 	# print(text)
# 	# import pdb;pdb.set_trace()
# 	y=Document.from_text(text,date_publish)
# 	y=extractor.parse(y)
# 	temp={}
# 	# import pdb;pdb.set_trace()
# 	what_event=y.get_answers('what')
# 	what=getFiveValue(what_event)
# 	where_event=y.get_answers('where')
# 	where=getFiveValue(where_event)
# 	when_event=y.get_answers('when')
# 	when=getFiveValue(when_event)
# 	who_event=y.get_answers('who')
# 	who=getFiveValue(who_event)
# 	why_event=y.get_answers('why')
# 	why=getFiveValue(why_event)

	
# 	temp["what"]=what
# 	temp["when"]=when
# 	temp["why"]=why
# 	temp["where"]=where
# 	temp["who"]=who
# 	print(temp)
# 	result.append(temp)
# 	rval = json.dumps(temp)
# 	RedisSave(conn,file_name,rval)
# print(result)
# accuracy=(count/total_count)*100
# print("accuracy is {}".format(accuracy))


# doc = Document.from_text(text, date_publish)
titleshort = "Barack Obama was born in Hawaii.  He is the president. Obama was elected in 2008."

title = "Taliban attacks German consulate in northern Afghan city of Mazar-i-Sharif with truck bomb"
lead = "The death toll from a powerful Taliban truck bombing at the German consulate in Afghanistan's Mazar-i-Sharif city rose to at least six Friday, with more than 100 others wounded in a major militant assault."
# text = """The Taliban said the bombing late Thursday, which tore a massive crater in the road and overturned cars, was a "revenge attack" for US air strikes this month in the volatile province of Kunduz that left 32 civilians dead.
# The explosion, followed by sporadic gunfire, reverberated across the usually tranquil northern city, smashing windows of nearby shops and leaving terrified local residents fleeing for cover.
# "The suicide attacker rammed his explosives-laden car into the wall of the German consulate," local police chief Sayed Kamal Sadat told AFP.
# All German staff from the consulate were unharmed, according to the foreign ministry in Berlin.
# But seven Afghan civilians were killed, including two motorcyclists who were shot dead by German forces close to the consulate after they refused to heed their warning to stop, said deputy police chief Abdul Razaq Qadri.
# A suspect had also been detained near the diplomatic mission on Friday morning, Qadri added.
# Local doctor Noor Mohammad Fayez said the city hospitals received six dead bodies, including two killed by bullets.
# At least 128 others were wounded, some of them critically and many with shrapnel injuries, he added.
# "The consulate building has been heavily damaged," the German foreign ministry said in a statement. "Our sympathies go out to the Afghan injured and their families."
# A diplomatic source in Berlin said Foreign Minister Frank-Walter Steinmeier had convened a crisis meeting.
# "There was fighting outside and on the grounds of the consulate," a ministry spokesman said. "Afghan security forces and Resolute Support (NATO) forces from Camp Marmal (German base in Mazar-i-Sharif) are on the scene."
# Afghan special forces have cordoned off the consulate, previously well-known as Mazar Hotel, as helicopters flew over the site and ambulances with wailing sirens rushed to the area after the explosion.
# The carnage underscores worsening insecurity in Afghanistan as Taliban insurgents ramp up nationwide attacks despite repeated government attempts to jump-start stalled peace negotiations.
# Taliban spokesman Zabihullah Mujahid said the "martyrdom attack" on the consulate had left "tens of invaders" dead. The insurgents routinely exaggerate battlefield claims.
# Posting a Google Earth image of the consulate on Twitter, Mujahid said the assault was in retaliation for American air strikes in Kunduz.
# US forces conceded last week that its air strikes "very likely" resulted in civilian casualties in Kunduz, pledging a full investigation into the incident.
# The strikes killed several children, after a Taliban assault left two American soldiers and three Afghan special forces soldiers dead near Kunduz city.
# The strikes triggered impassioned protests in Kunduz city, with the victims' relatives parading mutilated bodies of dead children piled into open trucks through the streets.
# Civilian casualties caused by NATO forces have been one of the most contentious issues in the 15-year campaign against the insurgents, prompting strong public and government criticism.
# The country's worsening conflict has prompted US forces to step up air strikes to support their struggling Afghan counterparts, fuelling the perception that they are increasingly being drawn back into the conflict.
# The latest attack in Mazar-i-Sharif comes just two days after a bitter US presidential election.
# Afghanistan got scarcely a passing mention in the election campaign - even though the situation there will be an urgent matter for the new president.
# President-elect Donald Trump is set to inherit America's longest war with no end in sight.
# """
text="A fire in juhu mansion burnt 3 men alive."
date_publish = '1997-11-10 07:44:00'
#doc = Document(title, lead, text, date_publish) 
extractor=MasterExtractor()
doc = Document.from_text(text, date_publish)
print(doc)
doc = extractor.parse(doc)
import pdb;pdb.set_trace()
top_who_answer = doc.get_top_answer('how').get_parts_as_text()
print(top_who_answer)


