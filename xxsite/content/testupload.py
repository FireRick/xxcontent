# import upload
# from upload import process_md_file
from content import upload
import unittest
import mistune
from datetime import datetime


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


class TestProcess_md_fileFuction(unittest.TestCase):
    def teststd_md_file(self):
        with open('std_md_file.md', 'rb') as f:
            md_dict = upload.process_md_file(f)
        self.assertEqual(md_dict, md_dict_)


class TestSave_md_dictFuction(unittest.TestCase):
    def testsave_article(self):
        pass
    def testupdate_article(self):
        pass
        

if __name__ == '__main__':
    unittest.main()