from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import (
    Site, SectionStyle, TopSection, SNSLink,
    MainSection, SubSection, AccessSection
)
from .forms import (
    SiteForm, SectionStyleForm, TopSectionForm,
    MainSectionForm, SubSectionForm, AccessSectionForm,
    SNSLinkFormSet
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

        messages.success(request, f'サイト「{title}」を作成しました。')
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
    sns_links_dict = {link.platform: link.url for link in sns_links}

    # フォームの初期化
    site_form = SiteForm(instance=site)
    top_form = TopSectionForm(instance=top_section)
    main_form = MainSectionForm(instance=main_section)
    sub_form = SubSectionForm(instance=sub_section)
    access_form = AccessSectionForm(instance=access_section)

    # スタイルフォーム
    style_forms = {}
    for section_name, style in styles.items():
        style_forms[section_name] = SectionStyleForm(instance=style, prefix=section_name)

    context = {
        'user': user,
        'site': site,
        'top_section': top_section,
        'main_section': main_section,
        'sub_section': sub_section,
        'access_section': access_section,
        'styles': styles,
        'sns_links': sns_links,
        'sns_links_dict': sns_links_dict,
        'site_form': site_form,
        'top_form': top_form,
        'main_form': main_form,
        'sub_form': sub_form,
        'access_form': access_form,
        'style_forms': style_forms,
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


# =============================================================================
# セクション保存ビュー
# =============================================================================

@require_POST
def save_basic(request, user_id, site_id):
    """基本情報の保存"""
    user = get_object_or_404(User, pk=user_id)
    site = get_object_or_404(Site, pk=site_id, user=user)

    form = SiteForm(request.POST, instance=site)
    if form.is_valid():
        form.save()
        if request.headers.get('HX-Request'):
            return HttpResponse(
                '<div class="text-green-600 text-sm">保存しました</div>',
                headers={'HX-Trigger': 'saved'}
            )
        messages.success(request, '基本情報を保存しました。')
    else:
        if request.headers.get('HX-Request'):
            return HttpResponse(
                '<div class="text-red-600 text-sm">エラーが発生しました</div>',
                status=400
            )
        messages.error(request, '保存に失敗しました。')

    return redirect('sites:site_edit', user_id=user_id, site_id=site_id)


@require_POST
def save_top(request, user_id, site_id):
    """トップセクションの保存"""
    user = get_object_or_404(User, pk=user_id)
    site = get_object_or_404(Site, pk=site_id, user=user)
    top_section, _ = TopSection.objects.get_or_create(site=site)
    style, _ = SectionStyle.objects.get_or_create(site=site, section_name='top')

    # トップセクションフォーム
    top_form = TopSectionForm(request.POST, request.FILES, instance=top_section)

    # スタイルフォーム
    style_form = SectionStyleForm(request.POST, instance=style, prefix='top')

    if top_form.is_valid() and style_form.is_valid():
        top_form.save()
        style_form.save()
        if request.headers.get('HX-Request'):
            return HttpResponse(
                '<div class="text-green-600 text-sm">保存しました</div>',
                headers={'HX-Trigger': 'saved'}
            )
        messages.success(request, 'トップセクションを保存しました。')
    else:
        if request.headers.get('HX-Request'):
            errors = {**top_form.errors, **style_form.errors}
            return HttpResponse(
                f'<div class="text-red-600 text-sm">エラー: {errors}</div>',
                status=400
            )
        messages.error(request, '保存に失敗しました。')

    return redirect('sites:site_edit', user_id=user_id, site_id=site_id)


@require_POST
def save_main(request, user_id, site_id):
    """メインセクションの保存"""
    user = get_object_or_404(User, pk=user_id)
    site = get_object_or_404(Site, pk=site_id, user=user)
    main_section, _ = MainSection.objects.get_or_create(site=site)
    style, _ = SectionStyle.objects.get_or_create(site=site, section_name='main')

    main_form = MainSectionForm(request.POST, request.FILES, instance=main_section)
    style_form = SectionStyleForm(request.POST, instance=style, prefix='main')

    if main_form.is_valid() and style_form.is_valid():
        main_form.save()
        style_form.save()
        if request.headers.get('HX-Request'):
            return HttpResponse(
                '<div class="text-green-600 text-sm">保存しました</div>',
                headers={'HX-Trigger': 'saved'}
            )
        messages.success(request, 'メインセクションを保存しました。')
    else:
        if request.headers.get('HX-Request'):
            errors = {**main_form.errors, **style_form.errors}
            return HttpResponse(
                f'<div class="text-red-600 text-sm">エラー: {errors}</div>',
                status=400
            )
        messages.error(request, '保存に失敗しました。')

    return redirect('sites:site_edit', user_id=user_id, site_id=site_id)


@require_POST
def save_sub(request, user_id, site_id):
    """サブセクションの保存"""
    user = get_object_or_404(User, pk=user_id)
    site = get_object_or_404(Site, pk=site_id, user=user)
    sub_section, _ = SubSection.objects.get_or_create(site=site)
    style, _ = SectionStyle.objects.get_or_create(site=site, section_name='sub')

    sub_form = SubSectionForm(request.POST, request.FILES, instance=sub_section)
    style_form = SectionStyleForm(request.POST, instance=style, prefix='sub')

    if sub_form.is_valid() and style_form.is_valid():
        sub_form.save()
        style_form.save()
        if request.headers.get('HX-Request'):
            return HttpResponse(
                '<div class="text-green-600 text-sm">保存しました</div>',
                headers={'HX-Trigger': 'saved'}
            )
        messages.success(request, 'サブセクションを保存しました。')
    else:
        if request.headers.get('HX-Request'):
            errors = {**sub_form.errors, **style_form.errors}
            return HttpResponse(
                f'<div class="text-red-600 text-sm">エラー: {errors}</div>',
                status=400
            )
        messages.error(request, '保存に失敗しました。')

    return redirect('sites:site_edit', user_id=user_id, site_id=site_id)


@require_POST
def save_access(request, user_id, site_id):
    """アクセスセクションの保存"""
    user = get_object_or_404(User, pk=user_id)
    site = get_object_or_404(Site, pk=site_id, user=user)
    access_section, _ = AccessSection.objects.get_or_create(site=site)
    style, _ = SectionStyle.objects.get_or_create(site=site, section_name='access')

    access_form = AccessSectionForm(request.POST, instance=access_section)
    style_form = SectionStyleForm(request.POST, instance=style, prefix='access')

    # 営業時間の処理
    days = request.POST.getlist('hours_day[]')
    times = request.POST.getlist('hours_time[]')
    business_hours = []
    for day, hours in zip(days, times):
        if day.strip() and hours.strip():
            business_hours.append({'day': day.strip(), 'hours': hours.strip()})

    if access_form.is_valid() and style_form.is_valid():
        access = access_form.save(commit=False)
        access.business_hours = business_hours
        access.save()
        style_form.save()
        if request.headers.get('HX-Request'):
            return HttpResponse(
                '<div class="text-green-600 text-sm">保存しました</div>',
                headers={'HX-Trigger': 'saved'}
            )
        messages.success(request, 'アクセスセクションを保存しました。')
    else:
        if request.headers.get('HX-Request'):
            errors = {**access_form.errors, **style_form.errors}
            return HttpResponse(
                f'<div class="text-red-600 text-sm">エラー: {errors}</div>',
                status=400
            )
        messages.error(request, '保存に失敗しました。')

    return redirect('sites:site_edit', user_id=user_id, site_id=site_id)


@require_POST
def save_sns(request, user_id, site_id):
    """SNSリンクの保存"""
    user = get_object_or_404(User, pk=user_id)
    site = get_object_or_404(Site, pk=site_id, user=user)

    platforms = ['instagram', 'x', 'line', 'facebook', 'youtube', 'tiktok']

    for platform in platforms:
        url = request.POST.get(f'sns_{platform}', '').strip()

        if url:
            sns_link, created = SNSLink.objects.update_or_create(
                site=site,
                platform=platform,
                defaults={'url': url, 'is_active': True}
            )
        else:
            # URLが空の場合は削除
            SNSLink.objects.filter(site=site, platform=platform).delete()

    if request.headers.get('HX-Request'):
        return HttpResponse(
            '<div class="text-green-600 text-sm">保存しました</div>',
            headers={'HX-Trigger': 'saved'}
        )
    messages.success(request, 'SNSリンクを保存しました。')
    return redirect('sites:site_edit', user_id=user_id, site_id=site_id)


# =============================================================================
# HTMXプレビュー更新ビュー
# =============================================================================

def preview_header(request, site_id):
    """ヘッダーのプレビュー更新"""
    site = get_object_or_404(Site, pk=site_id)
    style = SectionStyle.objects.filter(site=site, section_name='top').first()
    sns_links = site.sns_links.filter(is_active=True)

    context = {
        'site': site,
        'style': style,
        'sns_links': sns_links,
    }
    return render(request, 'components/header.html', context)


def preview_top(request, site_id):
    """トップセクションのプレビュー更新"""
    site = get_object_or_404(Site, pk=site_id)
    top_section = getattr(site, 'top_section', None)
    style = SectionStyle.objects.filter(site=site, section_name='top').first()

    context = {
        'site': site,
        'top_section': top_section,
        'style': style,
    }
    return render(request, 'components/top.html', context)


def preview_main(request, site_id):
    """メインセクションのプレビュー更新"""
    site = get_object_or_404(Site, pk=site_id)
    main_section = getattr(site, 'main_section', None)
    style = SectionStyle.objects.filter(site=site, section_name='main').first()

    context = {
        'site': site,
        'main_section': main_section,
        'style': style,
    }
    return render(request, 'components/main.html', context)


def preview_sub(request, site_id):
    """サブセクションのプレビュー更新"""
    site = get_object_or_404(Site, pk=site_id)
    sub_section = getattr(site, 'sub_section', None)
    style = SectionStyle.objects.filter(site=site, section_name='sub').first()

    context = {
        'site': site,
        'sub_section': sub_section,
        'style': style,
    }
    return render(request, 'components/sub.html', context)


def preview_access(request, site_id):
    """アクセスセクションのプレビュー更新"""
    site = get_object_or_404(Site, pk=site_id)
    access_section = getattr(site, 'access_section', None)
    style = SectionStyle.objects.filter(site=site, section_name='access').first()

    context = {
        'site': site,
        'access_section': access_section,
        'style': style,
    }
    return render(request, 'components/access.html', context)
