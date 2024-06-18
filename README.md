A web based software solution for managing and operating stores and warehouses. It is meant to be a clean and simple solution for small and midsize businesses. The key advantages of Ergo ERP are:
* Cloud-based solution - device independent, with responsive design , allows users to switch devices, based on their needs, stores data securely, allows for real time cooperation between departments.
* Has the ability to track lots and expiration dates of products, which allows its use with all types of merchandise, unlike many other similar solutions. 
* Keeps visible options and menus to a bare minimum at any time, so that chances for operator error are reduced and training of new employees is faster and easier.



**Setup Instructions**

Environment Setup - please use the requirements.txt file to install the necessary packages:

```bash
pip install -r requirements.txt
```
After setting up your environment and running migrations, load the initial data using the fixtures provided:

```bash
python manage.py loaddata initial_data_fixtures.json    
```   