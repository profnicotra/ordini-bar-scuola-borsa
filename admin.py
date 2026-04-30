from django.contrib import admin
from .models import Prodotto

@admin.register(Prodotto)
class ProdottoAdmin(admin.ModelAdmin):
    # Questo dice a Django di andare a cercare il tuo file HTML
    change_list_template = "admin/admin.html"

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        # Qui prendiamo i prodotti reali dal database
        extra_context['prodotti_reali'] = Prodotto.get_products()
        return super().changelist_view(request, extra_context=extra_context)
