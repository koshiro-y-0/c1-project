from django.contrib import admin
from .models import (
    Site, SectionStyle, TopSection, SNSLink,
    MainSection, SubSection, AccessSection
)


class SectionStyleInline(admin.TabularInline):
    model = SectionStyle
    extra = 0


class SNSLinkInline(admin.TabularInline):
    model = SNSLink
    extra = 0


class TopSectionInline(admin.StackedInline):
    model = TopSection
    can_delete = False


class MainSectionInline(admin.StackedInline):
    model = MainSection
    can_delete = False


class SubSectionInline(admin.StackedInline):
    model = SubSection
    can_delete = False


class AccessSectionInline(admin.StackedInline):
    model = AccessSection
    can_delete = False


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at', 'updated_at']
    list_filter = ['user', 'created_at']
    search_fields = ['title', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [
        SectionStyleInline,
        SNSLinkInline,
        TopSectionInline,
        MainSectionInline,
        SubSectionInline,
        AccessSectionInline,
    ]


@admin.register(SectionStyle)
class SectionStyleAdmin(admin.ModelAdmin):
    list_display = ['site', 'section_name', 'background_color', 'text_color', 'font_family']
    list_filter = ['section_name', 'site']


@admin.register(TopSection)
class TopSectionAdmin(admin.ModelAdmin):
    list_display = ['site', 'hero_image']


@admin.register(SNSLink)
class SNSLinkAdmin(admin.ModelAdmin):
    list_display = ['site', 'platform', 'url', 'is_active']
    list_filter = ['platform', 'is_active']


@admin.register(MainSection)
class MainSectionAdmin(admin.ModelAdmin):
    list_display = ['site', 'title', 'subtitle']


@admin.register(SubSection)
class SubSectionAdmin(admin.ModelAdmin):
    list_display = ['site']


@admin.register(AccessSection)
class AccessSectionAdmin(admin.ModelAdmin):
    list_display = ['site', 'section_title', 'address', 'phone']
