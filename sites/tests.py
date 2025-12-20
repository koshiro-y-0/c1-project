from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image
from .models import (
    Site, SectionStyle, TopSection, SNSLink,
    MainSection, SubSection, AccessSection
)


def create_test_image(name='test.jpg', size=(100, 100), format='JPEG'):
    """テスト用画像を作成"""
    file = BytesIO()
    image = Image.new('RGB', size, color='red')
    image.save(file, format=format)
    file.seek(0)
    return SimpleUploadedFile(
        name=name,
        content=file.read(),
        content_type=f'image/{format.lower()}'
    )


class SiteModelTestCase(TestCase):
    """Siteモデルのテスト"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.site = Site.objects.create(
            user=self.user,
            title='テストサイト'
        )

    def test_site_creation(self):
        """サイト作成が正常に動作する"""
        self.assertEqual(self.site.title, 'テストサイト')
        self.assertEqual(self.site.user, self.user)

    def test_site_str(self):
        """サイトの__str__メソッドが正しく動作する"""
        self.assertEqual(str(self.site), 'テストサイト')


class SectionStyleModelTestCase(TestCase):
    """SectionStyleモデルのテスト"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.site = Site.objects.create(user=self.user, title='テストサイト')
        self.style = SectionStyle.objects.create(
            site=self.site,
            section_name='top',
            background_color='#FFFFFF',
            text_color='#000000',
            font_family='Noto Sans JP'
        )

    def test_style_creation(self):
        """スタイル作成が正常に動作する"""
        self.assertEqual(self.style.section_name, 'top')
        self.assertEqual(self.style.background_color, '#FFFFFF')

    def test_unique_together_constraint(self):
        """同じサイト・セクションの重複を防止する"""
        with self.assertRaises(Exception):
            SectionStyle.objects.create(
                site=self.site,
                section_name='top'
            )


class SiteListViewTestCase(TestCase):
    """サイト一覧ビューのテスト"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.site1 = Site.objects.create(user=self.user, title='サイト1')
        self.site2 = Site.objects.create(user=self.user, title='サイト2')

    def test_site_list_view(self):
        """サイト一覧が正常に表示される"""
        response = self.client.get(
            reverse('sites:site_list', kwargs={'user_id': self.user.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'サイト1')
        self.assertContains(response, 'サイト2')

    def test_site_list_invalid_user(self):
        """存在しないユーザーで404を返す"""
        response = self.client.get(
            reverse('sites:site_list', kwargs={'user_id': 99999})
        )
        self.assertEqual(response.status_code, 404)


class SiteCreateViewTestCase(TestCase):
    """サイト新規作成ビューのテスト"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_site_create_post(self):
        """POSTでサイトを作成できる"""
        response = self.client.post(
            reverse('sites:site_create', kwargs={'user_id': self.user.id}),
            {'title': '新規サイト'}
        )
        self.assertEqual(response.status_code, 302)  # リダイレクト

        # サイトが作成されたか確認
        site = Site.objects.filter(title='新規サイト').first()
        self.assertIsNotNone(site)

        # 関連セクションも作成されているか確認
        self.assertTrue(hasattr(site, 'top_section'))
        self.assertTrue(hasattr(site, 'main_section'))
        self.assertTrue(hasattr(site, 'sub_section'))
        self.assertTrue(hasattr(site, 'access_section'))

        # スタイルも作成されているか確認
        self.assertEqual(site.section_styles.count(), 4)

    def test_site_create_default_title(self):
        """タイトルなしでもデフォルト名で作成される"""
        response = self.client.post(
            reverse('sites:site_create', kwargs={'user_id': self.user.id}),
            {}
        )
        self.assertEqual(response.status_code, 302)
        site = Site.objects.filter(user=self.user).first()
        self.assertIsNotNone(site)


class SiteEditViewTestCase(TestCase):
    """サイト編集ビューのテスト"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.site = Site.objects.create(user=self.user, title='テストサイト')

    def test_site_edit_view(self):
        """編集ページが正常に表示される"""
        response = self.client.get(
            reverse('sites:site_edit', kwargs={
                'user_id': self.user.id,
                'site_id': self.site.id
            })
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'テストサイト')

    def test_site_edit_creates_sections(self):
        """編集ページアクセス時にセクションが自動作成される"""
        response = self.client.get(
            reverse('sites:site_edit', kwargs={
                'user_id': self.user.id,
                'site_id': self.site.id
            })
        )
        self.assertEqual(response.status_code, 200)

        # セクションが作成されたか確認
        self.assertTrue(TopSection.objects.filter(site=self.site).exists())
        self.assertTrue(MainSection.objects.filter(site=self.site).exists())
        self.assertTrue(SubSection.objects.filter(site=self.site).exists())
        self.assertTrue(AccessSection.objects.filter(site=self.site).exists())


class SitePreviewViewTestCase(TestCase):
    """サイトプレビュービューのテスト"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.site = Site.objects.create(user=self.user, title='テストサイト')
        TopSection.objects.create(site=self.site)
        MainSection.objects.create(site=self.site, title='メイン', subtitle='サブタイトル')
        SubSection.objects.create(site=self.site)
        AccessSection.objects.create(site=self.site, section_title='アクセス')

    def test_preview_view(self):
        """プレビューページが正常に表示される"""
        response = self.client.get(
            reverse('sites:site_preview', kwargs={'site_id': self.site.id})
        )
        self.assertEqual(response.status_code, 200)


class SaveBasicViewTestCase(TestCase):
    """基本情報保存ビューのテスト"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.site = Site.objects.create(user=self.user, title='テストサイト')

    def test_save_basic(self):
        """基本情報の保存が正常に動作する"""
        response = self.client.post(
            reverse('sites:save_basic', kwargs={
                'user_id': self.user.id,
                'site_id': self.site.id
            }),
            {'title': '更新されたタイトル'}
        )
        self.assertEqual(response.status_code, 302)

        self.site.refresh_from_db()
        self.assertEqual(self.site.title, '更新されたタイトル')

    def test_save_basic_htmx(self):
        """HTMXリクエストでの保存が正常に動作する"""
        response = self.client.post(
            reverse('sites:save_basic', kwargs={
                'user_id': self.user.id,
                'site_id': self.site.id
            }),
            {'title': 'HTMXタイトル'},
            HTTP_HX_REQUEST='true'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('保存しました', response.content.decode())


class SaveTopViewTestCase(TestCase):
    """トップセクション保存ビューのテスト"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.site = Site.objects.create(user=self.user, title='テストサイト')

    def test_save_top_with_image(self):
        """画像付きでトップセクションを保存できる"""
        image = create_test_image()
        response = self.client.post(
            reverse('sites:save_top', kwargs={
                'user_id': self.user.id,
                'site_id': self.site.id
            }),
            {
                'hero_image': image,
                'top-background_color': '#FF0000',
                'top-text_color': '#FFFFFF',
                'top-font_family': 'Noto Sans JP'
            }
        )
        self.assertEqual(response.status_code, 302)

        top_section = TopSection.objects.get(site=self.site)
        self.assertTrue(top_section.hero_image)

    def test_save_top_style(self):
        """スタイル設定が正しく保存される"""
        response = self.client.post(
            reverse('sites:save_top', kwargs={
                'user_id': self.user.id,
                'site_id': self.site.id
            }),
            {
                'top-background_color': '#123456',
                'top-text_color': '#FEDCBA',
                'top-font_family': 'Noto Serif JP'
            }
        )
        self.assertEqual(response.status_code, 302)

        style = SectionStyle.objects.get(site=self.site, section_name='top')
        self.assertEqual(style.background_color, '#123456')
        self.assertEqual(style.text_color, '#FEDCBA')
        self.assertEqual(style.font_family, 'Noto Serif JP')


class SaveMainViewTestCase(TestCase):
    """メインセクション保存ビューのテスト"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.site = Site.objects.create(user=self.user, title='テストサイト')

    def test_save_main(self):
        """メインセクションを保存できる"""
        response = self.client.post(
            reverse('sites:save_main', kwargs={
                'user_id': self.user.id,
                'site_id': self.site.id
            }),
            {
                'title': 'メインタイトル',
                'subtitle': 'サブタイトル',
                'main-background_color': '#FFFFFF',
                'main-text_color': '#000000',
                'main-font_family': 'Noto Sans JP'
            }
        )
        self.assertEqual(response.status_code, 302)

        main_section = MainSection.objects.get(site=self.site)
        self.assertEqual(main_section.title, 'メインタイトル')
        self.assertEqual(main_section.subtitle, 'サブタイトル')


class SaveSubViewTestCase(TestCase):
    """サブセクション保存ビューのテスト"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.site = Site.objects.create(user=self.user, title='テストサイト')

    def test_save_sub(self):
        """サブセクションを保存できる"""
        response = self.client.post(
            reverse('sites:save_sub', kwargs={
                'user_id': self.user.id,
                'site_id': self.site.id
            }),
            {
                'text1': 'テキスト1の内容',
                'text2': 'テキスト2の内容',
                'text3': 'テキスト3の内容',
                'sub-background_color': '#FFFFFF',
                'sub-text_color': '#000000',
                'sub-font_family': 'Noto Sans JP'
            }
        )
        self.assertEqual(response.status_code, 302)

        sub_section = SubSection.objects.get(site=self.site)
        self.assertEqual(sub_section.text1, 'テキスト1の内容')


class SaveAccessViewTestCase(TestCase):
    """アクセスセクション保存ビューのテスト"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.site = Site.objects.create(user=self.user, title='テストサイト')

    def test_save_access(self):
        """アクセスセクションを保存できる"""
        response = self.client.post(
            reverse('sites:save_access', kwargs={
                'user_id': self.user.id,
                'site_id': self.site.id
            }),
            {
                'section_title': 'アクセス情報',
                'address': '東京都渋谷区1-2-3',
                'phone': '03-1234-5678',
                'hours_day[]': ['月-金', '土日祝'],
                'hours_time[]': ['9:00-18:00', '定休日'],
                'access-background_color': '#FFFFFF',
                'access-text_color': '#000000',
                'access-font_family': 'Noto Sans JP'
            }
        )
        self.assertEqual(response.status_code, 302)

        access_section = AccessSection.objects.get(site=self.site)
        self.assertEqual(access_section.section_title, 'アクセス情報')
        self.assertEqual(access_section.address, '東京都渋谷区1-2-3')
        self.assertEqual(len(access_section.business_hours), 2)


class SaveSNSViewTestCase(TestCase):
    """SNSリンク保存ビューのテスト"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.site = Site.objects.create(user=self.user, title='テストサイト')

    def test_save_sns(self):
        """SNSリンクを保存できる"""
        response = self.client.post(
            reverse('sites:save_sns', kwargs={
                'user_id': self.user.id,
                'site_id': self.site.id
            }),
            {
                'sns_instagram': 'https://instagram.com/test',
                'sns_x': 'https://x.com/test',
                'sns_youtube': 'https://youtube.com/test'
            }
        )
        self.assertEqual(response.status_code, 302)

        # SNSリンクが作成されたか確認
        self.assertEqual(SNSLink.objects.filter(site=self.site).count(), 3)

    def test_save_sns_empty_removes(self):
        """空のURLでSNSリンクを削除できる"""
        # 先にリンクを作成
        SNSLink.objects.create(
            site=self.site,
            platform='instagram',
            url='https://instagram.com/old'
        )

        response = self.client.post(
            reverse('sites:save_sns', kwargs={
                'user_id': self.user.id,
                'site_id': self.site.id
            }),
            {
                'sns_instagram': ''  # 空にする
            }
        )
        self.assertEqual(response.status_code, 302)

        # リンクが削除されたか確認
        self.assertFalse(
            SNSLink.objects.filter(site=self.site, platform='instagram').exists()
        )


class EdgeCaseTestCase(TestCase):
    """エッジケースのテスト"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.site = Site.objects.create(user=self.user, title='テストサイト')

    def test_empty_fields(self):
        """空のフィールドでも保存できる"""
        response = self.client.post(
            reverse('sites:save_main', kwargs={
                'user_id': self.user.id,
                'site_id': self.site.id
            }),
            {
                'title': '',
                'subtitle': '',
                'main-background_color': '#FFFFFF',
                'main-text_color': '#000000',
                'main-font_family': 'Noto Sans JP'
            }
        )
        self.assertEqual(response.status_code, 302)

        main_section = MainSection.objects.get(site=self.site)
        self.assertEqual(main_section.title, '')

    def test_long_text(self):
        """長いテキストでも保存できる"""
        long_text = 'あ' * 10000  # 10000文字

        response = self.client.post(
            reverse('sites:save_sub', kwargs={
                'user_id': self.user.id,
                'site_id': self.site.id
            }),
            {
                'text1': long_text,
                'text2': '',
                'text3': '',
                'sub-background_color': '#FFFFFF',
                'sub-text_color': '#000000',
                'sub-font_family': 'Noto Sans JP'
            }
        )
        self.assertEqual(response.status_code, 302)

        sub_section = SubSection.objects.get(site=self.site)
        self.assertEqual(len(sub_section.text1), 10000)

    def test_invalid_image_format(self):
        """不正な画像形式でのアップロードを処理できる"""
        # テキストファイルを画像として送信
        invalid_file = SimpleUploadedFile(
            name='test.txt',
            content=b'This is not an image',
            content_type='text/plain'
        )

        response = self.client.post(
            reverse('sites:save_top', kwargs={
                'user_id': self.user.id,
                'site_id': self.site.id
            }),
            {
                'hero_image': invalid_file,
                'top-background_color': '#FFFFFF',
                'top-text_color': '#000000',
                'top-font_family': 'Noto Sans JP'
            }
        )
        # エラーまたはリダイレクト（バリデーションエラー）
        self.assertIn(response.status_code, [302, 400])

    def test_valid_png_image(self):
        """PNG形式の画像をアップロードできる"""
        image = create_test_image(name='test.png', format='PNG')
        response = self.client.post(
            reverse('sites:save_top', kwargs={
                'user_id': self.user.id,
                'site_id': self.site.id
            }),
            {
                'hero_image': image,
                'top-background_color': '#FFFFFF',
                'top-text_color': '#000000',
                'top-font_family': 'Noto Sans JP'
            }
        )
        self.assertEqual(response.status_code, 302)

    def test_valid_webp_image(self):
        """WebP形式の画像をアップロードできる"""
        image = create_test_image(name='test.webp', format='WEBP')
        response = self.client.post(
            reverse('sites:save_top', kwargs={
                'user_id': self.user.id,
                'site_id': self.site.id
            }),
            {
                'hero_image': image,
                'top-background_color': '#FFFFFF',
                'top-text_color': '#000000',
                'top-font_family': 'Noto Sans JP'
            }
        )
        self.assertEqual(response.status_code, 302)


class GoogleMapsEmbedTestCase(TestCase):
    """Googleマップ埋め込みのテスト"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.site = Site.objects.create(user=self.user, title='テストサイト')
        self.access_section = AccessSection.objects.create(
            site=self.site,
            address='東京都港区芝公園4丁目2-8'
        )

    def test_google_maps_url_generation(self):
        """Googleマップ埋め込みURLが正しく生成される"""
        url = self.access_section.get_google_maps_embed_url()
        self.assertIsNotNone(url)
        self.assertIn('maps.google.com', url)
        self.assertIn('output=embed', url)
        # URLエンコードされているため、元の住所ではなくURLの形式を確認
        self.assertTrue(url.startswith('https://maps.google.com/maps?q='))

    def test_google_maps_url_empty_address(self):
        """住所が空の場合はNoneを返す"""
        self.access_section.address = ''
        self.access_section.save()
        url = self.access_section.get_google_maps_embed_url()
        self.assertIsNone(url)


class BusinessHoursTestCase(TestCase):
    """営業時間のテスト"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.site = Site.objects.create(user=self.user, title='テストサイト')

    def test_business_hours_json(self):
        """営業時間がJSON形式で正しく保存される"""
        response = self.client.post(
            reverse('sites:save_access', kwargs={
                'user_id': self.user.id,
                'site_id': self.site.id
            }),
            {
                'section_title': 'アクセス',
                'address': '東京都',
                'phone': '03-0000-0000',
                'hours_day[]': ['月-金', '土', '日祝'],
                'hours_time[]': ['9:00-18:00', '10:00-17:00', '定休日'],
                'access-background_color': '#FFFFFF',
                'access-text_color': '#000000',
                'access-font_family': 'Noto Sans JP'
            }
        )

        access_section = AccessSection.objects.get(site=self.site)
        self.assertEqual(len(access_section.business_hours), 3)
        self.assertEqual(access_section.business_hours[0]['day'], '月-金')
        self.assertEqual(access_section.business_hours[0]['hours'], '9:00-18:00')

    def test_empty_business_hours(self):
        """空の営業時間は無視される"""
        response = self.client.post(
            reverse('sites:save_access', kwargs={
                'user_id': self.user.id,
                'site_id': self.site.id
            }),
            {
                'section_title': 'アクセス',
                'address': '',
                'phone': '',
                'hours_day[]': ['', '月-金'],
                'hours_time[]': ['', '9:00-18:00'],
                'access-background_color': '#FFFFFF',
                'access-text_color': '#000000',
                'access-font_family': 'Noto Sans JP'
            }
        )

        access_section = AccessSection.objects.get(site=self.site)
        # 空の行は無視される
        self.assertEqual(len(access_section.business_hours), 1)
