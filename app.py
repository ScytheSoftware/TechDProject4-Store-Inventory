#DaVonte' Whitfield
#Tech Degree Project 4 
#Store Inventory

from collections import OrderedDict
import datetime
import os
import csv
import re

from peewee import *

db = SqliteDatabase('inventory.db')


class Product(Model):

	product_id = PrimaryKeyField() #use built-in primary_key. look it up
	product_name = CharField(max_length = 255, unique =True)
	product_price = IntegerField(default = 0.00)
	product_quantity = IntegerField(default = 0)
	date_updated = DateTimeField(default = datetime.datetime.now)

	class Meta:
		database = db


def initialize():
	#Create the database
	db.connect()
	db.create_tables([Product], safe = True)


def clean_data(data):
	#cleaning and converting the data
	num = 0

	for index in data: #index isn't being used in this loop. Only wanted to go through the data and place it back; didn't want a copy.

		#For quantity
		(data[num])['product_quantity'] = int((data[num])['product_quantity'])

		#price
		temp_num = re.sub(r'\$', '',(data[num])['product_price'])
		temp_num = float(temp_num)
		temp_num = temp_num * 100
		(data[num])['product_price'] = temp_num

		#datetime
		(data[num])['date_updated'] = str(datetime.datetime.strptime((data[num])['date_updated'], '%m/%d/%Y'))
		(data[num])['date_updated'] = re.sub(r'.00','',(data[num])['date_updated']) #keeping the formatting
		num += 1

	return data


def add_data():

	number_count = 1 #This will count through the records

	for product in cleaned_dict:
		try:
			Product.create(product_id = number_count,
							product_name = product['product_name'],
							product_price = '$' + str((product['product_price'] / 100)),
							product_quantity = product['product_quantity'],
							date_updated =  re.sub(r'.00','',   #keeps the normal format
							re.sub(r'-','/', str(datetime.datetime.strptime(str(product['date_updated']), '%Y-%m-%d')))) #Then turn '-' into '/'
							)

		except IntegrityError:
			product_record = Product.get(product_name = product['product_name'])
			
			if product_record.product_id != number_count: #When it notice the product exist in a different spot, it will run this
				product_record.product_id = product_record.product_id # It updates that spot
				number_count -= 1 #To keep the ordering of the id, minus one because it adds one at the end
			else:
				product_record.product_id = number_count

			product_record.product_price = '$' + str((product['product_price'] / 100))
			product_record.product_quantity = product['product_quantity']
			product_record.date_updated = re.sub(r'.00','',   #keeps the normal format
							re.sub(r'-','/', str(datetime.datetime.strptime(str(product['date_updated']), '%Y-%m-%d')))) #Then turn '-' into '/'
			#product_record.save()
		number_count += 1
		

def menu_loop():
	"""Menu"""
	choice = None

	while choice != 'q':
		print("")
		print("Enter [q] to quit.")

		for key, value in menu.items(): #loop through the dictionary and print
			print('[{}]) {}'.format(key,value.__doc__)) #the 'value__doc__': Because our values are functions, we need to use __doc__ to use the function

		while True:
			choice = input('>> ').lower().strip()

			if choice != 'a' and choice != 'b' and choice != 'v'  and choice != 'q':
				print("Invalid input. The options are [a], [b], [q], [v]. Select one of the option.")
			else:
				break

		if choice in menu:
			clear_screen()
			menu[choice]()

def clear_screen():
	os.system('cls' if os.name == 'nt' else 'clear')

def get_max_item_count():
	count = 0
	max_loop_count = Product.select()

	for items in max_loop_count: #Counting each item stored
		count +=1

	return count

def view_entries():
	"""View Data by ID."""
	
	number_of_items = get_max_item_count()

	while True:
		selection = input("Select an entry by ID between 1-" + str(number_of_items) + ": ")
		try:
			entries = Product.get(product_id = selection)
			break
		except:
			print("That ID selection isn't in the database. Try again\n")

	print("")
	print("Selection: " + str(entries.product_id) +
			" | "+ entries.product_name +
			" | "+ str(entries.product_price) +
			" | "+ str(entries.product_quantity) +
			" | "+ entries.date_updated)

	
def add_entry():
	"""Add Store Item"""

	product_name = input("Product Name:")

	clear_screen()
	while True:
		product_price = input("Example 489 = 4.89\nProduct Price")
		try:
			int(product_price) #Checking to see if it's a number
			break
		except:
			print("Invalid character were entered. Only numbers can be entered for the price. Try again\n")

	clear_screen()
	while True:
		product_quantity = input("Product Quantity:")
		try:
			int(product_quantity) #Checking to see if it's a number
			break
		except:
			print("Invalid character were entered. Only numbers can be entered for the quantity. Try again\n")

	now = datetime.datetime.now()
	date_updated = now.strftime('%m/%d/%Y') #getting the format for date

	new_item = {'product_name': product_name, 
				'product_price': product_price, 
				'product_quantity': product_quantity,
				'date_updated': date_updated}

	clear_screen()
	print(new_item['product_name'].title() + 
		" | " + '$' + str((float(new_item['product_price']) / 100)) + 
		" | " + str(new_item['product_quantity']) + 
		" | " + new_item['date_updated'])


	while True:
		response = input('Save entry? [Y]es | [N]o :').lower()
		if response != 'n' and response != 'y':
			print("Invalid input. The options are [y], [n]. Select one of the option.")
		else:
			break

	if response == 'y':
		number_of_items = get_max_item_count()

		try:
			Product.create(product_id = number_of_items + 1, #adding one is for a new line
							product_name = (new_item['product_name']).title(), #Whatever the user inputted, the string will become a 'title', same format as the data in the csv file 
							product_price = '$' + str((float(new_item['product_price']) / 100)),
							product_quantity = new_item['product_quantity'],
							date_updated = new_item['date_updated'])

		except IntegrityError:
			product_record = Product.get(product_name = (new_item['product_name']).title()) #Comparing the data with 'title' format

			if product_record.product_id != number_of_items + 1 : #When the notice the product exist in a different spot, run this
				product_record.product_id = product_record.product_id # It updates that spot
				print("The item you've entered was already in the database. It was update with the new info!")
				
			else:
				product_record.product_id = number_of_items

			product_record.product_price = '$' + str((float(new_item['product_price']) / 100))
			product_record.product_quantity = new_item['product_quantity']
			product_record.date_updated = new_item['date_updated']
			product_record.save()
		print("")
		print("Saved successfully!")


def backup_data():
	"""Backup Data"""
	dictionary_holder =[]
	id_counter = 0

	number_of_items = get_max_item_count()


	for item in range(number_of_items):
		if item == 0: #there isn't a 0 entry, so skip this
			continue
		else:
			full_store_records = Product.get(product_id = item)

		temp = {'product_id':full_store_records.product_id,
			'product_name':full_store_records.product_name ,
			'product_price':full_store_records.product_price,
			'product_quantity':full_store_records.product_quantity,
			'date_updated':full_store_records.date_updated}
		dictionary_holder.append(temp)
	
	#--------'csv_columns', 'csv_file', 'data' variables were not changed from the source https://www.tutorialspoint.com/How-to-save-a-Python-Dictionary-to-CSV-file
	csv_columns = ['product_id', 'product_name', 'product_price', 'product_quantity','date_updated'] 
	csv_file = "BackupInventory.csv"
	with open(csv_file, 'w') as csvfile:  #If this file doesn't exist, this creates it
		writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
		writer.writeheader()
		for data in dictionary_holder:
			writer.writerow(data)
	#----------

	print("")
	print("The data has been saved in a csv file")
	print("Filename: " + csv_file)
	print("")

with open('inventory.csv', newline='') as csvfile:
	artreader = csv.DictReader(csvfile) #reading the data from the csv file
	list_of_items = list(artreader)#This putting the data into a list

menu = OrderedDict([
	('a', add_entry),
	('v', view_entries),
	('b', backup_data),
	])


test = []
for rows in list_of_items:
	temp = {'product_name':rows['product_name'] ,
			'product_price':rows['product_price'],
			'product_quantity':rows['product_quantity'],
			'date_updated':rows['date_updated']}
	test.append(temp) #making the data a 'list of dictionaries'

cleaned_dict = clean_data(test)


initialize() #get database ready
add_data() #adding data to the database
menu_loop() #Menu prompt for user
	
