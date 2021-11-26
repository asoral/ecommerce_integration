frappe.ui.form.on("Item", {
    refresh:function(frm){
        if(frm.doc.has_variants){
            frm.add_custom_button(__("Update Variant Shopify"), function() {
                frappe.call({
                    method: 'ecommerce_integration.ecommerce_integration.shopify.item.update_variant',
                    args: {
                        "item_code" : frm.doc.item_code,
                    },
                    callback: function(r) {
                       
                        frappe.msgprint(__("Variants Updated"));
                        
                    }
                });
            })
        }
    }
})