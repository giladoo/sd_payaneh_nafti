/** @odoo-module **/

import fieldRegistry from 'web.field_registry';
import { _t } from 'web.core';
import { FieldChar } from 'web.basic_fields';
import { FieldMany2Many } from 'web.relational_fields';


var FieldMany2ManyButton = FieldMany2Many.extend({
    _render(){
        var res = this._super.apply(this, arguments);
        console.log('Render _render')
        return res
        }
});

fieldRegistry.add('many2many_button', FieldMany2ManyButton);
export default FieldMany2ManyButton;
