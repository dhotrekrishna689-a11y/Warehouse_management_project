
#Not found category
class Resource_Not_Found_Error(Exception):
    pass
class Product_Not_Found_Error(Resource_Not_Found_Error):
    pass

class Batch_Not_Found_Error(Resource_Not_Found_Error):
    pass

#Duplicate category
class Resource_Duplicate_Found_Error(Exception):
    pass

class Batch_Duplicate_Found_Error(Resource_Duplicate_Found_Error):
    pass

#Data validation category
class Validation_Error(Exception):
    pass

class Date_Validation_Error(Validation_Error):
    pass

class Resource_Cannot_Delete(Exception):
    pass
