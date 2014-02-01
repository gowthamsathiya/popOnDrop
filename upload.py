"""
__author__ = Gowtham
__summary__ = upload files to dropbox using dropbox put_file API
__copyright__ = GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
"""

#import dropbox module
import dropbox

#import python module
import sys
import os

#module to upload file to dropbox
def upload(client,strfilepath):
        filetoupload = open((strfilepath),'rb')
        simplefilename = "/" + strfilepath.split("/")[-1]
        #print simplefilename
        response = client.put_file(simplefilename,filetoupload,overwrite=True)
        return response
