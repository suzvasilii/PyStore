from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from ..models.product import Product
from ..schemas.product import ProductCreate

class ProductRepository:
    def __init__(self, db:Session):
        self.db = db

    def get_all(self) -> List[Product]:
        return self.db.query(Product).options(joinedload(Product.category)).all()

    def get_by_id(self, product_id:int)->Optional[Product]:
        return (
        self.db.query(Product)
            .options(joinedload(Product.category))
            .filter(Product.id == product_id)
            .first()
    )

    def get_by_category(self, category_id:int)->Optional[Product]:
        return (
            self.db.query(Product)
            .options(joinedload(Product.category))
            .filter(Product.category_id == category_id)
        )

    def get_multiple_by_ids(self, product_ids:List[int])->List[Product]:
        return (
            self.db.query(Product)
            .options(joinedload(Product.category))
            .filter(Product.id.in_(product_ids))
            .all()
        )

    def create (self, category_data:ProductCreate)->Product or None:
        try:
            product = Product(**category_data.model.dump())
            self.db.add(product)
            self.db.commit()
            self.db.refresh(product)
            return product
        except:
            return None