import secrets
import string

def generate_random_string(min=10, max=20):
    length = secrets.choice(range(min, max))
    characters = string.ascii_letters + string.digits + '-_'
    receipt = ''.join(secrets.choice(characters) for _ in range(length))
    return receipt

def get_page_meta(paginator, page):

    return {
        'totalItems': paginator.count,
        'currentItems': page.object_list.count(),
        'size': paginator.per_page,
        'totalPages': paginator.num_pages,
        'currentPage': page.number,
    }

def deef_update(replacement, original):                                    
    for key, value in replacement.items():                                 
        if isinstance(value, dict) and key in original.keys():             
            deef_update(value, original[key])                              
            continue                                                                                    
        original[key] = value