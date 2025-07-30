from datetime import datetime

def json_validation(data):
    errors = []

    for i, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            errors.append(f'Item {i}: Not a dict')
            continue

        if 'name' not in item:
            errors.append(f"Item {i}: Missing 'name' field")
        if 'date' not in item:
            errors.append(f"Item {i}: Missing 'date' field")
        
        if 'name' in item:
            if not isinstance(item['name'], str):
                errors.append(f"Item {i}: 'name' must be a string")
            elif len(item['name']) >=50:
                errors.append(f"Item {i}: 'name' length must be less than 50 chars")

        if 'date' in item:
            try:
                datetime.strptime(item['date'], '%Y-%m-%d_%H:%M')
            except ValueError:
                errors.append(f"Item {i}: Invalid date format. YYYY-MM-DD_HH:mm Expected")
        
    return errors