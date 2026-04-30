from django.contrib import admin
from .models import Prodotto

@admin.register(Prodotto)
class ProdottoAdmin(admin.ModelAdmin):
    change_list_template = "admin/admin.html"

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['prodotti_reali'] = Prodotto.get_products()
        return super().changelist_view(request, extra_context=extra_context)
