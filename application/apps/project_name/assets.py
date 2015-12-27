from django_assets import Bundle, register


register('{{ project_name }}_css', Bundle(
    Bundle(
        "{{ project_name }}/styles/{{ project_name }}.scss",
        filters="pyscss",
    ),
    filters='cssrewrite,cssmin',
    output='_/{{ project_name }}.css'
))

register('{{ project_name }}_js', Bundle(
    Bundle(
        "{{ project_name }}/scripts/{{ project_name }}.coffee",
        filters='coffeescript,jsmin',
    ),
    Bundle(
        "{{ project_name }}/scripts/jquery.{{ project_name }}.js",
        filters='jsmin'
    ),
    output='_/{{ project_name }}.js'
))
