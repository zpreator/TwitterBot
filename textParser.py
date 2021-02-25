import json
import os

testString = """
Yahoo Finance
Stock market news live updates: Stock futures open flat; GameStop, AMC shares surge
Emily McCormick
Emily McCormick·Reporter
Wed, February 24, 2021, 4:13 PM
Stock futures opened little changed on Wednesday, steadying following a rebound rally earlier in the day. 
During the regular session, the Dow rallied 1.4% to reach a record closing high. Though cyclical and value stocks maintained their leadership position, tech stocks also recovered some recent losses, and the Nasdaq rose for the first time this week by nearly 1%. 
Meanwhile, shares of GameStop (GME) extended gains in late trading after more than doubling during the regular session, after retail investors on Reddit took the news of Chief Financial Officer Jim Bell's resignation as a signal of a possible positive turnaround for the company. Shares of AMC (AMC), another speculative darling of vocal retail traders on Reddit, also rallied. 
U.S. Treasury yields steadied near one-year highs. The yield on the 10-year U.S. Treasury note briefly broke above 1.4% for the first time since February 2020 on Wednesday before paring some gains. 
Federal Reserve Chair Jerome Powell helped to temper market participants' recent, increasing fears over higher inflation and rates during his semiannual monetary policy testimony before Congress on Tuesday and Wednesday. He reaffirmed his view that upward pressure on prices in the coming months would be transitory, and that the U.S. economy still required policy support to emerge from the coronavirus pandemic. 
“It seems pretty clear to us that the move in rates has been driven by growing optimism about economic growth, and rates are finally ‘catching up’ to the bullish growth outlook in equities. So equity investors should not be overly concerned,” UBS strategist David Lefkowitz wrote in a note.
“But can rates rise too much before it begins to become a headwind for stocks? In theory, yes, but typically only if the rise in rates begins to choke off economic growth, perhaps because the Federal Reserve is worried about inflation,” he added. “With the pandemic winding down later this year, massive pent-up consumer demand (close to USD 2 trillion of excess savings by consumers), more fiscal stimulus on the way, and the Fed keeping the pedal to the metal, it's hard to see the recent rise in rates having a material drag on economic growth.”
"""

testString2 = """
Berkshire Hathaway (BRK.A, BRK.B) recently trimmed its position in Wells Fargo (WFC) by 58% in a sale of 74.95 million shares. And at the Daily Journal annual meeting, Berkshire’s long-time vice chairman Charlie Munger spoke about the bank — and his partner Warren Buffett’s views.
“Warren got disenchanted with Wells Fargo,” Munger said.
Munger, who is also executive chair of the Daily Journal (DJCO), a tech and publishing company, fielded questions at the company’s annual meeting Wednesday on everything from bitcoin to the GameStop frenzy to Wells Fargo.
The Daily Journal also has a sizable amount of stocks on its balance sheet, including Wells Fargo. Munger was asked why Berkshire has rapidly sold its Wells Fargo position while the Daily Journal has not.
“I don’t think it’s required we be the same on everything,” Munger said of Berkshire and the Daily Journal’s portfolios. One reason he gave for differences: “We have different tax considerations.”
Munger waded back into the 2016 Wells Fargo scandal, when it was revealed the company created many accounts in customers' names without their permission to meet internal targets as well as other poor incentives in the wealth management business.
“There’s no question about the fact Wells Fargo has disappointed long-term investors like Berkshire,” said Munger. The 97-year-old billionaire blamed the “old management,” but said they were not “consciously malevolent or thieving but had terrible judgment in creating a culture of cross-selling.”

"""

# try:
#     with open('output.json', 'r') as file:
#         suckThisDict = json.load(file)
# except:
#     suckThisDict = {}


# for i in range(len(words)-2):
#     # print(word)
#     key = words[i] + ' ' + words[i+1]
#     value = words[i+2]
#     try:
#         if value not in suckThisDict[key]:
#             suckThisDict[key].append(value)
#     except:
#         suckThisDict[key] = []
#         suckThisDict[key].append(value)
#     # print(key, value)

# for entry in suckThisDict.keys():
#     if len(suckThisDict[entry]) > 1:
#         print(entry, suckThisDict[entry])

# with open('output.json', 'w+') as f:
#     json.dump(suckThisDict, f)

def readJson(path):
    try:
        if os.path.exists(path):
            with open(path, 'r') as file:
                dictionary = json.load(file)
                return dictionary
        else:
            saveJson(path, {})
            return {}
    except Exception as e:
        print(e)
        return {}

def saveJson(path, dictionary):
    with open(path, 'w+') as f:
        json.dump(dictionary, f)

def parseString(text, dictionary):
    words = text.replace('.', '').replace(',', '').replace(':', '').replace(';', '').split(' ')
    for i in range(len(words)-2):
        key = words[i] + ' ' + words[i+1]
        value = words[i+2]
        try:
            if value not in dictionary[key]:
                dictionary[key].append(value)
        except:
            dictionary[key] = []
            dictionary[key].append(value)
    return dictionary


# dictionary = readJson('output.json')
# dictionary = parseString(testString, dictionary)
# saveJson('output.json', dictionary)