from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib import messages 

# Create your views here.
from bs4 import BeautifulSoup as soup
import csv
from django.conf import settings
import time
import requests

def view(request):
	full_name = []
	full_price = []
	full_rate = []
	full_url = []

	file_name = "{}data.csv".format(settings.STATIC_URL)
	file = open(file_name, 'w')
	header='Name,Price,Rate,Url\n'
	file.write(header)



	if request.method == "POST":
		url=request.POST['url']
		if 'https://' not in url:
			messages.error(request, "Error")
		else:
			page_url = requests.get(url)
			pagesoup = soup(page_url.text, 'html.parser')

			main_class = pagesoup.find_all('div', {'class': '_1UoZlX'})


			for i in main_class:
				pdt_name= i.find('div', {'class': '_3wU53n'}).text.replace(',', '').replace('\r', '').replace('\n', '')
				pdt_price = i.find('div', {'class': '_1vC4OE _2rQ-NK'}).text.replace(',', '').replace('\r', '').replace('\n', '')
				pdt_rate = i.find('div', {'class': 'hGSR34'}).text.replace(',', '').replace('\r', '').replace('\n', '')
				pdt_url = i.find('a', {'class': '_31qSD5'})['href']
				pdt_main_url = 'https://www.flipkart.com'+pdt_url

				full_name.append(pdt_name)
				full_price.append(pdt_price)
				full_rate.append(pdt_rate)
				full_url.append(pdt_main_url)

				file.write(pdt_name+','+str(pdt_price)+','+pdt_rate+','+pdt_main_url+'\n')

		mylist=zip(full_name,full_price,full_rate,full_url)
		file.close()
		return render(request,'index.html',{'mylist':mylist})
	return render(request,'index.html')