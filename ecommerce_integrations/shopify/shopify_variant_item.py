import requests
import json
from typing import Optional

import frappe
from frappe import _, msgprint
from frappe.utils import cint, cstr
from frappe.utils.nestedset import get_root_of
from shopify.resources import Product, Variant

from ecommerce_integrations.ecommerce_integrations.doctype.ecommerce_item import ecommerce_item
from ecommerce_integrations.shopify.connection import temp_shopify_session
from ecommerce_integrations.shopify.constants import (
	MODULE_NAME,
	SETTING_DOCTYPE,
	SHOPIFY_VARIANTS_ATTR_LIST,
	SUPPLIER_ID_FIELD,
	WEIGHT_TO_ERPNEXT_UOM_MAP,
)
from ecommerce_integrations.shopify.utils import create_shopify_log

@frappe.whitelist()
def update_variant(item_code):
    product_id = frappe.db.get_value(
			"Ecommerce Item",
			{"erpnext_item_code": item_code, "integration": MODULE_NAME},
			"integration_item_code",
		)
    key=frappe.db.get_single_value('Shopify Setting', 'api_key')
    docSettings = frappe.get_single("Shopify Setting")
    password = docSettings.get_password('password')

    # url="https://"+key+":"+password+"@farmley-dry-fruit.myshopify.com/admin/api/2021-10/products/"+product_id+".json"

    url = "https://"+key+":"+password+"@farmley-dry-fruit.myshopify.com/admin/api/2021-10/products/"+product_id+"/variants.json"
    # url="https://{{api_key}}:{{api_password}}@{{store_name}}.myshopify.com/admin/api/{{api_version}}/variants/{{variant_id}}.json"

    doc=frappe.db.get_all("Item",{"variant_of":item_code},["name"])
    for i in doc:
        sdoc=frappe.get_doc("Item",i.name)
        for i in sdoc.attributes:
            if i.attribute=="Size":
                payload = json.dumps({
                # "options":{
                #     "name":"Size",
                #     "position":1,
                #     "values":i.attribute_value
                    
                # },
                "variant": {
                    "option1":i.attribute_value,
                    "sku":sdoc.name
                }
                })
                headers = {
                'Content-Type': 'application/json'
                }

                response = requests.request("POST", url, headers=headers, data=payload)

                print(response.text)

