from selenium import webdriver
from bs4 import BeautifulSoup
import requests
from time import sleep

def getNews():
	text_box = browser.find_element_by_class_name("_2S1VP")
	response = "Let me fetch and send top 5 latest news:\n"
	text_box.send_keys(response)
	soup = BeautifulSoup(requests.get(url).content, "html5lib")
	articles = soup.find_all('article', class_="MQsxIb xTewfe R7GTQ keNKEd j7vNaf Cc0Z5d YKEnGe EyNMab t6ttFe Fm1jeb EjqUne")
	news = [i.find_all('a',class_="ipQwMb Q7tWef")[0].text for i in articles[:5]]
	links = [root+i.find('a')['href'][1:] for i in articles[:5]]
	links = [requests.get("http://thelink.la/api-shorten.php?url="+link).content.decode() for link in links]
	for i in range(5):
		text_box.send_keys(news[i] + "==>" + links[i] + "\n")

bot_users = {} # A dictionary that stores all the users that sent activate bot 
while True:
	unread = browser.find_elements_by_class_name("OUeyt") # The green dot tells us that the message is new
	name,message  = '',''
	if len(unread) > 0:
		ele = unread[-1]
		action = webdriver.common.action_chains.ActionChains(browser)
		action.move_to_element_with_offset(ele, 0, -20) # move a bit to the left from the green dot
        
        # Clicking couple of times because sometimes whatsapp web responds after two clicks
		try:
			action.click()
			action.perform()
			action.click()
			action.perform()
		except Exception as e:
			pass
		try:
			name = browser.find_element_by_class_name("_2zCDG").text  # Contact name
			message = browser.find_elements_by_class_name("vW7d1")[-1]  # the message content
			if 'activate bot' in message.text.lower():
				if name not in bot_users:
					bot_users[name] = True
					text_box = browser.find_element_by_class_name("_2S1VP")
					response = "Hi "+name+". Aravind's Bot here :). Now I am activated for you\n"
					text_box.send_keys(response)
			if name in bot_users:
				if 'show' in message.text.lower() and 'news' in message.text.lower():
					getNews()
			if 'deactivate' in message.text.lower():
				if name in bot_users:
					text_box = browser.find_element_by_class_name("_2S1VP")
					response = "Bye "+name+".\n"
					text_box.send_keys(response)
					del bot_users[name]
		except Exception as e:
			print(e)
			pass
	sleep(2) 
#A 2 second pause so that the program doesn't run too fast
#view raw https://github.com/GasComIT/NewsBot hosted with ❤ by GitHub
