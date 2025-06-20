from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
import pandas as pd
from joblib import Parallel, delayed
from datetime import datetime, date, timedelta
import re

def collect_ad_details(page_number, driver ):

    main_url = 'https://www.unegui.mn/l-hdlh/l-hdlh-zarna/azhlyin-bajroffis-zarna/'
    url = f'{main_url}?page={page_number}&ordering=newest'
    driver.get(url)

    data_list = []
    for ad_number in range(1, 61):  # 1-ээс 2 хүртэлх зараас мэдээлэл авах
        
        print(f"Page: {page_number} Ad: {ad_number}" )
        
        # Тухайн зар дээр очих
        try:
            ad_link = driver.find_element(
                By.XPATH, 
                f'/html/body/div[2]/div[3]/section/div[2]/div[1]/div[2]/div[2]/div[{ad_number}]/div[1]/div[1]/div[1]/a[1]'
            )
            ad_link.click()
        except Exception as e:
            print(f"Error opening ad {ad_number}: {e}")
            continue

        # Privacy зөвшөөрөл өгөх (эхний удаа)
        if ad_number == 1:
            try:
                first_page_link = driver.find_element(By.CSS_SELECTOR, 'a.page-number[data-page="1"]')
                ActionChains(driver).move_to_element(first_page_link).click().perform()
            except Exception as e:
                print(f"Error accepting privacy policy: {e}")

        # Collecting data
        data = {
                'page_number'   : page_number,
                'ad_number'     : ad_number,
                'url'           : driver.current_url,
                'title'         : driver.find_element(By.ID, 'ad-title').text,
                'location'      : driver.find_element(By.CLASS_NAME, 'announcement__location').text,
                'date'          : driver.find_element(By.CLASS_NAME, 'date-meta').text,
                'id'            : driver.find_element(By.CSS_SELECTOR, '[itemprop="sku"]').text,
                'price'         : driver.find_element(By.CLASS_NAME, 'announcement-price__cost').text, 
                'ad_text'       : driver.find_element(By.CLASS_NAME, 'js-description').text,
            }
        
        # Phone number
        try:
            driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/section[1]/div/div[3]/div/div[1]/div[2]/div").click()  # Нуугдсан дугаарыг үзүүлэх товч дээр дарах
            driver.implicitly_wait(1)  # Утасны дугаар гарч ирэхийг хүлээх

            try: # Утасны дугаар авах зөвшөөрөл өгөх
                driver.find_element(By.XPATH, "/html/body/div[10]/div[2]/div/button[1]").click() 
            except:
                pass

            try: # Утасны дугаар авах
                data['phone'] = driver.find_element(By.XPATH, "/html/body/div[11]/div[2]/div[1]/a").text
            except:
                data['phone'] = driver.find_element(By.XPATH, "/html/body/div[10]/div[2]/div[1]/a").text

            
            try: # Гарч буй цонхыг хаах
                driver.find_element(By.XPATH, "/html/body/div[10]/div[1]/button").click()
            except:
                driver.find_element(By.XPATH, "/html/body/div[11]/div[1]/button").click()

        except Exception as e:
            print(f"Error retrieving phone number for ad {ad_number}: {e}")
            data['phone'] = 'N/A'

        # Info office
        atts = driver.find_elements(By.XPATH, '/html/body/div[2]/div[3]/div/section[1]/div/div[2]/div[1]/div[4]/ul/li')
        for att in atts:
            try:
                key = att.find_element(By.CLASS_NAME, 'key-chars').text
                val = att.find_element(By.CLASS_NAME, 'value-chars').text
                data[key] = val
            except Exception as e:
                print(f"Error collecting data from ad {ad_number}: {e}")
    
        ''' Координат авах '''
        try: 
            element = driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/section[1]/div/div[2]/div[1]/div[1]/div[2]/div/a") 
            coords = element.get_attribute("data-coords")
            match = re.search(r"POINT \((.+)\)", coords)
            if match:
                lon, lat = match.group(1).split()
                data['clean_coords'] = f"{lat} {lon}"
            else:
                print("No coordinates found!")
        except:
            pass

        data_list.append(data)  # Мэдээллийг жагсаалтанд нэмэх
        driver.back()  # Буцаж хуудас руу шилжих
    return data_list

# WebDriver үүсгэх
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

    
    
all_data = []
for page in range(1, 5): # Хуудас нэмэх хэрэгтэй бол 3-г өөрчлөнө
    all_data.extend(collect_ad_details(page, driver))

# DataFrame үүсгэх
df = pd.DataFrame(all_data)
print(df)

# Одоогийн огноо, цагийг авах
current_time = datetime.now()
formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")  # Жишээ: 2025-01-05_15-30-45

# Файлын нэр үүсгэх
file_name = f"ads_data_{formatted_time}.csv"

# CSV файлд хадгалах
df.to_csv(file_name, index=False, encoding='utf-8-sig')

print(f"Мэдээлэл '{file_name}' нэртэйгээр амжилттай хадгалагдлаа.")