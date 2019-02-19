# Item Catalog

This is a simple Python application built on top of Flask to:

1. Demonstrate CRUD operations.
2. Demonstrate authorization and authentication in application using third party services.

## Set up 

To begin clone this project save it to a folder titled "Catalog Project". At the start this project create the database by first
running `python catalog_database_setup.py` in your terminal. From here you can either create your own data or run 
`python catalog_data.py` in your terminal to set up some sample data to get you started. To start the app run `python catalog_project.py`
in your terminal and visit `http://localhost:5000/` in your browser to view the main page.


## Accessing JSON endpoints. 

This project comes with two JSON endpoints built in. The first endpoint `http://localhost:5000/clothing/JSON` will output all current item groups that are present within the database. The second endpoint `http://localhost:5000//clothing/<int:clothing_group_id>/JSON` will list all items with item details that are within the specified item group. 