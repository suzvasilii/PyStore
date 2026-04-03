import datetime
from pydantic import BaseModel, Field
from .category import  CategoryResponse
from typing import Optional

class ProductBase(BaseModel):
    name: str = Field(..., min_length=5, max_length=50,
                      description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., gt=0, description="Product price(must be greater then 0")
    category_id: int = Field(..., description="Category ID")
    image_url: Optional[str] = Field(None, description="Product image URL")

class ProductCreate(ProductBase):
    pass

class ProductResponse(BaseModel):
    id: int = Field(..., description="Unique product ID")
    name: str
    description: Optional[str]
    price: float
    category_id: int
    image_url: Optional[str]
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    category:CategoryResponse = Field(..., description="Category details")

    class Config:
        from_attributes=True

class ProductListResponse(BaseModel):
    products: list[ProductResponse]
    total: int = Field(..., description="Total number of products")