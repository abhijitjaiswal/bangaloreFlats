import csv
import requests
from bs4 import BeautifulSoup

def get_data(name, area_id, bhk_num):
  url = "https://www.commonfloor.com/bangalore-property/in-"+name+"-a"+area_id+"/for-sale/apartment-ht/"+str(bhk_num)+"-bhk"
  print(url)
  res = requests.get(url)
  data=res.text
  soup = BeautifulSoup(data)
  leng = len(soup.find("div", {'class':'snb-content-list'}).find_all("div", {'class':'infodata'}))
  return soup, leng

def parse_data(name, bhk_num, soup, leng):
  d = {}
  if leng == 0:
    return d
  for i in range(0, int(leng/3)):
    if "region" not in d.keys():
      d["region"] = [name]
    else:
      d["region"].append(name)
    if "bhk_num" not in d.keys():
      d["bhk_num"] = [bhk_num]
    else:
      d["bhk_num"].append(bhk_num)
    if "price" not in d.keys():
      d["price"] = [soup.find("div", {'class':'snb-content-list'}).find_all("div", {'class':'infodata'})[i].find("span").text.strip()]
    else:
      d["price"].append(soup.find("div", {'class':'snb-content-list'}).find_all("div", {'class':'infodata'})[i*3].find("span").text.strip())
    if "title" not in d.keys():
      d["title"] = [soup.find("div", {'class':'snb-content-list'}).find_all("div", {"class":"snb-tile-info"})[i].find_all("h2")[0].find("a").text]
    else:
      d["title"].append(soup.find("div", {'class':'snb-content-list'}).find_all("div", {"class":"snb-tile-info"})[i].find_all("h2")[0].find("a").text)
    if "total_area" not in d.keys():
      d["total_area"] = [soup.find("div", {'class':'snb-content-list'}).find_all("div", {"class":"snb-tile-info"})[i].find_all("div", {"class":"infodata"})[1].find_all("span")[0].text.strip().split("sq.ft. @")[0].strip()]
    else:
      d["total_area"].append(soup.find("div", {'class':'snb-content-list'}).find_all("div", {"class":"snb-tile-info"})[i].find_all("div", {"class":"infodata"})[1].find_all("span")[0].text.strip().split("sq.ft. @")[0].strip())
    if "rate" not in d.keys():
      d["rate"] = [soup.find("div", {'class':'snb-content-list'}).find_all("div", {"class":"snb-tile-info"})[i].find_all("div", 
		{"class":"infodata"})[1].find_all("span")[0].text.strip().split("sq.ft. @")[1].strip()]
    else:
      try:
        d["rate"].append(soup.find("div", {'class':'snb-content-list'}).find_all("div", {"class":"snb-tile-info"})[i].find_all("div", 
                {"class":"infodata"})[1].find_all("span")[0].text.strip().split("sq.ft. @")[1].strip())
      except:
        d["rate"].append("")
    if "unit_href" not in d.keys():
      d["unit_href"] = ["https://www.commonfloor.com/"+soup.find("div", {'class':'snb-content-list'}).find_all("div", {"class":"snb-tile-info"})[i].find_all("h2")[0].find("a")["href"]]
    else:
      d["unit_href"].append("https://www.commonfloor.com/"+soup.find("div", {'class':'snb-content-list'}).find_all("div", {"class":"snb-tile-info"})[i].find_all("h2")[0].find("a")["href"])
    if "bathrooms" not in d.keys():
      d["bathrooms"] = [soup.find("div", {'class':'snb-content-list'}).find_all("div", {"class":"snb-tile-info"})[i].find_all("ul", {"class": "tileamt"})[0].find_all("li")[0].text]
    else:
      d["bathrooms"].append(soup.find("div", {'class':'snb-content-list'}).find_all("div", {"class":"snb-tile-info"})[i].find_all("ul", {"class": "tileamt"})[0].find_all("li")[0].text)
    if "type" not in d.keys():
      d["type"] = [soup.find("div", {'class':'snb-content-list'}).find_all("div", {"class":"snb-tile-info"})[i].find_all("ul", {"class": "tileamt"})[0].find_all("li")[1].text]
    else:
      d["type"].append(soup.find("div", {'class':'snb-content-list'}).find_all("div", {"class":"snb-tile-info"})[i].find_all("ul", {"class": "tileamt"})[0].find_all("li")[1].text)
    if "possesion" not in d.keys():
      d["possesion"] = [soup.find("div", {'class':'snb-content-list'}).find_all("div", {"class":"snb-tile-info"})[i].find_all("div", {"class":"infodata"})[2].find("span").text]
    else:
      d["possesion"].append(soup.find("div", {'class':'snb-content-list'}).find_all("div", {"class":"snb-tile-info"})[i].find_all("div", {"class":"infodata"})[2].find("span").text)
  return d

def write_csv(csv_file, d):
  with open(csv_file, "a") as c:
    for region, bhk_num, price, title, total_area, rate, unit_href, bathrooms, type, possesion in zip(d["region"], 
 		d["bhk_num"], d["price"], d["title"], d["total_area"], d["rate"], d["unit_href"], d["bathrooms"], d["type"], d["possesion"]):
      c.write(region+","+bhk_num+","+price+","+title+","+total_area+","+rate+","+unit_href+","+bathrooms+","+type+","+possesion+"\n")

"""
def get_regions():
  res1 = requests.get("https://en.wikipedia.org/wiki/List_of_neighbourhoods_in_Bangalore")
  data1 = BeautifulSoup(res1.text)
  suburbs = len(data1.find_all("table", {"class": "wikitable sortable"}))
  region = []
  for j in range(0, suburbs):
    for i in range(0, int(len(data1.find_all("table", {"class": "wikitable sortable"})[j].find_all("td"))/3)):
      region.append(data1.find_all("table", {"class": "wikitable sortable"})[j].find_all("td")[int(i*3)].text)
  return region
"""

def get_regions():
  res1 = requests.get("https://www.commonfloor.com/sitemap/index/city/Bangalore")
  data1 = BeautifulSoup(res1.text)
  regions = {}
  for i in range(0, len(data1.find_all("table")[0].find_all("tr"))):
    for j in range(0, len(data1.find_all("table")[0].find_all("tr")[i].find_all("td"))):
      regions[data1.find_all("table")[0].find_all("tr")[i].find_all("td")[j].find_all("a")[0].text] = data1.find_all("table")[0].find_all("tr")[i].find_all("td")[j].find_all("a")[0]["href"]
  return regions

def get_region_id(url):
  res1 = requests.get(url)
  data1 = BeautifulSoup(res1.text)
  for i in data1.find_all("script")[1].text.split("\n"):
    if "area_id" in i:
      j = i.split("area_id\":")
      return j[1].split(",")[0]


bhk = [1,2,3]
with open("region_id_mapping.csv", "r") as f:
  final_d={}
  #f.readline()
  for line in f.readlines():
    name = line.split(",")[0]
    id = line.split(",")[1].split("\"")[1].rstrip()
    for b in bhk:
      soup, leng = get_data(name, id, b)
      final_d = parse_data(name, b, soup, leng)
      if len(final_d) == 0:
        break
      with open("area_units.csv", "a") as a:
        l = len(final_d["region"])
        for i in range(0, l):
          a.write(final_d["region"][i]+","+str(final_d["bhk_num"][i])+","+final_d["price"][i]+","+final_d["title"][i]+","+final_d["total_area"][i]+","+final_d["rate"][i]+","+final_d["unit_href"][i]+","+final_d["bathrooms"][i]+","+final_d["type"][i]+","+final_d["possesion"][i]+"\n")
    
#Uncomment following in order to update region id
"""
r = get_regions()
for i in r.keys():
  with open("region_id_mapping.csv", "a") as z:
    z.write(i+",")
    #print(r[i])
    z.write(get_region_id("https://www.commonfloor.com"+r[i])+"\n")
"""
#with open(csv_file, "a") as c:
#  c.write("region,bhk_num, price,title,total_area,rate,unit_href,bathrooms,type,possesion\n")
