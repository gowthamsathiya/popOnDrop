"""
__author__      = Gowtham
__summary__     = Module to check dropbox for any **addition/**update/deletion to file.
                    **only file of type .doc and .txt is used
__copyright__   = GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
"""

#import submodules
import Accesstoken

#import dropbox module
import dropbox

#import python module
import requests
import time
from datetime import datetime
import sys

#import pyQt4 module
from PyQt4 import Qt
from PyQt4 import QtCore


#module to pop message on **addition/**update/deletion to file.
#**only file of type .doc and .txt is used
#Part of this coding is done with the help of https://www.dropbox.com/developers/blog/63/low-latency-notification-of-dropbox-file-changes
def popMessage():
    app = Qt.QApplication(sys.argv)

    access_token = Accesstoken.getaccesstoken()
    client = dropbox.client.DropboxClient(access_token)

    cursor = None
    while True:
        result = client.delta(cursor)
        #print result
        #print '------------------------------------------------------------'
        cursor = result['cursor']
        #print cursor
        #print '------------------------------------------------------------'
        if result['reset']:
            print 'RESET'

        for path, metadata in result['entries']:
            if metadata is not None and metadata['is_dir'] == False:
                if metadata['mime_type'] == 'application/msword' or metadata['mime_type'] == 'text/plain': #to restrict to .doc and .txt file type
                    mtime = time.strptime(" ".join(metadata['modified'].split()[0:-1]), '%a, %d %b %Y %H:%M:%S')
                    mmtime = datetime.fromtimestamp(time.mktime(mtime))
                    timenow = datetime.fromtimestamp(time.mktime(time.gmtime()))
                    dtime = ((timenow - mmtime).total_seconds()) / 3600
                    #print dtime
                    if dtime < 1: #files modified within past one hour
                        print '%s was created/updated' % path
                        alert = Qt.QLabel(path + " was created or updated")
                        alert.move(1000, 50)
                        alert.show()
                        app.exec_()
            else:
                print '%s was deleted' % path
                alert = Qt.QLabel(path + " was deleted")
                alert.move(1000, 50)
                alert.show()
                app.exec_()


    if not result['has_more']:

        changes = False
        while not changes:
            response = requests.get('https://api-notify.dropbox.com/1/longpoll_delta',
                                    params={
                                        'cursor': cursor, # latest cursor from delta call
                                        'timeout': 120     # default is 30 seconds
                                    })
            data = response.json()

            changes = data['changes']
            if not changes:
                print 'Timeout, polling again...'

            backoff = data.get('backoff', None)
            if backoff is not None:
                print 'Backoff requested. Sleeping for %d seconds...' % backoff
                time.sleep(backoff)
                print 'Resuming polling...'