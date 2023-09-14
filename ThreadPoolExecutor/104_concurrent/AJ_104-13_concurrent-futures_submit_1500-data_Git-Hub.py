from selenium import webdriver
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor, as_completed 
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

beforeurl = 'https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword=Python&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=14&asc=0&page='
afterurl = '&mode=s&jobsource=2018indexpoc&langFlag=0&langStatus=0&recommendJob=1&hotJob=1'

# 第一頁開始
url = (beforeurl + '1' + afterurl)
driver.get(url)

print(driver.title)
print()

# 第二十六頁 開始
url2 = (beforeurl + '26' + afterurl)
driver2.get(url2)

print(driver2.title)
print()

# 第五十一頁 開始
url3 = (beforeurl + '51' + afterurl)
driver3.get(url3)

print(driver3.title)
print()

def resptile_104_1_to_25():
    print()
    df = []

    soup = BeautifulSoup(driver.page_source, "lxml") #  抓取 並解析 網頁資料
    totaldata_location = soup.find('span',{'class':'js-txt'})
    total_number = int( totaldata_location.text.strip("()") )
    print('共', total_number ,'筆 data' )
    print()
    if total_number > 1500:
        total_number = 500      # 設定 抓幾筆資料
    total_page = math.ceil(total_number/20)
    print('總頁碼,共: ',total_page , '頁')
    print()
    
    for i in range(total_page):
        print('------------------------')
        print('現在正在讀取第',str(i+1),'頁')
        print('------------------------')
        url = (beforeurl + str(i+1) + afterurl)  # 從第一頁開始 讀取
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, "lxml")
        job = soup.find_all('article',class_="b-block--top-bord job-list-item b-clearfix js-job-item")

        count = 20 # 每一頁 有20 筆 內容

        for j in range (count): # 爬取 每一筆工作  的內容
            try:
                print(j+1)
                jobinfo = job[j].find('div', class_= 'b-block__left')

                job_position = jobinfo.a.text
                print(jobinfo.a.text)  # 印出職缺名稱

                web_site = "https:"+jobinfo.a['href']         # 網址 前面要加 "https:"
                print("https:"+jobinfo.a['href'])  # 職缺連結

                company = jobinfo.select('li')[1].a.text.strip()
                print(jobinfo.select('li')[1].a.text.strip())  # 公司名稱

                companysort_out = jobinfo.find('ul', class_= 'b-list-inline b-clearfix')
                companysort = companysort_out.select('li')[2].text
                print(companysort_out.select('li')[2].text)  # 公司類別

                area = jobinfo.find('ul',class_="b-list-inline b-clearfix job-list-intro b-content").li.text
                print(jobinfo.find('ul',class_="b-list-inline b-clearfix job-list-intro b-content").li.text)   # 工作地區
                
                # 薪資
                if jobinfo.find('div',class_="job-list-tag b-content").select('span')==[]:
                        #global salary_other_data
                    print(jobinfo.find('div',class_="job-list-tag b-content").a.text)
                    salary = jobinfo.find('div',class_="job-list-tag b-content").a.text
                else:            
                    print(jobinfo.find('div',class_="job-list-tag b-content").span.text)
                    salary = jobinfo.find('div',class_="job-list-tag b-content").span.text 

                # jobinfo2
                jobinfo2 = job[j].find('div', class_= "b-block__right b-pos-relative")

                person = jobinfo2.find('a', target="_blank" ).text
                print(jobinfo2.find('a', target="_blank" ).text)    # 應徵人數

                content = jobinfo.find('p', class_='job-list-item__info b-clearfix b-content').text.strip()

                print(jobinfo.find('p', class_='job-list-item__info b-clearfix b-content').text.strip())    # 其他事項

                print('=============================================')

                dfmono = pd.DataFrame([{'職務名稱':job_position,
                                        '工作網址': web_site,
                                        '公司名稱': company,
                                        '公司類別': companysort,
                                        '工作地點':area,
                                        '薪資':salary,
                                        '應徵人數':person,
                                        '其他事項':content 
                                        }],
                                        )
                df.append(dfmono)
            except:
                pass
            time.sleep(0.1)     # 爬完每一筆 工作 暫停時間
            #i += 1
        print('處理第 ' + str(i+1) + ' 頁完畢 ! ' )
    df = pd.concat(df, ignore_index=True)
    df.to_excel('104_ThreadPoolExecutor-submit_1~25_page_500-data_職缺清單'+str(datetime.date.today())+'.xlsx', index=0)  #存為excel檔
    driver.quit()    
    print()

def resptile_104_26_to_50():
    print()
    df = []

    soup2 = BeautifulSoup(driver2.page_source, "lxml") #  抓取 並解析 網頁資料
    totaldata_location = soup2.find('span',{'class':'js-txt'})
    total_number = int( totaldata_location.text.strip("()") )
    print('共', total_number ,'筆 data' )
    print()
    if total_number > 1500:
        total_number = 500      # 設定 抓幾筆資料
    total_page = math.ceil(total_number/20)
    print('總頁碼,共: ',total_page , '頁')
    print()
    
    for i in range(total_page):
        print('------------------------')
        print('現在正在讀取第',str(i+26),'頁')
        print('------------------------')
        url2 = (beforeurl + str(i+26) + afterurl)  # 從第二十六頁開始 讀取
        driver2.get(url2)
        soup2 = BeautifulSoup(driver2.page_source, "lxml")
        job = soup2.find_all('article',class_="b-block--top-bord job-list-item b-clearfix js-job-item")

        count = 20 # 每一頁 有20 筆 內容

        for j in range (count): # 爬取 每一筆工作  的內容
            try:

                print(j+1)
                jobinfo = job[j].find('div', class_= 'b-block__left')

                job_position = jobinfo.a.text
                print(jobinfo.a.text)  # 印出職缺名稱

                web_site = "https:"+jobinfo.a['href']         # 網址 前面要加 "https:"
                print("https:"+jobinfo.a['href'])  # 職缺連結

                company = jobinfo.select('li')[1].a.text.strip()
                print(jobinfo.select('li')[1].a.text.strip())  # 公司名稱

                companysort_out = jobinfo.find('ul', class_= 'b-list-inline b-clearfix')
                companysort = companysort_out.select('li')[2].text
                print(companysort_out.select('li')[2].text)  # 公司類別

                area = jobinfo.find('ul',class_="b-list-inline b-clearfix job-list-intro b-content").li.text
                print(jobinfo.find('ul',class_="b-list-inline b-clearfix job-list-intro b-content").li.text)   # 工作地區
                
                # 薪資
                if jobinfo.find('div',class_="job-list-tag b-content").select('span')==[]:
                        #global salary_other_data
                    print(jobinfo.find('div',class_="job-list-tag b-content").a.text)
                    salary = jobinfo.find('div',class_="job-list-tag b-content").a.text
                else:            
                    print(jobinfo.find('div',class_="job-list-tag b-content").span.text)
                    salary = jobinfo.find('div',class_="job-list-tag b-content").span.text 

                # jobinfo2
                jobinfo2 = job[j].find('div', class_= "b-block__right b-pos-relative")

                person = jobinfo2.find('a', target="_blank" ).text
                print(jobinfo2.find('a', target="_blank" ).text)    # 應徵人數

                content = jobinfo.find('p', class_='job-list-item__info b-clearfix b-content').text.strip()
                print(jobinfo.find('p', class_='job-list-item__info b-clearfix b-content').text.strip())    # 其他事項

                print('=============================================')

                dfmono = pd.DataFrame([{'職務名稱':job_position,
                                        '工作網址': web_site,
                                        '公司名稱': company,
                                        '公司類別': companysort,
                                        '工作地點':area,
                                        '薪資':salary,
                                        '應徵人數':person,
                                        '其他事項':content 
                                        }],
                                        )
                df.append(dfmono)
            except:
                pass
            time.sleep(0.1)     # 爬完每一筆 工作 暫停時間
            #i += 1
        print('處理第 ' + str(i+26) + ' 頁完畢 ! ' )
    df = pd.concat(df, ignore_index=True)
    df.to_excel('104_ThreadPoolExecutor-submit_26~50_page_500-data_職缺清單'+str(datetime.date.today())+'.xlsx', index=0)  #存為excel檔
    driver2.quit()     
    print()

def resptile_104_51_to_75():
    print()
    df = []

    soup3 = BeautifulSoup(driver3.page_source, "lxml") #  抓取 並解析 網頁資料
    totaldata_location = soup3.find('span',{'class':'js-txt'})
    total_number = int( totaldata_location.text.strip("()") )
    print('共', total_number ,'筆 data' )
    print()
    if total_number > 1500:
        total_number = 500      # 設定 抓幾筆資料
    total_page = math.ceil(total_number/20)
    print('總頁碼,共: ',total_page , '頁')
    print()
    
    for i in range(total_page):
        print('------------------------')
        print('現在正在讀取第',str(i+51),'頁')
        print('------------------------')
        url3 = (beforeurl + str(i+51) + afterurl)  # 從第五十一頁開始 讀取
        driver3.get(url3)
        soup3 = BeautifulSoup(driver3.page_source, "lxml")
        job = soup3.find_all('article',class_="b-block--top-bord job-list-item b-clearfix js-job-item")

        count = 20 # 每一頁 有20 筆 內容

        for j in range (count): # 爬取 每一筆工作  的內容
            try:

                print(j+1)
                jobinfo = job[j].find('div', class_= 'b-block__left')

                job_position = jobinfo.a.text
                print(jobinfo.a.text)  # 印出職缺名稱

                web_site = "https:"+jobinfo.a['href']         # 網址 前面要加 "https:"
                print("https:"+jobinfo.a['href'])  # 職缺連結

                company = jobinfo.select('li')[1].a.text.strip()
                print(jobinfo.select('li')[1].a.text.strip())  # 公司名稱

                companysort_out = jobinfo.find('ul', class_= 'b-list-inline b-clearfix')
                companysort = companysort_out.select('li')[2].text
                print(companysort_out.select('li')[2].text)  # 公司類別

                area = jobinfo.find('ul',class_="b-list-inline b-clearfix job-list-intro b-content").li.text
                print(jobinfo.find('ul',class_="b-list-inline b-clearfix job-list-intro b-content").li.text)   # 工作地區
                
                # 薪資
                if jobinfo.find('div',class_="job-list-tag b-content").select('span')==[]:
                        #global salary_other_data
                    print(jobinfo.find('div',class_="job-list-tag b-content").a.text)
                    salary = jobinfo.find('div',class_="job-list-tag b-content").a.text
                else:            
                    print(jobinfo.find('div',class_="job-list-tag b-content").span.text)
                    salary = jobinfo.find('div',class_="job-list-tag b-content").span.text 

                # jobinfo2
                jobinfo2 = job[j].find('div', class_= "b-block__right b-pos-relative")

                person = jobinfo2.find('a', target="_blank" ).text
                print(jobinfo2.find('a', target="_blank" ).text)    # 應徵人數

                content = jobinfo.find('p', class_='job-list-item__info b-clearfix b-content').text.strip()
                print(jobinfo.find('p', class_='job-list-item__info b-clearfix b-content').text.strip())    # 其他事項

                print('=============================================')

                dfmono = pd.DataFrame([{'職務名稱':job_position,
                                        '工作網址': web_site,
                                        '公司名稱': company,
                                        '公司類別': companysort,
                                        '工作地點':area,
                                        '薪資':salary,
                                        '應徵人數':person,
                                        '其他事項':content 
                                        }],
                                        )
                df.append(dfmono)
            except:
                pass
            time.sleep(0.1)     # 爬完每一筆 工作 暫停時間
            #i += 1
        print('處理第 ' + str(i+51) + ' 頁完畢 ! ' )
    df = pd.concat(df, ignore_index=True)
    df.to_excel('104_ThreadPoolExecutor-submit_51~75_page_500-data_職缺清單'+str(datetime.date.today())+'.xlsx', index=0)  #存為excel檔
    driver3.quit()     
    print()

#  分別建立、執行
with ThreadPoolExecutor() as executor:
    executor = ThreadPoolExecutor(max_workers=100)
    a = executor.submit(resptile_104_1_to_25)

with ThreadPoolExecutor() as executor2:
    executor2 = ThreadPoolExecutor(max_workers=100)
    b = executor2.submit(resptile_104_26_to_50)

with ThreadPoolExecutor() as executor3:
    executor3 = ThreadPoolExecutor(max_workers=100)
    c = executor3.submit(resptile_104_51_to_75)
