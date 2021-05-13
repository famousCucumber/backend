import json
import sys
import re

def replace_location(text, location, counties):
    with open("data/short_name.json","r") as json_file:
        short_name = json.load(json_file)
    for short in short_name:
        if short in text:
            text = text.replace(short,short_name[short])
    return text

def set_city(obj, location):
    for local in location:
        for county in location[local]:
            if obj["county"][0] == county:
                obj["city"].append(local)
                return obj
            
def to_return_obj(obj, location):
    result = {}
    result["keyword"] = obj["keyword"]
    result["location"] = []
    # 시 전체
    if len(obj["city"])>0 and len(obj["county"])==0:
        if obj["city"][0] == "세종특별자치시":
            result["location"].append("세종특별자치시")
        for city in obj["city"]:
            for county in location[city]:
                result["location"].append(f"{city} {county}")
    # 시는 하나 구가 여러개
    elif len(obj["city"])==1 and len(obj["county"])>0:
        for county in obj["county"]:
            result["location"].append(f"{obj['city'][0]} {county}")
    # 전국
    elif len(obj["city"]) == 0 and len(obj["county"]) == 0:
        for city in location:
            for county in location[city]:
                result["location"].append(f"{city} {county}")
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
    # 헬게이트
    elif len(obj["city"])>1 and len(obj["county"])>1:
        pass
        
    return result

def get_keyword(text):
    # input : content -> string
    # output : {city -> list[string], county -> list[string], keyword -> list[string]}
    
    with open("data/keywords.json","r",encoding="utf8") as json_file:
        keywords = json.load(json_file)
    with open("data/kor_city.json","r") as json_file:
        location = json.load(json_file)
        
    result = {"city":[],"county":[],"keyword":[]}
    cities = location.keys()
    counties = []
    for c in location.values():
        counties += c
        
        
    text = replace_location(text,location, counties)
    text.replace("\r","").replace("\n","")
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
    
    for city in cities:
        if city in text and city not in result["city"]:
            result["city"].append(city)
    for county in counties:
        if county in text and county not in result["county"]:
            result["county"].append(county)
                    
    if len(result["keyword"]) == 0:
        result["keyword"].append("기타")
        
    if len(result["city"])==0 and len(result["county"])>=1:
        result = set_city(result,location)
        
    obj = to_return_obj(result, location)
    
    return obj

if __name__ == "__main__":
    text = sys.argv[1]
    result = get_keyword(text)
    print(result)