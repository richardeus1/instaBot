# instaBot
A simple bot to obtain more followers and likes on Instagram. It uses the Full Xpath to detect the elements. Pending to fix unfollow function.
Code has a lot of patches due to instagram is constantly being modified to avoid these bots. For this reason, the code is not on his best shape. 

Quick environment setup: 

First You will need to setup bash profile as default environment in terminal.

Now, You need to setup python 3.X by default (using alias):

Now, You need to install custom Chrome browser and disable its updates. (disabling all kind of updates is a nice plus)

Give permissions to bash profile and python3 to file access. 

Proceed by installing mysql and mysql workbench
https://dev.mysql.com/downloads/mysql/
https://dev.mysql.com/downloads/workbench/

Install selenium for python
https://www.geeksforgeeks.org/how-to-install-pip-in-macos/
https://selenium-python.readthedocs.io/installation.html
Install python mysql connector
https://dev.mysql.com/downloads/connector/python/

Create the database and table (database name instabot, table name followed_users with 2 columns username and date_added):

Clone my instagram bot python script project.

Create the launchtl agent job

https://davidhamann.de/2018/03/13/setting-up-a-launchagent-macos-cron/

https://www.maketecheasier.com/use-launchd-run-scripts-on-schedule-macos/

To load the agent :
cd ~/Library/LaunchAgents/
launchctl bootstrap gui/501 com.instabot.customagentname.plist

To unload the agent:
cd ~/Library/LaunchAgents/
launchctl bootout gui/501 com.instabot.customagentname.plist

manual launch the agent:
launchctl kickstart -k gui/501/com.instabot.customagentname
