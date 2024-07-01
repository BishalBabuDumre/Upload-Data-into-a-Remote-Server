# Code to upload into a remote server
import os
import ftplib
from ftplib import FTP_TLS
from pathlib import Path

# Get home directory
localPath = os.path.join(Path.home(), ‘Pokhara’)

# Environment variables to connect to a remote server
website = ‘www.pqr.com’
username = ‘abc@xyz.com’
password = ‘XXXXXXXXXXX’

# Connecting to the remote server
folders = [‘/1’, ’/2’, ‘/3’, ‘/4’, ‘/5/ktm’]
for folder in folders:
    ftp = FTP_TLS(website, username, password)
    try:
        ftp.cwd(folder)
    except ftplib.error_perm:
        continue
    try:
    # Get list of files in folder
        files = ftp.nlst()
    except ftplib.error_perm as resp:
        if str(resp) == "550 No files found":
            print("No files in this directory")
        else:
            raise

# Lists all the files that we already have in the local folder to only download missing ones
    if folder[2:]==‘ktm’:# Setting a different path for 5/ktm folder
        localDataPath = os.path.join(Path.home(), folder[2:])
    else:    
        localDataPath = os.path.join(localPath, folder)

    localDataFiles = os.listdir(localDataPath)

# Compares the two lists
    missing = list(sorted(set(localDataFiles) - set(files)))

# Print the names of the missing files
    print(f'In total there are missing: {len(missing)}')
    if (missing != 0):
        print("Uploading...")
        for filename in missing:
            with open(os.path.join(localDataPath, filename), 'rb') as f:
                try:
                    ftp.storbinary(f'STOR {filename}', f)
                except:
                    print(filename, 'is empty')  
    ftp.close()
