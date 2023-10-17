from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import os
import wget
import base64

driver = webdriver.Chrome()
driver.get("https://www.google.com/imghp?hl=jp")

search = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, 'q'))
)
# 搜尋 dog 並按下Enter
keyword = "dog"
search.send_keys(keyword)
search.send_keys(Keys.RETURN)
# 等到第一個Class出現後執行接下來動作
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "rg_i.Q4LuWd"))
)
# 頁面移動到最下方(當要下載更多圖片時使用)
# for i in range(2):
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(5)

# 取得網頁上的class_name是rg_i.Q4LuWd的元素(即圖片共通的class_name)
imgs = driver.find_elements(By.CLASS_NAME, "rg_i.Q4LuWd")

# 在目前路徑建立一個資料夾
path = os.path.join(keyword)
os.mkdir(path)

count = 0
for img in imgs:
    # 取得img的src這個元素(即下載位置)
    img_url = img.get_attribute("src")
    if img_url is not None:
        # 因為Chrom有些圖片是二進制資料，所以要透過以下方式轉換
        if img_url[0:4] == 'data':
            data = img_url.split(",", 1)[1]
            binary_data  = base64.b64decode(data)
            save_as = os.path.join(path, keyword + str(count) + '.jpg')
            with open(save_as, "wb") as f:
                f.write(binary_data)
            count += 1
        else:
            save_as = os.path.join(path, keyword + str(count) + '.jpg')
            # 下載到save_as位置
            wget.download(img.get_attribute("src"), save_as)
            count += 1

# time.sleep(5)