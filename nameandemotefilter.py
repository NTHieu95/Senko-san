import re

def nameAndEmoteFilter(string,client):
    # clean whitespaces
    string = " ".join(string.split())
    # clean the fucking name-tagging shit
    if string.find('<@!') >=0:
        list1 = string.split('<@!')
        newString = ''
        for i in list1:
            if i.find('>') >= 0 and re.search('[a-zA-Z!@: ]',i.split('>')[0]) == None:
                newString = newString + '' + client.get_user(int(i.split('>')[0])).name + '' + i[(i.find('>')+1):]
            else:
                newString = newString + '' + i
    else:
        newString = string
    # print('clean <@!: ' + newString)
    if newString.find('<@') >=0:
        list2 = newString.split('<@')
        newString = ''
        for i in list2:
            if i.find('>') >= 0 and re.search('[a-zA-Z!@: ]',i.split('>')[0]) == None:
                newString = newString + '' + client.get_user(int(i.split('>')[0])).name + '' + i[(i.find('>')+1):]
            else:
                newString = newString + '' + i
    # newString is now clean of name-tagging shit, there're only emotes left
    # print('clean <@: ' + newString)
    if newString.find('<:') >=0:
        list3 = newString.split('<:')
        newString = ''
        for i in list3:
            if i.find('>') >= 0:
                newString = newString + '' + i[(i.find('>')+1):]
            else:
                newString = newString + '' + i
    return newString