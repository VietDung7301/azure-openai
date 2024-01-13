from mongodb_connector import user_vocabularys_collection as collections

def insert_azure_doc(name, vocabularies):
    new_document = {
        "name": name,
        "vocabularies": vocabularies
    }
    
    inserted_result = collections.insert_one(new_document)
    # Lấy _id của document mới được thêm vào
    inserted_id = inserted_result.inserted_id

    # Trả lại document mới bằng cách tìm theo _id
    inserted_document = collections.find_one({"_id": inserted_id})

    return inserted_document

def find_user_vocabulary_by_id(user_id):
    from bson.objectid import ObjectId

    _id = ObjectId(user_id)

    user = collections.find_one({"_id": _id})
    if user:
        return {
            "code" : True,
            "message" : "Found User!",
            "document" : user
        }
    else:
        return {
            "code" : False,
            "message" : "User not found!",
        }
        

def update_user_by_id(user_id, new_name, new_vocabularies):
    from bson.objectid import ObjectId

    _id = ObjectId(user_id)
    # Tạo dictionary chứa thông tin cần cập nhật
    update_data = {
        "$set": {
            "name": new_name,
            "vocabularies": new_vocabularies
        }
    }

    # Cập nhật document trong collection dựa trên user_id
    updated_document = collections.find_one_and_update(
        {"_id": _id},
        update_data,
        return_document=True
    )
    if updated_document:
        return {
            "code" : True,
            "message" : "User updated successfully!",
            "new_document" : updated_document
        }
    else:
        return {
            "code" : False,
            "message" : "No matching user found!",
        }

def add_vocabulary(user_id, new_vocabularies):
    from bson.objectid import ObjectId

    _id = ObjectId(user_id)
    # Tạo dictionary chứa thông tin cần cập nhật
    
    update_data = {
        "$push": {
            "vocabularies": new_vocabularies
        }
    }

    # Cập nhật document trong collection dựa trên user_id
    updated_document = collections.find_one_and_update(
        {"_id": _id},
        update_data,
        return_document=True
    )
    if updated_document:
        return {
            "code" : True,
            "message" : "User updated successfully!",
            "new_document" : updated_document
        }
    else:
        return {
            "code" : False,
            "message" : "No matching user found!",
        }
