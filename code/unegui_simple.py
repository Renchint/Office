from selenium import webdriver
from selenium.webdriver.common.by import By
import time

main_url = 'https://www.unegui.mn/l-hdlh/l-hdlh-zarna/azhlyin-bajroffis-zarna/'

# get the main page
driver = webdriver.Chrome()
driver.get(main_url)

# get a page by number
page_number = 6 
url = main_url + f"/?page={page_number}&ordering=newest"
driver.get(url)

# get an ad by number
ad_number = 1
driver.find_element(By.XPATH, f"/html/body/div[2]/div[3]/section/div[2]/div[1]/div[2]/div[2]/div[{ad_number}]").click()

data = {}

data['title']      = driver.find_element(By.ID, 'ad-title').text,
data['location']  = driver.find_element(By.XPATH,"/html/body/div[2]/div[3]/div/section[1]/div/div[2]/div[1]/div[1]/div[2]/div/a/span").text    
data['date_time']  = driver.find_element(By.XPATH,"/html/body/div[2]/div[3]/div/section[1]/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/span[1]").text
data['ad_id']  = driver.find_element(By.XPATH,"/html/body/div[2]/div[3]/div/section[1]/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/span[2]/span").text
data['price']  = driver.find_element(By.XPATH,"/html/body/div[2]/div[3]/div/section[1]/div/div[3]/div/div[1]/div[1]/div/div").text
data['author']  = driver.find_element(By.XPATH,"/html/body/div[2]/div[3]/div/section[1]/div/div[3]/div/div[2]/div[1]").text
data['url'] = driver.current_url

driver.find_element(By.XPATH,"/html/body/div[2]/div[3]/div/section[1]/div/div[3]/div/div[1]/div[2]/div").click()
driver.find_element(By.XPATH,"/html/body/div[11]/div[2]/div/button[1]").click()

# wait until phone number appears on the screen
# time.sleep(1) # wait exactly 1 second
driver.implicitly_wait(1) # wait up to 1 seconds

try: 
    data['phone']  = driver.find_element(By.CSS_SELECTOR,"#ui-id-3 > div > a").text
except:
    pass

try:
    driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(33) > div.ui-dialog-titlebar.ui-widget-header.ui-corner-all.ui-helper-clearfix.ui-draggable-handle > button").click()
except:
    pass


# attributes 
atts = driver.find_elements(By.XPATH,"/html/body/div[2]/div[3]/div/section[1]/div/div[2]/div[1]/div[4]/ul/li")

for att in atts:  # 'li' элемент бүрийн key болон value-г авах
    try:
        key = att.find_element(By.CLASS_NAME, 'key-chars').text
        val = att.find_element(By.CLASS_NAME, 'value-chars').text
        data[key] = val
    except Exception as e:
        print(f"Error getting data from li: {e}")

# description
data['description'] = driver.find_element(By.XPATH,"/html/body/div[2]/div[3]/div/section[1]/div/div[2]/div[1]/div[5]/div").text


# print data dict
for key, value in data.items():
    print(key, value)
