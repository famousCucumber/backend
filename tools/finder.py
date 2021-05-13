import json
import sys
import re

def to_return_obj(obj, location):
    result = {}
    result["keyword"] = obj["keyword"]
    result["location"] = []
    
    # 시가 없고 도시만 있는 경우
    if len(obj["city"])==0 and len(obj["county"])>=1:
        for county in obj["county"]:
            for city in location:
                if county in location[city]:
                    result["location"].append(f"{city} {county}")
                    break
    # 시 전체
    elif len(obj["city"])>0 and len(obj["county"])==0:
        if obj["city"][0] == "세종특별자치시":
            result["location"].append("세종특별자치시")
        for city in obj["city"]:
            for county in location[city]:
                result["location"].append(f"{city} {county}")
    # 시는 하나 구가 여러개
    elif len(obj["city"])==1 and len(obj["county"])>0:
        for county in obj["county"]:
            result["location"].append(f"{obj['city'][0]} {county}")

    # 시가 여러개 구가 하나
    # 구는 시 하나에 있다.
    # 구가 없는 시는 시 전체
    elif len(obj["city"])>1 and len(obj["county"]) == 1:
        county = obj["county"][0]
        for city in obj["city"]:
            if county in location[city]:
                result["location"].append(f"{city} {county}")
            else:
                for county in location[city]:
                    result["location"].append(f"{city} {county}")
        
    return result

def get_keyword(text):
    # input : content -> string
    # output : {location -> list[string], keyword -> list[string]}
    
    with open("data/keywords.json","r",encoding="utf8") as json_file:
        keywords = json.load(json_file)
    with open("data/kor_city.json","r",encoding="cp949") as json_file:
        location = json.load(json_file)
        

    result = {"keyword":[], "location":[]}
    cities = location.keys()
    counties = []
    for c in location.values():
        counties += c
        
        
    token = text.split()
    words = []
    
    for word in token:
        words.append(re.sub(r"[0-9]","","".join(char for char in word if char.isalnum())))
        
    for key in keywords:
        if key in result["keyword"]:
            continue
        for value in keywords[key]:
            if value in text:
                result["keyword"].append(key)
                break
            
    if "-송출지역-" in text:
        locales = text[text.find("-송출지역-")+len("-송출지역-")+2:].split("\n")
        for local in locales:
            local = local.replace("\r","")
            if local == "세종특별자치시":
                result["location"].append(local)
            else:
                try:
                    city, county = local.split(" ")
                except:
                    continue
                if county == "전체":
                    for c in location[city]:
                        result["location"].append(f"{city} {c}")
                else:
                    result["location"].append(local)
                    
    if len(result["location"]) == 0:
        obj = {"city":[],"county":[],"keyword":result["keyword"]}
        for city in cities:
            if city in text and city not in obj["city"]:
                obj["city"].append(city)
        for county in counties:
            if county in text and county not in obj["county"]:
                obj["county"].append(county)
                
        result = to_return_obj(obj, location)
    
    if len(result["keyword"]) == 0:
        result["keyword"].append("기타")
    
    return result

def get_prev_data():
    results = []
    with open("data/articleMap.json","r") as json_file:
        prev_data = json.load(json_file)
        
    for key in prev_data:
        keyword = get_keyword(prev_data[key][-1])
        obj = {}
        obj["ordr"] = int(key)
        obj["date"] = prev_data[key][1]
        obj["content"] = prev_data[key][-1]
        obj["keyword"] = keyword["keyword"]
        obj["location"] = keyword["location"]
        if len(obj["location"])>0:
            results.append(obj)
    return results

if __name__ == "__main__":
    text = sys.argv[1]
    if text == "prev":
        result= get_prev_data()
    else:
        result = get_keyword(text)
    print(json.dumps(result))