CRUD Application Testing package 
***
<b> Crud </b> is a python package consist of an application 
built on Flask framework to perform Create , Read , Update and Delete 
Operations on DB. It also contains the test cases in test_app.py module.
<br>
<br>

* Modules
  * app
  * database
  * test_app

***
#Installation
```buildoutcfg
pip install -i https://test.pypi.org/simple/ crud-application-toseef==0.0.6
```
***
After installing the package create the following python file
#Setting username and password for SQL 
set_cred.py
```python

from crud.database import Credentials

username = ""   #set your sql username
password = ""   #set your sql password
cred_obj = Credentials(username=username, password=password)
cred_obj.set()



```
run this script once and it will set the provided
username and password to the environment file
***
#Usage
test_package.py
```python
from crud import test_app

obj = test_app.FlaskTest()
obj.setUpClass()
obj.setUp()
obj.test_01_home_page_renders_successfully()
obj.test_02_file_upload_successful()
obj.test_03_add_view_rendered_successfully()
obj.test_04_record_added_successfully()
obj.test_05_edit_view_rendered_successfully()
obj.test_06_record_updated_successfully()
obj.test_07_record_deleted_successfully()
obj.test_09_check_updated_record_in_db()
obj.test_10_record_deleted_in_db()
obj.test_11_add_duplicate_record_in_db()
obj.test_12_update_duplicate_data_in_db()
obj.test_13_delete_invalid_data_in_db()
obj.test_14_wrong_url()
obj.test_08_add_invalid_row_in_db()

```

Create the above test_package.py file and run the program.
It should run without any error and all test cases will pass
for CRUD application testing.