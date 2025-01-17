#!/usr/bin/python3
import requests,sys, argparse
from bs4 import BeautifulSoup

# define constants
<<<<<<< HEAD
cookies 		  = dict(SACSID='<insert SACSID Cookie Value Here')
=======
cookies 		  = dict(SACSID='<insert SACSID here>')
>>>>>>> 0cc00cf8c3f1c3efd175f3e5559f274f2b83d264
base_url 		  = "https://www.pentesteracademy.com"
views_url 		  = "https://www.pentesteracademy.com/members?options=accountlogs"
getstats		  = "https://www.pentesteracademy.com/getstats"
UserAgent         = ""
VIDEOS_URL 		  = "https://www.pentesteracademy.com/topics"
headers 		  = {'useragent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"}
video_list 		  = []
download_list	  = []


# View checker - used to make sure we don't just spam the download button
# gotta fix this to do error checking.  need to add a try catch block
# need to redo the math.  cause it's not always base 100
def getViews():
	views = 0 # gotta initialize it first
	# make sure the request works first
	r = requests.get(views_url,cookies=cookies,headers=headers)
	if (r.status_code) == 200:
		soup = BeautifulSoup(r.text, 'html.parser')
		for results in soup.findAll('p'):
			if "Total plays allowed based on subscription" in results.text:
				total_views = (results.text.split("=",1)[1].strip())
			elif "Total plays till date" in results.text:
				views = (int(total_views) - int(results.text.split("=",1)[1].strip())) # gotta get the total views first.  cause you know... it's not always 100
		# idk why but for some reason returning 0 gives a NoneType so i'm changing this up a bit
		if views == 0:
			return 0
		else:
			return views
	else:
		print("Did not get a 200 OK")



def checkViews():
	views = getViews()
	print ("You have %i views left this month." % views)


# later we need to add in a videoID arg
def getViewed(videoid):
	# so this is sketchy as all hell
	# unwatched = https://s3.amazonaws.com/videos.pentesteracademy.com/spacer.gif
	# watched = https://s3.amazonaws.com/videos.pentesteracademy.com/tick.jpg
	# you can use the /getstats?videoid=<video ID number> to retreive which it is. 
	payload = {'videoid': videoid}
	# r = requests.get('https://httpbin.org/get', params=payload)
	r = requests.get(getstats,params=payload,cookies=cookies,headers=headers)
	if "spacer.gif" in r.url:
		return False
	elif "tick.jpg" in r.url:
		return True
	else:
		print (r.url)
		print ("Error: unknown status_code")
		return True # I guess i'm just going to return True if there are issues.  Future work handle errors better

# 
def download_file(url, title, extension):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter below
    print ("views left: %i" % getViews())
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
	# headers = {'useragent': UserAgent}
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
					videoid =  (link["href"].split("=",1)[1])
					if getViewed(videoid):
						print ("Have already watched...skipping download")
					else:
						print ("Downloading Video Titled: " + title)
						# Check title here for PDF and change the extension based on that
						extension = ".m4v"
						download_file(download_link, title, extension)
				else:
					print("Max views hit for the month")
					sys.exit()

			
# Video List downloader - gets the individual video list from the topic page
def videoList():
	r = requests.get(VIDEOS_URL,cookies=cookies, headers=headers)
	if (r.status_code) == 200:
		soup = BeautifulSoup(r.text, 'html.parser')
	else:
		sys.exit()

	# get which video they want and check validity based on video_list - if not kbye
	choice = input("Which Video Series do you want to download?\n")

	if choice.lower() not in video_list:
		sys.exit()

	for results in soup.find_all("h3", class_="media-heading"):
		if results.text.lower() == choice.lower():
			# at this point we should have found, just a double check nbd
			# i'm doing this to get the full URL since i'm not storing the values in a dict... future work
			for a in results.find_all('a', href=True):
				url = (base_url + a['href']) # this should be the topic ID value
	

	# I should add a check to see if the videos have already been downloaded to make sure we aren't wasting views
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
	# headers = {'useragent': UserAgent}
	r = requests.get(VIDEOS_URL,cookies=cookies, headers=headers)
	if (r.status_code) == 200:
		soup = BeautifulSoup(r.text, 'html.parser')
		print("Video List: \n")
		for results in soup.find_all("h3", class_="media-heading"):
			video_list.append(results.text.lower())
			print (results.text)


def menu():
	# check views first so we aren't wasting requests - they don't grow on trees alright
	views_left = getViews()
	# views should be good at this point
	if views_left > 0:
		print("Total views left: %i" % (views_left))
		answer = input("Downloading? [Y/N]  ")
		# answer = "y"
		if answer.lower() == "y":
			topicList()
			videoList()
		elif answer.lower() == "n":
			print("Exiting")
		else:
			print("Selection must be Y or N")
	else:
		print("You have run out of views for the month")



# main... you know what it do
if __name__ == "__main__":
	# parse dem args my boi
    parser = argparse.ArgumentParser(
        description="Pentester Academy Video Downloader -- Happy Hunting!"
    )
    parser.add_argument("-v","--version", action='version', version='%(prog)s 0.1')

    # setup subparsers for func action
    subparsers = parser.add_subparsers(dest="command")

    # check_ip subparser
    check_parser = subparsers.add_parser("check", help="Check the number of views currently left for the month.")
    check_parser.set_defaults(func=checkViews)

    # download subparser
    download_parser = subparsers.add_parser("download", help="Automate video downloads")
    download_parser.set_defaults(func=menu)

    # list videos
    list_parser = subparsers.add_parser("list", help="List the Topics on Pentester Academy")
    list_parser.set_defaults(func=topicList)

    # eventually i'd like to build a function to list out each topics with the percentage of videos downloaded. 
    # viewed_parser = subparsers.add_parser("stats", help="Get a list of stats using the built-in Pentester Academy /getstats function")
    # viewed_parser.set_defaults(func=getViewed)

    # finally parse the arg setup for commands I guess?
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        parser.exit(1)

    # finally parse the functions for argparse
    args.func()
#!/usr/bin/python3
import requests,sys, argparse
from bs4 import BeautifulSoup

# define constants
cookies 		  = dict(SACSID='~AJKiYcFgOS1Z5724EXMQEsfMv2wsInv5_hP0uqHtKJ-cX_X-FFb92DLBthCxzVrh6VsooTZu9dyLJHF_cBDu7ozEdKi_dEM1brdGMQ9iEdzk1T5aUwG4gnXDzHu1bgk5k6Z5-u7ORqjWcz10IBeSbhEhim9qMDE5DMgU1m1euBdbRyaQuGrRyp3flUmvM5SWJy0Ly2MFfB8_bs3UFvA-s8uSVZunHFCeY0S41KmYoKqmKYltY0OwGvLaXCxCHzw6SsQeeOgkVaj7Xn8QuIFw7k4HlvoymkM3_pfKn_ox-vsBjy7XYdrPkkN3OTMZqepOXwqgZmDfWzK23EBW9TLewo0xk0zg1TQ0DQ')
base_url 		  = "https://www.pentesteracademy.com"
views_url 		  = "https://www.pentesteracademy.com/members?options=accountlogs"
getstats		  = "https://www.pentesteracademy.com/getstats"
UserAgent         = ""
VIDEOS_URL 		  = "https://www.pentesteracademy.com/topics"
headers 		  = {'useragent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"}
video_list 		  = []
download_list	  = []


# View checker - used to make sure we don't just spam the download button
# gotta fix this to do error checking.  need to add a try catch block
# need to redo the math.  cause it's not always base 100
def getViews():
	views = 0 # gotta initialize it first
	# make sure the request works first
	r = requests.get(views_url,cookies=cookies,headers=headers)
	if (r.status_code) == 200:
		soup = BeautifulSoup(r.text, 'html.parser')
		for results in soup.findAll('p'):
			if "Total plays allowed based on subscription" in results.text:
				total_views = (results.text.split("=",1)[1].strip())
			elif "Total plays till date" in results.text:
				views = (int(total_views) - int(results.text.split("=",1)[1].strip())) # gotta get the total views first.  cause you know... it's not always 100
		# idk why but for some reason returning 0 gives a NoneType so i'm changing this up a bit
		if views == 0:
			return 0
		else:
			return views
	else:
		print("Did not get a 200 OK")



def checkViews():
	views = getViews()
	print ("You have %i views left this month." % views)


# later we need to add in a videoID arg
def getViewed(videoid):
	# so this is sketchy as all hell
	# unwatched = https://s3.amazonaws.com/videos.pentesteracademy.com/spacer.gif
	# watched = https://s3.amazonaws.com/videos.pentesteracademy.com/tick.jpg
	# you can use the /getstats?videoid=<video ID number> to retreive which it is. 
	payload = {'videoid': videoid}
	# r = requests.get('https://httpbin.org/get', params=payload)
	r = requests.get(getstats,params=payload,cookies=cookies,headers=headers)
	if "spacer.gif" in r.url:
		return False
	elif "tick.jpg" in r.url:
		return True
	else:
		print (r.url)
		print ("Error: unknown status_code")
		return True # I guess i'm just going to return True if there are issues.  Future work handle errors better

# 
def download_file(url, title, extension):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter below
    print ("views left: %i" % getViews())
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
	# headers = {'useragent': UserAgent}
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
					videoid =  (link["href"].split("=",1)[1])
					if getViewed(videoid):
						print ("Have already watched...skipping download")
					else:
						print ("Downloading Video Titled: " + title)
						# Check title here for PDF and change the extension based on that
						extension = ".m4v"
						download_file(download_link, title, extension)
				else:
					print("Max views hit for the month")
					sys.exit()

			
# Video List downloader - gets the individual video list from the topic page
def videoList():
	r = requests.get(VIDEOS_URL,cookies=cookies, headers=headers)
	if (r.status_code) == 200:
		soup = BeautifulSoup(r.text, 'html.parser')
	else:
		sys.exit()

	# get which video they want and check validity based on video_list - if not kbye
	choice = input("Which Video Series do you want to download?\n")

	if choice.lower() not in video_list:
		sys.exit()

	for results in soup.find_all("h3", class_="media-heading"):
		if results.text.lower() == choice.lower():
			# at this point we should have found, just a double check nbd
			# i'm doing this to get the full URL since i'm not storing the values in a dict... future work
			for a in results.find_all('a', href=True):
				url = (base_url + a['href']) # this should be the topic ID value
	

	# I should add a check to see if the videos have already been downloaded to make sure we aren't wasting views
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
	# headers = {'useragent': UserAgent}
	r = requests.get(VIDEOS_URL,cookies=cookies, headers=headers)
	if (r.status_code) == 200:
		soup = BeautifulSoup(r.text, 'html.parser')
		print("Video List: \n")
		for results in soup.find_all("h3", class_="media-heading"):
			video_list.append(results.text.lower())
			print (results.text)


def menu():
	# check views first so we aren't wasting requests - they don't grow on trees alright
	views_left = getViews()
	# views should be good at this point
	if views_left > 0:
		print("Total views left: %i" % (views_left))
		answer = input("Downloading? [Y/N]  ")
		# answer = "y"
		if answer.lower() == "y":
			topicList()
			videoList()
		elif answer.lower() == "n":
			print("Exiting")
		else:
			print("Selection must be Y or N")
	else:
		print("You have run out of views for the month")



# main... you know what it do
if __name__ == "__main__":
	# parse dem args my boi
    parser = argparse.ArgumentParser(
        description="Pentester Academy Video Downloader -- Happy Hunting!"
    )
    parser.add_argument("-v","--version", action='version', version='%(prog)s 0.1')

    # setup subparsers for func action
    subparsers = parser.add_subparsers(dest="command")

    # check_ip subparser
    check_parser = subparsers.add_parser("check", help="Check the number of views currently left for the month.")
    check_parser.set_defaults(func=checkViews)

    # download subparser
    download_parser = subparsers.add_parser("download", help="Automate video downloads")
    download_parser.set_defaults(func=menu)

    # list videos
    list_parser = subparsers.add_parser("list", help="List the Topics on Pentester Academy")
    list_parser.set_defaults(func=topicList)

    # eventually i'd like to build a function to list out each topics with the percentage of videos downloaded. 
    # viewed_parser = subparsers.add_parser("stats", help="Get a list of stats using the built-in Pentester Academy /getstats function")
    # viewed_parser.set_defaults(func=getViewed)

    # finally parse the arg setup for commands I guess?
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        parser.exit(1)

    # finally parse the functions for argparse
    args.func()
