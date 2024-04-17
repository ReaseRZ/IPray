def CityList():
    CityList = []
    text = open("inputTagLocation.txt",'r')
    for eachLine in text:
        containerC = eachLine.split('|')
        CCTemp = []
        for eachCity in containerC[1].split(','):
            CCTemp.append(eachCity)
        CityList.append(CCTemp)
    return CityList

def CountryList():
    CountryList = []
    text = open("inputTagLocation.txt",'r')
    for eachLine in text:
        containerC = eachLine.split('|')
        CountryList.append(containerC[0])
    return CountryList
