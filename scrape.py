import requests
from bs4 import BeautifulSoup
import pprint


def get_hackernews_pages(megalinks, megasubtext, pages):
	for i in range(1, int(pages) + 1):
		res = requests.get(f'https://news.ycombinator.com/?p={i}')
		soup = BeautifulSoup(res.text, 'html.parser')
		links = soup.select('.titleline > a') #array of the links
		subtext = soup.select('.subtext') #array of points
		megalinks = megalinks + links
		megasubtext = megasubtext + subtext
	return (megalinks, megasubtext)


def sort_stories_by_votes(hnlist):
	return sorted(hnlist, key=lambda k:k['points'], reverse=True)

def create_custom_hackernews(links, subtext):
	hn = []
	for idx, item in enumerate(links):
		title = links[idx].getText()
		href = links[idx].get('href', None)
		# get function is used to get the value for attribute passed to it. Here it gives us the href link 
		# the second parameter we pass above is 'None' which means if the href is broken or not available then the default is set to None.
		#  NOTE: "This is how a programer should think about possible conditions when solving a problem" 
		vote = subtext[idx].select('.score')
		if len(vote):
			points = int(vote[0].getText().replace(' points', ''))
			if points >= 100:
				hn.append({"title": title, "link": href, "points": points})
	return sort_stories_by_votes(hn)

def main():
	megalinks_arr = megasubtext_arr = []
	pages = 2
	hn_data = get_hackernews_pages(megalinks_arr, megasubtext_arr, pages)
	all_links = hn_data[0]
	all_subtext = hn_data[1]
	pprint.pprint(create_custom_hackernews(all_links, all_subtext))

main()

