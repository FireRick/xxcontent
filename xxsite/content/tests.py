import os

from datetime import datetime
from copy import deepcopy
from django.test import TestCase
from .models import Article, Category, Tag
from .upload import handle_uploaded_files

class MdFileTestCase(TestCase):
    """ Test extracting uploaded markdown file. """
    md_dict_ = {
        'title': '文章标题',
        'author': '作者名称',
        'create_time': datetime.strptime('2020-01-01T09:00+0800', '%Y-%m-%dT%H:%M%z'),
        'update_time': datetime.strptime('2020-01-01T09:00+0800', '%Y-%m-%dT%H:%M%z'),
        'category': '分类1',
        'tag': ['标签1', '标签2', '标签3'],
        'desc': '这里是文章的摘要信息，纯文本格式。',
        'content': '## 这里是文章的正文部分（不含文章标题）\n## 用 markdown 格式',
        'content_html': '<h2>这里是文章的正文部分（不含文章标题）</h2>\n<h2>用 markdown 格式</h2>\n',
    }

    def setUp(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

    def test_md_file_upload(self):
        md_dict = deepcopy(self.md_dict_)
        md_filename = os.path.join(self.base_dir, 'std_md_file.md')
        with open(md_filename, 'rb') as f:
            res = handle_uploaded_files(f)
        self.assertEqual(res, 0)
        article = Article.objects.get(title=md_dict['title'])
        category = Category.objects.get(name=md_dict['category'])
        tags = []
        for tag_name in md_dict['tag']:
            tags.append(Tag.objects.get(name=tag_name))
        md_dict.update({
            'category': category,
            'tag': tags,
        })
        for key, value in md_dict.items():
            if key == 'tag':
                self.assertEqual(set(article.tag.all()), set(value))
            else:
                self.assertEqual(getattr(article, key), value)

    def test_md_zip_upload(self):
        zip_filename = os.path.join(self.base_dir, 'test_md_files.zip')
        with open(zip_filename, 'rb') as f:
            res = handle_uploaded_files(f)
        self.assertEqual(res, 0)
        self.assertEqual(Article.objects.count(), 4)
        Article.objects.get(title='文章标题1')
        Article.objects.get(title='文章标题2')
        Article.objects.get(title='文章标题3')
        Article.objects.get(title='文章标题4')
