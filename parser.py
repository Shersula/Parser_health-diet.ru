from bs4 import BeautifulSoup
import requests
import json
import csv

# url = "http://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie"

headers = {
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 YaBrowser/21.6.4.786 Yowser/2.5 Safari/537.36"
}
# request = requests.get(url, headers=headers)
# src = request.text
# with open("index.html", "w", encoding="utf-8") as file:
# 	file.write(src)


# with open("index.html", "r", encoding="utf-8") as file:
# 	src = file.read()

# soup = BeautifulSoup(src, "lxml")
# links = soup.find_all("a", class_="mzr-tc-group-item-href")
# AllCategories = {}
# for i in links:
# 	text = i.text
# 	link = "health-diet.ru" + i["href"]
# 	AllCategories[text] = link

# with open("AllCategories.json", "w", encoding="utf-8") as file:
# 	json.dump(AllCategories, file, ensure_ascii=False, indent=4)

with open("AllCategories.json", "r", encoding="utf-8") as file:
 	AllCategories = json.load(file)
count = 0
for key, link in AllCategories.items():
	rep = [",", " ", "-", "'"]
	for i in rep:
		if i in key:
			key = key.replace(i, "_")
	req = requests.get(url="http://" + link, headers=headers)
	src = req.text
	with open("data\\" + str(count) + "_" + key + ".html", "w", encoding="utf-8") as file:
		file.write(src)

	with open("data\\" + str(count) + "_" + key + ".html", "r", encoding="utf-8") as file:
		src = file.read()

	soup = BeautifulSoup(src, "lxml")

	if soup.find(class_="uk-alert-danger") is not None:
		continue

	table = soup.find(class_="mzr-tc-group-table").find("tr").find_all("th")
	TableHeaders = []
	for i in table:
		TableHeaders.append(i.text)

	with open("data\\" + str(count) + "_" + key + ".csv", "w", encoding="cp1251", newline='') as file:
		writer = csv.writer(file, delimiter=";")
		writer.writerow(tuple(TableHeaders))

	with open("AllCategories.json", "w", encoding="utf-8") as file:
 		json.dump(AllCategories, file, ensure_ascii=False, indent=4)

	table = soup.find(class_="mzr-tc-group-table").find("tbody").find_all("tr")
	TableInfo = []
	TableDict = {}
	for i in table:
		TableInfo.clear();
		for SubItem in i.find_all("td"):
			TableInfo.append(SubItem.text.strip())

		with open("data\\" + str(count) + "_" + key + ".csv", "a", encoding="cp1251", newline='', errors='replace') as file:
			writer = csv.writer(file, delimiter=";")
			writer.writerow(tuple(TableInfo))

		with open("data\\json\\" + str(count) + "_" + key + ".json", "a", encoding="utf-8") as file:
			TableDict = {
				TableHeaders[0]:TableInfo[0],
				TableHeaders[1]:TableInfo[1],
				TableHeaders[2]:TableInfo[2],
				TableHeaders[3]:TableInfo[3],
				TableHeaders[4]:TableInfo[4],
			}
			json.dump(TableDict, file, ensure_ascii=False, indent=4)
	count += 1
