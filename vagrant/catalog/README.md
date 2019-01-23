Item Catalog Manager
This is a web application to manage a lit of items within different categories. The system provides
a user registration and authentication system. Only registrated users can add, edit or delete their
own items.

Software/Libarry Required
1. Python3
2. Vagrant
3. Linux-based virtual machine (VM)
4. psycopg2

Getting Start
1. Install vagrant and VirtualBox
2. Clone Vagrantfile @ https://github.com/udacity/fullstack-nanodegree-vm/vagrant
3. Run vagrant up to launch the virtual machine
4. Login to the virtual machine by vagrant ssh 
5. Run database_setup.py to set up database for the project
6. Run insertData.py to populate tables with data
7. Run the application within the VM 
8. Access the application @ http://localhost:8009

End Points
1. Homepage http://localhost:8009
2. Show list of items for a category: http://localhost:8009/catalog/<int:category_id>/items
3. Show a specific item: http://localhost:8009/catalog/<int:category_id>/items/<int:item_id>
4. Endpoint for login: http://localhost:8009/catalog/login
4. After login, a user can add item http://localhost:8009/catalog/items/new
5. After login, a user can update item http://localhost:8009/catalog/items/<int:item_id>/edit
6. After login, a user can delete item /catalog/items/<int:item_id>/delete
7. JSON endpoint: http://localhost:8009/catalog.json

Author
Maggie Zhou
Fullstack Web Developer

License
This project is licensed under the MIT License
