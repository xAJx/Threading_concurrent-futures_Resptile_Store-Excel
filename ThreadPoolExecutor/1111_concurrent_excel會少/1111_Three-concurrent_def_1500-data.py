# thread 開到 3個，爬蟲 excel結果，資料會不齊全，目前【推測部分原因】:可能是硬體不夠強大支援_例:散熱、cpu
from selenium import webdriver
from bs4 import BeautifulSoup
# from time import sleep
# from threading import Thread
from concurrent.futures import ThreadPoolExecutor, as_completed 
import time
import pandas as pd
import datetime, math
print()

driver = webdriver.Chrome()
driver2 = webdriver.Chrome()
driver3 = webdriver.Chrome()
driver.implicitly_wait(10)
print()
driver2.implicitly_wait(10)
print()
driver3.implicitly_wait(10)

def one():
    df = []
    baseurl = 'https://www.1111.com.tw/search/job?ks=軟體工程師&page='  # 軟體工程師
    #取得總資料數
    driver.get(baseurl + '1')
    soup = BeautifulSoup(driver.page_source, 'lxml')
    tem = soup.find('div', class_='srh-result-count nav_item job_count')
    jobn = int(tem.get('data-count').replace(',', ''))
    if jobn > 1500:  #最多取 1500筆資料
        jobn = 500    # 設定 取 多少筆 資料
    page = math.ceil(jobn/20)
    # 逐頁讀取資料
    for i in range(page):
        url = baseurl + str(i+1)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        job = soup.find_all('div', class_='body-wrapper')
        if (i+1)*20 > jobn:
            count = jobn - i*20
        else:
            count = 20
        for j in range(count):
            try:
                jobinfo = job[j].find('div', class_='job_item_info')
                work = jobinfo.find('h5').text  #職務名稱
                site = jobinfo.find('a').get('href')  #工作網址
                title = jobinfo.find('div', class_='card-subtitle mb-4 text-muted happiness-hidd').find('a').get('title')
                tlist = title.split('\n')
                company = tlist[0].replace('《公司名稱》', '')  #公司名稱
                companysort = tlist[1].replace('《行業類別》', '')  #公司類別
                area = tlist[2].replace('《公司住址》', '')  #工作地點
                salary = jobinfo.find('div', class_='job_item_detail_salary ml-3 font-weight-style digit_6').text  #薪資
                person = jobinfo.find('span', class_='applicants_data').text  #應徵人數
                content = jobinfo.find('p', class_='card-text job_item_description body_4').text  #其他事項
                dfmono = pd.DataFrame([{'職務名稱':work,
                                    '工作網址': site,
                                    '公司名稱': company,
                                    '公司類別': companysort,
                                    '工作地點':area,
                                    '薪資':salary,
                                    '應徵人數':person,
                                    '其他事項':content }],
                                    )
                df.append(dfmono)
            except:
                pass
            time.sleep(0.1)
        print('處理第 ' + str(i+1) + ' 頁完畢！')
    df = pd.concat(df, ignore_index=True)
    df.to_excel('1111_1_to_500_data.xlsx', index=0)  #存為excel檔
    driver.quit()    
    print()

def two():
    df = []
    baseurl = 'https://www.1111.com.tw/search/job?ks=軟體工程師&page='  # 軟體工程師
    #取得總資料數
    driver2.get(baseurl + '26')
    soup = BeautifulSoup(driver2.page_source, 'lxml')
    tem = soup.find('div', class_='srh-result-count nav_item job_count')
    jobn = int(tem.get('data-count').replace(',', ''))
    if jobn > 1500:  #最多取 1500筆資料
        jobn = 500    # 設定 取 多少筆 資料
    page = math.ceil(jobn/20)
    # 逐頁讀取資料
    for i in range(page):
        url = baseurl + str(i+26)
        driver2.get(url)
        soup = BeautifulSoup(driver2.page_source, 'lxml')
        job = soup.find_all('div', class_='body-wrapper')
        if (i+1)*20 > jobn:
            count = jobn - i*20
        else:
            count = 20
        for j in range(count):
            try:
                jobinfo = job[j].find('div', class_='job_item_info')
                work = jobinfo.find('h5').text  #職務名稱
                site = jobinfo.find('a').get('href')  #工作網址
                title = jobinfo.find('div', class_='card-subtitle mb-4 text-muted happiness-hidd').find('a').get('title')
                tlist = title.split('\n')
                company = tlist[0].replace('《公司名稱》', '')  #公司名稱
                companysort = tlist[1].replace('《行業類別》', '')  #公司類別
                area = tlist[2].replace('《公司住址》', '')  #工作地點
                salary = jobinfo.find('div', class_='job_item_detail_salary ml-3 font-weight-style digit_6').text  #薪資
                person = jobinfo.find('span', class_='applicants_data').text  #應徵人數
                content = jobinfo.find('p', class_='card-text job_item_description body_4').text  #其他事項
                dfmono = pd.DataFrame([{'職務名稱':work,
                                    '工作網址': site,
                                    '公司名稱': company,
                                    '公司類別': companysort,
                                    '工作地點':area,
                                    '薪資':salary,
                                    '應徵人數':person,
                                    '其他事項':content }],
                                    )
                df.append(dfmono)
            except:
                pass
            time.sleep(0.1)
        print('處理第 ' + str(i+26) + ' 頁完畢！')
    df = pd.concat(df, ignore_index=True)
    df.to_excel('1111_501-to-1000_data.xlsx', index=0)  #存為excel檔
    driver2.quit()    
    print()

def thr():
    df = []
    baseurl = 'https://www.1111.com.tw/search/job?ks=軟體工程師&page='  # 軟體工程師
    #取得總資料數
    driver3.get(baseurl + '51')
    soup = BeautifulSoup(driver3.page_source, 'lxml')
    tem = soup.find('div', class_='srh-result-count nav_item job_count')
    jobn = int(tem.get('data-count').replace(',', ''))
    if jobn > 1500:  #最多取 1500筆資料
        jobn = 500    # 設定 取 多少筆 資料
    page = math.ceil(jobn/20)
    # 逐頁讀取資料
    for i in range(page):
        url = baseurl + str(i+51)
        driver3.get(url)
        soup = BeautifulSoup(driver3.page_source, 'lxml')
        job = soup.find_all('div', class_='body-wrapper')
        if (i+1)*20 > jobn:
            count = jobn - i*20
        else:
            count = 20
        for j in range(count):
            try:
                jobinfo = job[j].find('div', class_='job_item_info')
                work = jobinfo.find('h5').text  #職務名稱
                site = jobinfo.find('a').get('href')  #工作網址
                title = jobinfo.find('div', class_='card-subtitle mb-4 text-muted happiness-hidd').find('a').get('title')
                tlist = title.split('\n')
                company = tlist[0].replace('《公司名稱》', '')  #公司名稱
                companysort = tlist[1].replace('《行業類別》', '')  #公司類別
                area = tlist[2].replace('《公司住址》', '')  #工作地點
                salary = jobinfo.find('div', class_='job_item_detail_salary ml-3 font-weight-style digit_6').text  #薪資
                person = jobinfo.find('span', class_='applicants_data').text  #應徵人數
                content = jobinfo.find('p', class_='card-text job_item_description body_4').text  #其他事項
                dfmono = pd.DataFrame([{'職務名稱':work,
                                    '工作網址': site,
                                    '公司名稱': company,
                                    '公司類別': companysort,
                                    '工作地點':area,
                                    '薪資':salary,
                                    '應徵人數':person,
                                    '其他事項':content }],
                                    )
                df.append(dfmono)
            except:
                pass
            time.sleep(0.1)
        print('處理第 ' + str(i+51) + ' 頁完畢！')
    df = pd.concat(df, ignore_index=True)
    df.to_excel('1111_1001-to-1500_data.xlsx', index=0)  #存為excel檔
    driver3.quit()    
    print()

'''one()
two()
thr()'''


'''a = Thread(target=one)
b = Thread(target=two)
c = Thread(target=thr)

# 開始計算時間
star = datetime.datetime.now()

# 開始 執行 Thread
a.start()
b.start()
c.start()

a.join()   # 要用 join 需要 多加一個變數 去承接  
b.join()
c.join()'''

# if a.join() & b.join() & c.join():  # 沒有這個語法，會錯誤

# star = datetime.datetime.now()

#  分別建立、執行
with ThreadPoolExecutor() as executor:
    executor = ThreadPoolExecutor(max_workers=100)
    a = executor.submit(one)

with ThreadPoolExecutor() as executor2:
    executor2 = ThreadPoolExecutor(max_workers=100)
    b = executor2.submit(two)

with ThreadPoolExecutor() as executor3:
    executor3 = ThreadPoolExecutor(max_workers=100)
    c = executor3.submit(thr)

'''end = datetime.datetime.now()
run_time = end - star
print()
print("開始時間:", star)
print("結束時間:", end)
print()
print("執行時間(時:分:秒.毫秒) : ", run_time )
print()
print("執行時間(毫秒) :" , run_time.microseconds, " (ms)")
print()'''
