from bs4 import BeautifulSoup
import urllib
import MySQLdb

db = MySQLdb.connect("localhost","root","mreva747","mydb")
cursor = db.cursor()
x=0
def insertPlayersDetails(data) :
    # print "entering insetPlayerDetails"
    sql = u"""INSERT INTO playerDetails(playerId,playerName,country,playerType,imgPath)
         VALUES ({},'{}','{}','{}','{}')""".format(data['id'],data['name'],data['country'],data['playerType'],data['imgPath'])
    # print sql
    print "player Query ", sql
    cursor.execute(sql)
    db.commit()

def insertBattingDetails(data) :
    # print "entering batting insert"
    sql = u"""INSERT INTO playerBattingDetails(playerId,matches,runs,balls,average,strikeRate,highestScore,100s,50s,4s,6s)
         VALUES ({},{},{},{},{},{},{},{},{},{},{})""".format(data['id'],data['matches'],data['runs'],data['balls'],data['average'],data['strikeRate'],data['highScore'],data['100s'],data['50s'],data['4s'],data['6s'])
    print "batting Query ", sql
    cursor.execute(sql)
    db.commit()

def insertBowlingDetails(data) :
    # print "entering bowling insert"
    sql = u"""INSERT INTO playerBowlingDetails(playerId,matches,wickets,economy,balls,runs,bbm,average)
         VALUES ({},{},{},{},{},{},'{}',{})""".format(data['id'],data['matches'],data['wickets'],data['economy'],data['balls'],data['runs'],data['bbm'],data['average'])
    print "bowling Query ", sql
    cursor.execute(sql)
    db.commit()

def isValid(val) :
    print "entering valid, val",val
    print "string val",val.get_text()
  
    if val is None:
        # print "val is none"
        return 0
  
    if val.string is None:
        # print "val string is none"
        return 0

    if val.get_text() == '-':
        return 0
    # print "finalstring: ", val.get_text().encode('utf-8');
    return val.get_text().encode('utf-8');
    # x = val.string.extract()
    # print "x ",x
    # x = val.string.extract().replace(u'\u2020',' ')
    # print "x replace ",x
    # x = val.string.extract().replace(u'\u2020',' ').encode('utf-8')
    # print "x encode ",x

    # if x == '-':
    #     return 0
    # else :
    #     return x

def insertFieldingDetails(data) :
    # print "entering fielding insert"
    sql = """INSERT INTO playerFieldingDetails(playerId,noOfCatches,noOfStumpings)
         VALUES ({},{},{})""".format(data['id'],data['catches'],data['stumpings'])
    print "fielding Query ", sql
    cursor.execute(sql)
    db.commit()

def newGetData(url,pid):
    try:
        player={}
        playerBatting={}
        playerBowling={}
        playerFielding={}
        data = urllib.urlopen(url).read()
        soup = BeautifulSoup(data)
    
        table = soup.select("table.engineTable td.left > b")
        #print table
        for i in range(len(table)):
            if "T20" in repr(table[i]):
                #print i+1
                break;
        rownum = i+1
        return getData(url,pid,rownum)
    except:
        print "Exception"
        pass    
    

def getData(url,pid,rownum) :
    try :
        player={}
        playerBatting={}
        playerBowling={}
        playerFielding={}
        data = urllib.urlopen(url).read()
        soup = BeautifulSoup(data)
        
        playerData=soup.find_all('td',attrs={"title":"record rank: "+ str(rownum)})
        matchDetails = soup.find('td',attrs={"title":"record rank: "+ str(rownum)})
        if matchDetails is not None:
            playerShortName = soup.find('div',class_="ciPlayernametxt")
            playerInfo=soup.find('p',class_="ciPlayerinformationtxt")
            # player['name'] = isValid(playerInfo.span)
            # print playerShortName.h1.get_text();
            player['name'] = playerShortName.h1.get_text()
            # print "Player Name",player['name']
            playerInfo=playerInfo.find_next_siblings("p")
            player['country'] = soup.find("h3",class_="PlayersSearchLink").b.string.extract().replace(u'\u2020',' ').encode('utf-8')
            player['id'] = pid
            playerBatting['id'] = pid
            playerFielding['id'] = pid
            playerBowling['id'] = pid
            matchDetails=matchDetails.find_next_siblings("td")
            player['style'] = isValid(playerInfo[4].span)
            
            if player['style']=='Allrounder':
                player['playerType']='Allrounder'
            elif player['style'] == 'Wicketkeeper':
                player['playerType']=player['style']
            elif player['style'].find('bat')!=-1:
                player['playerType']='Batsman'
            else:
                player['playerType']='Bowler'
            
            playerBatting['matches']=isValid(matchDetails[0])
            playerBatting['runs']=isValid(matchDetails[3])
            high=str(isValid(matchDetails[4]))
            if high.endswith("*"): 
                high = high[:-1]
            playerBatting['highScore']=high
            playerBatting['average']=isValid(matchDetails[5])
            playerBatting['balls']=isValid(matchDetails[6])
            playerBatting['strikeRate']=isValid(matchDetails[7])
            playerBatting['100s']=isValid(matchDetails[8])
            playerBatting['50s']=isValid(matchDetails[9])
            playerBatting['4s']=isValid(matchDetails[10])
            playerBatting['6s']=isValid(matchDetails[11])
            playerFielding['catches']=isValid(matchDetails[12])
            playerFielding['stumpings']=isValid(matchDetails[13])
            print "done splitting image path"
            img = soup.find_all('img')
            try:
                imgPath="http://www.espncricinfo.com/"+img[17].get('src').split('html')[0]+'jpg'
            except:
                try:
                    imgPath="http://www.espncricinfo.com/"+img[8].get('src').split('html')[0]+'jpg'
                except:
                    imgPath="asdf"
            # urllib.urlretrieve(imgPath, str(player['id'])+".jpg")
            player['imgPath']= str(player['id'])+".jpg"
            insertPlayersDetails(player)
            insertBattingDetails(playerBatting)
            insertFieldingDetails(playerFielding)
            playerData=playerData[1].find_next_siblings("td")
            if  playerData is not None :
                playerBowling['matches']=playerBatting['matches']
                playerBowling['balls']=isValid(playerData[2])
                playerBowling['runs']=isValid(playerData[3])
                playerBowling['wickets']=isValid(playerData[4])
                playerBowling['bbm']=isValid(playerData[6])
                playerBowling['average']=isValid(playerData[7])
                playerBowling['economy']=isValid(playerData[8])
                insertBowlingDetails(playerBowling)
        return 1
    except Exception,e:
        with open("error.txt", "a") as f:
            f.write(url)
            f.write(str(pid))
        print 'hello',str(e)
        return 0

with open('data.txt') as urlList:

    pid=1
    for url in urlList:
        print pid
        print url
        x=0
        x = newGetData(url,pid)
        if x==1:
            pid = pid + 1
        else:
            print "Ellam pochu"

db.close()
