import pandas
import requests
from bs4 import BeautifulSoup

def get_response(serial_number):
    '''输入序列号，输出requests对象'''
	url = f'https://runway-webstore.com/ap/item/i/m/{str(serial_number)}'#网页最后的序列号是货号的前十位
    response = requests.get(url)
    return response

def get_soup(response):
	'''输入requests对象，以bs4把其中的html代码转换为beautifulsoup对象'''
	soup = BeautifulSoup(response.text,'html.parser')
	return soup
	
def get_item_detail_info_text(soup):
	'''输入soup对象，输出物品详细描述的字符串'''
	item_detail_info_text = soup.find(class_= "item_detail_info_text").text.strip()
	return item_detail_info_text
	
def get_item_detail_info_table(soup):
	'''输入soup对象，将物品详细描述表格转为dict输出'''
	results = {}
	for row in soup.find(class_="item_detail_info_table").find_all('tr'):
		name = row.find('th')
		value = row.find('td')
		results[name.text] = value.text
	return results
    
def get_image_url(soup):
	'''输入soup对象，输出示例图片的大图url字符串'''
	image_url = "https:" + soup.find(bigimage=True)['bigimage']#货品图片的大图存在'bigimage'标签下，有不止一张
	return image_url
	
def save_image(image_url, serial_number_in_filename):
	'''输入url字符串，和货号，将图片以货号为文件名保存在指定路径'''
	response = requests.get(image_url)
	if response.status_code == 200:
		with open(f'c:/Users/sl410k/Desktop/lotus/picture/{serial_number_in_filename}.jpg', 'wb') as f:#保存的绝对路径是静态写在源代码里的，改保存路径需要手动修改此处的路径
			f.write(response.content)
			f.close

def worker(row):
	'''封装用于apply进dataframe的工作函数，每次加载一行数据，抓取页面信息之后写入dataframe'''
	serial_number = row["品番"][:-2]#读取一行里“品番”那一列的数据，因此以后货号所在的列标题一定得是“品番”二字
	serial_number_in_filename = row["品番"]
	try:
		response = get_response(serial_number)
		#print('serial_number is: '+str(serial_number)+' status_code is: '+str(response.status_code))
		if response.status_code == 200:
			try:
				soup = get_soup(response)
				row["item_detail_info_text"]=get_item_detail_info_text(soup)
				table = get_item_detail_info_table(soup)
				#print(table)
				row = row.append(pandas.Series(table,dtype=str))
				save_image(get_image_url(soup),serial_number_in_filename)
				#print(str(serial_number_in_filename)+' done')
			except:
				pass
		row['status_code'] = str(response.status_code)
	except:
		row['status_code'] = 'network error'
	return row

def load_excel():
	#name = input("请输入文件名，如example.xlsx：")
	name = 'c:/Users/sl410k/Desktop/lotus/1_191028货号.xlsx'#读取货号文件的路径是静态写在源代码里的，改读取路径或者读取文件名需要手动修改此处的路径
	file = pandas.read_excel(name,dtype=str)
	df = pandas.DataFrame(file)
	return df

def function():
	df_in = load_excel()
	df_out = df_in.apply(worker,1)
	return df_out.to_excel('c:/Users/sl410k/Desktop/lotus/result.xlsx')#输出结果文件的路径是静态写在源代码里的，改保存路径或者输出文件名需要手动修改此处的路径

import datetime
starttime = datetime.datetime.now()#用于计算整个任务花了多久
function()
endtime = datetime.datetime.now()
print('done')
print (endtime - starttime)
	
#response = get_response('0219500003')
#soup = get_soup(response)041950000301
#print(response.status_code)
