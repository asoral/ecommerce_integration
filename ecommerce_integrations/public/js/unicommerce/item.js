frappe.ui.form.on("Item", {
	refresh(frm) {
		if (frm.doc.sync_with_unicommerce) {
			frm.add_custom_button(
				__("Open Unicommerce Item"),
				function () {
					frappe.call({
						method:
							"ecommerce_integrations.unicommerce.utils.get_unicommerce_document_url",
						args: {
							code: frm.doc.item_code,
							doctype: frm.doc.doctype,
						},
						callback: function (r) {
							if (!r.exc) {
								window.open(r.message, "_blank");
							}
						},
					});
				},
				__("Unicommerce")
			);
		}
		if(frm.doc.has_variants){
            frm.add_custom_button(__("Update Variant Shopify"), function() {
                frappe.call({
                    method: 'ecommerce_integrations.shopify.item.update_variant',
                    args: {
                        "item_code" : frm.doc.item_code,
                    },
                    callback: function(r) {
                       
                        frappe.msgprint(__("Variants Updated"));
                        
                    }
                });
            })
        }
	},
});
