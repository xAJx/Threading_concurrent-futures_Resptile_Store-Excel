from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from threading import Thread
import pandas as pd
import datetime, math
print()

driver = webdriver.Chrome()
driver2 = webdriver.Chrome()
driver.implicitly_wait(10)
print()
driver2.implicitly_wait(10)

beforeurl = 'https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword=Python&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=14&asc=0&page='
afterurl = '&mode=s&jobsource=2018indexpoc&langFlag=0&langStatus=0&recommendJob=1&hotJob=1'

# 第一頁開始
url = (beforeurl + '1' + afterurl)
driver.get(url)

print(driver.title)
print()

# 第六頁 開始
url2 = (beforeurl + '6' + afterurl)
driver2.get(url2)

print(driver2.title)
print()

def resptile_104_1_to_5():
    print()
    df = []

    soup = BeautifulSoup(driver.page_source, "lxml") #  抓取 並解析 網頁資料
    totaldata_location = soup.find('span',{'class':'js-txt'})
    total_number = int( totaldata_location.text.strip("()") )
    print('共', total_number ,'筆 data' )
    print()
    if total_number > 1500:
        total_number = 100      # 設定 抓幾筆資料
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
            sleep(0.1)     # 爬完每一筆 工作 暫停時間
            #i += 1
        print('處理第 ' + str(i+1) + ' 頁完畢 ! ' )
    df = pd.concat(df, ignore_index=True)
    df.to_excel('104_Thread-combin_1_to_5_def_職缺清單'+str(datetime.date.today())+'.xlsx', index=0)  #存為excel檔
    driver.quit()    
    print()

def resptile_104_6_to_10():
    print()
    df = []

    soup2 = BeautifulSoup(driver2.page_source, "lxml") #  抓取 並解析 網頁資料
    totaldata_location = soup2.find('span',{'class':'js-txt'})
    total_number = int( totaldata_location.text.strip("()") )
    print('共', total_number ,'筆 data' )
    print()
    if total_number > 1500:
        total_number = 100      # 設定 抓幾筆資料
    total_page = math.ceil(total_number/20)
    print('總頁碼,共: ',total_page , '頁')
    print()
    
    for i in range(total_page):
        print('------------------------')
        print('現在正在讀取第',str(i+6),'頁')
        print('------------------------')
        url2 = (beforeurl + str(i+6) + afterurl)  # 從第六頁開始 讀取
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
            sleep(0.1)     # 爬完每一筆 工作 暫停時間
            #i += 1
        print('處理第 ' + str(i+6) + ' 頁完畢 ! ' )
    df = pd.concat(df, ignore_index=True)
    df.to_excel('104_Thread-combin_6_to_10_def_職缺清單'+str(datetime.date.today())+'.xlsx', index=0)  #存為excel檔
    driver2.quit()     
    print()

a = Thread(target=resptile_104_1_to_5)
b = Thread(target=resptile_104_6_to_10)

# 開始計算時間
star = datetime.datetime.now()

# 開始 執行 Thread
a.start()
b.start()
a.join()   
b.join()

end = datetime.datetime.now()
run_time = end - star
print()
print("開始時間:", star)
print("結束時間:", end)
print()
print("執行時間(時:分:秒.毫秒) : ", run_time )
print()
print("執行時間(毫秒) :" , run_time.microseconds, " (ms)")
print()
