# cftools.py
# codeforces小助手

import requests
import re
import xlwt
import json
import sqlite3

dbbase = "./cfdata.db"

findLink = re.compile(r'<a href="(.*?)">')  # 创建正则表达式对象，标售规则   影片详情链接的规则
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)
findTitle = re.compile(r'<span class="title">(.*)</span>')
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findJudge = re.compile(r'<span>(\d*)人评价</span>')
findInq = re.compile(r'<span class="inq">(.*)</span>')
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)

class CodeForces:
    url = "https://codeforces.com/api/contest.list"
    contests = "contests/"
    savepath = "./contest.xls"

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    }

    def __init__(self):
        pass

    def getContests(self):
        res = requests.get(url=self.url, headers=self.headers)
        with open("./test.txt", "w") as f:
            f.write(res.text)
        #print(res.text)

# 爬取网页
def getData(baseurl):
    datalist = []  #用来存储爬取的网页信息
    for i in range(0, 10):  # 调用获取页面信息的函数，10次
        url = baseurl + str(i * 25)
        html = askURL(url)  # 保存获取到的网页源码
        # 2.逐一解析数据
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="item"):  # 查找符合要求的字符串
            data = []  # 保存一部电影所有信息
            item = str(item)
            link = re.findall(findLink, item)[0]  # 通过正则表达式查找
            data.append(link)
            imgSrc = re.findall(findImgSrc, item)[0]
            data.append(imgSrc)
            titles = re.findall(findTitle, item)
            if (len(titles) == 2):
                ctitle = titles[0]
                data.append(ctitle)
                otitle = titles[1].replace("/", "")  #消除转义字符
                data.append(otitle)
            else:
                data.append(titles[0])
                data.append(' ')
            rating = re.findall(findRating, item)[0]
            data.append(rating)
            judgeNum = re.findall(findJudge, item)[0]
            data.append(judgeNum)
            inq = re.findall(findInq, item)
            if len(inq) != 0:
                inq = inq[0].replace("。", "")
                data.append(inq)
            else:
                data.append(" ")
            bd = re.findall(findBd, item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?', "", bd)
            bd = re.sub('/', "", bd)
            data.append(bd.strip())
            datalist.append(data)

    return datalist

def askURL(url):
    pass

# 保存数据到表格
def saveData(datalist,savepath):
    print("save.......")
    book = xlwt.Workbook(encoding="utf-8",style_compression=0) #创建workbook对象
    sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True) #创建工作表
    col = ("电影详情链接","图片链接","影片中文名","影片外国名","评分","评价数","概况","相关信息")
    for i in range(0,8):
        sheet.write(0,i,col[i])  #列名
    for i in range(0,250):
        # print("第%d条" %(i+1))       #输出语句，用来测试
        data = datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])  #数据
    book.save(savepath) #保存



def getProblem():
    #req = requests.get("https://codeforces.com/api/problemset.problems")
    #html = req.text
    with open("./cf_contest.js", "r") as f:
        html = f.readlines()[0]
    data = json.loads(html)["result"]  # problems  problemStatistics
    problems = data["problems"]
    problemStatistics = data["problemStatistics"]
    for pro in problems:
        contestId = pro["contestId"]
        index = pro["index"]
        name = pro["name"]
        type = pro["type"]
        tags = pro["tags"]
        print(contestId)
        print(index)
        print(name)
        print(type)
        print(tags)
        break
    #print(problems[0].keys())

def sqlite_create():
   

    # 连接到 SQLite 数据库
    conn = sqlite3.connect(dbbase)
    cursor = conn.cursor()

    # 创建表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cf_contest (
            contestId INTEGER NOT NULL,
            index TEXT NOT NULL,
            name TEXT,
            type TEXT,
            PRIMARY KEY(contestId, index)
        )
    ''')
    conn.commit()


if __name__ == "__main__":  # 当程序执行时
    sqlite_create()