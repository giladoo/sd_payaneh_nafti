/** @odoo-module **/
const { Component, useRef } = owl
const { onMounted, onWillUnmount } = owl.hooks
import core from 'web.core';
import { useBus } from "@web/core/utils/hooks";

import { browser } from "@web/core/browser/browser";
import { registry } from "@web/core/registry";
import { patch } from "@web/core/utils/patch";
import { session } from "@web/session";
import { DataDashboard } from "../data_dashboard";

patch(DataDashboard.prototype, 'data_dashboard',{
    setup(){
        this._super()
        onMounted(()=>{
            Component.env.bus.on('barcode_scanned', this, this._onBarcodeScanned);
//            console.log('patch(DataDashboard mounted')
        })
        onWillUnmount(function(){
            Component.env.bus.off('barcode_scanned', this, this._onBarcodeScanned);
//            console.log('patch(DataDashboard unmounted')

        })


    },
    _onBarcodeScanned(barcode){
        Component.env.bus.off('barcode_scanned', this, this._onBarcodeScanned);
        this._viewInputInfo(barcode)
        console.log('_onBarcodeScanned',barcode)
        Component.env.bus.on('barcode_scanned', this, this._onBarcodeScanned);

    },
    async _viewInputInfo(barcode){
        const INPUT_INFO = 200;
        const CONTRACT_REGISTRATION = 210;
        let prefix = barcode.slice(0, 3)
        let code_no = barcode.slice(4)
        let today = moment().locale('en').format('YYYY/MM/DD')
        let res_id;
        let domain;
//        console.log('_viewInputInfo', document_no, prefix)
        if (prefix == INPUT_INFO){
            res_id = await this.orm.searchRead("sd_payaneh_nafti.input_info", [['document_no', '=', code_no]],['id'])
//            domain = [['document_no', '=', document_no]]
            this.actionService.doAction({
                name: "",
                res_model: "sd_payaneh_nafti.input_info",
                res_id: res_id[0].id,
                views: [ [false, "form"]],
                type: "ir.actions.act_window",
                view_mode: "form",
//                domain: domain,
    //            context: {'search_default_meter_no_group': 1},
                target: "new",
            });
        }else if (prefix == CONTRACT_REGISTRATION){
            res_id = await this.orm.searchRead("sd_payaneh_nafti.contract_registration", [['registration_no', '=', code_no]],['id'])
            this.actionService.doAction({
                name: "",
                res_model: "sd_payaneh_nafti.contract_registration",
                res_id: res_id[0].id,
                views: [ [false, "form"]],
                type: "ir.actions.act_window",
                view_mode: "form",
//                domain: domain,
    //            context: {'search_default_meter_no_group': 1},
                target: "new",
            });
        }

    },

})