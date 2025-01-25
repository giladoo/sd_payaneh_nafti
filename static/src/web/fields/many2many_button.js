/** @odoo-module **/

import { patch } from 'web.utils';
import { FieldMany2Many } from 'web.relational_fields';

//export class Many2ManyCustom extends FieldMany2Many {
//    constructor(...args) {
//        super(...args);
//        this._onAddRecordOpenDialog = this._onAddRecordOpenDialog.bind(this);
//    }
//
//    _onAddRecordOpenDialog(event) {
//        // Your custom logic here
//        console.log('Custom logic for onAddRecordOpenDialog');
//        super._onAddRecordOpenDialog(event); // Call the original method if needed
//    }
//}
//
//patch(Many2ManyWidget, 'your_module.many2many_custom', {
//    __extends__: Many2ManyCustom,
//});
