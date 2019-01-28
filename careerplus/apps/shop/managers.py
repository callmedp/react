from django.db import models

class ProductQuerySet(models.query.QuerySet):

    def base_queryset(self):
        
        return self.select_related('product_class', 'vendor')\
            .prefetch_related('countries',
				'categories',
				'productcategories',
				'attributes'
				'productattributes',
				'faqs',
				'productfaqs'
				'childs',
				'variation',
                'variationproduct',
				'siblingproduct')

    def indexable(self):
        return self.filter(is_indexable=True,
        	type_product__in=[0, 1, 3, 5])

    def saleable(self):
    	return self.filter(active=True)
    	
    def browsable(self):
    	return self.filter(is_indexable=True, active=True,
    		type_product__in=[0, 1, 3, 5])


class ProductManager(models.Manager):
    
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def base_queryset(self):
        return self.get_queryset().base_queryset()


class BrowsableProductManager(ProductManager):
    
    def get_queryset(self):
        return super(BrowsableProductManager, self).get_queryset().browsable()


class IndexableProductManager(ProductManager):
    
    def get_queryset(self):
        return super(IndexableProductManager, self).get_queryset().indexable()


class SaleableProductManager(ProductManager):
    
    def get_queryset(self):
        return super(SaleableProductManager, self).get_queryset().saleable()


class SelectedFieldProductManager(models.Manager):

    def get_queryset(self):
        queryset = super(SelectedFieldProductManager,self).get_queryset()
        return queryset.only('id','product_class', 'name')

