import requests
import json

categories_file = open('./data/categories.json', 'r')
categories = json.load(categories_file)
categories_file.close()

items_file = open('./data/items.json', 'r')
items = json.load(items_file)
items_file.close()

config_file = open('./config.json', 'r')
config = json.load(config_file)
config_file.close()

server_url = config['host'] + ':' + config['port']
headers = {
  'Content-Type': 'application/json',
  'Authorization': f'Bearer {config['token']}'
}

#inserting categories
for index in range(len(categories)):
    category = {
        "category_name": categories[index]['category_name']
    }
    print("inserting category: ", category['category_name'])
    response = requests.post(server_url + config['category_insert'], data=json.dumps(category), headers=headers).json()
    category['id'] = response['_id']
    categories[index] = category

categories_file = open('./data/categories.json', 'w')
json.dump(categories, categories_file, indent=4)
categories_file.close()

# inserting menu items
for index in range(len(items)):
    item = items[index]
    print("inserting item: " + item['item_name'] + " \ncategory: " + item['category_name'])
    for category in categories:
        if category['category_name'] == item['category_name']:
            item['category'] = category['id']
    del item['category_name']
    response = requests.post(server_url + config['item_insert'], data=json.dumps(item), headers=headers).json()

