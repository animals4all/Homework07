"""
call.py - Telemarketing script that displays the next name 
          and phone number of a Customer to call.

          This script is used to drive promotions for 
          specific customers based on their order history.
          We only want to call customers that have placed
          an order of over 20 Watermelons.

"""

# Module to get current date
import datetime

# Load the customers from the passed filename
# Return a dictionary containing the customer data
#    (key = customer_id)
def load_customers(filename):
	customers = {}
	f = open(filename)

	# First line of the file should be the header, 
	#   split that into a list
	header = f.readline().rstrip().split(',')

	# Process each line in a file, create a new
	#   dict for each customer
	for line in f:
		data = line.rstrip().split(',')
		customer = {}

		# Loop through each column, adding the data
		#   to the dictionary using the header keys
		for i in range(len(header)):
			customer[header[i]] = data[i]

		# Add the customer to our dictionary by customer id
		customers[customer['customer_id']] = customer

	# Close the file
	f.close()

	return customers

# Load the orders from the passed filename
# Return a list of all the orders
def load_orders(filename):
	orders = []
	f = open(filename)

	# First line of the file should be the header, 
	#   split that into a list
	header = f.readline().rstrip().split(',')

	# Process each line in a file, create a new
	#   dict for each order
	for line in f:
		data = line.rstrip().split(',')

		# Create a dictionary for the order by combining
		#   the header list and the data list
		order = dict(zip(header, data))

		# Add the order to our list of orders to return
		orders.append(order)

	# Close the file
	f.close()

	return orders

def display_customer(customer):
	print "---------------------"
	print "Next Customer to call"
	print "---------------------\n"
	print "Name: ", customer.get('first', ''), customer.get('last', '')
	print "Phone: ", customer.get('telephone')
	print "\n"

def main():
	# Load data from our csv files
	customers = load_customers('customers.csv')
	orders    = load_orders('orders.csv')

	# Loop through each order
	for order in orders:
		# Is this order over 20 watermelon?
		if order.get('num_watermelons', 0) > 20:
			# Has this customer not been contacted yet?
			customer = customers.get(order.get('customer_id', 0), 0)
			if customer.get('called', '') == '':
				display_customer(customer)
				
				# The index of the customer's line in the file is the
				# customer's ID
				customer_file_index = int(customer['customer_id'])

				# Get the current date and split into a list
				current_date = str(datetime.date.today()).split("-")
				year = current_date[0]
				month = current_date[1]
				day = current_date[2]

				fo = open('customers.csv', 'r')
				file_contents = fo.readlines()
				fo.close()

				# Remove the newline character from the end of the line
				file_contents[customer_file_index] = file_contents[customer_file_index].rstrip("\n")

				# Append the date to the customer's line in
				# the 'customers.csv' file
				file_contents[customer_file_index] += month + "/" + day + "/" + year + "\n"

				# Write the altered contents back to the file
				fo = open('customers.csv', 'w')
				fo.writelines(file_contents)
				fo.close()

				break

if __name__ == '__main__':
	main()