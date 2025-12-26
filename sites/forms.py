from django import forms
from django.forms import inlineformset_factory
from .models import (
    Site, SectionStyle, TopSection, SNSLink,
    MainSection, SubSection, AccessSection
)


class SiteForm(forms.ModelForm):
    """サイト基本情報フォーム"""
    class Meta:
        model = Site
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'サイトタイトルを入力',
            }),
        }


class SectionStyleForm(forms.ModelForm):
    """セクションスタイル設定フォーム"""
    FONT_CHOICES = [
        # ゴシック系
        ('Noto Sans JP', 'Noto Sans JP（ゴシック）'),
        ('M PLUS 1p', 'M PLUS 1p（ゴシック）'),
        ('M PLUS Rounded 1c', 'M PLUS Rounded 1c（丸ゴシック）'),
        ('Kosugi Maru', 'Kosugi Maru（丸ゴシック）'),
        ('Zen Kaku Gothic New', 'Zen Kaku Gothic New（ゴシック）'),
        # 明朝系
        ('Noto Serif JP', 'Noto Serif JP（明朝）'),
        ('Sawarabi Mincho', 'Sawarabi Mincho（明朝）'),
        ('Zen Old Mincho', 'Zen Old Mincho（明朝）'),
        ('Shippori Mincho', 'Shippori Mincho（明朝）'),
        # デザイン系
        ('Zen Maru Gothic', 'Zen Maru Gothic（丸ゴシック）'),
        ('Kaisei Decol', 'Kaisei Decol（デコラティブ）'),
        ('Dela Gothic One', 'Dela Gothic One（太字）'),
        ('Reggae One', 'Reggae One（ポップ）'),
        ('RocknRoll One', 'RocknRoll One（ポップ）'),
        ('Yusei Magic', 'Yusei Magic（手書き風）'),
        ('Klee One', 'Klee One（手書き風）'),
        ('Hachi Maru Pop', 'Hachi Maru Pop（ポップ）'),
        # 英語フォント
        ('Roboto', 'Roboto（英語）'),
        ('Open Sans', 'Open Sans（英語）'),
        ('Lato', 'Lato（英語）'),
        ('Montserrat', 'Montserrat（英語）'),
        ('Poppins', 'Poppins（英語）'),
        ('Playfair Display', 'Playfair Display（英語セリフ）'),
    ]

    font_family = forms.ChoiceField(
        choices=FONT_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full px-2 py-1 text-sm border border-gray-300 rounded',
        })
    )

    class Meta:
        model = SectionStyle
        fields = ['background_color', 'text_color', 'font_family']
        widgets = {
            'background_color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'color-picker',
            }),
            'text_color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'color-picker',
            }),
        }


class TopSectionForm(forms.ModelForm):
    """トップセクションフォーム"""
    class Meta:
        model = TopSection
        fields = ['hero_image', 'hero_image_fit', 'hero_image_height']
        widgets = {
            'hero_image': forms.FileInput(attrs={
                'accept': '.jpg,.jpeg,.png,.webp',
                'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100',
            }),
            'hero_image_fit': forms.Select(attrs={
                'class': 'w-full px-2 py-1 text-sm border border-gray-300 rounded',
            }),
            'hero_image_height': forms.NumberInput(attrs={
                'class': 'w-full px-2 py-1 text-sm border border-gray-300 rounded',
                'min': '100',
                'max': '1000',
                'step': '50',
            }),
        }


class MainSectionForm(forms.ModelForm):
    """メインセクション（カルーセル）フォーム"""
    class Meta:
        model = MainSection
        fields = ['title', 'subtitle', 'image1', 'image2', 'image3', 'image_fit', 'image_height']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'タイトルを入力',
            }),
            'subtitle': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'サブタイトルを入力',
            }),
            'image1': forms.FileInput(attrs={
                'accept': '.jpg,.jpeg,.png,.webp',
                'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100',
            }),
            'image2': forms.FileInput(attrs={
                'accept': '.jpg,.jpeg,.png,.webp',
                'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100',
            }),
            'image3': forms.FileInput(attrs={
                'accept': '.jpg,.jpeg,.png,.webp',
                'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100',
            }),
            'image_fit': forms.Select(attrs={
                'class': 'w-full px-2 py-1 text-sm border border-gray-300 rounded',
            }),
            'image_height': forms.NumberInput(attrs={
                'class': 'w-full px-2 py-1 text-sm border border-gray-300 rounded',
                'min': '100',
                'max': '800',
                'step': '50',
            }),
        }


class SubSectionForm(forms.ModelForm):
    """サブセクションフォーム"""
    class Meta:
        model = SubSection
        fields = ['image1', 'text1', 'image2', 'text2', 'image3', 'text3', 'image_fit', 'image_height']
        widgets = {
            'image1': forms.FileInput(attrs={
                'accept': '.jpg,.jpeg,.png,.webp',
                'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100',
            }),
            'text1': forms.Textarea(attrs={
                'rows': 3,
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'テキストを入力',
            }),
            'image2': forms.FileInput(attrs={
                'accept': '.jpg,.jpeg,.png,.webp',
                'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100',
            }),
            'text2': forms.Textarea(attrs={
                'rows': 3,
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'テキストを入力',
            }),
            'image3': forms.FileInput(attrs={
                'accept': '.jpg,.jpeg,.png,.webp',
                'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100',
            }),
            'text3': forms.Textarea(attrs={
                'rows': 3,
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'テキストを入力',
            }),
            'image_fit': forms.Select(attrs={
                'class': 'w-full px-2 py-1 text-sm border border-gray-300 rounded',
            }),
            'image_height': forms.NumberInput(attrs={
                'class': 'w-full px-2 py-1 text-sm border border-gray-300 rounded',
                'min': '100',
                'max': '600',
                'step': '50',
            }),
        }


class AccessSectionForm(forms.ModelForm):
    """アクセスセクションフォーム"""
    class Meta:
        model = AccessSection
        fields = ['section_title', 'address', 'phone']
        widgets = {
            'section_title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'セクションタイトル',
            }),
            'address': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': '例: 東京都港区芝公園4丁目2-8',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': '例: 03-1234-5678',
            }),
        }


class SNSLinkForm(forms.ModelForm):
    """SNSリンクフォーム"""
    class Meta:
        model = SNSLink
        fields = ['platform', 'url', 'is_active']
        widgets = {
            'platform': forms.Select(attrs={
                'class': 'px-3 py-2 border border-gray-300 rounded-lg',
            }),
            'url': forms.URLInput(attrs={
                'class': 'flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'https://...',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500',
            }),
        }


# SNSリンクのフォームセット
SNSLinkFormSet = inlineformset_factory(
    Site,
    SNSLink,
    form=SNSLinkForm,
    extra=6,  # 6つのプラットフォーム分
    max_num=6,
    can_delete=True,
)


class BusinessHoursForm(forms.Form):
    """営業時間フォーム（動的追加用）"""
    day = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'flex-1 px-3 py-2 border border-gray-300 rounded-lg',
            'placeholder': '曜日（例: 月-金）',
        })
    )
    hours = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'flex-1 px-3 py-2 border border-gray-300 rounded-lg',
            'placeholder': '時間（例: 9:00-18:00）',
        })
    )
