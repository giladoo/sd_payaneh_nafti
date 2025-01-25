/** @odoo-module **/

import FormView from 'web.FormView';
import FormController from 'web.FormController';
import viewRegistry from 'web.view_registry';

const RemoveActionButtonFormController = FormController.extend({
    // It ignor the menu items, so the action menu would not be shown
    _getActionMenuItems: function(state){
    },
});

export const RemoveActionButtonFormView = FormView.extend({
    config: Object.assign({}, FormView.prototype.config, {
        Controller: RemoveActionButtonFormController,
    }),
});

viewRegistry.add('remove_action_button', RemoveActionButtonFormView);
