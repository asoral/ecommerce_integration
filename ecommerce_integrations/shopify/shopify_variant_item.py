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
    shopify_url=frappe.db.get_single_value('Shopify Setting', 'shopify_url')
    docSettings = frappe.get_single("Shopify Setting")
    password = docSettings.get_password('password')

    url1="https://"+key+":"+password+"@"+shopify_url+"/admin/api/2021-10/products/"+product_id+".json"

    url = "https://"+key+":"+password+"@"+shopify_url+"/admin/api/2021-10/products/"+product_id+"/variants.json"

    varurl="https://"+key+":"+password+"@"+shopify_url+"/admin/api/2021-10/products/"+product_id+"/variants.json"

    # url="https://{{api_key}}:{{api_password}}@{{store_name}}.myshopify.com/admin/api/{{api_version}}/variants/{{variant_id}}.json"
    payload1= json.dumps({ 
        
        "product": {
            "options":[
            {
                "name":"Size","position":1,"values":["Rose","Dark Red"]
            }
            ]
        }
        
    })
   
    headers1 = {
        'Content-Type': 'application/json'
    }

    response = requests.request("PUT", url1, headers=headers1, data=payload1)
   
    doc=frappe.db.get_all("Item",{"variant_of":item_code},["name"])
    for i in doc:
        sdoc=frappe.get_doc("Item",i.name)
        for i in sdoc.attributes:
            if i.attribute=="Size":
                payload = json.dumps({
                "variant": {
                    "option1":i.attribute_value,
                    "sku":sdoc.name,
                    "weight": sdoc.weight_per_unit,
                    "weight_unit": "kg",
                }
                })
                headers = {
                'Content-Type': 'application/json'
                }

                response = requests.request("POST", url, headers=headers, data=payload)
                
    payload1= ""
   
    headers1 = {
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", varurl, headers=headers1, data=payload1)
    print("$$$$$$$$$$$$$$$$$$$$$$###############",json.loads(response.content))
    varlst=json.loads(response.content)
    # lst=[]
    EcItem=frappe.db.sql("select erpnext_item_code from `tabEcommerce Item`",as_list=1)
    doc=frappe.get_doc("Ecommerce Item",item_code)
    if doc.has_variants==1:
        doc.has_variants=1
        doc.save(ignore_permissions=True)

    for i in varlst["variants"]:
        if i.get("sku") not in EcItem:
            doc=frappe.new_doc("Ecommerce Item")
            doc.integration="shopify"
            doc.erpnext_item_code=i.get("sku")
            doc.sku=i.get("sku")
            doc.integration_item_code=i.get("product_id")
            doc.variant_id=i.get("id")
            doc.variant_of=item_code
            doc.save(ignore_permissions=True)

    
    

