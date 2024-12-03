# About Pokemon Draft Database
  A database created with the collaborative efforts from Jhun Baclaan, Rhyanne Zyrelle-Javier, and Matthew Holck. This database is a project for our CSCI-3301 class and is meant to be a demo of a database that could replace the tedious software and websites that are often used by league hosters.
# Installation
There are a few things you will need to install before running the database.
1. MYSQL Workbench and MYSQL Community Server. **Install these if you plan to use MYSQL to run the database.** Please download the latest version for your OS from [Oracle's official website](https://dev.mysql.com/downloads/workbench/). MYSQL Community Server can be downloaded from [here](https://dev.mysql.com/downloads/mysql/8.0.html).
2. Python & Anaconda. Again, please download the latest versions of both from their websites. Python's can be found [here](https://www.python.org/downloads/) and Anaconda's can be found [here](https://www.anaconda.com/download).
3. Python dependencies; specifically Streamlit, pandas, pypokedex, and pymysql. You will be able to install these via your terminal/command prompt. Refer to [the setup instructions](README.md#setup-mysql) for quick installation.**If you are setting up via pandas, refer to [this set of instructions](README.md#setup-pandas)**
4. The necessary files. These are packaged as `database_mysqlpkg.zip` and `database_pandaspkg.zip` for MYSQL and pandas setup, respectively.
# Setup (MYSQL)
1. Start by creating an environment. Please do this via the Anaconda Navigator; name it whatever you'd like, and you do not need to change any settings with this newly-made environment.
2. Via Anaconda Navigator, open the environment's terminal and **activate** the environment with `conda activate ENV_NAME`
3. With the environment activated, use `pip` to install the required python dependencies:
```
pip install streamlit
pip install pandas
pip install pypokedex
pip install pymysql
```
Keep this terminal window open.
**To check if your installation was successful, use `pip list | grep MODULE_NAME`. This will return any matches along with their versions.**

4. Open up MYSQL Workbench and create a new database. Use these specific settings:
```
host: 127.0.0.1
user: root
password: junesworld
```
Create a schema in your newly created database. Name it schema1. Don't change any of its other settings.

5. In the schema, insert all of the SQL code found in our database's proposal doc. At this point, you will be ready to run the code.
# Setup (pandas)
**This setup process excludes the MYSQL Workbench altogether, as well as the pymysql module installation.**

**Before touching any of the applications you just installed, first download the CSVs and .py files included in the repository. This will ease the data-import process for setting up via pandas.**

1. Create an environment in Anaconda. Please do this via the Anaconda Navigator; name it whatever you'd like, and you do not need to change any settings with this newly-made environment.
2. Via the Anaconda Navigator, open the environment's terminal and **activate** the environment with `conda activate ENV_NAME`
3. With the environment activated, use `pip` to install the required python dependencies:
```
pip install streamlit
pip install pandas
pip install pypokedex
```
Keep this terminal window open.
**To check if your installation was successful, use `pip list | grep MODULE_NAME`. This will return any matches along with their versions.**
# Running the Database
Running the database is simple, no matter how you set up the database.
## If You Setup via MYSQL
1. From the Anaconda environment terminal, run the following command: `streamlit run testing.py`. This will show the user login screen. For a draft screen, run `streamlit run testing2.py`.
2. You will be able to interact with the screens and navigate the database as you'd like.
## If You Setup via MYSQL
1. From the Anaconda environment terminal, run the following command: `streamlit run test2.py`. This will show the user login screen.
2. You will be able to interact with the screens and navigate the database as you'd like.
