import mistune
import os

from datetime import datetime
from zipfile import ZipFile

from .models import Article, Category, Tag


def process_md_file(md_file):
    """ md_file should be a file-like object. 
    If process success, return a dict with key-values, otherwise, return None.
    """
    md_dict = {}
    for line in md_file:
        line_str = line.decode()
        if line_str[0] == '<':
            label_and_value = line_str[1:].split('>')
            if len(label_and_value) == 2:
                label, value = label_and_value
                value = value.strip()
                if label == 'title':
                    md_dict['title'] = value
                elif label == 'author':
                    md_dict['author'] = value
                elif label == 'create_time':
                    md_dict['create_time'] = datetime.strptime(
                            value, '%Y-%m-%dT%H:%M%z')
                elif label == 'update_time':
                    md_dict['update_time'] = datetime.strptime(
                            value, '%Y-%m-%dT%H:%M%z')
                elif label == 'category':
                    md_dict['category'] = value
                elif label == 'tag':
                    md_dict['tag'] = value.split()
                elif label == 'desc':
                    md_dict['desc'] = value
                elif label == 'content':
                    md_dict['content'] = md_file.read().decode()
                    md_dict['content_html'] = mistune.markdown(
                                              md_dict['content'])
                    if len(md_dict) == 9:
                        return md_dict
                    else:
                        return
        else:
            continue #skip blank line

def save_md_dict(md_dict):
    """ Check articles in database with the same title.
    If the same title exists, update this article, otherwise, insert new one.
    Also check specific category and tag in database, if it doesn't exist,
    insert new one.
    """
    # check category
    category, new_category_created = Category.objects.get_or_create(name=md_dict['category'])
    md_dict['category'] = category

    # extract tag names and delete key 'tag' from md_dict
    tag_names = md_dict['tag']
    del(md_dict['tag'])

    # check article
    article, new_article_created = Article.objects.update_or_create(
        title=md_dict['title'],
        defaults=md_dict,
    )

    # check tag
    if not new_article_created:
        article.tag.clear() #clear old tags
    for tag_name in tag_names:
        tag, new_tag_created = Tag.objects.get_or_create(name=tag_name)
        article.tag.add(tag)

def handle_uploaded_files(f):
    """ Handle uploaded md files. 
    If uploaded file is a zip, upzip at first.
    """
    filetype = f.name.split('.')[-1]
    if filetype == 'zip':
        with ZipFile(f) as myzip: # ZipFile(f) may exhaust memory
            for md_file in myzip.namelist():
                with myzip.open(md_file) as md:
                    md_dict = process_md_file(md)
                    print(md_dict) ###
                    if md_dict:
                        save_md_dict(md_dict)
    elif filetype == 'md':
        # save md file to disk, then process
        tempfilename = str(datetime.now().timestamp())
        with open(tempfilename, 'wb+') as tempfile:
            for chunk in f.chunks():
                tempfile.write(chunk)
        # this can be done async
        with open(tempfilename, 'rb') as tempfile:
            md_dict = process_md_file(tempfile)
        os.remove(tempfilename)
        print(md_dict) ###
        if md_dict:
            save_md_dict(md_dict)
    else:
        return # If uploaded file is not md and zip, return None
    return 0 # Handled Success!