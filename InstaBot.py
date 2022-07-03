from selenium import webdriver
import BotEngine
#from selenium.webdriver.chrome.service import Service
#from webdriver_manager.chrome import ChromeDriverManager

chromedriver_path = '/Users/exampleuser/Library/Python/3.8/bin/chromedriver' 
webdriver = webdriver.Chrome(executable_path=chromedriver_path)

#s=Service('/Users/exampleuser/Library/Python/3.8/bin/chromedriver')
#webdriver = webdriver.Chrome(service=s)
BotEngine.init(webdriver)
BotEngine.update(webdriver)

webdriver.close()
#