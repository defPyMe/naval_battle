from tabulate import tabulate

data_list = [('25/04/2023', 's'), ('23/06/2023', 's'), ('25/04/2023', 'e'), ('23/06/2023', 'e')]

result_dict = {}

# Iterate over the tuples in the list
for date, value in data_list:
    if value not in result_dict or date < result_dict[value]:
        result_dict[value] = date

# Create a list of tuples using the values from the dictionary
result_list = [(date, value) for value, date in result_dict.items()]

# Format the result list into a table
table = tabulate(result_list, headers=['Date', 'Value'], tablefmt='plain')

print(table)

