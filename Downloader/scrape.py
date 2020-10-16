#!/usr/bin/python3
import requests,sys
from bs4 import BeautifulSoup

# define constants
cookies 		  = dict(SACSID='<insert SACSID here>')
base_url 		  = "https://www.pentesteracademy.com"
VIEWS_URLS 		  = "https://www.pentesteracademy.com/members?options=accountlogs"
UserAgent         = ""
VIDEOS_URL 		  = "https://www.pentesteracademy.com/topics"
headers 		  = {'useragent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"}
video_list 		  = []
download_list	  = []


# View checker - used to make sure we don't just spam the download button
# gotta fix this to do error checking.  need to add a try catch block
def getViews():
	headers = {'useragent': UserAgent}
	# make sure the request works first
	r = requests.get(VIEWS_URLS,cookies=cookies,headers=headers)
	if (r.status_code) == 200:
		soup = BeautifulSoup(r.text, 'html.parser')
		for results in soup.findAll('p'):
			if "Total plays till date" in results.text:
				views = (100 - int(results.text.split("=",1)[1].strip())) # 100 views per month - how many you have used thus far

		# idk why but for some reason returning 0 gives a NoneType so i'm changing this up a bit
		if views == 0:
			return 0
		else:
			return views
	else:
		print("Did not get a 200 OK")


def download_file(url, title, extension):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter below
    headers = {'useragent': UserAgent}
    with requests.get(url, cookies=cookies, headers=headers, stream=True) as r:
        r.raise_for_status()
        # gotta add the format name
        with open(title + extension, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
    return local_filename

# downloader will actually grab the links and download the shiz
def downloadVideos(url, title):
	headers = {'useragent': UserAgent}
	r = requests.get(url,cookies=cookies,headers=headers)
	if (r.status_code) == 200:
		# get the download links
		soup = BeautifulSoup(r.text, 'html.parser')
		for results in soup.find_all("div", {"id": "myTabContent"}):
			for link in results.find_all("a",href=True):
				views = getViews()
				if views > 0:
					# I should pass the title as well
					download_link = base_url + link["href"]
					print ("views left: %i" % views)
					print ("Downloading Video Titled: " + title)
					# Check title here for PDF and change the extension based on that
					extension = ".m4v"
					download_file(download_link, title, extension)
				else:
					print("Max views hit for the month")
					sys.exit()

			
# Video List downloader - gets the individual video list from the topic page
def videoList(url):
	# I should add a check to see if the videos have already been downloaded to make sure we aren't wasting views
	# for now make sure you just have a list that doesn't have some downloaded
	r = requests.get(url,cookies=cookies, headers=headers)
	if (r.status_code) == 200:
		# get the video links
		soup = BeautifulSoup(r.text, 'html.parser')
		for results in soup.find_all("div", class_="media"):
			for item in results.find_all("h4", class_="media-heading"):
				for link in item.find_all("a", href=True):
					title = item.text
					downloadVideos(base_url + link['href'], title)


# Topic List - Grabs the different categories from the topics page
def topicList():
	headers = {'useragent': UserAgent}
	r = requests.get(VIDEOS_URL,cookies=cookies, headers=headers)
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
		answer = input("Downloading? [Y/N]  ")
		# answer = "y"
		if answer.lower() == "y":
			topicList()
		elif answer.lower() == "n":
			print("Exiting")
		else:
			print("Selection must be Y or N")
	else:
		print("You have run out of views for the month")