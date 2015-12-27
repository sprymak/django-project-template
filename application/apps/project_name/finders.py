from django.contrib.staticfiles import finders as static_finders


class {{ project_name|title }}AssetsFinder(static_finders.AppDirectoriesFinder):
    source_dir = 'assets'
