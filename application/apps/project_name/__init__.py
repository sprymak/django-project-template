import django.template


custom_builtins = [
    'mcutils.django.templatetags.collections_utils',
    'mcutils.django.templatetags.form_utils',
    'mcutils.django.templatetags.http_utils',
]

# Add our own template tags library to the builtins.
library_name = __name__.rsplit('.', 1)[0] + '.templatetags'
if not library_name in django.template.base.libraries:
    custom_builtins.insert(0, library_name)

for library_name in custom_builtins:
    if not library_name in django.template.base.builtins:
        django.template.base.add_to_builtins(library_name)
