import random
import json
import textParser as tp

# filename = 'elonText.json'
filename = 'techGuys.json'
# filename = 'comediansText.json'

dictionary = tp.readJson(filename)
newDict = {}
for entry in dictionary.keys():
    if len(dictionary[entry]) > 1:
        # print(entry, dictionary[entry])
        newDict[entry] = dictionary[entry]

# dictionary = newDict
# print(newDict)


key, values = random.choice(list(newDict.items()))
value = random.choice(values)
tweet = key.split(' ')[0]
print('trying: ', key, value)
newKey = key.split(' ')[1] + ' ' + value
for j in range(30):
    tweet += ' ' + newKey.split(' ')[0]
    # print(newKey)

    if newKey in dictionary.keys():
        value = random.choice(list(dictionary[newKey]))
        newKey = newKey.split(' ')[1] + ' ' + value
    else:
        tweet += ' ' + value + '.'
        key, values = random.choice(list(newDict.items()))
        value = random.choice(values)
        newKey = key.split(' ')[1] + ' ' + value
print(tweet.replace('\n', '').replace('\t', ''))