
# ------------------------------------------
#          edx web scraping
# ------------------------------------------

import requests
from bs4 import BeautifulSoup
import os
import csv
import sqlite3

title = []
link = []
time = []
How_study = []
cost = []

db = sqlite3.connect("edx.db")

cr = db.cursor()

cr.execute("drop table edx_data ")
cr.execute("CREATE TABLE if not exists edx_data  (id tinyint AUTO_INCREMENT,name varchar(255) ,  Duration varchar(255), Cost varchar(255))")

os.chdir(os.path.dirname(os.path.abspath(__file__)))

reselt = requests.get(
    "https://www.edx.org/learn/computer-programming")

soup = BeautifulSoup(reselt.content, "html.parser")

titles = soup.find_all("h3", {"class": "h4"})
links = soup.find_all("div", {"class": "discovery-card"})

for i in titles:
    title.append(i.text)

for i in links:
    link.append("https://www.edx.org"+i.find("a").attrs["href"])


for i in link:
    # print(i)
    sub_reselt = requests.get(i)
    # print(sub_reselt)
    sub_soup = BeautifulSoup(sub_reselt.content, "html.parser")
    # print(sub_soup.text)
    inf = sub_soup.find_all("div", {"class": "ml-3"})
    if inf == []:
        inf = sub_soup.find_all("div", {"class": "details"})
        if inf == []:
            time.append(" ")
            How_study.append(" ")
            cost.append(" ")
        else:
            for i in range(len(inf)):
                time.append(inf[i+2].text)
                How_study.append(inf[i+1].text)
                cost.append(inf[i+3].text)
                break
        continue
    for i in range(len(inf)):
        time.append(inf[i].text)
        How_study.append(inf[i+1].text)
        cost.append(inf[i+2].text)
        break


# for i in range(len(title)):
#                 print([title[i],time[i],How_study[i],cost[i]])
#                 print("!"*20)

# print(len(title))
# print(len(time))
# print(len(How_study))
# print(len(cost))

title[25] = 'Introduction to Computer Science and Programming…'
with open("edx.csv", "w") as myfile :
            wr = csv.writer(myfile)
            wr.writerow(['Course title', 'Time', 'How to study it', 'Cost'])
            for i in range(len(title)):
                wr.writerow([title[i],time[i],How_study[i],cost[i]])
                try:
                    cr.execute(f"insert into edx_data (id,name, Duration, Cost) values({i+1},'{title[i]}', '{time[i]}', '{cost[i]}')")
                except:
                    print("aaaaaahhhhh")
                db.commit()
            


