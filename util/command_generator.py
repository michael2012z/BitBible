#!/usr/bin/python3

v = ["AB", "ABP", "ACV", "AKJV", "ASV", "Anderson", "BBE", "BWE", "CPDV", "Common", "DRC", "Darby", "EMTV", "Etheridge", "Geneva1599", "Godbey", "GodsWord", "ISV", "JPS", "Jubilee2000", "KJV", "KJVA", "KJVPCE", "LEB", "LITV", "LO", "Leeser", "MKJV", "Montgomery", "Murdock", "NETfree", "NETtext", "NHEB", "NHEBJE", "NHEBME", "Noyes", "OEB", "OEBcth", "OrthJBC", "RKJNT", "RNKJV", "RWebster", "Rotherham", "SPE", "Twenty", "Tyndale", "UKJV", "WEB", "WEBBE", "WEBME", "Webster", "Weymouth", "Worsley", "YLT"]

for i in v:
    print("unzip ../source/sword_modules/en/" + i + ".zip -d tmp/ && mod2osis " + i + " > tmp/" + i + ".xml")

print()

for i in v:
    print("./generate_pages_from_osis.py " + i + " tmp/" + i + ".xml")
    
