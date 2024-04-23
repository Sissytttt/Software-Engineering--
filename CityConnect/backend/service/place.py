from dao.models import Place

def get(id):
    try:
        return Place.objects.get(id=id)
    except Place.DoesNotExist:
        return None

def search_keyword(keyword):
    return Place.objects.filter(content__icontains=keyword)
