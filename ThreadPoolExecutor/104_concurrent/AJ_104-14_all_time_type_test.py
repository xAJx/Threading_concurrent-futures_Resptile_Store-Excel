# all_time_type_test
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import time
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import datetime, math
print()


# 開始計算時間
#star = datetime.datetime.now()
#star = time.localtime()
#star = time.ctime()
star = time.asctime()
sleep (3)
end = time.asctime()
#end = time.ctime()
#end = time.localtime()
#end = time.time()

#run_time = end - star
print()
print("開始時間:", star)
print()
print("結束時間:", end)
print()
#print("執行時間(時:分:秒.毫秒) : ", run_time )
print()
#print("執行時間(毫秒) :" , run_time.microseconds, " (ms)")
print()

