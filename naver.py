from selenium import webdriver
import logging
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import os
import shutil
import pandas as pd
import time
from geopy.geocoders import Nominatim
import requests
import urllib.parse
import re
from bs4 import BeautifulSoup
from itertools import product

# pip install beautifulsoup4 requests geopy pandas webdriver_manager selenium

# try:
#    service = Service(ChromeDriverManager().install())
# except ValueError:
#   latest_chromedriver_version_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
#   latest_chromedriver_version = urllib.request.urlopen(latest_chromedriver_version_url).read().decode('utf-8')
#   service = Service(ChromeDriverManager(driver_version=latest_chromedriver_version).install())

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# driver = webdriver.Chrome(service=Service) # --> run this code once then deactiuvate it like shift + #
options = webdriver.ChromeOptions() 
options.add_argument('--disable-dev-shm-usage')
# options.add_argument('--headless=new')
options.add_argument("--no-sandbox")
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
options.add_argument("--window-size=1920x1080")



driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)


def appendProduct(file_path2, data):
    temp_file = 'temp_file.csv'
    if os.path.isfile(file_path2):
        df = pd.read_csv(file_path2, encoding='utf-8')
    else:
        df = pd.DataFrame()

    df_new_row = pd.DataFrame([data])
    df = pd.concat([df, df_new_row], ignore_index=True)

    try:
        df.to_csv(temp_file, index=False, encoding='utf-8')
    except Exception as e:
        print(f"An error occurred while saving the temporary file: {str(e)}")
        return False

    try:
        os.replace(temp_file, file_path2)
    except Exception as e:
        print(f"An error occurred while replacing the original file: {str(e)}")
        return False

    return True


# Input paths here
logging.basicConfig(filename='script.log', level=logging.INFO)
logging.info('Script started.')
df = pd.read_excel('Consolidated_File2.xlsx')


# Let's make it easy for you, if you wish to change just put here
output_file_path = 'naver_copy_sample.csv'


try:
    # here you put the name of the output file basically
    recent = pd.read_csv(output_file_path)
except:
    recent = ''

# Print the values in the "Search Query" column
search_query_values = df['Search Query'].values
store_id_values = df['Store_ID_raw'].values
try:
    last_store_count = recent['New_Store_ID'].iloc[-1]
except:
    last_store_count = 0
    store_count = 1
try:
    last_review_count = recent['Review_ID'].iloc[-1]
except:
    last_review_count = 0
    review_count = 1

if last_store_count:
    store_count = int(last_store_count) + 1
else:
    store_count = 1

if last_review_count:
    review_count = int(last_review_count.replace('R', '').replace('B', '')) + 1
else:
    review_count = 1
# store_count = 1
# review_count = 1
driver.get(f"https://naver.com")
time.sleep(2)
for idx, value in enumerate(search_query_values):
    try:
        print(value)
        driver.get(f"https://map.naver.com/p/search/{value}?c=6,0,0,0,dh")
        time.sleep(10)
        logging.info(value)
        WebDriverWait(driver, 5).until(
                EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe#searchIframe")))
        element = driver.find_element(By.CSS_SELECTOR, "div#_pcmap_list_scroll_container")
        df = df[df['Search Query'] != value]
        df.to_excel('Consolidated_File2.xlsx', index=False)  # Save the updated DataFrame to the same file
    except:
        print("not found")
        logging.info("not found")
        continue

    next_flag = True
    while next_flag:
            driver.switch_to.default_content()    
            WebDriverWait(driver, 5).until(
                EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe#searchIframe")))

            stores = []
            element = driver.find_element(By.CSS_SELECTOR, "div#_pcmap_list_scroll_container")
            for scroll_idx in range(0, 5):
                driver.execute_script("arguments[0].scroll({top: arguments[0].scrollHeight, behavior: 'smooth'})",
                                      element)
                time.sleep(1)

            stores_css = driver.find_elements(By.XPATH, "//div[@id='_pcmap_list_scroll_container']/ul/li/div[1]/a")
            if len(stores_css) == 0:
                stores_css = driver.find_elements(By.XPATH,
                                                  "//div[@id='_pcmap_list_scroll_container']/ul/li/div[1]/div[1]/a")
                
            print(len(stores_css))
            logging.info(len(stores_css))

            # for single opening store
            if len(stores_css) == 1:
                # break
                try:
                        if len(driver.window_handles) >= 3:
                            try:
                                driver.switch_to.window(driver.window_handles[2])    
                                driver.close()
                            except:
                                pass
                            try:
                                driver.switch_to.window(driver.window_handles[1])
                                driver.close()
                            except:
                                pass
                            driver.switch_to.window(driver.window_handles[0])
                except:
                        pass
                   
                try:
                    stores_css[0].click()
                    stores_css[0].click()
                except:
                    pass
                try:
                    driver.switch_to.default_content()
                    WebDriverWait(driver, 10).until(
                        EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe#entryIframe")))
                except:
                    pass
                try:
                    driver.find_element(By.XPATH,"//span[contains(text(),'홈')]/parent::a").click()
                    time.sleep(0.5)
                except:
                    pass
                now = datetime.now()
                scrapping_time = now.strftime("%d/%m/%Y-%H:%M:%S")
                try:
                    store_name = driver.find_element(By.CSS_SELECTOR, "span.Fc1rA").text
                except:
                    store_name = "NA"
                try:
                    store_rating = driver.find_element(By.XPATH,"//div[@id='_title']/following-sibling::div/span[@class='PXMot LXIwF']").text.replace("별점",'').replace("\n",'')
                except:
                    store_rating = "NA"
                try:
                    category = driver.find_element(By.CSS_SELECTOR, "span.DJJvD").text
                except:
                    category = "NA"
                try:
                    link = driver.current_url
                except:
                    link = 'NA'
                    print("no link")

                try:
                    address = driver.find_element(By.CSS_SELECTOR, "span.LDgIH").text
                except:
                    address = "NA"
                try:
                    n_reviews = driver.find_element(By.XPATH, "//a[contains(text(),'방문자리뷰')]/em").text
                except:
                    n_reviews = "0"
                try:
                    n_blog_reviews = driver.find_element(By.XPATH, "//a[contains(text(),'블로그리뷰')]/em").text
                except:
                    n_blog_reviews = "0"
                try:
                    booking_hub = driver.find_element(By.XPATH,
                                                      "//span[contains(text(),'편의')]/parent::strong/following-sibling::div").text
                except:
                    booking_hub = "NA"
                try:
                    website_store = driver.find_element(By.CSS_SELECTOR, "a.CHmqa").get_attribute('href')
                except:
                    website_store = 'NA'
                review_type = ""

                try:
                    try:
                        visitor_review = driver.find_element(By.XPATH, "//span[.='리뷰']/parent::a").get_attribute('href')
                    except:
                        print("")
                        driver.switch_to.default_content()
                        WebDriverWait(driver, 10).until(
                            EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe#searchIframe")))
                        break
                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[1])
                    driver.get(visitor_review)
                    time.sleep(2)
                    review_type = "Visitor Review"
                    try:
                        check_skip = driver.find_element(By.XPATH,"//h2[text()='리뷰']/span[@class='place_section_count']")
                    except:
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        store_count = store_count + 1
                        driver.switch_to.default_content()
                        WebDriverWait(driver, 10).until(
                            EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe#searchIframe")))
                        continue

                    try:
                        stop_flag = True
                        try:
                            total_reviews = int(n_reviews.strip().replace(',',''))
                        except:
                            total_reviews = 0
                        if total_reviews >= 9000:
                            for count_review in range(0,900):
                                try:
                                    see_more_btn = driver.find_element(By.XPATH, "(//span[.='더보기'])[2]/parent::a").click()
                                    time.sleep(0.5)
                                except:
                                    stop_flag = False
                                    break

                        else:
                            while stop_flag:
                                try:
                                    see_more_btn = driver.find_element(By.XPATH, "(//span[.='더보기'])[2]/parent::a").click()
                                    time.sleep(0.5)
                                except:
                                    stop_flag = False
                                    break
                    except:
                        print("no see more button")

                    list_reviews = []
                    time.sleep(1)
                    list_reviews_xp = driver.find_elements(By.XPATH, "//li[@class='YeINN']")
                    for list_review_xp in list_reviews_xp:
                        list_reviews.append(list_review_xp)
                    print(len(list_reviews))
                    for rev_idx in range(0, len(list_reviews)):
                        try:
                            reviewer_id = driver.find_element(By.XPATH,
                                                              f"(//li[@class='YeINN'])[{rev_idx + 1}]/div/a[2]/div[1]").text.strip()
                        except:
                            reviewer_id = "NA"

                        try:
                                reviewer_id2 = driver.find_element(By.XPATH,f"(//li[@class='YeINN'])[{rev_idx + 1}]/div[1]/a").get_attribute('href').split('/')[4]
                        except:
                                review_id2 = "NA"

                        try:
                            review_written = driver.find_element(By.XPATH,
                                                                 f"(//li[@class='YeINN'])[{rev_idx + 1}]/div[@class='ZZ4OK IwhtZ']").text.strip()
                        except:
                            review_written = "NA"

                        try:
                            review_selected = driver.find_element(By.XPATH,
                                                                  f"(//li[@class='YeINN'])[{rev_idx + 1}]/div[@class='gyAGI']/span[1]").text.strip()
                        except:
                            review_selected = 'NA'

                        try:
                            no_reviews_sel = driver.find_element(By.XPATH, "//a[@class='P1zUJ ZGKcF']").text.strip()
                            match_no = re.search(r"\+(\d{1})", no_reviews_sel)
                            count = 0
                            if match_no:
                                count = int(match_no.group(1).replace('+', ''))
                                no_reviews_selected = count + 1
                            else:
                                no_reviews_selected = 1
                        except:
                            no_reviews_selected = 'NA'
                        try:
                            # print(review_selected_array)
                            review_selected_string = review_selected
                        except:
                            review_selected_string = 'NA'
                        if review_selected_string == 'NA' or review_selected_string == '':
                            no_reviews_selected = 1
                        pattern = r"\d+\.\d+\."
                        try:
                            try:
                                review_time_str = driver.find_element(By.XPATH,
                                                                      f"(//li[@class='YeINN'])[{rev_idx + 1}]/div[last()-1]/div/div/span/time").text.strip().replace(
                                    '목', '')
                            except:
                                try:
                                    review_time_str = driver.find_element(By.XPATH,
                                                                          f"(//li[@class='YeINN'])[{rev_idx + 1}]/div[last()]/div[last()]/span/time").text.strip().replace(
                                        '목', '')
                                except:
                                    review_time_str = driver.find_element(By.XPATH,
                                                                          f"(//li[@class='YeINN'])[{rev_idx + 1}]/div[last()]/div/div[2]/span[1]/time").text.strip().replace(
                                        '목', '')
                            matches = re.findall(pattern, review_time_str)
                            if matches:
                                review_time = matches[0] + "23"
                            else:
                                pattern2 = r"\d+\.\d+\.\d+\."
                                matches2 = re.findall(pattern2, review_time_str)
                                if matches2:
                                    review_time = matches2[0]
                        except:
                            review_time = "NA"
                        try:
                            nth_visit = driver.find_element(By.XPATH,
                                                            f"(//li[@class='YeINN'])[{rev_idx + 1}]/div[last()-1]/div[last()]/span[2]").text.strip()
                        except:
                            try:
                                nth_visit = driver.find_element(By.XPATH,
                                                                f"(//li[@class='YeINN'])[{rev_idx + 1}]/div[last()]/div[last()]/span[2]").text.strip()

                            except:
                                try:
                                    nth_visit = driver.find_element(By.XPATH,
                                                                    f"(//li[@class='YeINN'])[{rev_idx + 1}]/div[last()]/div/div[2]/span[2]").text.strip()
                                except:
                                    nth_visit = 'NA'

                        try:

                            proof_method = driver.find_element(By.XPATH,
                                                               f"(//li[@class='YeINN'])[{rev_idx + 1}]/div[last()-1]/div[last()]/span[3]").text.strip()

                        except:
                            try:
                                proof_method = driver.find_element(By.XPATH,
                                                                   f"(//li[@class='YeINN'])[{rev_idx + 1}]/div[last()]/div[last()]/span[3]").text.strip()
                            except:
                                try:
                                    proof_method = driver.find_element(By.XPATH,
                                                                       f"(//li[@class='YeINN'])[{rev_idx + 1}]/div[last()]/div/div[2]/span[3]").text.strip()
                                except:
                                    proof_method = "NA"

                        try:

                            rating = driver.find_element(By.XPATH,
                                                         f"(//li[@class='YeINN'])[{rev_idx + 1}]/div[@class='f2MVU']").text.strip().replace(
                                "별점", '').replace("\n", '').replace("점", '')
                        except:
                            try:
                                rating = driver.find_element(By.XPATH,
                                                             f"(//li[@class='YeINN'])[{rev_idx + 1}]/div[@class='f2MVU']").text.strip().replace(
                                    "별점", '').replace("\n", '').replace("점", '')
                            except:
                                rating = 'NA'
                        try:
                            rating_f = float(rating)
                            if rating.count('.') > 0:
                                rating_f = round(rating_f, 1)
                                visit_day = 'NA'
                        except ValueError:
                            try:
                                visit_day = rating
                                rating = 'NA'
                            except:
                                visit_day = "NA"

                        review_id = f"R{review_count}"
                        review_position = rev_idx + 1

                        data = {
                            "Scrapping_time": scrapping_time,
                            "Link": link,
                            "New_Store_ID": store_count,
                            "Store_ID_raw": store_id_values[idx],
                            "Search Query": value,
                            "Store Name": store_name,
                            "Store Rating": store_rating,
                            "Category": category,
                            "Website Store": website_store,
                            "Address": address,       
                            "N_Reviews": n_reviews,
                            "N_Blog_Reviews": n_blog_reviews,
                            "Booking Hub Button Name": booking_hub,
                            "Review_position": review_position,
                            "Review_Type": review_type,
                            "Reviewer_ID": reviewer_id,
                            "Reviewer_ID2": reviewer_id2,
                            "Review_written": review_written,
                            "# Reviews_selected": no_reviews_selected,
                            "Review_selected": review_selected_string,
                            "Review_ID": review_id,
                            "Review_Time": review_time,
                            "Nth_visit": nth_visit,
                            "Proof method": proof_method,
                            "Rating": rating,
                            "Visit_Day": visit_day,
                        }
                        review_count = review_count + 1

                        if not appendProduct(output_file_path, data):
                            # Handle the error or interruption, for example:
                            print("An error occurred while appending data. Process interrupted.")
                            break
                        print(data)

                    try:
                        try:
                            blog_review = driver.find_element(By.XPATH, "//span[.='블로그리뷰']/parent::a").get_attribute(
                                'href')
                            reviewe_type2 = 'Blog Review'
                        except:
                            driver.close()
                            driver.switch_to.window(driver.window_handles[0])
                            continue
                        driver.get(blog_review)
                        time.sleep(1)
                    except:
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        data = {
                            "Scrapping_time": scrapping_time,
                            "Link": link,
                            "New_Store_ID": store_count,
                            "Store_ID_raw": store_id_values[idx],
                            "Search Query": value,
                            "Store Name": store_name,
                            "Store Rating": store_rating,
                            "Category": category,
                            "Website Store": website_store,
                            "Address": address,      
                            "N_Reviews": n_reviews,
                            "N_Blog_Reviews": n_blog_reviews,
                            "Booking Hub Button Name": booking_hub,
                            "Review_position": 'NA',
                            "Review_Type": 'NA',
                            "Reviewer_ID": 'NA',
                            "Reviewer_ID2": 'NA',
                            "Review_written": 'NA',
                            "# Reviews_selected": 'NA',
                            "Review_selected": 'NA',
                            "Review_ID": 'NA',
                            "Review_Time": 'NA',
                            "Nth_visit": 'NA',
                            "Proof method": 'NA',
                            "Rating": 'NA',
                            "Visit_Day": 'NA',
                            "Have_reply": 'NA',
                            "Time_reply": 'NA'
                        }
                        appendProduct(output_file_path, data)
                        print('no blog review')
                        continue
                    try:
                        stop_flag2 = True
                        while stop_flag2:
                            try:
                                 see_more_btn = driver.find_element(By.XPATH, "(//span[.='더보기'])[1]/parent::a").click()

                            #  time.sleep(1)
                            except:
                                stop_flag = False
                                break
                    except:
                        print("no see more blog")
                    try:
                            blog_reviews = []
                            blog_reviews_xp = driver.find_elements(By.XPATH, "//li[@class='pcPAT']")
                            if len(blog_reviews_xp) == 0:
                                try:
                                    blog_reviews_xp = driver.find_elements(By.XPATH, "//li[@class='xg2_q']")
                                    reviewer_id_xp = f"//li[@class='xg2_q'][{blog_idx + 1}]/a/div[@class='Kt2JN']/div[@class='q29yy']/div[@class='XhMTc']"
                                    reviewer_time_str_xp = f"//li[@class='xg2_q'][{blog_idx + 1}]/a/div[@class='kT8X8']/div[@class='FYQ74']/span[1]"
                                    review_written_xp = f"//li[@class='xg2_q'][{blog_idx + 1}]/a/div[@class='kT8X8']/div[@class='hPTBw']/div/span"
                                    proof_method_xp = f"//li[@class='xg2_q'][{blog_idx + 1}]/a/div[@class='kT8X8']/div[@class='FYQ74']/span[2]"
                                except:
                                    blog_reviews_xp = []
                            else:
                                    reviewer_id_xp = f"//li[@class='pcPAT'][{blog_idx + 1}]/a/div[@class='sDBiR']/span[@class='AoB7r']]"
                                    reviewer_time_str_xp = f"//li[@class='pcPAT'][{blog_idx + 1}]/a/div[@class='sDBiR']/span[@class='BB1G2']/time"
                                    review_written_xp = f"//li[@class='pcPAT'][{blog_idx + 1}]/a/div[@class='frxwq']/div[@class='QDJES']/div[@class='Ns0Qo']"
                                    proof_method_xp = f"//li[@class='pcPAT'][{blog_idx + 1}]/a/div[@class='kT8X8']/div[@class='FYQ74']/span[2]"

                                
                            for blog_review_xp in blog_reviews_xp:
                                blog_reviews.append(blog_review_xp)

                            print(str(len(blog_reviews)) + " blog reviews")
                            for blog_idx in range(0, len(blog_reviews)):
                                review_type2 = "Blog Review"
                                try:
                                    reviewer_id = driver.find_element(By.XPATH,
                                                                    reviewer_id_xp).text.strip()
                                except:
                                    reviewer_id = 'NA'

                                try:
                                    review_time_str = driver.find_element(By.XPATH,
                                                                        reviewer_time_str_xp).text.strip()
                                    matches = re.findall(pattern, review_time_str)
                                    if matches:
                                        review_time = matches[0] + "2023"
                                    else:
                                        pattern2 = r"\d+\.\d+\.\d+\."
                                        matches2 = re.findall(pattern2, review_time_str)
                                        if matches2:
                                            review_time = matches2[0]
                                except:
                                    review_time = 'NA'

                                try:
                                    review_written = driver.find_element(By.XPATH,
                                                                        review_written_xp).text.strip()
                                except:
                                    review_written = 'NA'
                                try:
                                    proof_method = driver.find_element(By.XPATH,
                                                                    proof_method_xp).text.strip()
                                except:
                                    proof_method = 'NA'
                            review_id = f"B{review_count}"
                            blog_review_pos = blog_idx + 1
                            data = {
                                "Scrapping_time": scrapping_time,
                                "Link": link,
                                "New_Store_ID": store_count,
                                "Store_ID_raw": store_id_values[idx],
                                "Search Query": value,
                                "Store Name": store_name,
                                "Store Rating": store_rating,
                                "Category": category,
                                "Website Store": website_store,
                                "Address": address,                             
                                "N_Reviews": n_reviews,
                                "N_Blog_Reviews": n_blog_reviews,
                                "Booking Hub Button Name": booking_hub,
                                "Review_position": blog_review_pos,
                                "Review_Type": review_type2,
                                "Reviewer_ID": reviewer_id,
                                "Reviewer_ID2": reviewer_id2,
                                "Review_written": review_written,
                                "# Reviews_selected": "NA",
                                "Review_selected": "NA",
                                "Review_ID": review_id,
                                "Review_Time": review_time,
                                "Nth_visit": "NA",
                                "Proof method": proof_method,
                                "Rating": rating,
                                "Visit_Day": 'NA',
                            }
                            print(data)
                            review_count = review_count + 1

                            if not appendProduct(output_file_path, data):
                                # Handle the error or interruption, for example:
                                print("An error occurred while appending data. Process interrupted.")
                                break
                            print(data)


                    except Exception as e:
                        print(repr(e))

    
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])

                    store_count = store_count + 1

                    driver.switch_to.default_content()
                    WebDriverWait(driver, 10).until(
                        EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe#searchIframe")))
                    next_flag = False   

                except:
                    # driver.close()
                    # driver.switch_to.window(driver.window_handles[0])
                    data = {
                        "Scrapping_time": scrapping_time,
                        "Link": link,
                        "New_Store_ID": store_count,
                        "Store_ID_raw": store_id_values[idx],
                        "Search Query": value,
                        "Store Name": store_name,
                        "Store Rating": store_rating,
                        "Category": category,
                        "Website Store": website_store,
                        "Address": address,
                        "N_Reviews": n_reviews,
                        "N_Blog_Reviews": n_blog_reviews,
                        "Booking Hub Button Name": booking_hub,
                        "Review_position": 'NA',
                        "Review_Type": 'NA',
                        "Reviewer_ID": 'NA',
                        "Reviewer_ID2": 'NA',
                        "Review_written": 'NA',
                        "# Reviews_selected": 'NA',
                        "Review_selected": 'NA',
                        "Review_ID": 'NA',
                        "Review_Time": 'NA',
                        "Nth_visit": 'NA',
                        "Proof method": 'NA',
                        "Rating": 'NA',
                        "Visit_Day": 'NA',
                        "Have_reply": 'NA',
                        "Time_reply": 'NA'
                    }
                    appendProduct(output_file_path, data)
                    print('no visitor review')
                    continue
            #multiple stores
            else:
                stores = []
                for store_css in stores_css:
                    stores.append(store_css)
                for store_idx in range(0, len(stores)):
                    try:
                        if len(driver.window_handles) >= 3:
                            try:
                                driver.switch_to.window(driver.window_handles[2])    
                                driver.close()
                            except:
                                pass
                            try:
                                driver.switch_to.window(driver.window_handles[1])
                                driver.close()
                            except:
                                pass
                            driver.switch_to.window(driver.window_handles[0])
                    except:
                        pass
                    print("here 3")
                    try:
                        stores[store_idx].click()
                        time.sleep(4)
                        stores[store_idx].click()
                    except:
                        continue
                    time.sleep(2)
                    
                    try:
                        driver.switch_to.default_content()
                        WebDriverWait(driver, 10).until(
                        EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe#entryIframe")))
                    except TimeoutException:
                        continue
                    try:
                        driver.find_element(By.XPATH,"//span[contains(text(),'홈')]/parent::a").click()  
                    except:
                        try:
                            driver.find_element(By.XPATH,"//span[contains(text(),'메뉴')]/parent::a").click()
                            time.sleep(0.2)
                            driver.find_element(By.XPATH,"//span[contains(text(),'홈')]/parent::a").click()
                        except:
                            pass
                    time.sleep(0.5)    
                    now = datetime.now()
                    scrapping_time = now.strftime("%d/%m/%Y-%H:%M:%S")
                    try:
                        store_name = driver.find_element(By.CSS_SELECTOR, "span.Fc1rA").text
                    except:
                        store_name = "NA"
                    try:
                        store_rating = driver.find_element(By.XPATH,"//div[@id='_title']/following-sibling::div/span[@class='PXMot LXIwF']").text.replace("별점",'').replace('\n','')
                    except:
                        store_rating = "NA"      
                    try:
                        category = driver.find_element(By.CSS_SELECTOR, "span.DJJvD").text
                    except:
                        category = "NA"
                    try:
                        link = driver.current_url
                    except:
                        link = 'NA'
                        print("no link")

                    try:
                        address = driver.find_element(By.CSS_SELECTOR, "span.LDgIH").text
                    except:
                        address = "NA"
                    try:
                        n_reviews = driver.find_element(By.XPATH, "//a[contains(text(),'방문자리뷰')]").text.replace('방문자리뷰','')
                    except:
                        n_reviews = "0"
                    try:
                        n_blog_reviews = driver.find_element(By.XPATH, "//a[contains(text(),'블로그리뷰')]").text.replace('블로그리뷰','')
                    except:
                        n_blog_reviews = "0"
                    try:
                        booking_hub = driver.find_element(By.XPATH,
                                                        "//span[contains(text(),'편의')]/parent::strong/following-sibling::div").text
                    except:
                        booking_hub = "NA"
                    try:
                        website_store = driver.find_element(By.CSS_SELECTOR, "a.place_bluelink.CHmqa").text.strip()
                    except:
                        website_store = 'NA'
                    review_type = ""

                    try:
                        try:
                            visitor_review = driver.find_element(By.XPATH, "//span[.='리뷰']/parent::a").get_attribute('href')
                        except:
                            driver.switch_to.default_content()
                            WebDriverWait(driver, 10).until(
                                EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe#searchIframe")))
                            continue
                        driver.execute_script("window.open('');")
                        driver.switch_to.window(driver.window_handles[1])
                        driver.get(visitor_review)
                        time.sleep(2)
                        review_type = "Visitor Review"
                        try:
                            check_skip = driver.find_element(By.XPATH,"//h2[text()='리뷰']/span[@class='place_section_count']")
                        except:
                            driver.close()
                            driver.switch_to.window(driver.window_handles[0])
                            store_count = store_count + 1
                            driver.switch_to.default_content()
                            WebDriverWait(driver, 10).until(
                                EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe#searchIframe")))
                            continue
                        
                        try:
                            stop_flag = True
                            try:
                                total_reviews = int(n_reviews.strip().replace(',',''))
                            except:
                                total_reviews = 0
                            if total_reviews >= 9000:
                                print("inside 9000")
                                logging.info("inside 9000")
                                for count_review in range(0,900):
                                    try:
                                        see_more_btn = driver.find_element(By.XPATH, "(//span[.='더보기'])[2]/parent::a").click()
                                        time.sleep(0.5)
                                    except:
                                        stop_flag = False
                                        break

                            else:
                                while stop_flag:
                                    try:
                                        see_more_btn = driver.find_element(By.XPATH, "(//span[.='더보기'])[2]/parent::a").click()
                                        time.sleep(0.5)
                                    except:
                                        stop_flag = False
                                        break

                                time.sleep(1)                                
                                new_review_button2 = driver.find_element(By.CSS_SELECTOR,"a.I8cuq")
                                new_review_button2.click()                               
            
                                time.sleep(1)

                                stop_flag = True
                                while stop_flag:
                                    try:
                                        see_more_btn = driver.find_element(By.XPATH, "(//span[.='더보기'])[2]/parent::a").click()
                                        time.sleep(0.5)
                                    except:
                                        stop_flag = False
                                        break
                        except:
                            print("no see more button")

                        list_reviews = []
                        time.sleep(1)
                        list_reviews_xp = driver.find_elements(By.XPATH, "//li[@class='YeINN']")
                        for list_review_xp in list_reviews_xp:
                            list_reviews.append(list_review_xp)
                        print(len(list_reviews))
                        try:
                            n_reviews = driver.find_element(By.XPATH, "//a[contains(text(),'방문자리뷰')]").text.replace('방문자리뷰','')
                        except:
                            n_reviews = "0"
                        time.sleep(1)
                        for rev_idx in range(0, len(list_reviews)):
                           
                            try:
                                reviewer_id = driver.find_element(By.XPATH,
                                                                f"(//li[@class='YeINN'])[{rev_idx + 1}]/div/a[2]/div[1]").text.strip()
                            except:
                                reviewer_id = "NA"

                            try:
                                reviewer_id2 = driver.find_element(By.XPATH,f"(//li[@class='YeINN'])[{rev_idx + 1}]/div[1]/a").get_attribute('href').split('/')[4]
                            except:
                                reviewer_id2 = "NA"
                            
                            try:
                                review_written = driver.find_element(By.XPATH,
                                                                    f"(//li[@class='YeINN'])[{rev_idx + 1}]/div[@class='ZZ4OK IwhtZ']").text.strip()
                            except:
                                review_written = "NA"

                            try:
                                review_selected = driver.find_element(By.XPATH,
                                                                    f"(//li[@class='YeINN'])[{rev_idx + 1}]/div[@class='gyAGI']/span[1]").text.strip()
                            except:
                                review_selected = 'NA'

                            try:
                                no_reviews_sel = driver.find_element(By.XPATH, "//a[@class='P1zUJ ZGKcF']").text.strip()
                                match_no = re.search(r"\+(\d{1})", no_reviews_sel)
                                count = 0
                                if match_no:
                                    count = int(match_no.group(1).replace('+', ''))
                                    no_reviews_selected = count + 1
                                else:
                                    no_reviews_selected = 1
                            except:
                                no_reviews_selected = 'NA'
                            try:
                                # print(review_selected_array)
                                review_selected_string = review_selected
                            except:
                                review_selected_string = 'NA'
                            if review_selected_string == 'NA' or review_selected_string == '':
                                no_reviews_selected = 1
                            pattern = r"\d+\.\d+\."
                            try:
                                try:
                                    review_time_str = driver.find_element(By.XPATH,
                                                                        f"(//li[@class='YeINN'])[{rev_idx + 1}]/div[last()-1]/div/div/span/time").text.strip().replace(
                                        '목', '')
                                except:
                                    try:
                                        review_time_str = driver.find_element(By.XPATH,
                                                                            f"(//li[@class='YeINN'])[{rev_idx + 1}]/div[last()]/div[last()]/span/time").text.strip().replace(
                                            '목', '')
                                    except:
                                        review_time_str = driver.find_element(By.XPATH,
                                                                            f"(//li[@class='YeINN'])[{rev_idx + 1}]/div[last()]/div/div[2]/span[1]/time").text.strip().replace(
                                            '목', '')
                                matches = re.findall(pattern, review_time_str)
                                if matches:
                                    review_time = matches[0] + "23"
                                else:
                                    pattern2 = r"\d+\.\d+\.\d+\."
                                    matches2 = re.findall(pattern2, review_time_str)
                                    if matches2:
                                        review_time = matches2[0]
                            except:
                                review_time = "NA"

                            try:
                                nth_visit = driver.find_element(By.XPATH,
                                                                f"(//li[@class='YeINN'])[{rev_idx + 1}]/div[last()-1]/div[last()]/span[2]").text.strip()
                            except:
                                try:
                                    nth_visit = driver.find_element(By.XPATH,
                                                                    f"(//li[@class='YeINN'])[{rev_idx + 1}]/div[last()]/div[last()]/span[2]").text.strip()

                                except:
                                    try:
                                        nth_visit = driver.find_element(By.XPATH,
                                                                        f"(//li[@class='YeINN'])[{rev_idx + 1}]/div[last()]/div/div[2]/span[2]").text.strip()
                                    except:
                                        nth_visit = 'NA'

                            try:
                                proof_method = driver.find_element(By.XPATH,
                                                                f"(//li[@class='YeINN'])[{rev_idx + 1}]/div[last()-1]/div[last()]/span[3]").text.strip()

                            except:
                                try:
                                    proof_method = driver.find_element(By.XPATH,
                                                                    f"(//li[@class='YeINN'])[{rev_idx + 1}]/div[last()]/div[last()]/span[3]").text.strip()
                                except:
                                    try:
                                        proof_method = driver.find_element(By.XPATH,
                                                                        f"(//li[@class='YeINN'])[{rev_idx + 1}]/div[last()]/div/div[2]/span[3]").text.strip()
                                    except:
                                        proof_method = "NA"

                            try:

                                rating = driver.find_element(By.XPATH,
                                                            f"(//li[@class='YeINN'])[{rev_idx + 1}]/div[@class='f2MVU']").text.strip().replace(
                                    "별점", '').replace("\n", '').replace("점", '')
                            except:
                                try:
                                    rating = driver.find_element(By.XPATH,
                                                                f"(//li[@class='YeINN'])[{rev_idx + 1}]/div[@class='f2MVU']").text.strip().replace(
                                        "별점", '').replace("\n", '').replace("점", '')
                                except:
                                    rating = 'NA'
                            try:
                                rating_f = float(rating)
                                if rating.count('.') > 0:
                                    rating_f = round(rating_f, 1)
                                    visit_day = 'NA'
                            except ValueError:
                                try:
                                    visit_day = rating
                                    rating = 'NA'
                                except:
                                    visit_day = "NA"

                            review_id = f"R{review_count}"
                            review_position = rev_idx + 1

                            data = {
                                "Scrapping_time": scrapping_time,
                                "Link": link,
                                "New_Store_ID": store_count,
                                "Store_ID_raw": store_id_values[idx],
                                "Search Query": value,
                                "Store Name": store_name,
                                "Store Rating": store_rating,
                                "Category": category,
                                "Website Store": website_store,
                                "Address": address,
                                "N_Reviews": n_reviews,
                                "N_Blog_Reviews": n_blog_reviews,
                                "Booking Hub Button Name": booking_hub,                               
                                "Review_position": review_position,
                                "Review_Type": review_type,
                                "Reviewer_ID": reviewer_id,
                                "Reviewer_ID2": reviewer_id2,
                                "Review_written": review_written,
                                "# Reviews_selected": no_reviews_selected,
                                "Review_selected": review_selected_string,
                                "Review_ID": review_id,
                                "Review_Time": review_time,
                                "Nth_visit": nth_visit,
                                "Proof method": proof_method,
                                "Rating": rating,
                                "Visit_Day": visit_day,
                            }
                            review_count = review_count + 1

                            if not appendProduct(output_file_path, data):
                                # Handle the error or interruption, for example:
                                print("An error occurred while appending data. Process interrupted.")
                                break
                            print(data)                        

                        try:
                            try:
                                blog_review = driver.find_element(By.XPATH, "//span[.='블로그리뷰']/parent::a").get_attribute(
                                    'href')
                                reviewe_type2 = 'Blog Review'
                            except:
                                driver.close()
                                driver.switch_to.window(driver.window_handles[0])                                
                                store_count = store_count + 1

                                driver.switch_to.default_content()
                                WebDriverWait(driver, 10).until(
                                    EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe#searchIframe")))
                                continue
                            driver.get(blog_review)
                            time.sleep(1)
                        except:
                            # driver.close()
                            driver.switch_to.window(driver.window_handles[0])
                            data = {
                                "Scrapping_time": scrapping_time,
                                "Link": link,
                                "New_Store_ID": store_count,
                                "Store_ID_raw": store_id_values[idx],
                                "Search Query": value,
                                "Store Name": store_name,
                                "Store Rating": store_rating,
                                "Category": category,
                                "Website Store": website_store,
                                "Address": address,
                                "N_Reviews": n_reviews,
                                "N_Blog_Reviews": n_blog_reviews,
                                "Booking Hub Button Name": booking_hub,                               
                                "Review_position": 'NA',
                                "Review_Type": 'NA',
                                "Reviewer_ID": 'NA',
                                "Reviewer_ID2": 'NA',
                                "Review_written": 'NA',
                                "# Reviews_selected": 'NA',
                                "Review_selected": 'NA',
                                "Review_ID": 'NA',
                                "Review_Time": 'NA',
                                "Nth_visit": 'NA',
                                "Proof method": 'NA',
                                "Rating": 'NA',
                                "Visit_Day": 'NA',
                                "Have_reply": 'NA',
                                "Time_reply": 'NA'
                            }
                            appendProduct(output_file_path, data)
                            print('no blog review')
                            continue
                        try:
                            stop_flag2 = True
                            while stop_flag2:
                                try:
                                    see_more_btn = driver.find_element(By.XPATH, "(//span[.='더보기'])[1]/parent::a").click()

                                #  time.sleep(1)
                                except:
                                    stop_flag = False
                                    break
                        except:
                            print("no see more blog")
                        try:
                            blog_reviews = []
                            blog_reviews_xp = driver.find_elements(By.XPATH, "//li[@class='pcPAT']")
                            blog_check_flag = False
                            if len(blog_reviews_xp) == 0:
                                try:
                                    blog_reviews_xp = driver.find_elements(By.XPATH, "//li[@class='xg2_q']")
                                    blog_check_flag = True

                                except:
                                    blog_reviews_xp = []
                            else:
                                    blog_check_flag = False
                                
                            for blog_review_xp in blog_reviews_xp:
                                blog_reviews.append(blog_review_xp)

                            print(str(len(blog_reviews)) + " blog reviews")
                            try:
                                n_blog_reviews = driver.find_element(By.XPATH, "//a[contains(text(),'블로그리뷰')]").text.replace('블로그리뷰','')
                            except:
                                n_blog_reviews = "0"
                            for blog_idx in range(0, len(blog_reviews)):
                                if blog_check_flag == True:
                                    reviewer_id_xp = f"//li[@class='xg2_q'][{blog_idx + 1}]/a/div[@class='Kt2JN']/div[@class='q29yy']/div[@class='XhMTc']"
                                    reviewer_time_str_xp = f"//li[@class='xg2_q'][{blog_idx + 1}]/a/div[@class='kT8X8']/div[@class='FYQ74']/span[1]"
                                    review_written_xp = f"//li[@class='xg2_q'][{blog_idx + 1}]/a/div[@class='kT8X8']/div[@class='hPTBw']/div/span"
                                    proof_method_xp = f"//li[@class='xg2_q'][{blog_idx + 1}]/a/div[@class='kT8X8']/div[@class='FYQ74']/span[2]" 
                                else:
                                    reviewer_id_xp = f"//li[@class='pcPAT'][{blog_idx + 1}]/a/div[@class='sDBiR']/span[@class='AoB7r']]"
                                    reviewer_time_str_xp = f"//li[@class='pcPAT'][{blog_idx + 1}]/a/div[@class='sDBiR']/span[@class='BB1G2']/time"
                                    review_written_xp = f"//li[@class='pcPAT'][{blog_idx + 1}]/a/div[@class='frxwq']/div[@class='QDJES']/div[@class='Ns0Qo']"
                                    proof_method_xp = f"//li[@class='pcPAT'][{blog_idx + 1}]/a/div[@class='kT8X8']/div[@class='FYQ74']/span[2]"
                                review_type2 = "Blog Review"
                                try:
                                    reviewer_id = driver.find_element(By.XPATH,
                                                                    reviewer_id_xp).text.strip()
                                except:
                                    reviewer_id = 'NA'

                                try:
                                    review_time_str = driver.find_element(By.XPATH,
                                                                        reviewer_time_str_xp).text.strip()
                                    matches = re.findall(pattern, review_time_str)
                                    if matches:
                                        review_time = matches[0] + "2023"
                                    else:
                                        pattern2 = r"\d+\.\d+\.\d+\."
                                        matches2 = re.findall(pattern2, review_time_str)
                                        if matches2:
                                            review_time = matches2[0]
                                except:
                                    review_time = 'NA'

                                try:
                                    review_written = driver.find_element(By.XPATH,
                                                                        review_written_xp).text.strip()
                                except:
                                    review_written = 'NA'
                                try:
                                    proof_method = driver.find_element(By.XPATH,
                                                                    proof_method_xp).text.strip()
                                except:
                                    proof_method = 'NA'
                        
                                review_id = f"B{review_count}"
                                blog_review_pos = blog_idx + 1
                                data = {
                                    "Scrapping_time": scrapping_time,
                                    "Link": link,
                                    "New_Store_ID": store_count,
                                    "Store_ID_raw": store_id_values[idx],
                                    "Search Query": value,
                                    "Store Name": store_name,
                                    "Store Rating": store_rating,
                                    "Category": category,
                                    "Website Store": website_store,
                                    "Address": address,                                    
                                    "N_Reviews": n_reviews,
                                    "N_Blog_Reviews": n_blog_reviews,
                                    "Booking Hub Button Name": booking_hub,                                    
                                    "Review_position": blog_review_pos,
                                    "Review_Type": review_type2,
                                    "Reviewer_ID": reviewer_id,
                                    "Reviewer_ID2": reviewer_id2,                                    
                                    "Review_written": review_written,
                                    "# Reviews_selected": "NA",
                                    "Review_selected": "NA",
                                    "Review_ID": review_id,
                                    "Review_Time": review_time,
                                    "Nth_visit": "NA",
                                    "Proof method": proof_method,
                                    "Rating": rating,
                                    "Visit_Day": 'NA',                                    
                                }
                                print(data)
                                review_count = review_count + 1

                                if not appendProduct(output_file_path, data):
                                    # Handle the error or interruption, for example:
                                    print("An error occurred while appending data. Process interrupted.")
                                    break
                                print(data)


                        except Exception as e:
                            print(repr(e))

        
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])

                        store_count = store_count + 1

                        driver.switch_to.default_content()
                        WebDriverWait(driver, 10).until(
                            EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe#searchIframe")))
                        # next_flag = False   

                    except:
                        # driver.close()
                        # driver.switch_to.window(driver.window_handles[0])
                        data = {
                            "Scrapping_time": scrapping_time,
                            "Link": link,
                            "New_Store_ID": store_count,
                            "Store_ID_raw": store_id_values[idx],
                            "Search Query": value,
                            "Store Name": store_name,
                            "Store Rating": store_rating,
                            "Category": category,
                            "Website Store": website_store,
                            "Address": address,                           
                            "N_Reviews": n_reviews,
                            "N_Blog_Reviews": n_blog_reviews,
                            "Booking Hub Button Name": booking_hub,                            
                            "Review_position": 'NA',
                            "Review_Type": 'NA',
                            "Reviewer_ID": 'NA',
                            "Reviewer_ID2": 'NA',                            
                            "Review_written": 'NA',
                            "# Reviews_selected": 'NA',
                            "Review_selected": 'NA',
                            "Review_ID": 'NA',
                            "Review_Time": 'NA',
                            "Nth_visit": 'NA',
                            "Proof method": 'NA',
                            "Rating": 'NA',
                            "Visit_Day": 'NA',
                            "Have_reply": 'NA',
                            "Time_reply": 'NA'
                        }
                        appendProduct(output_file_path, data)
                        print('no visitor review')
                        continue

                


            try:
                next_btn = driver.find_element(By.XPATH,"//span[contains(text(),'다음페이지')]/parent::a[@aria-disabled='false']")
                next_btn.click()
            except:
                next_flag = False
                break