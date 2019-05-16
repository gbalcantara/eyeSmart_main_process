import psycopg2
from datetime import datetime, timedelta, time
import requests
import json

currentDT = datetime.now()
prevDT = currentDT - timedelta(minutes=30)

year = 2019
month = 4
date = 23
hour = 7
min = 0
sec = 0
fsec = 0
#start_time = datetime.strptime('2019-04-22 13:00:00.000000', '%Y-%m-%d %H:%M:%S.%f')
start_time = datetime(year, month, date, hour, min, sec, fsec)
end_time = start_time + timedelta(minutes=30) - timedelta(seconds=1)
day = start_time.weekday()
date = start_time.date()
#conn = psycopg2.connect(database="dateandtime", user = "gab",
#        password = "admin1234", host = "192.168.0.104", port = "5432")
#print("Opened database datandtime successfully")
#cur = conn.cursor()

#cur.execute("SELECT id, fn, mdytm, zn, ps, ac FROM db11 \
#            WHERE ps IS NOT NULL AND mdytm BETWEEN '%s' AND '%s' ORDER BY id" \
#            % (start_time, end_time))


conn = psycopg2.connect(database="timeinterval", user = "sjeckem",
        password = "admin1234", host = "127.0.0.1", port = "5432")
print("Opened database timeinterval successfully")
cur = conn.cursor()

while start_time.date() <= currentDT.date():
    time_interval = {
            "ntig" : [],
            "mty" : [],
            "mnill" : [],
            "cdz" : [],
            "jom" : []
            }
    fac_id = {
        "mty" : 1,
        "mnill" : 2,
        "jom" : 3,
        "ntig" : 4,
        "cdz" : 5
        }
    url = 'https://eyesmart.herokuapp.com/api/free-time/'
    headers = {'Content-Type': 'application/json', 'Authorization': 'Token a9120e6f98291c3efa6dba047ac99b0103f9954f'}

    for i in range(22):
        cur.execute("SELECT id, fn, mdytm, zn, ps, ac FROM db1 \
                    WHERE ps IS NOT NULL AND mdytm BETWEEN '%s' AND '%s' ORDER BY id" \
                    % (start_time, end_time))

        print(start_time, end_time)
        start_time += timedelta(minutes=30)
        end_time += timedelta(minutes=30)
        # ID, FILENAME, DATE_TIME, ZONE, PERSON, ACTION

        rows = cur.fetchall()
        if not rows:
            print("No entries\n")
            continue

        count = {
                "ntig" : 0,
                "mty" : 0,
                "mnill" : 0,
                "cdz" : 0,
                "jom" : 0
                }

        init = rows[0]
        for index, row in enumerate(rows):
            # db1-types.txt
            '''
            print ("ID = ", type(row[0]))
            print ("FN = ", type(row[1]))
            print ("MDYTM = ", type(row[2]))
            print ("ZN = ", type(row[3]))
            print ("PS = ", type(row[4]))
            print ("AC = ", type(row[5]), "\n")
            '''
            # database.txt
            '''
            print ("ID = ", (row[0]))
            print ("FN = ", (row[1]))
            print ("MDYTM = ", (row[2]))
            print ("ZN = ", (row[3]))
            print ("PS = ", (row[4]))
            print ("AC = ", (row[5]), "\n")
            '''
            # db2-relevantinfo.txt

            id, _, curtime, _, ps, *_ = row
            prevtime = rows[index-1][2]
            #day = curtime.weekday()
            #print("ID = ", id)
            #print("MDYTM = ", curtime)
            #print("PERSON = ", ps)
            #if row != init:
                #print(curtime - prevtime)
            #print("\n")
            if ps:
                count[ps] += 1

        #print("Total entries:")
        #print(count, "\n")

        #print("time_interval = ", i)
        #print("day = ", day)
        for ps, value in count.items():
            if value > 300:
                print(ps, value, start_time.date())
                time_interval[ps].append('%s' % i)

        print("\n")
    print(time_interval)
    for ps, intervals in time_interval.items():
        if intervals:
            cur.execute("SELECT id, ps, date, day, time_interval FROM db2b ")
            id1 = cur.rowcount
            id2 = id1 + 1
            cur.execute("INSERT INTO db2b (id, ps, date, day, time_interval) \
                VALUES (%s, '%s', '%s', %s, ARRAY %s)" % (id2, ps, date, day, intervals))
            conn.commit()
            print("Inserted data into database")

            data = json.dumps({'faculty': '%s' % fac_id[ps],
                    'free_time': intervals,
                    'day': '%s' % day
                    })
            r = requests.post(url, data=data, headers=headers)
            print("RESPONSE:",r)

    start_time += timedelta(days=1)
    start_time = datetime.combine(start_time.date(), time(7, 0, 0))
    end_time = start_time + timedelta(minutes=30) - timedelta(seconds=1)
    day = start_time.weekday()
    date = start_time.date()
#cur.execute("INSERT INTO db11 (ID,MDYTM) VALUES (%s,current_timestamp)", (id2))

#cur.execute("SELECT mdytm from db11 WHERE id = %s",[id2])
#mtime = cur.fetchone()
#print(mtime)
#stringDT = str(mtime[0])

#conn.commit()
#print ("Records created successfully")

conn.close()
conn.close()
print("Closed database successfully")
