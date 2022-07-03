from time import sleep
from selenium.common.exceptions import NoSuchElementException
import datetime
import DBUsers, Constants
import traceback
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

followed = 0
countLikes = 0
limitFollowed = 13
limitLikes = 13
next_button = Keys.RIGHT


def login(webdriver):
    #Open the instagram login page
    webdriver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
    #sleep for 3 seconds to prevent issues with the server
    sleep(3)
    #Find username and password fields and set their input using our constants
    username = webdriver.find_element_by_name('username')
    username.send_keys(Constants.INST_USER)
    password = webdriver.find_element_by_name('password')
    password.send_keys(Constants.INST_PASS)
    #Get the login button
    try:
        button_login = webdriver.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button')
    except:
        button_login = webdriver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div')

    #sleep again
    sleep(2)
    #click login
    button_login.click()
    sleep(20)
    #In case you get a popup after logging in, press not now.
    #If not, then just return
    try:
        notnow = webdriver.find_element_by_css_selector(
            'body > div.RnEpo.Yx5HN > div > div > div.mt3GC > button.aOOlW.HoLwm')
        notnow.click()
    except:
        return
    

def follow_people(webdriver):
    #all the followed user
    prev_user_list = DBUsers.get_followed_users()
    #a list to store newly followed users
    new_followed = []
    #counters    
    global followed 
    likes = 0
    global countLikes

    #Iterate through all the hashtags from the constants
    for hashtag in Constants.HASHTAGS:
        #Visit the hashtag
        webdriver.get('https://www.instagram.com/explore/tags/' + hashtag+ '/')
        sleep(12)
        
        #Get the first post thumbnail and click on it  
        first_thumbnail = webdriver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div/div[2]')

        first_thumbnail.click()
        sleep(random.randint(1,3))

        try:
            #iterate over the first 240 posts in the hashtag
            for x in range(1,3):
                t_start = datetime.datetime.now()
                #Get the poster's username                   
                username = ''
                WebDriverWait(webdriver, 7).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[1]/div/header/div[2]/div[1]/div[1]')))
                username = webdriver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[1]/div/header/div[2]/div[1]/div[1]').text
                print("printing username {0}".format(username))
                if username == '':
                     
                    webdriver.find_element_by_css_selector('body').send_keys(next_button)
                    sleep(random.randint(80, 99))
                
                    
                likes_over_limit = False
                sleep(6)
                try:
                    #get number of likes and compare it to the maximum number of likes to ignore post  
                    likes = webdriver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[2]/div/div/div/a/div/span').text
                    likes = likes.replace(',', '')
                    likes = int(likes)
                        
                    if likes > Constants.LIKES_LIMIT:
                        print("likes over {0}".format(Constants.LIKES_LIMIT))
                        likes_over_limit = True

                    print("Detected: {0}".format(username))
                    
                    if not likes_over_limit:
                        action = ActionChains(webdriver);
                        sleep(6)
                        firstLevelMenu = webdriver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[1]/div/header/div[2]/div[1]/div[1]/div/span/a')
                        action.move_to_element(firstLevelMenu).perform()
                        
                        sleep(6)
                        if(webdriver.find_elements_by_xpath("/html/body/div[6]/div/div/div/div[4]/button")):
                            itExists = True
                            
                            secondLevelMenu = webdriver.find_element_by_xpath("/html/body/div[6]/div/div/div/div[4]/button")
                        else:
                            itExists = False
                            
                            if countLikes < limitLikes:
                                
                                button_like = webdriver.find_element_by_css_selector("span._aamw > button  > div > span > svg")
                                valueButton = button_like.get_attribute('aria-label')
                                if valueButton == 'Like':
                                    button_like.click()
                                    likes += 1
                                    countLikes += 1
                                print("Liked {0}'s post, #{1}, Total likes from me: {2}".format(username, likes, countLikes))
                                sleep(random.randint(80, 118))
                                webdriver.find_element_by_css_selector('body').send_keys(next_button)
                                sleep(random.randint(80, 99))
                            
                            elif countLikes >= limitLikes:
                                followed = 0
                                countLikes = 0
                                sleep(10800)
                                webdriver.find_element_by_css_selector('body').send_keys(next_button)
                            
                            
                        
                        if itExists:    
                            
                            action.move_to_element(secondLevelMenu).perform()
                            #Don't press the button if the text doesn't say follow 
                            if secondLevelMenu.text == 'Follow' and followed < limitFollowed:
                                #Use DBUsers to add the new user to the database
                                DBUsers.add_user(username)
                                #Click follow                    
                                
                                secondLevelMenu.click()
                                sleep(4)
                                followed += 1
                                print("Followed: {0}, #{1}".format(username, followed))
                                new_followed.append(username)
                                
                            elif secondLevelMenu.text == 'Following' or secondLevelMenu.text == '':
                                sleep(4)
                            
                            elif followed >= limitFollowed:
                                followed = 0
                                countLikes = 0
                                sleep(10800)

                                
                            else:
                                sleep(4)    
                        
                        if countLikes < limitLikes and itExists:

                            button_like = webdriver.find_element_by_css_selector("span._aamw > button  > div > span > svg")
                            valueButton = button_like.get_attribute('aria-label')
                            if valueButton == 'Like':
                                button_like.click()
                                likes += 1
                                countLikes += 1
                   
                            print("Liked {0}'s post, #{1}, Total likes from me: {2}".format(username, likes, countLikes))
                            sleep(random.randint(80, 118))
                            webdriver.find_element_by_css_selector('body').send_keys(next_button)
                            sleep(random.randint(80, 99))

                        elif countLikes >= limitLikes:
                            followed = 0
                            countLikes = 0
                            sleep(10800)
                            webdriver.find_element_by_css_selector('body').send_keys(next_button)
                            
                    else:
                        webdriver.find_element_by_css_selector('body').send_keys(next_button)
                        sleep(random.randint(80, 99))
                        
                    
                except NoSuchElementException:

                    continue
                
                finally:
                    
                    t_end = datetime.datetime.now()
                    #calculate elapsed time
                    t_elapsed = t_end - t_start
                    print("This post took {0} seconds".format(t_elapsed.total_seconds()))
                    '''if followed == limitFollowed and countLikes == limitLikes:
                        print(datetime.datetime.now())
                        webdriver.quit()
                        sys.exit()'''


        except NoSuchElementException:

            continue

        #add new list to old list
        for n in range(0, len(new_followed)):
            prev_user_list.append(new_followed[n])
        print('Liked {} photos.'.format(likes))
        print('Followed {} new people.'.format(followed))
        

def unfollow_people(webdriver, people):
    #if only one user, append in a list
    global followed

    if not isinstance(people, (list,)):
        p = people
        people = []
        people.append(p)

    for user in people:
        try:
            webdriver.get('https://www.instagram.com/' + user + '/')
            sleep(5) 
            unfollow_xpath = '/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[2]/button'
            unfollow_confirm_xpath = '/html/body/div[5]/div/div/div[3]/button[1]'   

            if webdriver.find_element_by_xpath(unfollow_xpath).text == "Following" and followed < limitFollowed:
                sleep(random.randint(4, 15))
                webdriver.find_element_by_xpath(unfollow_xpath).click()
                sleep(2)
                webdriver.find_element_by_xpath(unfollow_confirm_xpath).click()
                sleep(4)
                followed += 1
            DBUsers.delete_user(user)

        except Exception:
            traceback.print_exc()
            continue
    print("people unfollowed ",followed)
