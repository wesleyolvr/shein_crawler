from typing import Optional

from pydantic import BaseModel, Field, validator


class ProductBase(BaseModel):
    product_id: int
    product_type: str
    href: str
    data_title: str
    data_price: float
    data_id_category: str
    data_sku: str
    data_spu: str
    data_us_price: float
    data_us_origin_price: float
    discount: str
    image_src: str


class ProductCreate(ProductBase):
    product_id: int
    product_type: str
    data_title: str
    data_price: float
    data_us_price: float
    data_us_origin_price: float
    discount: Optional[float] = Field(default=None)

    @validator('data_price', 'data_us_price', 'data_us_origin_price', pre=True)
    # pylint: disable=no-self-argument
    def check_comma_and_convert(cls, value):
        """Verifica se o valor tem vírgula e converte para float."""
        if ',' in str(value):
            return float(value.replace(',', '.'))
        return float(value)

    @validator(
        'data_price',
        'data_us_price',
        'data_us_origin_price',
        'discount',
        pre=True,
    )
    # pylint: disable=no-self-argument
    def check_empty_values(cls, value):
        """Verifica se o valor esta vazio e retorna 0."""
        if value is None or value == '':
            return 0.0
        return value

    @validator('product_type', pre=True)
    # pylint: disable=no-self-argument
    def format_type_products(cls, value):
        """Formata o nome dotipo de produto."""
        return value.replace('-', ' ')

    @validator('data_price', pre=False)
    # pylint: disable=no-self-argument
    def format_price(cls, value):
        """Formata o preço para float."""
        return float(value)


class ProductRead(ProductBase):
    class Config:
        orm_mode = True


class ProductUpdate(ProductBase):
    pass
