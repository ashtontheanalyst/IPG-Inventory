# Example inventory item structure
class InventoryItem:
    def __init__(self, project, category, object_code, checked_out):
        self.project = project
        self.category = category
        self.object = object_code
        self.checked_out = checked_out

# Example: get inventory items by project
def get_inventory_items(project_name):
    # Replace with real DB query
    return [item for item in all_items if item.project == project_name and item.checked_out]

# Serial number lookup function
def find_serial_number_by_object(object_code):
    # Replace with your logic
    return object_serial_map.get(object_code, "")
