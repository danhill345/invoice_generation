#Setup guide
A setup guide for the invoice generation system for C.A.Ts (change based on what title we end up with)
#Pre-requisites
Before following the setup, you must have python installed and added to PATH, python 3.6 was used throughout development and testing with other versions of python hasn’t been done however there shouldn’t be any major problem if a newer version is used. Here’s a separate guide for how to do that if you aren’t sure
https://realpython.com/add-python-to-path/
#Setup
##Step 1:
To start the setup open a command-line interface, the example shown in this guide will be Git Bash. Once open navigate to the place you want to store the program using the command line interface. 
 
##Step 2:
Next clone the repository of the program: https://github.com/danhill345/invoice_creation_system 
To do this type git clone then the link to the repository.
 
##Step 3:
Change into the folder created by cloning the repository then create and activate the virtual environment 
 
 

##Step 4 (optional):
Type “python -m pip install --upgrade pip” to ensure the version of pip being use is the latest, there may be some issues installing the needed libraries if an older version is used.  
##Step 5:
Type “pip install -r requirements.txt” to install the needed libraries to run the program, if none of the libraries are pre-installed it may take a minute to install all of them. 
##Step 6:
Once the libraries have been installed type “python setup.py”. This will create the database and populate it with dummy data.
 
##Step 7:
Type “python main.py”, this will launch the program and open the login page, by default there are 4 usernames and one password added into the database. The password for every username is “password” and the usernames are split into two user types, finance and admin. 
 
Admin:
Usernames: adam/admin (password is password)
 
Finance:
Usernames: ian/user  (password is password)
 
Step 8:
Once logged in you can interact with the program has either user type, there are 19 csvs in “Example CSVs” that contain the data produced by a C.A.T which can be used to test the system



