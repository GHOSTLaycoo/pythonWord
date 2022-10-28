from bs4 import BeautifulSoup
from selenium import webdriver
import time,random
import pymysql

# 控制爬取页数
num = 2

# 插入语句
sql = "insert into boos(id,title, company, price, education, text, introduce , address, `scale`, url) values(null,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

# 请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",

    # 爬取boos直聘cookie必不可少，参考图1
    "cookie": ""
}

# IP代理
proxy = {
    'https': '61.178.118.86:8080'
}


# 爬取数据
def Crawling(cur, conn):
    # 引入全局变量
    global sql
    job = "java"
    page = 10
    htmls_list = []
    for num in range(1, page):
        url = "https://www.zhipin.com/c101010100/?query={}&page=1&ka=page-{}".format(job, num)
        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(6)
        htmls = driver.page_source
        htmls_list.append(str(htmls))
        driver.close()
        ran_time = random.randint(1, 5)
        time.sleep(ran_time)

    info_list = []
    for htmls in htmls_list:
        soup = BeautifulSoup(htmls, "lxml")
        li_list = soup.find_all(class_="job-card-wrapper")
        for i in li_list:
            i2 = BeautifulSoup(str(i), "lxml")
            job = i2.find("span", class_="job-name").text
            area = i2.find('span', class_="job-area").text
            salary = i2.find('span', class_='salary').text  # 获取薪酬信息
            title = i2.find("h3").find("a").text  # 获取企业名称
            edu = i2.find('ul', class_="tag-list").find_all("li")# 获取学历要求
            # text = i2.find('ul', class_="tag-list").find_all("li")[1].text  # 获取试用期要求
            # introduce = i2.find('ul', class_="tag-list").find_all("li")[0].text  # 获取上班时间要求
            scale = i2.find('ul', class_="company-tag-list").find_all("li")  # 获取条件信息
            url = "https://www.zhipin.com" + i2.find("a", class_="job-card-left")['href']  # 获取详情页信息
            cur.execute(sql, (job, title, salary, edu, scale, "introduce", area, "scale", url))
            conn.commit()
    return cur, conn


# 初始化mysql连接
def init_mysql():
    dbparams = {
        'host': '192.168.4.20',
        'port': 3306,
        'user': 'root',
        'password': 'root',
        'database': 'xxl_job',  # 数据库名
        'charset': 'utf8'
    }
    conn = pymysql.connect(**dbparams)
    cur = conn.cursor()
    return cur, conn


# 关闭数据库连接
def close(cur, conn):
    cur.close()
    conn.close()


# 起始
if __name__ == "__main__":
    # print("="*40)
    # 防止请求频繁，关闭多余链接，可参考博主的文章
    cur, conn = init_mysql()

    # 爬取数据
    cur, conn = Crawling(cur, conn)

    # 关闭数据库连接
    close(cur, conn)

