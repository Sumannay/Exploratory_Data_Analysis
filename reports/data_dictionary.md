# InsightLab — Relational Data Dictionary & Schema Profile

> **Platform**: InsightLab Advanced Analytics Engine  
> **Source Dataset**: Olist E-Commerce Brazilian Relational Database  
> **Status**: Raw Baseline Inspection  

## Summary of Ingested Tables

| Table Name | Total Rows | Total Columns | Memory (MB) | Duplicate Rows |
| :--- | :--- | :--- | :--- | :--- |
| **`customers`** | 99,441 | 5 | 29.62 MB | 0 (0.0%) |
| **`orders`** | 99,441 | 8 | 58.97 MB | 0 (0.0%) |
| **`order_items`** | 112,650 | 7 | 39.43 MB | 0 (0.0%) |
| **`payments`** | 103,886 | 5 | 17.82 MB | 0 (0.0%) |
| **`reviews`** | 100,000 | 7 | 43.20 MB | 0 (0.0%) |
| **`products`** | 32,951 | 9 | 6.79 MB | 0 (0.0%) |
| **`sellers`** | 3,095 | 4 | 0.66 MB | 0 (0.0%) |
| **`category_translation`** | 71 | 2 | 0.01 MB | 0 (0.0%) |
| **`marketing_leads`** | 8,000 | 4 | 2.38 MB | 0 (0.0%) |
| **`closed_deals`** | 842 | 14 | 0.65 MB | 0 (0.0%) |

---

## Detailed Table Schemas

### Table: `customers`
- **Dimensions**: 99,441 rows × 5 columns
- **Memory Footprint**: 29.62 MB
- **Duplicate Rows**: 0

| Column Name | Type | Null Count | Null % | Unique Values | Key? | Sample Values |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `customer_id` | `object` | 0 | 0.0% | 99,441 | **YES (PK)** | `06b8999e2fba1a1fbc88172c00ba8bc7, 18955e83d337fd6b2def6b18a428ac77, 4e7b3e00288586ebd08712fdd0374a03` |
| `customer_unique_id` | `object` | 0 | 0.0% | 96,096 | No | `861eff4711a542e4b93843c6dd7febb0, 290c77bc529b7ac935b93aa66c333dc3, 060e732b5b29e8181a18229c7b0b2b5e` |
| `customer_zip_code_prefix` | `int64` | 0 | 0.0% | 14,994 | No | `14409, 9790, 1151` |
| `customer_city` | `object` | 0 | 0.0% | 4,119 | No | `franca, sao bernardo do campo, sao paulo` |
| `customer_state` | `object` | 0 | 0.0% | 27 | No | `SP, SC, MG` |

### Table: `orders`
- **Dimensions**: 99,441 rows × 8 columns
- **Memory Footprint**: 58.97 MB
- **Duplicate Rows**: 0

| Column Name | Type | Null Count | Null % | Unique Values | Key? | Sample Values |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `order_id` | `object` | 0 | 0.0% | 99,441 | **YES (PK)** | `e481f51cbdc54678b7cc49136f2d6af7, 53cdb2fc8bc7dce0b6741e2150273451, 47770eb9100c2d0c44946d9cf07ec65d` |
| `customer_id` | `object` | 0 | 0.0% | 99,441 | **YES (PK)** | `9ef432eb6251297304e76186b10a928d, b0830fb4747a6c6d20dea0b8c802d7ef, 41ce2a54c0b03bf3443c3d931a367089` |
| `order_status` | `object` | 0 | 0.0% | 8 | No | `delivered, invoiced, shipped` |
| `order_purchase_timestamp` | `object` | 0 | 0.0% | 98,875 | No | `2017-10-02 10:56:33, 2018-07-24 20:41:37, 2018-08-08 08:38:49` |
| `order_approved_at` | `object` | 160 | 0.16% | 90,733 | No | `2017-10-02 11:07:15, 2018-07-26 03:24:27, 2018-08-08 08:55:23` |
| `order_delivered_carrier_date` | `object` | 1,783 | 1.79% | 81,018 | No | `2017-10-04 19:55:00, 2018-07-26 14:31:00, 2018-08-08 13:50:00` |
| `order_delivered_customer_date` | `object` | 2,965 | 2.98% | 95,664 | No | `2017-10-10 21:25:13, 2018-08-07 15:27:45, 2018-08-17 18:06:29` |
| `order_estimated_delivery_date` | `object` | 0 | 0.0% | 459 | No | `2017-10-18 00:00:00, 2018-08-13 00:00:00, 2018-09-04 00:00:00` |

### Table: `order_items`
- **Dimensions**: 112,650 rows × 7 columns
- **Memory Footprint**: 39.43 MB
- **Duplicate Rows**: 0

| Column Name | Type | Null Count | Null % | Unique Values | Key? | Sample Values |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `order_id` | `object` | 0 | 0.0% | 98,666 | No | `00010242fe8c5a6d1ba2dd792cb16214, 00018f77f2f0320c557190d7a144bdd3, 000229ec398224ef6ca0657da4fc703e` |
| `order_item_id` | `int64` | 0 | 0.0% | 21 | No | `1, 2, 3` |
| `product_id` | `object` | 0 | 0.0% | 32,951 | No | `4244733e06e7ecb4970a6e2683c13e61, e5f2d52b802189ee658865ca93d83a8f, c777355d18b72b67abbeef9df44fd0fd` |
| `seller_id` | `object` | 0 | 0.0% | 3,095 | No | `48436dade18ac8b2bce089ec2a041202, dd7ddc04e1b6c2c614352b383efe2d36, 5b51032eddd242adc84c38acab88f23d` |
| `shipping_limit_date` | `object` | 0 | 0.0% | 93,318 | No | `2017-09-19 09:45:35, 2017-05-03 11:05:13, 2018-01-18 14:48:30` |
| `price` | `float64` | 0 | 0.0% | 5,968 | No | `58.9, 239.9, 199.0` |
| `freight_value` | `float64` | 0 | 0.0% | 6,999 | No | `13.29, 19.93, 17.87` |

### Table: `payments`
- **Dimensions**: 103,886 rows × 5 columns
- **Memory Footprint**: 17.82 MB
- **Duplicate Rows**: 0

| Column Name | Type | Null Count | Null % | Unique Values | Key? | Sample Values |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `order_id` | `object` | 0 | 0.0% | 99,440 | No | `b81ef226f3fe1789b1e8b2acac839d17, a9810da82917af2d9aefd1278f1dcfa0, 25e8ea4e93396b6fa0d3dd708e76c1bd` |
| `payment_sequential` | `int64` | 0 | 0.0% | 29 | No | `1, 2, 4` |
| `payment_type` | `object` | 0 | 0.0% | 5 | No | `credit_card, boleto, voucher` |
| `payment_installments` | `int64` | 0 | 0.0% | 24 | No | `8, 1, 2` |
| `payment_value` | `float64` | 0 | 0.0% | 29,077 | No | `99.33, 24.39, 65.71` |

### Table: `reviews`
- **Dimensions**: 100,000 rows × 7 columns
- **Memory Footprint**: 43.20 MB
- **Duplicate Rows**: 0

| Column Name | Type | Null Count | Null % | Unique Values | Key? | Sample Values |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `review_id` | `object` | 0 | 0.0% | 99,173 | No | `7bc2406110b926393aa56f80a40eba40, 80e641a11e56f04c1ad469d5645fdfde, 228ce5500dc1d8e020d8d1322874b6f0` |
| `order_id` | `object` | 0 | 0.0% | 99,441 | No | `73fc7af87114b39712e6da79b0a377eb, a548910a1c6147796b98fdf73dbeba33, f9e4b658b201a9f2ecdecbb34bed034b` |
| `review_score` | `int64` | 0 | 0.0% | 5 | No | `4, 5, 1` |
| `review_comment_title` | `object` | 88,285 | 88.28% | 4,600 | No | `recomendo, Super recomendo, Não chegou meu produto ` |
| `review_comment_message` | `object` | 58,247 | 58.25% | 36,921 | No | `Recebi bem antes do prazo estipulado., Parabéns lojas lannister adorei comprar pela Internet seguro e prático Parabéns a todos feliz Páscoa, aparelho eficiente. no site a marca do aparelho esta impresso como 3desinfector e ao chegar esta com outro nome...atualizar com a marca correta uma vez que é o mesmo aparelho` |
| `review_creation_date` | `object` | 0 | 0.0% | 637 | No | `2018-01-18 00:00:00, 2018-03-10 00:00:00, 2018-02-17 00:00:00` |
| `review_answer_timestamp` | `object` | 0 | 0.0% | 99,010 | No | `2018-01-18 21:46:59, 2018-03-11 03:05:13, 2018-02-18 14:36:24` |

### Table: `products`
- **Dimensions**: 32,951 rows × 9 columns
- **Memory Footprint**: 6.79 MB
- **Duplicate Rows**: 0

| Column Name | Type | Null Count | Null % | Unique Values | Key? | Sample Values |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `product_id` | `object` | 0 | 0.0% | 32,951 | **YES (PK)** | `1e9e8ef04dbcff4541ed26657ea517e5, 3aa071139cb16b67ca9e5dea641aaa2f, 96bd76ec8810374ed1b65e291975717f` |
| `product_category_name` | `object` | 610 | 1.85% | 73 | No | `perfumaria, artes, esporte_lazer` |
| `product_name_lenght` | `float64` | 610 | 1.85% | 66 | No | `40.0, 44.0, 46.0` |
| `product_description_lenght` | `float64` | 610 | 1.85% | 2,960 | No | `287.0, 276.0, 250.0` |
| `product_photos_qty` | `float64` | 610 | 1.85% | 19 | No | `1.0, 4.0, 2.0` |
| `product_weight_g` | `float64` | 2 | 0.01% | 2,204 | No | `225.0, 1000.0, 154.0` |
| `product_length_cm` | `float64` | 2 | 0.01% | 99 | No | `16.0, 30.0, 18.0` |
| `product_height_cm` | `float64` | 2 | 0.01% | 102 | No | `10.0, 18.0, 9.0` |
| `product_width_cm` | `float64` | 2 | 0.01% | 95 | No | `14.0, 20.0, 15.0` |

### Table: `sellers`
- **Dimensions**: 3,095 rows × 4 columns
- **Memory Footprint**: 0.66 MB
- **Duplicate Rows**: 0

| Column Name | Type | Null Count | Null % | Unique Values | Key? | Sample Values |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `seller_id` | `object` | 0 | 0.0% | 3,095 | **YES (PK)** | `3442f8959a84dea7ee197c632cb2df15, d1b65fc7debc3361ea86b5f14c68d2e2, ce3ad9de960102d0677a81f5d0bb7b2d` |
| `seller_zip_code_prefix` | `int64` | 0 | 0.0% | 2,246 | No | `13023, 13844, 20031` |
| `seller_city` | `object` | 0 | 0.0% | 611 | No | `campinas, mogi guacu, rio de janeiro` |
| `seller_state` | `object` | 0 | 0.0% | 23 | No | `SP, RJ, PE` |

### Table: `category_translation`
- **Dimensions**: 71 rows × 2 columns
- **Memory Footprint**: 0.01 MB
- **Duplicate Rows**: 0

| Column Name | Type | Null Count | Null % | Unique Values | Key? | Sample Values |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `product_category_name` | `object` | 0 | 0.0% | 71 | **YES (PK)** | `beleza_saude, informatica_acessorios, automotivo` |
| `product_category_name_english` | `object` | 0 | 0.0% | 71 | **YES (PK)** | `health_beauty, computers_accessories, auto` |

### Table: `marketing_leads`
- **Dimensions**: 8,000 rows × 4 columns
- **Memory Footprint**: 2.38 MB
- **Duplicate Rows**: 0

| Column Name | Type | Null Count | Null % | Unique Values | Key? | Sample Values |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `mql_id` | `object` | 0 | 0.0% | 8,000 | **YES (PK)** | `dac32acd4db4c29c230538b72f8dd87d, 8c18d1de7f67e60dbd64e3c07d7e9d5d, b4bc852d233dfefc5131f593b538befa` |
| `first_contact_date` | `object` | 0 | 0.0% | 336 | No | `2018-02-01, 2017-10-20, 2018-03-22` |
| `landing_page_id` | `object` | 0 | 0.0% | 495 | No | `88740e65d5d6b056e0cda098e1ea6313, 007f9098284a86ee80ddeb25d53e0af8, a7982125ff7aa3b2054c6e44f9d28522` |
| `origin` | `object` | 60 | 0.75% | 10 | No | `social, paid_search, organic_search` |

### Table: `closed_deals`
- **Dimensions**: 842 rows × 14 columns
- **Memory Footprint**: 0.65 MB
- **Duplicate Rows**: 0

| Column Name | Type | Null Count | Null % | Unique Values | Key? | Sample Values |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `mql_id` | `object` | 0 | 0.0% | 842 | **YES (PK)** | `5420aad7fec3549a85876ba1c529bd84, a555fb36b9368110ede0f043dfc3b9a0, 327174d3648a2d047e8940d7d15204ca` |
| `seller_id` | `object` | 0 | 0.0% | 842 | **YES (PK)** | `2c43fb513632d29b3b58df74816f1b06, bbb7d7893a450660432ea6652310ebb7, 612170e34b97004b3ba37eae81836b4c` |
| `sdr_id` | `object` | 0 | 0.0% | 32 | No | `a8387c01a09e99ce014107505b92388c, 09285259593c61296eef10c734121d5b, b90f87164b5f8c2cfa5c8572834dbe3f` |
| `sr_id` | `object` | 0 | 0.0% | 22 | No | `4ef15afb4b2723d8f3d81e51ec7afefe, d3d1e91a157ea7f90548eef82f1955e3, 6565aa9ce3178a5caf6171827af3a9ba` |
| `won_date` | `object` | 0 | 0.0% | 824 | No | `2018-02-26 19:58:54, 2018-05-08 20:17:59, 2018-06-05 17:27:23` |
| `business_segment` | `object` | 1 | 0.12% | 33 | No | `pet, car_accessories, home_appliances` |
| `lead_type` | `object` | 6 | 0.71% | 8 | No | `online_medium, industry, online_big` |
| `lead_behaviour_profile` | `object` | 177 | 21.02% | 9 | No | `cat, eagle, wolf` |
| `has_company` | `object` | 779 | 92.52% | 2 | No | `True, False` |
| `has_gtin` | `object` | 778 | 92.4% | 2 | No | `True, False` |
| `average_stock` | `object` | 776 | 92.16% | 6 | No | `20-50, 1-5, 5-20` |
| `business_type` | `object` | 10 | 1.19% | 3 | No | `reseller, manufacturer, other` |
| `declared_product_catalog_size` | `float64` | 773 | 91.81% | 33 | No | `2000.0, 80.0, 15.0` |
| `declared_monthly_revenue` | `float64` | 0 | 0.0% | 27 | No | `0.0, 100000.0, 20000.0` |
