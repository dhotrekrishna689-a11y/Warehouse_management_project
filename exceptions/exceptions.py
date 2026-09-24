
# ─── Base Exceptions ────────────────────────────────────────────────────────────

class AppBaseError(Exception):
    """Root exception for the entire application."""
    pass


# ─── Not Found ──────────────────────────────────────────────────────────────────

class Resource_Not_Found_Error(AppBaseError):
    pass

class Resource_Not_Exit_Error(Resource_Not_Found_Error):
    pass

class Product_Not_Found_Error(Resource_Not_Found_Error):
    pass

class Batch_Not_Found_Error(Resource_Not_Found_Error):
    pass

class Rack_Not_Found_Error(Resource_Not_Found_Error):
    pass

class Inventory_Not_Found_Error(Resource_Not_Found_Error):
    pass

class Category_Not_Found_Error(Resource_Not_Found_Error):
    pass

class Shipment_Not_Found_Error(Resource_Not_Found_Error):
    pass

class Order_Not_Found_Error(Resource_Not_Found_Error):
    pass

class Order_Item_Not_Found_Error(Resource_Not_Found_Error):
    pass

class Shipment_Item_Not_Found_Error(Resource_Not_Found_Error):
    pass

# ─── Duplicate / Already Exists ─────────────────────────────────────────────────

class Resource_Duplicate_Found_Error(AppBaseError):
    pass

class Resource_existance(Resource_Duplicate_Found_Error):
    """Category / generic already-exists error."""
    pass

class Batch_Duplicate_Found_Error(Resource_Duplicate_Found_Error):
    pass

class Category_Duplicate_Found_Error(Resource_Duplicate_Found_Error):
    pass

class Inventory_Duplicate_Found_Error(Resource_Duplicate_Found_Error):
    pass

class Rack_Duplicate_Found_Error(Resource_Duplicate_Found_Error):
    pass

class Shipment_Duplicate_Found_Error(Resource_Duplicate_Found_Error):
    pass

class Product_Duplicate_Found_Error(Resource_Duplicate_Found_Error):
    pass

class Order_Item_Duplicate_Found_Error(Resource_Duplicate_Found_Error):
    pass

class Shipment_Item_Duplicate_Found_Error(Resource_Duplicate_Found_Error):
    pass


# ─── Validation ─────────────────────────────────────────────────────────────────

class Validation_Error(AppBaseError):
    pass

class Date_Validation_Error(Validation_Error):
    pass

class Qunatity_validation_Error(Validation_Error):
    pass

class Empty_Field_Error(Validation_Error):
    pass


# ─── Cannot Delete ──────────────────────────────────────────────────────────────

class Resource_Cannot_Delete(AppBaseError):
    pass

class Category_Cannot_Delete(Resource_Cannot_Delete):
    pass

class Inventory_cannot_Delete(Resource_Cannot_Delete):
    pass

class Rack_Cannot_Delete(Resource_Cannot_Delete):
    pass

class Shipment_Cannot_Delete(Resource_Cannot_Delete):
    pass

class Product_Cannot_Delete(Resource_Cannot_Delete):
    pass

class Order_Cannot_Delete(Resource_Cannot_Delete):
    pass


class Insufficient_Stock_Error(Exception):
    pass