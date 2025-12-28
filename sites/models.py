from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


def validate_image_extension(value):
    """画像形式をJPG, PNG, WebPに制限"""
    valid_extensions = ['jpg', 'jpeg', 'png', 'webp']
    validator = FileExtensionValidator(allowed_extensions=valid_extensions)
    validator(value)


class Site(models.Model):
    """サイト基本情報"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sites')
    title = models.CharField('サイトタイトル', max_length=100)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    class Meta:
        verbose_name = 'サイト'
        verbose_name_plural = 'サイト'
        ordering = ['-updated_at']

    def __str__(self):
        return self.title


class SectionStyle(models.Model):
    """セクションスタイル設定"""
    SECTION_CHOICES = [
        ('top', 'トップ'),
        ('main', 'メイン'),
        ('sub', 'サブ'),
        ('access', 'アクセス'),
    ]

    TEXT_ALIGN_CHOICES = [
        ('text-left', '左揃え'),
        ('text-center', '中央揃え'),
        ('text-right', '右揃え'),
    ]

    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='section_styles')
    section_name = models.CharField('セクション名', max_length=20, choices=SECTION_CHOICES)
    background_color = models.CharField('背景色', max_length=7, default='#FFFFFF')
    text_color = models.CharField('文字色', max_length=7, default='#000000')
    font_family = models.CharField('フォント', max_length=100, default='Noto Sans JP')
    text_size = models.IntegerField('文字サイズ(px)', default=16)
    text_align = models.CharField('文字配置', max_length=20, choices=TEXT_ALIGN_CHOICES, default='text-left')

    class Meta:
        verbose_name = 'セクションスタイル'
        verbose_name_plural = 'セクションスタイル'
        unique_together = ['site', 'section_name']

    def __str__(self):
        return f'{self.site.title} - {self.get_section_name_display()}'


class TopSection(models.Model):
    """トップセクション"""
    IMAGE_FIT_CHOICES = [
        ('cover', 'カバー（トリミング）'),
        ('contain', '全体表示'),
        ('fill', '引き伸ばし'),
    ]

    site = models.OneToOneField(Site, on_delete=models.CASCADE, related_name='top_section')
    hero_image = models.ImageField(
        'ヒーロー画像',
        upload_to='top/',
        validators=[validate_image_extension],
        blank=True,
        null=True
    )
    hero_image_fit = models.CharField('画像表示モード', max_length=20, choices=IMAGE_FIT_CHOICES, default='cover')
    hero_image_height = models.IntegerField('画像高さ(px)', default=500)

    class Meta:
        verbose_name = 'トップセクション'
        verbose_name_plural = 'トップセクション'

    def __str__(self):
        return f'{self.site.title} - トップ'


class SNSLink(models.Model):
    """SNSリンク"""
    PLATFORM_CHOICES = [
        ('instagram', 'Instagram'),
        ('x', 'X (Twitter)'),
        ('line', 'LINE'),
        ('facebook', 'Facebook'),
        ('youtube', 'YouTube'),
        ('tiktok', 'TikTok'),
    ]

    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='sns_links')
    platform = models.CharField('プラットフォーム', max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField('URL')
    is_active = models.BooleanField('有効', default=True)

    class Meta:
        verbose_name = 'SNSリンク'
        verbose_name_plural = 'SNSリンク'
        unique_together = ['site', 'platform']

    def __str__(self):
        return f'{self.site.title} - {self.get_platform_display()}'


class MainSection(models.Model):
    """メインセクション（カルーセル）"""
    IMAGE_FIT_CHOICES = [
        ('cover', 'カバー（トリミング）'),
        ('contain', '全体表示'),
        ('fill', '引き伸ばし'),
    ]

    site = models.OneToOneField(Site, on_delete=models.CASCADE, related_name='main_section')
    title = models.CharField('タイトル', max_length=100, blank=True)
    subtitle = models.CharField('サブタイトル', max_length=200, blank=True)
    image1 = models.ImageField(
        '画像1',
        upload_to='main/',
        validators=[validate_image_extension],
        blank=True,
        null=True
    )
    image2 = models.ImageField(
        '画像2',
        upload_to='main/',
        validators=[validate_image_extension],
        blank=True,
        null=True
    )
    image3 = models.ImageField(
        '画像3',
        upload_to='main/',
        validators=[validate_image_extension],
        blank=True,
        null=True
    )
    image_fit = models.CharField('画像表示モード', max_length=20, choices=IMAGE_FIT_CHOICES, default='cover')
    image_height = models.IntegerField('画像高さ(px)', default=400)

    class Meta:
        verbose_name = 'メインセクション'
        verbose_name_plural = 'メインセクション'

    def __str__(self):
        return f'{self.site.title} - メイン'


class SubSection(models.Model):
    """サブセクション（画像+テキスト）"""
    IMAGE_FIT_CHOICES = [
        ('cover', 'カバー（トリミング）'),
        ('contain', '全体表示'),
        ('fill', '引き伸ばし'),
    ]

    site = models.OneToOneField(Site, on_delete=models.CASCADE, related_name='sub_section')
    image1 = models.ImageField(
        '画像1',
        upload_to='sub/',
        validators=[validate_image_extension],
        blank=True,
        null=True
    )
    text1 = models.TextField('テキスト1', blank=True)
    image2 = models.ImageField(
        '画像2',
        upload_to='sub/',
        validators=[validate_image_extension],
        blank=True,
        null=True
    )
    text2 = models.TextField('テキスト2', blank=True)
    image3 = models.ImageField(
        '画像3',
        upload_to='sub/',
        validators=[validate_image_extension],
        blank=True,
        null=True
    )
    text3 = models.TextField('テキスト3', blank=True)
    image_fit = models.CharField('画像表示モード', max_length=20, choices=IMAGE_FIT_CHOICES, default='cover')
    image_height = models.IntegerField('画像高さ(px)', default=256)

    class Meta:
        verbose_name = 'サブセクション'
        verbose_name_plural = 'サブセクション'

    def __str__(self):
        return f'{self.site.title} - サブ'


class AccessSection(models.Model):
    """アクセスセクション"""
    site = models.OneToOneField(Site, on_delete=models.CASCADE, related_name='access_section')
    section_title = models.CharField('セクションタイトル', max_length=100, default='アクセス')
    address = models.CharField('住所', max_length=300, blank=True)
    phone = models.CharField('電話番号', max_length=20, blank=True)
    business_hours = models.JSONField(
        '営業時間',
        default=list,
        blank=True,
        help_text='例: [{"day": "月-金", "hours": "9:00-18:00"}, {"day": "土日祝", "hours": "定休日"}]'
    )

    class Meta:
        verbose_name = 'アクセスセクション'
        verbose_name_plural = 'アクセスセクション'

    def __str__(self):
        return f'{self.site.title} - アクセス'

    def get_google_maps_embed_url(self):
        """Googleマップ埋め込み用URLを生成"""
        if self.address:
            from urllib.parse import quote
            encoded_address = quote(self.address)
            return f'https://maps.google.com/maps?q={encoded_address}&output=embed'
        return None
