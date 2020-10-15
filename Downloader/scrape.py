#!/usr/bin/python3
import requests,sys
from bs4 import BeautifulSoup

# define constants
cookies 		  = dict(SACSID='<insert your SACSID cookie here>')
base_url 		  = "https://www.pentesteracademy.com"
VIEWS_URLS 		  = "https://www.pentesteracademy.com/members?options=accountlogs"
UserAgent         	  = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
VIDEOS_URL 		  = "https://www.pentesteracademy.com/topics"
video_list 		  = []
download_list	  	  = []


# View checker - used to make sure we don't just spam the download button
def getViews():
	headers = {'useragent': UserAgent}
	r = requests.get(VIEWS_URLS,cookies=cookies)
	if (r.status_code) == 200:
		soup = BeautifulSoup(r.text, 'html.parser')
		for results in soup.findAll('p'):
			if "Total plays till date" in results.text:
				return(100 - int(results.text.split("=",1)[1].strip())) # 100 views per month - how many you have used thus far
	else:
		print("Couldn't Connect")


# downloader will actually grab the links and download the shiz
def downloadVideos(url):
	headers = {'useragent': UserAgent}
	r = requests.get(url,cookies=cookies)
	if (r.status_code) == 200:
		# get the download links
		soup = BeautifulSoup(r.text, 'html.parser')
		for results in soup.find_all("div", {"id": "myTabContent"}):
			for link in results.find_all("a",href=True):
				if getViews() > 0:
					download_link = base_url + link["href"]
					print ("downloading from URL: " + download_link)
				else:
					print("Max views hit for the month")
					sys.exit()

# Video List downloader - gets the individual video list from the topic page
def videoList(url):
	# I should add a check to see if the videos have already been downloaded to make sure we aren't wasting views
	# for now make sure you just have a list that doesn't have some downloaded
	# the checkmark is used to show that the video has been downloaded, but the checkmark is added via JS i think
	headers = {'useragent': UserAgent}
	r = requests.get(url,cookies=cookies)
	if (r.status_code) == 200:
		# get the video links
		soup = BeautifulSoup(r.text, 'html.parser')
		for results in soup.find_all("div", class_="media"):
			for item in results.find_all("h4", class_="media-heading"):
				for link in item.find_all("a", href=True):
					downloadVideos(base_url + link['href'])


# Topic List - Grabs the different categories from the topics page
def topicList():
	headers = {'useragent': UserAgent}
	r = requests.get(VIDEOS_URL,cookies=cookies)
	if (r.status_code) == 200:
		soup = BeautifulSoup(r.text, 'html.parser')
		print("Video List: \n")
		for results in soup.find_all("h3", class_="media-heading"):
			video_list.append(results.text.lower())
			print (results.text)

	# get which video they want and check validity based on video_list - if not kbye
	choice = input("Which Video Series do you want to download?\n")

	if choice.lower() not in video_list:
		sys.exit()

	for results in soup.find_all("h3", class_="media-heading"):
		if results.text.lower() == choice.lower():
			# at this point we should have found, just a double check nbd
			# i'm doing this to get the full URL since i'm not storing the values in a dict... future work
			for a in results.find_all('a', href=True):
				videoList(base_url + a['href'])



# main... you know what it do
if __name__ == "__main__":
	# check views first so we aren't wasting requests - they don't grow on trees alright
	views_left = getViews()
	# views should be good at this point
	if views_left > 0:
		print("Total views left: %i" % (views_left))
		answer = input("want to download some shit? [Y/N]  ")
		# answer = "y"
		if answer.lower() == "y":
			topicList()
		elif answer.lower() == "n":
			print("nah")
		else:
			print("it's gotta be Yes or No dude")
	else:
		print("You gotta chill man")