# Setup Guide

Invoice generation for locate tools using data extrapolation setup guide


## Pre-requisites

Before following the setup, you must have Python installed and added to PATH. Python 3.6 was used throughout development, and testing with other versions of Python hasn’t been done. However, there shouldn’t be any major problem if a newer version is used. Here’s a separate guide for how to do that if you aren’t sure:
[Real Python: Add Python to PATH](https://realpython.com/add-python-to-path/)

## Setup

### Step 1

To start the setup, open a command-line interface. The example shown in this guide will be Git Bash. Once open, navigate to the place you want to store the program using the command-line interface.

### Step 2

Next, clone the repository of the program: [https://github.com/danhill345/invoice_generation](https://github.com/danhill345/invoice_generation) 
To do this, type `git clone` followed by the link to the repository.

### Step 3

Change into the folder created by cloning the repository, then create a virtual environment by typing `python -m venv env`. Once this is done activate the virtual environment by typing `source env/Scripts/activate`.

### Step 4 (optional)

Type `python -m pip install --upgrade pip` to ensure the version of pip being used is the latest. There may be some issues installing the needed libraries if an older version is used. 

### Step 5

Type `pip install -r requirements.txt` to install the needed libraries to run the program. If none of the libraries are pre-installed, it may take a minute to install all of them. 

### Step 6

Once the libraries have been installed, type `python setup.py`. This will create the database and populate it with dummy data.

### Step 7

Type `python main.py`. This will launch the program and open the login page. By default, there are 4 usernames and one password added into the database. The password for every username is `password` and the usernames are split into two user types: finance and admin.

#### Admin:
Usernames: `adam`, `admin` (password is `password`)

#### Finance:
Usernames: `ian`, `user`  (password is `password`)

### Step 8

Once logged in, you can interact with the program as either user type. There are 19 CSVs in the “Example CSVs” folder that contain the data produced by a C.A.T which can be used to test the system.
