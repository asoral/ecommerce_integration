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
    # password=frappe.db.get_single_value('Shopify Setting', 'password')
    docSettings = frappe.get_single("Shopify Setting")
    password = docSettings.get_password('password')

    url = "https://"+key+":"+password+"@farmley-dry-fruit.myshopify.com/admin/api/2021-10/products/"+product_id+"/variants.json"

    payload = json.dumps({
    "variant": {
        "option1": "Yellow",
        "price": "100"
    }
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

