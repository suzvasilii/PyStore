from sqlalchemy.orm import Session
from typing import List

from ..repositories.product_repository import ProductRepository
from ..repositories.category_repository import CategoryRepository
from ..schemas.product import ProductResponse, ProductListResponse, ProductCreate
from fastapi import HTTPException, status

class ProductService:
    def __init__(self, db: Session):
        self.product_repository = ProductRepository(db)
        self.category_repository = CategoryRepository(db)

    def get_all_products(self)->List[ProductListResponse]:
        products = self.product_repository.get_all()
        products_response =  [ProductResponse.model_validate(prod) for prod in products]
        return ProductListResponse(products=products_response, total=len(products_response))

    def get_product_by_id(self, product_id:int)->ProductResponse:
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {product_id} not found"
            )
        return ProductResponse.model_validate(product)

    def get_product_by_category(self, category_id: int)->ProductListResponse:
        products = self.product_repository.get_by_category(category_id)
        if products is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Products with category {category_id} not found"
            )
        else:
            products_response = [ProductResponse.model_validate(prod) for prod in products]
            return ProductListResponse(products=products_response, total=len(products_response))

    def create_product(self, product_data: ProductCreate)->ProductResponse:
        category = self.category_repository.get_by_id(product_data.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {product_data.category_id} not found"
            )
        product = self.product_repository.create(product_data)
        if not product:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail="BAD Request! check the data you sent"
            )
        return ProductResponse.model_validate(product)