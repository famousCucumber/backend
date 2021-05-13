import json
import sys
import re

def get_keyword(text):
    # input : content -> string
    # output : {city -> list[string], county -> list[string], keyword -> list[string]}
    
    text.replace("\r","").replace("\n","")
    token = text.split()
    words = []
    for word in token:
        words.append(re.sub(r"[0-9]","","".join(char for char in word if char.isalnum())))
        
    with open("data/keywords.json","r",encoding="utf8") as json_file:
        keywords = json.load(json_file)
    with open("data/kor_city.json","r") as json_file:
        location = json.load(json_file)
        
        
    result = {"city":[],"county":[],"keyword":[]}
    cities = location.keys()
    counties = []
    for c in location.values():
        counties += c

    for key in keywords:
        if key in result["keyword"]:
            continue
        for value in keywords[key]:
            if value in text:
                result["keyword"].append(key)
                break
    
    for word in words:
        if "시" in word or "도" in word or "구" in word or "군" in word:
            if word in cities and word not in result["city"]:
                result["city"].append(word)
            if word in counties and word not in result["county"]:
                result["county"].append(word)
                    
    if len(result["keyword"]) == 0:
        result["keyword"].append("기타")
        
    return result

if __name__ == "__main__":
    text = sys.argv[1]
    result = get_keyword(text)
    print(result)