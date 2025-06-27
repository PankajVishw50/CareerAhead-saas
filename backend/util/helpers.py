import secrets
import string
import uuid


def generate_random_string(min=10, max=20):
    length = secrets.choice(range(min, max))
    characters = string.ascii_letters + string.digits + "-_"
    receipt = "".join(secrets.choice(characters) for _ in range(length))
    return receipt


@DeprecationWarning
def get_page_meta(page):
    return {
        "totalItems": page.paginator.count,
        "count": len(page.object_list),
        "totalPages": page.paginator.num_pages,
        "page": page.number,
        "size": page.paginator.per_page,
    }


def paginated_response(page, items=[]):
    if not isinstance(items, list):
        raise ValueError("`items` arg must be list")

    return {
        "totalItems": page.paginator.count,
        "count": len(page.object_list),
        "totalPages": page.paginator.num_pages,
        "page": page.number,
        "size": page.paginator.per_page,
        "items": items,
    }


def deep_update(replacement, original):
    for key, value in replacement.items():
        if isinstance(value, dict) and key in original.keys():
            deep_update(value, original[key])
            continue
        original[key] = value


def convert_uuid(obj):
    if isinstance(obj, uuid.UUID):
        return str(obj)
    raise TypeError("Type not serializable")


def serializer_uuid_dict(obj):

    for k, v in obj.items():
        if isinstance(v, dict):
            serializer_uuid_dict(v)
        elif isinstance(v, uuid.UUID):
            obj[k] = str(v)

    return obj
