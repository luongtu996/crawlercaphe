# Crawl post

Ở tròn file `main_blog.py` chạy: 

```py
  # khởi tạo
  main = MainBlog()
  # lấy paginate
  main.save_post_paginate()
  # lấy tất cả url post
  main.save_post_urls()
  # lấy và lưu tất cả post vào json
  main.save_posts()
```

# Crawl Product

Ở tròn file `main_product.py` chạy: 

```py
  # khởi tạo
  main = MainProduct()
  # lấy và lưu categories
  main.save_categories()
  # lấy và lưu product tags
  main.save_product_tags()
  # lấy collections (chưa có paginate)
  main.save_collection_urls()
  # lấy tất cả collections 
  main.save_all_collection_urls()
  # lấy tất cả product url
  main.save_all_products_url()
  # lấy và lưu tất cả products
  main.save_products()
```
# chi tiết file json
`posts.json`

```json

{
  "title": "noi dung tieu de",
  "image": "anh chinh/ anh background",
  "content": "content bai viet",
  "posted_in": "tags",
}

```

`product.json`
```json

{
  "breadcum": "category cha/con",
  "title": "tiêu đề",
  "short_desc": "mô tả ngắn",
  "content": "mô tả dài",
  "content_images": "images trong content",
  "images": "image slider",
  "posted_in": "product collection",
  "tagged_as": "product tags",
  "has_price": "sản phẩm có giá hay ko",
  "price": "giá sp = 0 có nghĩa là k có giá",
  "sale_price": "giá sale",
}

```