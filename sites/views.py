from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.http import Http404
from .models import (
    Site, SectionStyle, TopSection, SNSLink,
    MainSection, SubSection, AccessSection
)


def site_list(request, user_id):
    """サイト一覧ページ"""
    user = get_object_or_404(User, pk=user_id)
    sites = Site.objects.filter(user=user)

    context = {
        'user': user,
        'sites': sites,
    }
    return render(request, 'sites/list.html', context)


def site_create(request, user_id):
    """サイト新規作成"""
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        title = request.POST.get('title', 'New Site')

        # サイト作成
        site = Site.objects.create(user=user, title=title)

        # 関連セクションを自動作成
        TopSection.objects.create(site=site)
        MainSection.objects.create(site=site)
        SubSection.objects.create(site=site)
        AccessSection.objects.create(site=site)

        # デフォルトのスタイルを作成
        for section_name in ['top', 'main', 'sub', 'access']:
            SectionStyle.objects.create(site=site, section_name=section_name)

        return redirect('sites:site_edit', user_id=user.id, site_id=site.id)

    context = {
        'user': user,
    }
    return render(request, 'sites/create.html', context)


def site_edit(request, user_id, site_id):
    """サイト編集ページ"""
    user = get_object_or_404(User, pk=user_id)
    site = get_object_or_404(Site, pk=site_id, user=user)

    # 関連データを取得（なければ作成）
    top_section, _ = TopSection.objects.get_or_create(site=site)
    main_section, _ = MainSection.objects.get_or_create(site=site)
    sub_section, _ = SubSection.objects.get_or_create(site=site)
    access_section, _ = AccessSection.objects.get_or_create(site=site)

    # スタイル設定を取得（なければ作成）
    styles = {}
    for section_name in ['top', 'main', 'sub', 'access']:
        style, _ = SectionStyle.objects.get_or_create(
            site=site,
            section_name=section_name
        )
        styles[section_name] = style

    # SNSリンクを取得
    sns_links = SNSLink.objects.filter(site=site)

    context = {
        'user': user,
        'site': site,
        'top_section': top_section,
        'main_section': main_section,
        'sub_section': sub_section,
        'access_section': access_section,
        'styles': styles,
        'sns_links': sns_links,
    }
    return render(request, 'sites/edit.html', context)


def site_preview(request, site_id):
    """サイトプレビューページ"""
    site = get_object_or_404(Site, pk=site_id)

    # 関連データを取得
    top_section = getattr(site, 'top_section', None)
    main_section = getattr(site, 'main_section', None)
    sub_section = getattr(site, 'sub_section', None)
    access_section = getattr(site, 'access_section', None)

    # スタイル設定を取得
    styles = {}
    for style in site.section_styles.all():
        styles[style.section_name] = style

    # SNSリンクを取得
    sns_links = site.sns_links.filter(is_active=True)

    context = {
        'site': site,
        'top_section': top_section,
        'main_section': main_section,
        'sub_section': sub_section,
        'access_section': access_section,
        'styles': styles,
        'sns_links': sns_links,
    }
    return render(request, 'sites/preview.html', context)
