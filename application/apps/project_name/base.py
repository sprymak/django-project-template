"""
This is private API for the application. All the functions here is the
subject of changes without notice in the documentation.
"""


def publish_article(article):
    article.is_private = False
    article.save()
