
### Project Title
Item Catalog App
Udacity Full Stack Nanodegree

### Description
Item Catalog App is a dynamic RESTful web application developed using the Python framework Flask along with third-party OAuth authentication. This application deals with a SQLite database which has Category, User and Category Item tables. It is styled using Bootstrap.

This application provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

### Skills Used
    *   Python
    *   HTML
    *   CSS
    *   Bootstrap
    *   Flask
    *   SQLAchemy
    *   Oauth2
    *   Google Login

### Software's used
To complete this project, you'll require the following softwares:

    Python 3
    A text editor, like Sublime or Atom or Visual Studio Code
    Vagrant
    Virtual Box 
    A terminal application like Bash


### Files used
Files
This project contains 3 python file
    database_setup.py    -  to create the database
    lotsofmenus.py       -  to populate the database
    application.py       -  Main python code 

Folders
This project contains 2 folders
    static            - contains the style sheets
    templates         - HTML templates of all the files

    
### Executing Project
Requirements
To run this final project : 

   1.  Install Vagrant and VirtualBox
   2.  Clone the Vagrantfile from the Udacity Repo
   3.  Clone this repo into the catlog/ directory found in the Vagrant directory
   4.  Run vagrant up to run the virtual machine, then vagrant ssh to login to the VM
   5.  Navigate to the /catalog directory inside the vagrant environment
   6.  Run database_setup.py to create the database
   3.  Run Demodatawithuser.py to populate the database
   4.  Run application.py and navigate to localhost:8000 in your browser

### JSON Endpoints
    
    1.  Catalog JSON: /catalog/catalog.json - Returns JSON of all items in catalogitems.
    2.  Categories JSON: /catalog/<int:category_id>/JSON - Returns JSON of all categories in catalog
    3.  Category Items JSON: /catalog/<int:category_id>/<int:item_id>/JSON - Returns JSON of selected item in catalog



### Credits
Udacity Full Stack Web Developer Nano Degree :
https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004

