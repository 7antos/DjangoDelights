from django.core.paginator import Paginator


def filter_name(request, query):

    # Queryset
    if 'name' in request.GET:
        query = query.filter(name__contains=request.GET['name'])

    return query


def pagination(request, context):

    # Pagination
    context['paginator'] = Paginator(context['object_list'], 10)
    context['page_number'] = request.GET.get('page')
    context['page_obj'] = context['paginator'].get_page(context['page_number'])

    return context
