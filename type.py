import MySQLdb
db = MySQLdb.connect("localhost","root","mreva747","mydb")
cursor = db.cursor()
sql="SELECT style,playerId FROM playerDetails";
cursor.execute(sql)
playerList=cursor.fetchall()
for player in playerList:
    if player[0]=='Allrounder':
        playerType='Allrounder'
    elif player[0] == 'Wicketkeeper':
        playerType='Wicketkeeper'
    elif player[0].find('bat')!=-1:
        playerType='Batsman'
    else:
        playerType='Bowler'
    sql="UPDATE playerDetails SET playerType='{}' WHERE playerId={}".format(playerType,player[1])
    print sql
    cursor.execute(sql)
    db.commit()
db.close()
