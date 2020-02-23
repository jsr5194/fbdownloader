from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import argparse
import re

parser = argparse.ArgumentParser(description='Download a linked video from Facebook')
parser.add_argument('-l', '--link', type=str, required=True, help='link to a facebook video in the format https://www.facebook.com/<video id>/videos/<video id>/')
parser.add_argument('-o', '--outfile', type=str, default="facebook_video.mp4", help='filename for the downloaded video')
args = parser.parse_args()

def main():
	# verify that the provided video link uses the allowed format
	uri = args.link
	uriRegex = "^https://www.facebook.com/\d+?/videos/\d+?/?$"
	if re.match(uriRegex, uri):
		# request the provided uri
		# this is needed to extract the actual video uri
		# currently need to use selenium because facebook checks for javascript and the noscript page gets served with requests not coming from a browser
		# TODO: implement a check to switch between other browsers
		driver = webdriver.Safari()
		driver.get(uri)
		resp = driver.page_source

		# parse the response and extract the video link
		soup = BeautifulSoup(resp, "html.parser")
		videoUri = soup.video.get("src")

		# end the selenium session
		driver.close()

		# request the actual video
		resp = requests.get(videoUri)
		
		# write the video data out to the supplied filename
		with open(args.outfile, "w+") as f:
			f.write(resp.content)
	else:
		print("ERROR: Bad link provided")






if __name__ == "__main__":
	main()
