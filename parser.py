from lxml import etree
def get_text(filename):
    
    tree = etree.parse(filename)
    notags = etree.tostring(tree, encoding='unicode', method='text')
    
    return notags

import xml.etree.ElementTree as ET 
def xml_parser(path) :
    #Parsing XML Data
    event_dict = {} 
    arg_dict = {}
    event_list = ['NATURAL_EVENT','MAN_MADE_EVENT']
    arg_list = ['NATURAL_EVENT','MAN_MADE_EVENT','TIME-ARG','PLACE-ARG','PARTICIPANT-ARG', 'EPICENTRE-ARG', 'INTENSITY-ARG', 'MAGNITUDE-ARG', 'AFTER_EFFECTS-ARG','CASUALTIES-ARG','REASON-ARG'] 
    #arg_list = ['NATURAL_EVENT','MAN_MADE_EVENT','TIME-ARG','PLACE-ARG','PARTICIPANT-ARG','AFTER_EFFECTS-ARG','CASUALTIES-ARG','REASON-ARG'] 
    count = {}
    sent = []
    tags = {}
    doc_events = {}
    
    
    import os
    for file in os.listdir(path): 
        
        #print("-------------------------------------------------------------------------------") 
        filename = path + file 
        sent.append(get_text(filename))
        #full_text.append(''.join(sentence_split(filename)))
        tree = ET.parse(filename)
        root = tree.getroot()

        
        for tag in event_list: 
            for event in tree.iter(tag): 
                text = ''

                for i in range(len(event)):
                    if type(event[i].text) == str: 
                            text += event[i].text 

                    if event[i].tag in event_list:
                        for j in range(len(event[i])):
                            if type(event[i][j].text) == str: 
                                text += event[i][j].text
                #print('------------yoyo-----------------')            


                if tag == 'NATURAL_EVENT' or tag == 'MAN_MADE_EVENT':
                    #key = event id - filename
                    
                    label = event.attrib['TYPE']
                    if label == 'CYCLONE' or label == 'BLIZZARD' or label == 'TORNADO' or label == 'HURRICANE' or label == 'HAIL_STORMS' or label == 'STORM':
                        label = 'STORM'
                    if label == 'SEISMIC_RISK':
                        label = 'EARTHQUAKE'
                    if label == 'ROCK_FALL':
                        label = 'LAND_SLIDE'
                    if label == 'FOREST_FIRE':
                        label = 'FIRE'
                    if label == 'AVALANCHES':
                        label = 'LAND_SLIDE'
                    if label == 'ACCIDENTS' or label == 'VEHICULAR_COLLISION' or label == 'TRAIN_COLLISION':
                        label = 'TRANSPORT_HAZARDS'
                    if label == 'SUICIDE_ATTACK':
                        label = 'TERRORIST_ATTACK'
                    if label == 'CRIME' or label == 'LIMNIC_ERRUPTIONS' or label == 'FAMINE' or label == 'HEAVY_RAINFALL' or label =='DROUGHT':
                        label = 'MISCELLANEOUS'
                    if label == 'HEAT_WAVE' or label == 'COLD_WAVE':
                        label = 'CLIMATE_CHANGE'
                    if label == 'EPIDEMIC' or label == 'PANDEMIC' :
                        label = 'DISEASE_OUTBREAK'
                    
                    event_dict[event.attrib['ID'] + '-' + file ] = (label, text)
                
                    if file not in doc_events:
                        doc_events[file] = [label]
                    else:
                        if label not in doc_events[file]:
                            doc_events[file].append(label)
                            
            
    
        try:
            for type_ in list(set(doc_events[file])):
                if type_ not in count:
                    count[type_] = 1
                else:
                    count[type_] = count[type_] + 1
        except:
            print(file)
            continue
            
        '''try:
            print(doc_events[file])
        except:
            continue
        '''
                    
        
        tagged = []
        for child in root:

            for child1 in child:
                link = ''
                text = ''

                if child1.text != None:
                    tagged.append(('O', child1.text.strip())) 

                if child1.tag in arg_list:
                    for child2 in child1:

                        if child2.tag == 'LINK' :
                            link = child2.attrib['EVENT_ARG']   #the id of the event it is linked to
                            tag = child1.tag
                            begin_flag = 0
                            continue

                        elif child2.tag == 'ASSOCIATED-EVENT-LINK':
                            link = child2.attrib['EVENT_ID']
                            #print('yo', file)
                            tag = 'REASON-ARG'
                            begin_flag = 0
                            continue
                            
                        elif child1.tag in event_list and child2.text != None and link == '':
                            tagged.append(('O', child2.text.strip()))   #events

                        if link != '' :
                            try:

                                text = text + child2.text
                                
                                #key = arg id - filename
                                arg_dict[child1.attrib['ID'] + '-' + file] = (link, tag, text)    
                                
                                #BIO tagging
                                if begin_flag == 0 :
                                    tagged.append(('B' + '_' + tag + '__' + event_dict[link + '-' + file][0] + '__' + event_dict[link + '-' + file][1].strip(), child2.text.strip()))
                                    begin_flag = 1
                                
                                else :
                                    tagged.append(('I' + '_' + tag + '__' + event_dict[link + '-' + file][0] + '__' + event_dict[link + '-' + file][1].strip() , child2.text.strip()))
                            
                            
                            except:
                                continue
                       
        tags[file] = tagged
        
    
    total = {}
    fault = []
    for k, v in arg_dict.items():
        #key = event id + arg id + filename
        key = v[0] + '-' + k.split('-')[0] + '-' + k.split('-')[1]
        total[key] = {}
        try:
            total[key]['event_type'] = event_dict[v[0] + '-' + k.split('-')[1]][0]
            total[key]['event_trigger'] = event_dict[v[0] + '-' + k.split('-')[1]][1]
            total[key]['arg_type'] = v[1]
            total[key]['arg_trigger'] = v[2]
        except:
            fault.append((v[0] + '-' + k.split('-')[1]))
            
    #print('FAULTS:', fault)
            
            
    print(count)
    return tags, doc_events, count

