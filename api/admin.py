from django.contrib import admin
from .models import Dataset, TextEntry, Category, Operator


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'total_entries', 'tagged_entries', 'category_count', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    inlines = [CategoryInline]

    def category_count(self, obj):
        return obj.categories.count()
    category_count.short_description = 'Number of Categories'



@admin.register(TextEntry)
class TextEntryAdmin(admin.ModelAdmin):
    list_display = ('content', 'dataset', 'is_tagged', 'tagged_by', 'tagged_at', 'created_at')
    list_filter = ('dataset', 'is_tagged', 'tagged_by')
    search_fields = ('content',)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "categories":
            obj_id = request.resolver_match.kwargs.get('object_id')
            if obj_id:
                entry = TextEntry.objects.get(pk=obj_id)
                kwargs["queryset"] = Category.objects.filter(dataset=entry.dataset)
        return super().formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'dataset', 'is_active', 'labeled_instances_count')
    search_fields = ('name',)
    list_filter = ('dataset', 'is_active')
    ordering = ('name',)



class DatasetInline(admin.TabularInline):
    model = Operator.datasets.through
    extra = 1

@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)
    inlines = [DatasetInline]
    exclude = ('datasets',)

