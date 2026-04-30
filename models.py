from django.db import models

class Prodotto(models.Model):
    nome = models.CharField(max_length=100)
    costo = models.DecimalField(max_digits=6, decimal_places=2)
    prezzo_esterno = models.DecimalField(max_digits=6, decimal_places=2)
    prezzo_interno = models.DecimalField(max_digits=6, decimal_places=2)
    categoria = models.CharField(max_length=50)
    disponibile = models.BooleanField(default=True)

    @staticmethod
    def get_products():
        return Prodotto.objects.all()

    def __str__(self):
        return self.nome
