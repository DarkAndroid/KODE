import re

def phrase_search(object_list: list, search_string: str) -> int:
    lowstr=search_string.lower()
    #print (search_string)
    for obj in object_list:            
        #print (obj)         
        phrase=obj["phrase"]
        obj_id=obj['id']
        slots=obj["slots"]
        reg = re.findall(r'{\w+}', phrase)
        #print (reg)
        if len(obj)>0 and obj_id>0 and len(phrase)<=120 and len(slots)<=50:             
            if len(slots)==0 or len(reg)==0:
                #print (phrase)
                lowphr=phrase.lower()
                if lowstr in lowphr:
                   #print (obj_id)           
                   return int(obj_id)                     
            elif len(reg)==1:
                purephrase=phrase.replace(reg[0],reg[0][1:-1])
                #print (purephrase)
                lowphr=purephrase.lower()
                if lowstr in lowphr:
                   #print (obj_id)           
                   return int(obj_id)                  
                for slot in slots:
                    slotphrase=phrase.replace(reg[0],slot)
                    #print (slotphrase)
                    lowphr=slotphrase.lower()
                    if lowstr in lowphr:
                        #print (obj_id)           
                        return int(obj_id)  
            elif len(reg)==2:
                purephrase=phrase.replace(reg[0],reg[0][1:-1]).replace(reg[1],reg[1][1:-1])
                #print (purephrase)
                lowphr=purephrase.lower()
                if lowstr in lowphr:
                   #print (obj_id)           
                   return int(obj_id)                  
                for slot1 in slots:
                    for slot2 in slots:
                        slotphrase=phrase.replace(reg[0],slot1).replace(reg[1],slot2)
                        #print (slotphrase)
                        lowphr=slotphrase.lower()
                        if lowstr in lowphr:
                            #print (obj_id)           
                            return int(obj_id)       
    return 0

        



if __name__ == "__main__":
    """ 
    len(object) != 0
    object["id"] > 0
    0 <= len(object["phrase"]) <= 120
    0 <= len(object["slots"]) <= 50
    """
    object = [
        {"id": 1, "phrase": "Hello world!", "slots": []},
        {"id": 2, "phrase": "I wanna {pizza}", "slots": ["pizza", "BBQ", "pasta"]},
        {"id": 3, "phrase": "Give me your power", "slots": ["money", "gun"]},
        #{"id": 4, "phrase": "I wanna {eat} and {drink}", "slots": ["pizza", "BBQ", "pepsi", "tea"]}
    ]

    assert phrase_search(object, 'I wanna pasta') == 2
    assert phrase_search(object, 'Give me your power') == 3
    assert phrase_search(object, 'Hello world!') == 1
    assert phrase_search(object, 'I wanna nothing') == 0
    assert phrase_search(object, 'Hello again world!') == 0
    assert phrase_search(object, 'I need your clothes, your boots & your motorcycle') == 0
    #assert phrase_search(object, 'I wanna BBQ and pepsi') == 4
    #assert phrase_search(object, 'i wanna pizza') == 2