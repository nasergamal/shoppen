from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def query(context, **kwargs):
    '''
    Returns the URL-encoded querystring for the current page,
    updating the params with the key/value pairs passed to the tag.
    
    E.g: given the querystring ?foo=1&bar=2
    {% query_transform bar=3 %} outputs ?foo=1&bar=3
    {% query_transform foo='baz' %} outputs ?foo=baz&bar=2
    {% query_transform foo='one' bar='two' baz=99 %} outputs ?foo=one&bar=two&baz=99
    
    A RequestContext is required for access to the current querystring.
    '''
    query = context['request'].GET.copy()
    for k, v in kwargs.items():
        query[k] = v
    return query.urlencode()


@register.simple_tag(takes_context=True)
def query_add(context, **kwargs):
    '''
    Returns the URL-encoded querystring for the current page,
    updating the params with the key/value pairs passed to the tag.
    
    E.g: given the querystring ?foo=1&bar=2
    {% query_transform bar=3 %} outputs ?foo=1&bar=3
    {% query_transform foo='baz' %} outputs ?foo=baz&bar=2
    {% query_transform foo='one' bar='two' baz=99 %} outputs ?foo=one&bar=two&baz=99
    
    A RequestContext is required for access to the current querystring.
    '''
    query = context['request'].GET.copy()
    for k, v in kwargs.items():
        v = str(v)
        if k in query:
            q_list = query[k].split('_')
            if v in q_list:
                q_list.remove(v)
                if len(q_list) > 0:
                    query[k] = '_'.join(q_list)
                else:
                    query.pop(k)
            else:
                query[k] += f'_{v}'
        else:
            query[k] = v
    return query.urlencode()


@register.simple_tag(takes_context=True)
def remove_query(context, *keys):
    '''
    Returns the URL-encoded querystring without selected query parameter,
    updating the params with the key/value pairs passed to the tag.
    
    E.g: given the querystring ?foo=1&bar=2
    {% remove_query bar %} outputs ?foo=1
    {% remove_query foo %} outputs ?bar=2
    
    A RequestContext is required for access to the current querystring.
    '''
    query = context['request'].GET.copy()
    for key in keys:
        query.pop(key, None)
    return query.urlencode()