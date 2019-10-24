from django.db import models
from django.utils.safestring import mark_safe   # 防止html转义
from django.template.loader import render_to_string


# Create your models here.
class Category(models.Model):
    """ 分类数据结构 """
    name = models.CharField(max_length=50, verbose_name="名称")
    content = models.TextField(verbose_name="分类描述正文")
    desc = models.CharField(max_length=1024, verbose_name="摘要")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = "分类"


class Tag(models.Model):
    """ 标签数据结构 """
    name = models.CharField(max_length=50, verbose_name="名称")
    content = models.TextField(verbose_name="标签描述正文")
    desc = models.CharField(max_length=1024, verbose_name="摘要")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = "标签"


class Article(models.Model):
    """ 文章数据结构 """
    title = models.CharField(max_length=50, verbose_name="标题")
    author = models.CharField(max_length=10, verbose_name="作者")
    create_time = models.DateTimeField(verbose_name="创建时间")
    update_time = models.DateTimeField(verbose_name="更新时间")
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, verbose_name="分类")
    tag = models.ManyToManyField(Tag, verbose_name="标签")
    desc = models.CharField(max_length=1024, verbose_name="摘要")
    content = models.TextField(verbose_name="正文", help_text="用 markdown 书写")
    pv = models.PositiveIntegerField(default=0)
    uv = models.PositiveIntegerField(default=0)

    @classmethod
    def latest_articles(cls):
        return cls.objects.all()[:5]

    @classmethod
    def hotest_articles(cls):
        return cls.objects.order_by('-pv')[:5]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = verbose_name_plural = "文章"
        ordering = ["-id"]


class SideBar(models.Model):
    """ 侧栏数据结构 """
    SIDEBAR_TYPE = (
        (1, "HTML"),
        (2, "最热文章"),
        (3, "最新文章"),
    )

    title = models.CharField(
        max_length=50, verbose_name="标题",
        help_text="不填则不显示标题",
    )
    does_show_title = models.BooleanField(default=True, verbose_name="是否显示标题")
    sidebar_type = models.PositiveIntegerField(
        default=1, choices=SIDEBAR_TYPE, verbose_name="展示类型",
    )
    content = models.CharField(
        max_length=1024, blank=True, verbose_name="内容",
        help_text="只有选择 HTML 时才需要填写内容",
    )

    @property
    def content_html(self):
        """
        直接返回渲染后的HTML内容，以供在模板中直接调用
        """

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = verbose_name_plural = "侧边栏"


class IndexContent(models.Model):
    """ 首页内容区数据结构 """
    CONTENT_HTML = 1
    CONTENT_HOTEST = 2
    CONTENT_LATEST = 3
    CONTENT_TYPE = (
        (CONTENT_HTML, "HTML"),
        (CONTENT_HOTEST, "最热文章"),
        (CONTENT_LATEST, "最新文章"),
    )

    title = models.CharField(
        max_length=50, verbose_name="标题",
        help_text="不填则不显示标题",
    )
    does_show_title = models.BooleanField(default=True, verbose_name="是否显示标题")
    content_type = models.PositiveIntegerField(
        default=1, choices=CONTENT_TYPE, verbose_name="展示类型",
    )
    content = models.CharField(
        max_length=1024, blank=True, verbose_name="内容",
        help_text="只有选择 HTML 时才需要填写内容",
    )

    @property
    def content_html(self):
        """
        直接返回渲染后的HTML内容，以供在模板中直接调用
        """
        if self.content_type == self.CONTENT_HTML:
            result = mark_safe(self.content)
        elif self.content_type == self.CONTENT_LATEST:
            context = {
                'title': self.title,
                'show_title': self.does_show_title,
                'articles': Article.latest_articles()
            }
            result = render_to_string('content/articles_list_index.html', context)
        elif self.content_type == self.CONTENT_HOTEST:
            context = {
                'title': self.title,
                'show_title': self.does_show_title,
                'articles': Article.hotest_articles()
            }
            result = render_to_string('content/articles_list_index.html', context)
        else:
            result = "这是非法类型，注意排查数据库是否写入了非法数据"
        return result

    @classmethod
    def get_all(cls):
        return cls.objects.all()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = verbose_name_plural = "首页内容区"

class Page(models.Model):
    """ 独立页面数据结构 """
    url = models.CharField(
        max_length=200, verbose_name="URL", help_text="建议使用绝对路径")
    title = models.CharField(max_length=50, verbose_name="标题")
    author = models.CharField(max_length=10, verbose_name="作者")
    content = models.TextField(verbose_name="正文", help_text="用 markdown 书写")
    create_time = models.DateTimeField(verbose_name="创建时间")
    update_time = models.DateTimeField(verbose_name="更新时间")
    does_follow = models.BooleanField(default=False, verbose_name="是否跟踪")
    desc = models.CharField(max_length=1024, verbose_name="摘要")
    pv = models.PositiveIntegerField(default=0)
    uv = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = verbose_name_plural = "独立页面"


class Link(models.Model):
    """ 底部文字链接数据结构 """
    url = models.CharField(
        max_length=200, verbose_name="URL", help_text="建议使用绝对路径")
    anchor_word = models.CharField(max_length=50, verbose_name="锚文字")
    create_time = models.DateTimeField(verbose_name="创建时间")
    does_follow = models.BooleanField(default=False, verbose_name="是否跟踪")

    def __str__(self):
        return self.anchor_word

    class Meta:
        verbose_name = verbose_name_plural = "底部文字链接"
