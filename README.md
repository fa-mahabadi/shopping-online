# Store-website
# Store-website


Project Description


In this website, the store manager and employees can define new products on their website or the previous products.
Edit or delete. Also, the products defined in the store have their own category.
And it can be subject to discount. All these changes can be done through the store manager panel.
On the other hand, customers of the collection can add the desired product to their shopping cart after viewing the product from the main page of the site.
Add and finally place an order by choosing an address from among your addresses.
Each order can include several different products with different quantities


---------------------------------------------------

setup project:

for setup this project follow below steps:

1. git clone 
    git clone https://github.com/fa-mahabadi/Store-website.git
2. install requirements
    pip install -r requirements.txt
3. create venv
    python -m venv venv
4. create table, superuser,runserver
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver