from pymongo import MongoClient 
from bson.objectid import ObjectId 

mongo_uri = "mongodb+srv://olenakatsyashvili:0U5oYxbWcY3eRjDD@cluster0.7xizwcp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Підключення до MongoDB
client = MongoClient(mongo_uri)

db = client['my_db'] 

# Вибір колекції
collection = db['cats'] 

# Читання (Read)
def get_all_cats():
    return list(collection.find({}))

def get_cat_by_name(name):
    return collection.find_one({"name": name})

# Оновлення (Update)
def update_cat_age(name, new_age):
    collection.update_one({"name": name}, {"$set": {"age": new_age}})

def add_feature_to_cat(name, feature):
    collection.update_one({"name": name}, {"$addToSet": {"features": feature}})

# Видалення (Delete)
def delete_cat_by_name(name):
    collection.delete_one({"name": name})

def delete_all_cats():
    collection.delete_many({})

if __name__ == "__main__":
    
    print("All Cats:", get_all_cats())
    print("Cat by Name (Barsik):", get_cat_by_name("barsik"))

    update_cat_age("barsik", 4)
    add_feature_to_cat("barsik", "playing with yarn")

    print("Updated Cat by Name (Barsik):", get_cat_by_name("barsik"))

    delete_cat_by_name("barsik")
    print("All Cats after deletion:", get_all_cats())

    delete_all_cats()
    print("All Cats after deleting all:", get_all_cats())
