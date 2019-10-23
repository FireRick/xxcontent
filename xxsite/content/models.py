from django.db import models

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

    title = models.CharField(max_length=50, verbose_name="标题")
    sidebar_type = models.PositiveIntegerField(
        default=1, choices=SIDEBAR_TYPE, verbose_name="展示类型")
    content = models.CharField(
        max_length=1024, blank=True, verbose_name="内容",
        help_text="只有选择 HTML 时才需要填写内容")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = verbose_name_plural = "侧边栏"


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
