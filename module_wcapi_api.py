from config_con import *
from woocommerce import API


class WOO_API(object):

    def __init__(self):
        self.wcapi = API(
            url="https://karenkashop.com/",  # Your store URL
            consumer_key = WOO_CONSUMER_KEY,  # Your consumer key
            consumer_secret = WOO_SECRET,  # Your consumer secret
            wp_api = True,  # Enable the WP REST API integration
            version = "wc/v3")
        self.new_product_info = []
        self.product_id = 28038


    def product_create(self, new_name='Test jewelry', new_description='Test jewelry', new_short_description='Test jewelry',
                       new_comments=None, new_sku='1234567', new_price='1', new_stock=10, new_tags=[],
                       new_color='Red', new_length='5', new_size='5', new_material='Other', new_categories='98',
                       new_main_image='https://karenkashop.com/wp-content/uploads/2021/07/ypg8cusgd8.jpg',
                       new_additional_image='https://karenkashop.com/wp-content/uploads/2021/07/ypg8cusgd8.jpg'):
        if new_comments is not None:
            product = {
                "name": new_name,
                "type": "simple",
                "catalog_visibility": "visible",
                "description": new_description,
                "short_description": new_short_description,
                "meta_data": [{'id': 13422, 'key': 'alg_wc_public_product_note_tab_title', 'value': 'Comments'},
                              {'id': 13421, 'key': '_alg_wc_public_product_note',
                               'value': [{'value': new_comments}]}],
                "sku": new_sku,
                "regular_price": new_price,
                "tax_status": 'taxable',
                "shipping_required": True,
                "shipping_taxable": True,
                "shipping_class": 'standard',
                "shipping_class_id": 94,
                "manage_stock": True,
                "stock_quantity": new_stock,
                "stock_status": "instock",
                "tags": new_tags,
                "attributes": [{'id': 4, 'name': 'Color', 'position': 0, 'visible': True, 'variation': False,
                                'options': [new_color]},
                               {'id': 2, 'name': 'Length', 'position': 1, 'visible': True, 'variation': False,
                                'options': [new_length]},
                               {'id': 3, 'name': 'Material', 'position': 2, 'visible': True, 'variation': False,
                                'options': [new_material]},
                               {'id': 1, 'name': 'Size', 'position': 3, 'visible': True, 'variation': False,
                                'options': [new_size]}],
                "images": [{"src": new_main_image}, {"src": new_additional_image}],
                "categories": [{"id": new_categories}]
            }
        else:
            product = {
                "name": new_name,
                "type": "simple",
                "catalog_visibility": "visible",
                "description": new_description,
                "short_description": new_short_description,
                "sku": new_sku,
                "regular_price": new_price,
                "tax_status": 'taxable',
                "shipping_required": True,
                "shipping_taxable": True,
                "shipping_class": 'standard',
                "shipping_class_id": 94,
                "manage_stock": True,
                "stock_quantity": new_stock,
                "stock_status": "instock",
                "tags": new_tags,
                "attributes": [{'id': 4, 'name': 'Color', 'position': 0, 'visible': True, 'variation': False,
                                'options': [new_color]},
                               {'id': 2, 'name': 'Length', 'position': 1, 'visible': True, 'variation': False,
                                'options': [new_length]},
                               {'id': 3, 'name': 'Material', 'position': 2, 'visible': True, 'variation': False,
                                'options': [new_material]},
                               {'id': 1, 'name': 'Size', 'position': 3, 'visible': True, 'variation': False,
                                'options': [new_size]}],
                "images": [{"src": new_main_image}, {"src": new_additional_image}],
                "categories": [{"id": new_categories}]
            }

        try:
            print(self.wcapi.post('products', product).json())
        except Exception as error:
            print(error)
            return error

    def get_all_products(self):
        try:
            data = self.wcapi.get("products", params={'per_page': 100, 'status': 'publish', 'featured': False}).json()
            return data
        except Exception as error:
            return error

    def get_product(self):
        try:
            result = self.wcapi.get("products/28038?fields=sku").json()
            sku = result.get('sku')
            return sku
        except Exception as error:
            print(error)


    def update_product(self):
        try:
            data = {"description": self.new_product_info}
            print(self.wcapi.put("products/26475", data).json())
        except Exception as error:
            print(error)
            return error

    def orders_all(self):
        try:
            result = self.wcapi.get("orders").json()
            return result
        except Exception as error:
            print(error)
            return error

    def order_get(self):
        try:
            result = self.wcapi.get("orders/27521").json()
            return result
        except Exception as error:
            print(error)
            return error

    def order_user(self):
        try:
            data = {
                "orders": [
                    {
                        "status": "processing"
                    },
                    {
                        "status": "completed"
                    }
                ]
            }
            result = self.wcapi.post("orders/bulk", data).json()
            return result
        except Exception as error:
            return error


# woo1 = WOO_API()
# # SKU = woo1.get_product()
# # print(SKU)
# all = woo1.get_all_products()
# # all_products = db1.select_table_fb()
# k = 0
# for i in all:
#     k = k + 1
#     print(i)
# print(k)
# # p = woo1.get_product()
# # print(p)
# #
# # print(woo1.get_product())
#
#
# # meta = order1.get('meta_data')
# # for i in all:
# #     print(i)
#
#
#
# # for i in orders:
# #     print(f' Order: {i}\n')
#
#
# # print(order1.orders_all())




