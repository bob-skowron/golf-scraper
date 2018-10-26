import bs4 as bs
import requests as req
import pandas as pd
import datetime
import urllib
espn_url = 'http://espn.go.com/golf/leaderboard'
response = req.get(espn_url)
html = response.content
soup = bs.BeautifulSoup(html,  'lxml')

#datagolf_url = 'http://datagolf.ca/live-predictive-model'
#datagolf_response = req.get(datagolf_url)
#datagolf_html = datagolf_response.
#datagolf_soup = bs.BeautifulSoup(urllib3.(datagolf_html).read(),  'lxml')

# zero based; Thurs = 3
roundNum = datetime.datetime.today().weekday() - 2
roundName = 'leaderboard-table round-' + str(roundNum)

# parse the data table
table = soup.find('table',  attrs={'class' : roundName})
col = ['Name',  'Round1',  'Round2',  'Round3',  'Round4',  'Thru',  'Today',  'Total',  'TeeTime', 'Round3Adj', 'Round4Adj', 'TotalAdj'];
df = pd.DataFrame(columns=col)

# parse the html to find even par
parTag = soup.find('div', attrs={'class' : 'course-detail'}).find('div',attrs={'class' : "type"}).text[-2:]
par = int(parTag)

# find projected cut line
projCutTag = table.find('span', attrs={'class' : 'cut-score'})
if projCutTag is None:
    projCut = 20
elif projCutTag.text == 'E':
    projCut = 0
else:
    projCut = int(projCutTag.text)

projCut = 50

# loop through all the playes and calculate scores
for result in table.findAll('tr',  attrs={'class' : lambda L: L and L.startswith('player-overview')}):
    name = result.find('td',  attrs={'class' : lambda L: L and L.startswith('playerName')}).find('a',  attrs={'class' : 'full-name'}).text
    round1Score = result.find('td',  attrs={'class' :  'round1 in post'}).text
    round2Score = result.find('td',  attrs={'class' :  'round2 in post'}).text
    round3Score = result.find('td',  attrs={'class' :  'round3 in post'}).text
    round4Score = result.find('td',  attrs={'class' :  'round4 in post'}).text
    thrudiv = result.find('td',  attrs={'class' :  'thru in'})
    todayScore = result.find('td',  attrs={'class' :  'currentRoundScore today in'}).text
    totalScore = result.find('td',  attrs={'class' :  'relativeScore sm asc in post'}).text

    # logic for tee times
    if thrudiv.find('span'):
        teeTime = thrudiv.find('span')['data-date']
        thru = '-'
    else:
        thru = thrudiv.text
        teeTime = '-'

    if totalScore == 'E':
        totalScore = 0

    #logic for missed cut
    if totalScore == 'WD':
        totalScoreAdj = (par + 8)*4.0
    elif totalScore == 'CUT':
        round3ScoreAdj = (par + 8)
        round4ScoreAdj = (par + 8)
        totalScoreAdj = int(round1Score) - par + int(round2Score) - par + 16
    elif int(totalScore) > projCut:
        round3ScoreAdj = (par + 8)
        round4ScoreAdj = (par + 8)
        totalScoreAdj = int(totalScore) + 16
    else:
        round3ScoreAdj = round3Score
        round4ScoreAdj = round4Score
        totalScoreAdj = int(totalScore)

    resultSet = [{'Name' : name,  'Round1' : round1Score,  'Round2' : round2Score,  'Round3' : round3Score,
        'Round4' : round4Score,  'Thru' : thru,  'Today' : todayScore,  'Total' : totalScore,  'TeeTime' : teeTime,
        'Round3Adj' : round3ScoreAdj, 'Round4Adj' : round4ScoreAdj, 'TotalAdj' : totalScoreAdj}]
    df = df.append(pd.DataFrame(resultSet), sort=False)


df[col].to_csv('G:\BobS\GolfData.csv', index = False)



for k in range(1,size):
    w_=-w[-1]/k*(d-k+1)
    w.append(w_)