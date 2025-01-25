/** @odoo-module **/

import FormView from 'web.FormView';
import FormRenderer from 'web.FormRenderer';
import viewRegistry from 'web.view_registry';

const ContractMonthlyReportWizardRenderer = FormRenderer.extend({
    // It ignor the menu items, so the action menu would not be shown
       events: _.extend({}, FormRenderer.prototype.events, {
        'change .registration_no_selection': '_onRegistrationChange',
    }),
    start: function(){
        let self = this;
        console.log('ContractMonthly')
        var res = this._super.apply(this, arguments);
        return res
    },
    _onRegistrationChange: function(ev){
        console.log('_onRegistrationChange', ev)

    },
});

export const ContractMonthlyReportWizardFormView = FormView.extend({
    config: Object.assign({}, FormView.prototype.config, {
        Renderer: ContractMonthlyReportWizardRenderer,
    }),
});

viewRegistry.add('contract_monthly_report_wizard', ContractMonthlyReportWizardFormView);
