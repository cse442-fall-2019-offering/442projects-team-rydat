# Instructions on how to run the application via VirtualBox

1. Visit [https://www.virtualbox.org/wiki/Downloads] to download Virtualbox if you do not have it already
2. After installation, download the .ova file for the virtual machine (VM) image that holds our application 
  - It is 6 GB so it will take a while
3. After getting the VM image, open the Virtualbox application and select "Tools" then "Import"
4. Navigate to the directory where you have saved the .ova file and click "Next"
5. You may change the name of the VM but be sure to check the "Base Folder" since that is where the VM will be saved 
6. Keep all other settings then click "Import"
7. After successfully importing, start up the VM
8. Log into "Alan Pinkhasik" with the password "TempPass442@"
9. Open the terminal and run these commands

```
cd Desktop/Environments 
source 442_proj/bin/activate (this activates the virtualenv)
cd django_project
python3 manage.py runserver **MUST BE PYTHON3, NOT JUST PYTHON**
```

10. After starting up the server, head to Google Chrome and type "localhost:8000" in the URL
11. You have reached the application and are now able to use it!
12. To stop the server, head back into the terminal and press Ctrl+C
13. To stop the virtualenv, type "deactivate" without the quotes into the terminal
