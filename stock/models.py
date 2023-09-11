from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
import uuid

# Create your models here.
class Category(models.Model):
    label = models.CharField(max_length=50, blank=False, null=False)

    class Meta:
        ordering = ['label']
    
    def __str__(self):
        return self.label
    
    def get_absolute_url(self):
        return reverse('category-detail', args=[str(self.id)])
    
    @property
    def sale_count(self):
        return ProductSale.objects.filter(product__category=self).count()
    
    @property
    def product_count(self):
        return self.product_set.count()
    
    @property
    def weight(self):
        total = ProductSale.objects.count()
        return self.sale_count / total if total != 0 else 0.0
    
    @property
    def popularity(self):
        highest = max(list(cat.weight for cat in Category.objects.all()))
        return round(self.weight/highest*10.0, 1) if highest != 0.0 else 0.0


class Product(models.Model):
    UNITS = (
        ('u', 'Unit'),
        ('kg', 'Kilogram'),
        ('g', 'Gram'),
        ('l', 'Litre'),
        ('ml', 'Millilitre'),
    )

    name = models.CharField(max_length=50, help_text='Product name', blank=False, null=False)
    brand = models.CharField(max_length=50, help_text='Product brand', blank=False, null=False)
    category = models.ForeignKey(Category, help_text='Product category', on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField(max_length=400, help_text='Product description', blank=True, null=True)
    unit = models.CharField(max_length=2, choices=UNITS, help_text='Product unit', blank=False, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Price per unit', blank=False, null=False, validators=[MinValueValidator(0.0)])
    cost = models.DecimalField(max_digits=10, decimal_places=2, help_text='Base cost per unit', blank=False, null=False, validators=[MinValueValidator(0.0)])
    quantity = models.PositiveIntegerField(help_text='Quantity available', blank=False, null=False)
    enabled = models.BooleanField(help_text='Product enabled', default=True, blank=False, null=False)

    class Meta:
        ordering = ['name', 'brand']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product-detail', args=[str(self.id)])
    
    @property
    def available(self):
        return self.enabled and self.quantity > 0
    
    @property
    def unit_label(self):
        for item in Product.UNITS:
            if item[0] == self.unit:
                return item[1]
        return ''
    
    @property
    def weight(self):
        total = ProductSale.objects.count()
        return self.productsale_set.count() / total if total != 0 else 0.0
    
    @property
    def popularity(self):
        highest = max(list(p.weight for p in Product.objects.all()))
        return round(self.weight/highest*10.0, 1) if highest != 0.0 else 0.0
    
    @property
    def profit(self):
        return round(self.price-self.cost, 2)
    
    @property
    def sale_count(self):
        return self.productsale_set.count()


class ProductSale(models.Model):
    product = models.ForeignKey(Product, help_text='Sold product', on_delete=models.RESTRICT, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Checkout price per unit', default=0.0, blank=False, null=False, validators=[MinValueValidator(0.0)])
    cost = models.DecimalField(max_digits=10, decimal_places=2, help_text='Checkout cost per unit', default=0.0, blank=False, null=False, validators=[MinValueValidator(0.0)])
    quantity = models.PositiveIntegerField(help_text='Quantity sold', default=0, blank=False, null=False)
    bill = models.ForeignKey('Bill', default=None, on_delete=models.SET_NULL, help_text='Associated bill', null=True)

    class Meta:
        ordering = ['bill', 'product']

    def __str__(self):
        return f'ProductSale#{self.id}'
    
    # Save must be called only once
    def save(self, *args, **kwargs):
        if self.quantity < 0:
            raise ValueError('Quantity cannot be negative!')
        # Editing Product quantity
        p = self.product
        if not p or p.quantity < self.quantity:
            raise ValueError('Product must be non-null and quantity must be <= Product stock quantity!')
        p.quantity -= self.quantity
        # Calculating product's current price here
        # TO-DO: implement discounted price
        self.price = p.price
        self.cost = p.cost
        p.save()
        super().save(*args, **kwargs)
    
    @property
    def profit(self):
        return round((self.price-self.cost)*self.quantity, 2)


class Bill(models.Model):
    MEMO_ITEM_NO = 'no'
    MEMO_ITEM_PRODUCT_NAME = 'product-name'
    MEMO_ITEM_PRODUCT_UNIT = 'product-unit'
    MEMO_ITEM_PRODUCT_PRICE = 'product-price'
    MEMO_ITEM_QUANTITY = 'quantity'
    MEMO_ITEM_PRICE = 'price'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(auto_now_add=True, help_text='Date of purchase')
    time = models.TimeField(auto_now_add=True, help_text='Time of purchase')
    
    class Meta:
        ordering = ['date', 'time']
    
    def __str__(self):
        return f'Bill#{self.id}-{self.date}'
    
    def get_absolute_url(self):
        return reverse('bill-detail', args=[str(self.id)])
    
    @property
    def total(self):
        return sum(list(sale.quantity*sale.price for sale in self.productsale_set.all()))
    
    @property
    def display_items(self):
        return ', '.join(sorted(item.product.name for item in self.productsale_set.all()))
    
    @property
    def items(self):
        return sorted(item for item in self.productsale_set.all())
    
    @property
    def product_count(self):
        return self.productsale_set.count()
    
    @property
    def profit(self):
        return sum(sale.profit for sale in self.productsale_set.all())
    
    @property
    def categories(self):
        return set(list(sale.product.category for sale in self.productsale_set.all()))
    
    @property
    def display_categories(self):
        return ', '.join(set(list(sale.product.category.label for sale in self.productsale_set.all())))
    
    @property
    def memo(self):
        data = list()
        no = 0
        for sale in self.productsale_set.all():
            no = no + 1
            memo_item = {
                Bill.MEMO_ITEM_NO: str(no),
                Bill.MEMO_ITEM_PRODUCT_NAME: sale.product.name,
                Bill.MEMO_ITEM_PRODUCT_UNIT: sale.product.unit_label,
                Bill.MEMO_ITEM_PRODUCT_PRICE: str(sale.product.price),
                Bill.MEMO_ITEM_QUANTITY: str(sale.quantity),
                Bill.MEMO_ITEM_PRICE: str(sale.quantity * sale.product.price)
            }
            data.append(memo_item)
        return data
