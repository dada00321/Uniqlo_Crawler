'''
# 資料綱目
1. product_name: 商品名稱 (受眾: [消費者,服飾業者])\ni.e. 商品標題)
2. product_price_NTD: 商品價格 (受眾: [消費者], 功能: 即時比價)
3. product_link: 商品連結 (受眾: [服飾業者], 功能: 導入流量、介紹給更多人認識)
4. product_image: 商品圖片 (受眾: [消費者], 有臉 or 無臉)
------------
5. [專業屬性-1] 色彩設計 相關屬性 (colour attrs)
6. [專業屬性-2] 服飾設計 相關屬性 (jargons)
7. [專業屬性-3] 紡織材質 相關屬性 (jargons)
------------
> 爬蟲只需針對基礎屬性即可, 能滿足大部份消費者及服飾業者的需求
> 專業屬性則需要 domain knowledge, dive in the deeper studies

# 滑鼠游標放置於網頁元素中間
Python 網路爬蟲與資料視覺化 > 7-27 & 7-28

# 從網路上下載圖檔
Python 網路爬蟲與資料視覺化 > 5-28

# 反反爬蟲 > 設定 Request Headers
https://www.learncodewithmike.com/2020/09/7-tips-to-avoid-getting-blocked-while-scraping.html
```
import requests
 
 
headers = {
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
	"Accept-Encoding": "gzip, deflate, br", 
	"Accept-Language": "zh-TW,zh;q=0.9", 
	"Host": "example.com",  #目標網站 
	"Sec-Fetch-Dest": "document", 
	"Sec-Fetch-Mode": "navigate", 
	"Sec-Fetch-Site": "none", 
	"Upgrade-Insecure-Requests": "1", 
	"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36" #使用者代理
}
 
response = requests.get(url="https://example.com", headers=headers)
```

# 反反爬蟲 > 設定 User-Agent
https://www.learncodewithmike.com/2020/09/7-tips-to-avoid-getting-blocked-while-scraping.html
```
import requests
from fake_useragent import UserAgent
 
 
user_agent = UserAgent()
response = requests.get(url="https://example.com", headers={ 'user-agent': user_agent.random })
```

# 反反爬蟲 > 取消網頁中的彈出視窗
from selenium.webdriver.chrome.options import Options
import time
 
options = Options()
options.add_argument("--disable-notifications")

# 反反爬蟲 > 設定 Options
https://zhuanlan.zhihu.com/p/60852696

```
from selenium import webdriver
option = webdriver.ChromeOptions()

# 設定 user-agent
options.add_argument("user-agent=Your_Custom_User_Agent_String")

# 添加UA
options.add_argument('user-agent="MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"')

# 指定浏览器分辨率
options.add_argument('window-size=1920x3000') 

# 谷歌文档提到需要加上这个属性来规避bug
chrome_options.add_argument('--disable-gpu') 

 # 隐藏滚动条, 应对一些特殊页面
options.add_argument('--hide-scrollbars')

# 不加载图片, 提升速度
options.add_argument('blink-settings=imagesEnabled=false') 

# 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
options.add_argument('--headless') 

# 以最高权限运行
options.add_argument('--no-sandbox')

# 手动指定使用的浏览器位置
options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" 

#添加crx插件
option.add_extension('d:\crx\AdBlock_v2.17.crx') 

# 禁用JavaScript
option.add_argument("--disable-javascript") 

# 设置开发者模式启动，该模式下webdriver属性为正常值
options.add_experimental_option('excludeSwitches', ['enable-automation']) 

# 禁用浏览器弹窗
prefs = {  
	'profile.default_content_setting_values' :  {  
		'notifications' : 2  
	 }  
}  
options.add_experimental_option('prefs',prefs)


driver=webdriver.Chrome(chrome_options=chrome_options)
```

# CSS Selector
1. 選取包含特定字串的 <div>
div:contains('特定字串')

2. 選取 <div class="test"> 的下一個 <div>
div.test + div
'''

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains 
from datetime import datetime 
import pandas as pd
import os
from random import randint
import requests
# =============================================================================
# Common functions for GU's web pages
# =============================================================================
def create_save_dirs():
	os.makedirs("csv", exist_ok=True)
	
def get_timestamp():
	e = datetime.today()
	return f"{e.year:02d}-{e.month:02d}-{e.day:02d}_{e.hour:02d}-{e.minute:02d}-{e.second:02d}"

def get_schema(data_name):
	if data_name == "menu":
		return ["timestamp", "brand_id", "brand", "customer_type_id", "customer_type", "big_category_id", "big_category_type", "sales_category_id", "sales_category_type", "sales_category_link"]
	elif data_name == "spu":
		return ["timestamp", "brand_id", "sales_category_id", "spu_id", "spu_raw_name", "spu_name", "spu_link", "spu_price"]
	elif data_name == "sku":
		return ["timestamp", "spu_id", "sku_id", "sku_img_link", "outfit_id", "outfit_img_link", "colour_chip_id", "colour_chip_name", "colour_chip_link"]
	elif data_name == "img":
		return ["timestamp", "sku_id", "outfit_id", "sku_img_path", "outfit_img_path", "colour_chip_path"]

def get_UNIQLO_driver():
	chromedriver_autoinstaller.install()
	chromedriver_path = "C:/Users/USER/.conda/envs/tf/lib/site-packages/chromedriver_autoinstaller/120/chromedriver.exe"
	# C:\\Users\\USER\\.conda\\envs\\tf\\lib\\site-packages\\chromedriver_autoinstaller\\120\\chromedriver.exe 
	
	service = Service(executable_path=chromedriver_path)
	
	#options = webdriver.ChromeOptions()
	options = Options()
	
	# 不載入圖片，提升速度
	#options.add_argument('blink-settings=imagesEnabled=false')
	
	# 以最高權限執行
	options.add_argument('--no-sandbox')
	
	# 設定 ua
	#my_ua = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36"
	#my_ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
	#options.add_argument(f"user-agent={my_ua}")
	
	#options.add_argument('--headless')
	#options.add_argument('--headless')
	#options.add_argument('--no-sandbox')
	#options.add_argument('--disable-dev-shm-usage')
	#options.add_argument("--disable-notifications")
	
	driver = webdriver.Chrome(service=service, options=options)
	return driver

def visit_link(driver, link, is_scroll=True):
	driver.maximize_window()
	
	driver.get(link)
	
	driver.implicitly_wait(20)
	
	# 分 n 次: 捲動 scroll bar 至頁面底部
	## 計算每次捲動的距離
	if is_scroll:
		n = 10
		## 開始執行 n 次捲動
		for _ in range(n):
			#if is_scroll:
			scroll_height = driver.execute_script("return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")
			scroll_distance = scroll_height / n
			js = f"window.scrollTo(0, {scroll_distance} + window.scrollY);"
			driver.execute_script(js) # 捲動至目前位置加上捲動距離
			sleep(1 + randint(0,10)/10) # 每次捲動完，稍等 1 ~ 2 秒（讓圖片載入）
	for t in range(20, 0, -1):
		print(f"[INFO] 自行捲動到頁面下方，倒數 {t} 秒\n")
		
# =============================================================================
# Stage-1. Crawl: Menu ("product links", or "links of sales-categories")
# =============================================================================
def crawl_menu(brand, home_page_link):
	menu_path = f"csv/{brand}_menu.csv"
	
	if os.path.exists(menu_path):
		print(f"[INFO] 已蒐集 {brand} 的 menu\n")
	else:
		print(f"[INFO] 開始爬蟲 {brand} 的 menu\n")
		columns = get_schema("menu")
		brand_id = 1
		tmp_dict_menu = {k: list() for k in columns}
		
		customer_type_ids__num_of_big_cats = {1: 10, 2: 9, 3: 10, 4: 4} # 需手動更新 (依據網站內容)
		big_cat_ids_cannot_expand = [9, 10, 18, 19, 28, 29]
		big_category_id = 1
		sales_category_id = 1
		customer_type_ids__customer_types = dict(sorted({1: "women", 2: "men", 3: "kids", 4: "babies"}.items(), key=lambda x:x[0]))
		
		driver = get_UNIQLO_driver()
		for customer_type_id, customer_type in customer_type_ids__customer_types.items(): # 客群 (women, men, kids & babies)
			if customer_type_id == 1: 
				big_category_id = 10
				continue
			
			#driver = get_UNIQLO_driver()
			visit_link(driver, home_page_link, False)
			
			# 滑鼠游標放置於 [菜單標題文字] (客群) 的中間
			menu = driver.find_element("xpath", f"//li[@data-category='PC_HMenu'][{customer_type_id}]")
			ActionChains(driver).move_to_element(menu).perform()
			print(f"customer_type: {customer_type}")
			sleep(1)
			
			# 粗分類標籤
			#soup = BeautifulSoup(driver.page_source, "lxml")
			#soup.select("div.gender-left div.col1 a")
			big_categories = driver.find_elements("css selector", "div.gender-left div.col1 a")
			#print(f"[INFO] 找到 {len(big_categories)} 個粗分類標籤\n")
			
			for exec_num in range(customer_type_ids__num_of_big_cats[customer_type_id]):
				if big_category_id in big_cat_ids_cannot_expand:
					big_category_id += 1
					continue
				big_category = big_categories[big_category_id - 1] # 定位 [粗分類] 的網頁元素
				big_category_type = big_category.text # 取出 [粗分類] 文字
				print(f"  ({big_category_id}) big_category: {big_category_type}")
				big_category.click() # 按一下，展開 [銷售分類]
				
				# 銷售分類標籤
				sales_categories = driver.find_elements("xpath", "//ul[@class='active']/li/a")
				
				for sales_category in sales_categories:
					sales_category_type = sales_category.text
					if sales_category_type == "": # 位於尚未展開的其它粗分類底下
						continue
					else:
						sales_category_link = sales_category.get_attribute("href")
						print(f"	sales_category_link: {sales_category_link}")
						print(f"	sales_category_type: {sales_category_type}")
						
						tmp_dict_menu["timestamp"].append(get_timestamp())
						tmp_dict_menu["brand_id"].append(brand_id)
						tmp_dict_menu["brand"].append(brand)
						tmp_dict_menu["customer_type_id"].append(customer_type_id)
						tmp_dict_menu["customer_type"].append(customer_type)
						tmp_dict_menu["big_category_id"].append(big_category_id)
						tmp_dict_menu["big_category_type"].append(big_category_type)
						tmp_dict_menu["sales_category_id"].append(sales_category_id)
						tmp_dict_menu["sales_category_type"].append(sales_category_type)
						tmp_dict_menu["sales_category_link"].append(sales_category_link)
						sleep(1)
						sales_category_id += 1
				big_category_id += 1
		driver.quit()
		#break

		df = pd.DataFrame.from_dict(tmp_dict_menu)
		df.to_csv(menu_path, index=False, encoding="utf-8-sig")

	return menu_path

# =============================================================================
# Stage-2. Crawl: Basic Attributes
# =============================================================================
def crawl_basic_attributes_multiSalesCategories(brand, menu_path):
	# [test] 
	#link = "https://www.uniqlo.com/tw/zh_TW/women_outer_down.html"

	# =============================================================================
	basic_attr_path = f"csv/{brand}_basic_attr.csv"
	if os.path.exists(basic_attr_path):
		print(f"[INFO] 已蒐集 {brand} 的 基本商品屬性\n")
	else:
		tmp_dir = f"csv/tmp__{brand}_basic_attr"
		os.makedirs(tmp_dir, exist_ok=True)
		print(f"[INFO] 開始爬蟲 {brand} 的 基本商品屬性\n")
		columns = get_schema("spu")
		
		df_menu = pd.read_csv(menu_path)
		#df_menu = pd.read_csv(menu_path)
		
		exec_sales_category_ids = []
		for i, row in df_menu.iterrows():
			#if i == 1: break 
			sales_category_type = row["sales_category_type"]
			sales_category_id = row["sales_category_id"]
			exec_sales_category_ids.append(sales_category_id)
			
			dst_tmp_path = f"{tmp_dir}/{sales_category_id}.csv"
			if not os.path.exists(dst_tmp_path):
				tmp_dict_spu = {k: list() for k in columns}
			
				sales_category_link = row["sales_category_link"]
				sales_category_type = row["sales_category_type"]
				print(f'[INFO] Crawling sales categoty: {row["sales_category_type"]}\nlink:\n{sales_category_link}\n')
				spu_links_multiPages, product_raw_names_multiPages, spu_names_multiPages, spu_prices_multiPages = __crawl_basic_attributes(sales_category_link, sales_category_type) 
				
				# [TEST] Check if crawled values have the same length
				len_pages, len_names, len_prices = len(spu_links_multiPages), len(spu_names_multiPages), len(spu_prices_multiPages)
				
				if len_pages == len_names ==  len_prices:
					for tmp_spu_index in range(len(spu_links_multiPages)):
						tmp_dict_spu["timestamp"].append(get_timestamp())
						brand_id = row["brand_id"]
						tmp_dict_spu["brand_id"].append(brand_id)
						tmp_dict_spu["sales_category_id"].append(sales_category_id)
						SPU_ID = f"{brand_id}_{sales_category_id}_{tmp_spu_index}"
						tmp_dict_spu["spu_id"].append(SPU_ID)
						tmp_dict_spu["spu_raw_name"].append(product_raw_names_multiPages[tmp_spu_index])
						tmp_dict_spu["spu_name"].append(spu_names_multiPages[tmp_spu_index])
						tmp_dict_spu["spu_link"].append(spu_links_multiPages[tmp_spu_index])
						tmp_dict_spu["spu_price"].append(spu_prices_multiPages[tmp_spu_index])
					
					df_tmp = pd.DataFrame.from_dict(tmp_dict_spu)
					df_tmp.to_csv(dst_tmp_path, index=False, encoding="utf-8-sig")
				
				else:
					print("[WARNING] The crawled values have different length!")
					print("len(spu_links_multiPages): ", len_pages)
					print("len(spu_names_multiPages): ", len_names)
					print("len(spu_prices_multiPages): ", len_prices)
					print("\nSorry, the program stopped early due to the web contents has been revised.")
					break
		
		# Merge the csv files from all desired sales-categories
		df_merged = pd.DataFrame()
		for sales_category_id in exec_sales_category_ids:
			df_batch = pd.read_csv(f"{tmp_dir}/{sales_category_id}.csv")
			df_merged = pd.concat([df_merged, df_batch], axis=0)
		
		# Save final csv file
		#df = pd.DataFrame.from_dict(tmp_dict_spu)
		df_merged.to_csv(basic_attr_path, index=False, encoding="utf-8-sig")
		
	return basic_attr_path

def __crawl_basic_attributes(sales_category_link, sales_category_type):
	product_links_multiPages = []
	product_raw_names_multiPages = []
	product_names_multiPages = []
	product_prices_multiPages = []
	
	# Get driver with options to fit GU's web pages
	driver = get_UNIQLO_driver()
	
	# 造訪網頁連結
	try:
		visit_link(driver, sales_category_link, False)
		
		'''
		spu_categories = [e.text.strip() for e in driver.find_elements("xpath", "//ul[@class='bd-nav_list']/li/a")]
		
		spu_links, spu_raw_names, spu_names, spu_prices = [], [], [], []
		#invalid_h2_names = ["零碼"]
		for spu_category in spu_categories:
			spu_links = [e.get_attribute("href") for e in driver.find_elements("xpath", f"//h2[contains(text(),{spu_category})]/../following-sibling::div[1]/ul/li/div/a")]
			print(f"spu_links: {spu_links}")
			spu_raw_names = [e.text.strip() for e in driver.find_elements("xpath", f"//h2[contains(text(),{spu_category})]/../following-sibling::div[1]/ul/li/div/a/div/p[2]")]
			print(f"spu_raw_names: {spu_raw_names}")
			spu_names = [' '.join(e.split(' ')[:-1]) for e in spu_raw_names]
			spu_prices = [e.text.strip().replace("NT$",'').replace(',','') for e in driver.find_elements(f"//h2[contains(text(),{spu_category})]/../following-sibling::div[1]/ul/li/div/a/div/span")]
			print(f"spu_prices: {spu_prices}")
		'''
		get_elements = lambda xpath: driver.find_elements("xpath", xpath)
		link_xpath = "//h2/../following-sibling::div[1]/ul/li/div/a"
		tmp_spu_links = [e.get_attribute("href") for e in get_elements(link_xpath)]
		if len(tmp_spu_links) > 0:
			spu_links = tmp_spu_links
			spu_raw_names = [e.text.strip() for e in get_elements(f"{link_xpath}/div/p[2]")]
			spu_names = [' '.join(e.split(' ')[:-1]) for e in spu_raw_names]
			spu_prices = [e.text.strip().replace("NT$",'').replace(',','') for e in get_elements(f"{link_xpath}/div/span")]
		else:
			link_xpath = "//a[@class='product-herf']"
			spu_links = [e.get_attribute("href") for e in get_elements(link_xpath)]
			spu_raw_names = [e.text.strip() for e in get_elements(f"{link_xpath}/div/p[2]")]
			spu_names = [' '.join(e.split(' ')[:-1]) for e in spu_raw_names]
			spu_prices = [e.text.strip().replace("NT$",'').replace(',','') for e in get_elements(f"{link_xpath}/div/span")]
			
		# 新增此頁資料
		product_links_multiPages.extend(spu_links)
		product_raw_names_multiPages.extend(spu_raw_names)
		product_names_multiPages.extend(spu_names)
		product_prices_multiPages.extend(spu_prices)
		print(f"[INFO] {sales_category_type}: 此銷售分類的 [基本屬性] 已取出\n")
		print("[INFO] Take a short break~ (5 sec)\n")
		sleep(5)

	except Exception as e:
		print(f"[WARNING] 造訪網頁連結 {sales_category_link} 時，出現問題\n{e}\n")
	
	driver.close()
	driver.quit()
	return product_links_multiPages, product_raw_names_multiPages, product_names_multiPages, product_prices_multiPages 

# =============================================================================
# Stage-3. Crawl: SKU (Specific) Product Details
# =============================================================================
def __crawl_specific_attributes(spu_link, driver, is_other_attrs_empty):
	#driver = get_UNIQLO_driver()
	
	# 造訪網頁連結
	try:
		visit_link(driver, spu_link, is_scroll=False)
	
	except Exception as e:
		print(f"[WARNING] 造訪網頁連結 {spu_link} 時，出現問題\n{e}\n")
		#driver.quit()
		return None, None
	
	else:
		specific_attr_dict = {"sku_img_link": [], "outfit_img_link": [], "colour_chip_id":[], "colour_chip_name": [], "colour_chip_link": [], "texture": [], "product_description": []}
		
		t = 20
		for i in range(t):
			print(f"[INFO] 等待 1 秒鐘 ({i+1} / {t})")
			sleep(1)
		
		# 使用 BeautifulSoup 解析網頁
		soup = BeautifulSoup(driver.page_source, "lxml")
		
		"""
		# 若造訪商品頁時有 pop-ups 則自動按下
		popup = soup.select("div.h-modal-footer button")
		
		#print("len(popup):", len(popup))
		try:
			if len(popup) > 0:
				print("[INFO] 正在自動按下彈出式視窗\n")
				'''
				pop-op text:
				溫馨提醒
				目前無法取得您的定位，故未能顯示鄰近店舖的庫存狀況。
				※在部份能夠取得定位的瀏覽器亦有可能無法顯示。
				'''
				pop_ops = driver.find_elements("xpath", "//div[@class='h-modal-container']/div/button[@type='button']")
				[pop_op.click() for pop_op in pop_ops]
		except:
			pass
		"""
		
		sku_image_links = []
		outfit_image_links = []
		colour_chip_ids = []
		colour_chip_names = []
		colour_chip_links = []
		textures = []
		product_descriptions = []
		#---
		missing_info = {"spu_price": None, "spu_raw_name": None, "spu_name": None}
		
		
		soup_curr = None
		# crawl: [價格] => 檢查是否售罄(缺貨)，若售罄，則之後的顏色 <li> 不可點擊
		is_sold_out = False
		if_not_dound = False
		tmp = None
		try_times = 0
		while True:
			soup = BeautifulSoup(driver.page_source, "lxml")
			tmp = soup.select("span.product-detail-list-price-main > span") #ok
			if len(tmp) > 0:
				break
			else:
				tmp2 = soup.select("span.product-detail-list-price-main") #ok
				if len(tmp2) > 0:
					#if tmp2[0].text.strip() in ["已售罄", "缺貨", "缺貨中","售罄"]:
					is_sold_out = True
					break
				tmp3 = soup.select("div.page-404-title") #ok
				if len(tmp3) > 0:
					if_not_dound = True
					break
				else:
					print("[INFO] 找不到商品價格所在的網頁元素，等待 1 秒（直到網頁載入完成）")
					sleep(1)
					try_times += 1
					if try_times == 3: 
						is_sold_out = True
						break
		
		#is_sold_out = True if raw_text in ("缺貨","已售罄", "缺貨中","售罄","售完") else False
		if not if_not_dound:
			if is_other_attrs_empty:
				if is_sold_out:
					missing_info["spu_price"] = 'X'
				else:
					raw_text = tmp[0].text.replace('\n','').strip()
					missing_info["spu_price"] = raw_text.replace("NT$",'').replace(',','')
					
				tmp = soup.select("div.product-detail-list-title") #ok
				missing_info["spu_raw_name"] = tmp[0].text.replace('\n','').strip()
				missing_info["spu_name"] = ' '.join(missing_info["spu_raw_name"].split(' ')[:-1])
		
			
			if not is_sold_out:
				print("[INFO] 商品尚有庫存")
				# crawl: [圖片連結], [顏色]   
				for i, e in enumerate(driver.find_elements("xpath", "//div[@class='h-col product-detail-list']/div/div[@class='sku-select']/ul[1]/li")): #ok
					sleep(3)
					print("[INFO] 等待 3 秒鐘")
					e.click()
				
					#driver.implicitly_wait(10)
					soup_curr = BeautifulSoup(driver.page_source, "lxml")
					
					raw_text_colour = ""
					while True:
						#raw_text_colour = soup_curr.select("div.gu-sku-select-box > div.sku-select.gu-sku-select > label > b:contains('顏色') + span.gu-select-color")[0].text
						# //div[@class='h-col product-detail-list']/div/div[@class='sku-select']/label/b[contains(text(),'顏色')]
						raw_text_colour = soup_curr.select("div.h-col.product-detail-list > div > div.sku-select > label:has(b:contains('顏色'))")[0].text.replace("顏色：",'') #ok
						
						if raw_text_colour.strip() == '':
							e.click()
							soup_curr = BeautifulSoup(driver.page_source, "lxml") #ok
							sleep(1)
						else:
							break
					
					#print(f"顏色: {raw_text_colour}")
					tmp_list = raw_text_colour.split(' ')
					colour_number = tmp_list[0]
					#colour_number = tmp_list[0].replace('/','').strip()
					#colour_chip_id, colour_chip_name = int(colour_number), ' '.join(tmp_list[1:])
					colour_chip_id, colour_chip_name = colour_number, ' '.join(tmp_list[1:])
					colour_chip_ids.append(colour_chip_id)
					colour_chip_names.append(colour_chip_name)
					
					#results = soup_curr.select("div.gu-sku-select-box > div.sku-select.gu-sku-select > ul.h-clearfix.sku-select-colors > li > img")
					results = soup_curr.select("div.h-col.product-detail-list div > div.sku-select > ul.h-clearfix.sku-select-colors > li > img") #ok
					colour_chip_links.append(results[i]["src"]) #ok
					
					# crawl: [圖片連結]
					raw_text = soup_curr.select("div.detail-img")[0]["style"] #ok
					#product_img_link = raw_text
					#product_img_link = raw_text[raw_text.find("&quot;")+6:raw_text.rfind("&quot;")] #ok
					product_img_link = raw_text[raw_text.find('url(')+5:raw_text.rfind(') ')-1]
					sku_image_links.append(product_img_link) #ok
					
					# [deprecated] 爬取圖片 (下一階段再來爬)
					'''
					for e in driver.find_elements("xpath", "//div[@class='gu-sku-select-box']/div[@class='sku-select gu-sku-select']/ul[@class='h-clearfix sku-select-colors']/li/img"):
						e.click()
						colour_chip_links.append(e.get_attribute("src"))
						sleep(1)
						product_img = driver.find_element("xpath", "//div[@class='detail-img']")
						raw_text = product_img.get_attribute("style")
						product_img_link = raw_text[raw_text.find("&quot;")+6:raw_text.rfind("&quot;")]
						sku_image_links.append(product_img_link)
					'''
			else:
				print("[INFO] 商品售罄")
				# 售罄商品 沒有 顏色資訊 可以爬
				colour_chip_ids.append('X')
				colour_chip_names.append('X')
				colour_chip_links.append('X')
				
				# crawl: [圖片連結] (只有一張 [商品圖片]，無其它顏色可點選，故無其它 [商品圖片])
				tmp = soup.select("div.detail-img")
				if len(tmp) > 0:
					raw_text = tmp[0]["style"]
					#product_img_link = raw_text[raw_text.find("&quot;")+6:raw_text.rfind("&quot;")]
					product_img_link = raw_text[raw_text.find('url(')+5:raw_text.rfind(') ')-1]#ok
					sku_image_links.append(product_img_link)
				else:
					sku_image_links.append(['X'])
			
			print("等待 3 秒鐘")
			sleep(3)
			scroll_height = driver.execute_script("return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")
			scroll_distance = int(0.3 * scroll_height / 10)
			n = 7
			## 開始執行 n 次捲動
			for _ in range(n):
				js = f"window.scrollTo(0, {scroll_distance} + window.scrollY);"
				driver.execute_script(js) # 捲動至目前位置加上捲動距離
				sleep(1 + randint(0,10)/10) # 每次捲動完，稍等 1 ~ 2 秒（讓圖片載入）
	
			# =============================================================================
	
			n = 3
			## 開始執行 n 次捲動
			for _ in range(n):
				js = f"window.scrollTo(0, {scroll_distance} + window.scrollY);"
				driver.execute_script(js) # 捲動至目前位置加上捲動距離
				sleep(1 + randint(0,10)/10) # 每次捲動完，稍等 1 ~ 2 秒（讓圖片載入）
	
			soup = BeautifulSoup(driver.page_source, "lxml")
			#outfit_image_links.extend([e["style"].split("&quot;")[1] for e in soup.select("a div.zoom-image")]) #ok
			outfit_image_links.extend([''.join(f'https://{e["style"].split("https://")[1]}'.split("\"")[:-1]) for e in soup.select("a div.zoom-image")])
			
			
			# div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div:contains('商品說明') + div
			# //div[contains(text(), '商品說明')]/following-sibling::div[1]
			
			raw_text = driver.find_element("xpath", "//div[contains(text(), '商品說明')]/following-sibling::div[1]").text #ok
			product_descriptions = [raw_text.split("商品材質")[0].strip()] #ok
			textures = [raw_text.split("商品材質")[1].split("洗滌方式")[0].strip()] #ok
			specific_attr_dict["sku_img_link"] = sku_image_links #ok
			specific_attr_dict["outfit_img_link"] = outfit_image_links #ok
			specific_attr_dict["colour_chip_id"] = colour_chip_ids
			specific_attr_dict["colour_chip_name"] = colour_chip_names
			specific_attr_dict["colour_chip_link"] = colour_chip_links
			specific_attr_dict["texture"] = textures #ok
			specific_attr_dict["product_description"] = product_descriptions #ok
		
			#driver.quit()
		return specific_attr_dict, missing_info

def crawl_specific_attributes_multiSPUs(brand, basic_attr_path):
	specific_attr_path = f"csv/{brand}_specific_attr.csv"
	specific_newAttr_path = f"csv/{brand}_specific_attr_newAttrs.csv"
	
	if os.path.exists(specific_attr_path):
		print(f"[INFO] 已蒐集 {brand} 的 特定商品屬性\n")
	else:
		tmp_dir = f"csv/tmp__{brand}_specific_attr"
		os.makedirs(tmp_dir, exist_ok=True)
		print(f"[INFO] 開始爬蟲 {brand} 的 特定商品屬性\n")
		
		df_spu = pd.read_csv(basic_attr_path)
		tmp_percentage_weight = 100 / len(df_spu)
		
		df_sku_merged = pd.DataFrame()
		is_interrupt = False
		
		'''
		print(len(df_spu))
		print(len(df_spu["spu_link"]))
		print(df_spu["spu_link"].iloc[0])
		#https://www.uniqlo.com/tw/zh_TW/product-detail.html?productCode=u0000000017746
		print(len(df_spu[pd.isnull(df_spu["spu_raw_name"])]))
		print(len(df_spu[pd.isnull(df_spu["spu_name"])]))
		print(len(df_spu[pd.isnull(df_spu["spu_price"])]))
		'''
		
		driver = get_UNIQLO_driver()
		df_spu_new = df_spu.copy()
		
		df_spu_newAttrs = None
		tmp_dict_spu_new_attr = None
		if os.path.exists(specific_newAttr_path):
			df_spu_newAttrs = pd.read_csv(specific_newAttr_path)
			tmp_dict_spu_new_attr = {"spu_id": list(df_spu_newAttrs["spu_id"]), "texture": list(df_spu_newAttrs["texture"]), "product_description": list(df_spu_newAttrs["product_description"])}
		else:
			data_size = len(df_spu_new)
			tmp_dict_spu_new_attr = {"spu_id": ['X'] * data_size, "texture": ['X'] * data_size, "product_description": ['X'] * data_size}
		
		old_cols = list(df_spu_new.columns)
		idx_raw_name = old_cols.index("spu_raw_name")
		idx_name = old_cols.index("spu_name")
		idx_price = old_cols.index("spu_price")
		
		for i, row in list(df_spu.iterrows()):
			df_sku_partial = None
			
			spu_id = row["spu_id"]
			
			#if spu_id == "1.0_1_1":
			#	break
			
			spu_link = row["spu_link"]
			is_other_attrs_empty = pd.isnull(row["spu_name"])
			
			dst_tmp_path = f"{tmp_dir}/{spu_id}.csv"
			
			if not os.path.exists(dst_tmp_path):
				columns = get_schema("sku")
				tmp_dict_sku = {k: list() for k in columns}
				
				print(f"[INFO] 開始爬蟲 spu_link: {spu_link}", '\n')
				
				#spu_link = df_spu["spu_link"].iloc[randint(0, len(df_spu)-1)]
				#spu_link = "https://www.gu-global.com/tw/zh_TW/product-detail.html?productCode=u0000000008429"
				
				specific_attr_dict, missing_info = __crawl_specific_attributes(spu_link, driver, is_other_attrs_empty)
				
				if is_other_attrs_empty and missing_info is not None:
					df_spu.to_csv(basic_attr_path.replace(".csv", f"_{get_timestamp()}.csv"))
					df_spu.iloc[i, idx_raw_name] = missing_info["spu_raw_name"]
					df_spu.iloc[i, idx_name] = missing_info["spu_name"]
					df_spu.iloc[i, idx_price] = missing_info["spu_price"]
					df_spu.to_csv(basic_attr_path)
				
				if specific_attr_dict is not None:		
					sku_index = 0
					
					sku_type_code = 1
					for j, sku_img_link in enumerate(specific_attr_dict["sku_img_link"]):
						tmp_dict_sku["timestamp"].append(get_timestamp())
						tmp_dict_sku["spu_id"].append(spu_id)
						sku_id = f"{spu_id}_{sku_type_code}_{sku_index}"
						tmp_dict_sku["sku_id"].append(sku_id)
						tmp_dict_sku["sku_img_link"].append(sku_img_link)
						tmp_dict_sku["outfit_id"].append('X')
						tmp_dict_sku["outfit_img_link"].append('X')
						tmp_dict_sku["colour_chip_id"].append(specific_attr_dict["colour_chip_id"][j])
						tmp_dict_sku["colour_chip_name"].append(specific_attr_dict["colour_chip_name"][j])
						tmp_dict_sku["colour_chip_link"].append(specific_attr_dict["colour_chip_link"][j])
						sku_index += 1
					
					sku_type_code = 2
					for j2, outfit_img_link in enumerate(specific_attr_dict["outfit_img_link"]):
						tmp_dict_sku["timestamp"].append(get_timestamp())
						tmp_dict_sku["spu_id"].append(spu_id)
						outfit_id = f"{spu_id}_{sku_type_code}_{sku_index}"
						tmp_dict_sku["sku_id"].append('X')
						tmp_dict_sku["sku_img_link"].append('X')
						tmp_dict_sku["outfit_id"].append(outfit_id)
						tmp_dict_sku["outfit_img_link"].append(outfit_img_link)
						tmp_dict_sku["colour_chip_id"].append('X')
						tmp_dict_sku["colour_chip_name"].append('X')
						tmp_dict_sku["colour_chip_link"].append('X')
						sku_index += 1
					
					for k, v in tmp_dict_sku.items():
						print(k, len(v))
					
					df_sku_partial = pd.DataFrame.from_dict(tmp_dict_sku)
					df_sku_partial.to_csv(dst_tmp_path, index=False, encoding="utf-8-sig")
					
					tmp_dict_spu_new_attr["spu_id"][i] = spu_id
					texture = "" if len(specific_attr_dict["texture"]) == 0 else specific_attr_dict["texture"][0]
					tmp_dict_spu_new_attr["texture"][i] = texture
					product_description = "" if len(specific_attr_dict["product_description"]) == 0 else specific_attr_dict["product_description"][0]
					tmp_dict_spu_new_attr["product_description"][i] = product_description
					
					df_spu_newAttr_partial = pd.DataFrame.from_dict(tmp_dict_spu_new_attr)
					df_spu_newAttr_partial.to_csv(specific_newAttr_path, index=False, encoding="utf-8-sig")
					
				else:
					pass
					#is_interrupt = True
					#break

				progress_percentage = round(tmp_percentage_weight * (i+1), 2)
				print(f"[INFO] spu_id: {spu_id} 的 特定商品屬性 已取出，爬蟲進度: {progress_percentage} %", '\n')
				print("[INFO] Take a short break~ (5 sec)\n")
				sleep(5)
				
			else:
				df_sku_partial = pd.read_csv(dst_tmp_path)
			
			
			df_sku_merged = pd.concat([df_sku_merged, df_sku_partial], axis=0)
		
		if not is_interrupt:
			df_sku_merged.to_csv(specific_attr_path, index=False, encoding="utf-8-sig")
		
		#test_spu_link = "https://www.gu-global.com/tw/zh_TW/product-detail.html?productCode=u0000000008429"
		#test_spu_link = "https://www.gu-global.com/tw/zh_TW/product-detail.html?productCode=u0000000008716"
		#spu_link = "https://www.gu-global.com/tw/zh_TW/product-detail.html?productCode=u0000000008429"
	
	return specific_attr_path

# =============================================================================
# Stage-4. Crawl:SKU (Specific) Product Image
# =============================================================================
def __crawl_image(link, path):
	if 'X' not in link:
		my_ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
		my_headers = {'User-Agent': my_ua}
		response = requests.get(link, headers=my_headers, stream=True)
		if response.status_code == 200:
			try:
				with open(path, "wb") as f:
					for chunk in response:
						f.write(chunk)
			except Exception as e:
				print(f"[WARNING] 圖片網址: {link} 下載遭中斷\n{e}\n")
		else:
			print("[WARNING] 圖片網址: {link} 發送 request 失敗\n")

def crawl_images(brand, specific_attr_path):
	#test_product_img_link_hi_reso = "https://www.gu-global.com/tw/hmall/test/u0000000008429/main/first/1000/1.jpg"
	#test_product_img_link_lo_reso = "https://www.gu-global.com/tw/hmall/test/u0000000008429/main/first/561/1.jpg"
	#test_outfit_img_link = "https://api.fastretailing.com/ugc/v1/gu/tw/SR_IMAGES/ugc_stylehint_gu_tw_photo_230722_1138882_r-500-500"
	
	dst_csv_path = f"csv/{brand}_images.csv"
	[os.makedirs(f"image/{img_type}", exist_ok=True) for img_type in ["sku_img", "outfit_img", "colour_chip"]]
	
	tmp_csv_dir = f"csv/tmp__{brand}_image"
	os.makedirs(tmp_csv_dir, exist_ok=True)
	
	if os.path.exists(dst_csv_path):
		print(f"[INFO] 已蒐集 {brand} 的 商品圖片\n")
	
	else:
		print(f"[INFO] 開始爬蟲 {brand} 的 商品圖片\n")
		# Define attributes to record the paths for images (Primary Key: sku_id)
		
		# 本來想說把資料拆成多個 batchs, 每個 batch 用 multi-thread 跑 (比較快)
		# 但放棄, 主要是考慮到: 分段爬蟲資料 merge 的複雜度較高
		# 而且可能出錯 (如果砍掉重練, 那可能與 [逐筆 sequentially 跑] 相比, 浪費更多時間)
		'''
		# Split data into "SKU-product images", "outfit images", and "colour chips"
		df = pd.read_csv(specific_attr_path)
		is_data_valid = True
		
		sku_product_images = df[df["sku_id"]!='X']
		if len(sku_product_images["sku_id"]) != len(sku_product_images["sku_id"].unique()):
			is_data_valid = False
			print("[WARNING] `sku_id` is not unique.\n")
		
		sku_outfit_images = df[df["outfit_id"]!='X']
		if len(sku_outfit_images["outfit_id"]) != len(sku_outfit_images["outfit_id"].unique()):
			is_data_valid = False
			print("[WARNING] `outfit_id` is not unique.\n")
			
		colour_chips = df[df["colour_chip_id"]!='X']
		#print(len(colour_chips["colour_chip_id"].unique())) # 151
		
		# For each record: (1) crawl the image (2) record the path
		if is_data_valid:
			
			data_size = 21 # test
			#data_size = len(df)
			batch_size = 10
			#for start_idx in range(0, len(df), 10):
			for start_idx in range(0, data_size, batch_size):
				#print("start_index:", start_idx)
				end_idx = start_idx+batch_size-1 
				if end_idx >= data_size:
					end_idx = data_size - 1
				#print("end_index:", end_idx)
				#print()
				
				df_batch = df.iloc[start_idx: end_idx+1]
				df_sku_imgs = df_batch[df_batch["outfit_id"]=='X']
				[{"link": link, "path": path} for link, path in zip(df_sku_imgs["sku_img_link"], "img/{sku_id}") for sku_id in df_sku_imgs["sku_id"]]
				df_outfit_imgs = df_batch[df_batch["outfit_id"]!='X']
				
				df_batch[""]
			#print()
		'''
		
		df_img = pd.DataFrame()
		df_sku = pd.read_csv(specific_attr_path)
		
		is_interrupt = False
		
		img_csv_attrs = get_schema("img")
		for df_sku_index, row in df_sku.iterrows():
			img_path_dict = {k: [] for k in img_csv_attrs}
			
			is_new_img_downloaded = False
			
			tmp_csv_path = f"{tmp_csv_dir}/{df_sku_index}.csv"
			
			tmp_percentage_weight = 100 / len(df_sku)
			progress_percentage = round(tmp_percentage_weight * (df_sku_index+1), 2)
			
			if os.path.exists(tmp_csv_path):
				df_img_partial = pd.read_csv(tmp_csv_path)
				print(f"[INFO] df_sku_index: {df_sku_index} 的 商品圖片 先前已下載，爬圖進度: {progress_percentage} %", '\n')

			else:
				record_id, record_id_name = None, None
				sku_id, outfit_id, colour_chip_id = row["sku_id"], row["outfit_id"], row["colour_chip_id"]
				if sku_id != 'X':
					record_id_name = "sku_id"
					record_id = sku_id
				else:
					record_id_name = "outfit_id"
					record_id = outfit_id
					
				outfit_img_link = row["outfit_img_link"]
				if outfit_img_link != 'X':
					outfit_img_path = f"image/outfit_img/{record_id}.png"
					
					if not os.path.exists(outfit_img_path):
						try:
							__crawl_image(row["outfit_img_link"], outfit_img_path)
							is_new_img_downloaded = True
						except Exception as e:
							print(f"[WARNING] outfit_img 無法下載，執行中斷\n{e}\n")
							is_interrupt = True
							break
					
					img_path_dict["timestamp"].append(get_timestamp())
					img_path_dict["sku_id"].append('X')
					img_path_dict["outfit_id"].append(outfit_id)
					img_path_dict["sku_img_path"].append('X') 
					img_path_dict["outfit_img_path"].append(outfit_img_path)
					img_path_dict["colour_chip_path"].append('X')
						
				else:
					sku_img_path = f"image/sku_img/{record_id}.png"
					colour_chip_path = f"image/colour_chip/{colour_chip_id}.png"
					
					if not os.path.exists(sku_img_path):
						try:
							__crawl_image(row["sku_img_link"], sku_img_path)
							is_new_img_downloaded = True
						except Exception as e:
							print(f"[WARNING] sku_img 無法下載，執行中斷\n{e}\n")
							is_interrupt = True
							break
					
					if not os.path.exists(colour_chip_path):
						try:
							__crawl_image(row["colour_chip_link"], colour_chip_path)
							is_new_img_downloaded = True
						except Exception as e:
							print(f"[WARNING] outfit_img 無法下載，執行中斷\n{e}\n")
							is_interrupt = True
							break
					
					img_path_dict["timestamp"].append(get_timestamp())
					img_path_dict["sku_id"].append(sku_id)
					img_path_dict["outfit_id"].append('X')
					img_path_dict["sku_img_path"].append(sku_img_path) 
					img_path_dict["outfit_img_path"].append('X')
					img_path_dict["colour_chip_path"].append(colour_chip_path)
				
				print(f"[INFO] {record_id_name}: {record_id} 的 商品圖片 已下載，爬蟲進度: {progress_percentage} %", '\n')
				
				if is_new_img_downloaded:
					t = randint(1, 2)
					print(f"[INFO] 等待 {t} 秒鐘 ...")
					sleep(t)
					
				df_img_partial = pd.DataFrame.from_dict(img_path_dict)
				df_img_partial.to_csv(tmp_csv_path, index=False, encoding="utf-8-sig")
			
			df_img = pd.concat([df_img, df_img_partial], axis=0)
		
		if not is_interrupt:
			df_img.to_csv(dst_csv_path, index=False, encoding="utf-8-sig")

	return dst_csv_path
	
if __name__ == "__main__":
	create_save_dirs()
	home_page_link = "https://www.uniqlo.com/tw/zh_TW/"
	brand = "UNIQLO"
	
	menu_path = crawl_menu(brand, home_page_link) # crawl: 客群種類、粗分類、銷售分類、銷售分類連結
	
	
	basic_attr_path = crawl_basic_attributes_multiSalesCategories(brand, menu_path) # for each: 銷售分類連結 { crawl: 商品名稱、商品價格、商品連結 }
	
	specific_attr_path = crawl_specific_attributes_multiSPUs(brand, basic_attr_path)
	
	"""
	crawl_images(specific_attr_path)
	"""