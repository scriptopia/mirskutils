from django import template
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.template.defaultfilters import stringfilter
from django.template import Context, Template
from django.contrib.sites.models import Site, RequestSite

register = template.Library()

@register.simple_tag
def urlOptions(viewname, *args, **kwargs):
    params = [ a for a in args if a ]
    kwparams = { k:v for k,v in kwargs.iteritems() if v }
    return reverse(viewname, args=params, kwargs=kwparams)

@register.filter(takes_content=True)
@stringfilter
def makeAbsolute(context, value):
    """
    takes a url and adds the site's domain name to make it an absolute URL
    """
    # TODO: should check if the url is already absolute before appending
    
    items = {
        'protocol': "https://" if context.request.is_secure() else "http://",
        'domain':RequestSite(request).domain,
        'uri':value
    }
    
    return "%(protocol)s://%(domain)s%(uri)s" % items

@register.simple_tag
def urlAbsolute(viewname, *args, **kwargs):
    return makeAbsolute(urlOptions(viewname, *args, **kwargs))

@register.simple_tag
def css(stylesheet):
    if not stylesheet:
        return ""    
    return '<link rel="stylesheet" href="%s" />' % makeAbsolute("%s%s" % (settings.STATIC_URL, stylesheet))
    
@register.simple_tag
def js(script):
    if not script:
        return ""    
    return '<script type="text/javascript" src="%s"></script>' % makeAbsolute("%s%s" % (settings.STATIC_URL, script))

formTemplate = Template('''{% if form.is_multipart and button %}
	<form enctype="multipart/form-data" method="post" action="{{ action }}">
{% elif button %}
	<form method="post" action="{{ action }}">
{% else %}
{% endif %}
    {% if form.non_field_errors %}{{ form.non_field_errors }}{% endif %}
     <input type='hidden' name='csrfmiddlewaretoken' value='{{ csrf_token }}' />
  	{% for field in form.hidden_fields %}{{ field }}{% endfor %}
    {% for field in form.visible_fields %}
	  <p class="{%if field.field.widget.input_type %}infield {% endif %} {{ field.name }}">
         {{ field.label_tag }} {{ field }}
         {% if field.errors %}<div class="error"><div class="valign">{{ field.errors }}</div></div>{% endif %}
         {% if field.help_text %}<a class="tooltip" title="{{ field.help_text }}"><span class="sc-icon sc-icon-question"></span></a>{% endif %}
      </p>
	{% endfor %}
    {% if button %}
	<button type="submit" class="sc-button">
    <span class="sc-button-text">{{ button }}</span></button>		
    </form>
    {% endif %}
  ''')

@register.simple_tag(takes_context=True)
def renderForm(context, form, button='Submit', action=None, **params):
    '''
    renders a django form with a specific structure so that forms are consistently displayed.
    ensure compatibility with jquery.infieldlabel.js with this additional css
        <script>$('form').inFieldLabels()</script>
    '''
    
    ps = {key:value for key,value in params.items() if value }
    
    d = {
        'form':form,
        'button':button,
        'csrf_token':context.get('csrf_token', None),
        'action':'.'
    }
    
    if action:
        d['action'] = reverse(action, kwargs=ps)
        
    return formTemplate.render(Context(d))