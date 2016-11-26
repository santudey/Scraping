import random 
import os
import requests
from bs4 import BeautifulSoup

user_agents = [  
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.142 Safari/535.19',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:8.0.1) Gecko/20100101 Firefox/8.0.1',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.151 Safari/535.19',
 	'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0'
]

base_url = "https://www.youtube.com/results?search_query="

def change_string(search_query):
	words = search_query.split()
	ans_query = ""
	for word in words:
		ans_query = ans_query + word.lower() + "+"
	return ans_query[:len(ans_query)-1]

def correct_string(search_query):
	words = search_query.split()
	ans_query = ""
	for word in words:
		ans_query = ans_query + word + " "
	return ans_query[:len(ans_query)-1]

def get_requests(url):
	headers={'User-Agent':user_agents[random.randint(0,8)]}
	r = requests.get(url,headers = headers)
	r.raise_for_status()
	html = r.text.encode("utf8")
	return html

def download_video_youtube(url,tagline,song_name,artist_name):
	html = get_requests(url)
	print url
	soup = BeautifulSoup(html, "lxml")
	ex = soup.find('a',attrs = {'class':"yt-ui-ellipsis-2"})
	video_url = "https://www.youtube.com" + ex['href']
	# print (tagline)
	tt = artist_name + " - " + song_name + ".%(ext)s"
	os.system("youtube-dl --extract-audio --audio-format mp3 -o " + "\"" + tt + "\"" + " " + video_url)
	print()

def get_song_name():
	url = "http://www.saavn.com/s/featured/hindi/Weekly_Top_Songs?qt=a&st=1&t=1480160054116&ct=1930160659"
	html = get_requests(url)
	soup = BeautifulSoup(html, "lxml")
	songslist = soup.findAll('div', attrs={'itemprop':"track"})
	for songs in songslist:
		ex = songs.find('meta',attrs={'itemprop':"name"})
		ex2 = songs.find('meta',attrs={'itemprop':"inAlbum"})
		song_name = ex["content"]
		artist_name = ex2["content"]
		search_query = song_name + " "+artist_name
		search_query = change_string(search_query)
		tagline="hello"
		download_video_youtube(base_url + search_query,tagline, correct_string(song_name), correct_string(artist_name))
		os.system(u"osascript -e 'display notification \""+song_name +"\" with title \""+artist_name +"\" '")



def main():
	print()
	get_song_name()

if __name__ == '__main__':
	main()

