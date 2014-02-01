"""
__author__ = Gowtham
__summary__ = Generate and store access token from dropbox using app_key and app_secret and return the stored access token
__copyright__ = GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
"""

#import dropbox module
import dropbox

#import python module
import os

#module to return access token
def getaccesstoken():
    access_token = ""
    if os.path.exists('atfile.txt'): #Accesstoken is generated and stored in atfile.txt already
        atfile = open('atfile.txt','r')
        access_token = atfile.readline()

    else: #Generating access token using app_key and app_secret
    	atfile = open('atfile.txt','w')
    	app_key = 'xxxxxxxxxxx'
    	app_secret = 'xxxxxxxxxxx'
        flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
        print 'Go here and "allow": %s' % flow.start()
    	code = raw_input('Paste in your authorization code: ').strip()
        access_token, _ = flow.finish(code)
        atfile.write(access_token)
        atfile.close()
    return access_token
