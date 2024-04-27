/** @odoo-module */
    const { Component, useRef, useState } = owl
const { onMounted } = owl.hooks
import core from 'web.core';
const _t = core._t;
import { useBus } from "@web/core/utils/hooks";
import { browser } from "@web/core/browser/browser";
import { registry } from "@web/core/registry";
import { patch } from "@web/core/utils/patch";
import { session } from "@web/session";
import { useService } from "@web/core/utils/hooks"
import { DataDashboard } from "../data_dashboard";


export class InputCards extends Component {
    setup(){
    super.setup();
//        console.log('InputCards',this)

    }
}

InputCards.template = "input_cards"
DataDashboard.components = { ...DataDashboard.components, InputCards }





patch(DataDashboard.prototype, 'data_dashboard_input',{
    setup(){
        this._super()
//        console.log('InputCards patch',this)
        this.state = useState({
            ...this.state,
            openInputInfo: {
                name: _t('Search'),
                view: _t('View'),
                value: 0,
                status: "",
            },
        })
        console.log('data_dashboard_input', this)
    },
    async openInputInfo(e){
//        console.log('openInputInfo', e)
        let value = e.target.value;
        if (e.target.tagName == 'BUTTON'){
            value = e.target.previousSibling.value
        }
        if( e.keyCode == 13 || e.target.tagName == 'BUTTON'){
            if(Number.isInteger(Number(value))){
                this.state.openInputInfo.status = ''
                const document = await this.orm.searchRead("sd_payaneh_nafti.input_info", [['document_no','=', Number(value)]],['id'])
                if (document.length == 1){
//                    console.log('document:', Number(value), document)
                    this.actionService.doAction({
//                                name: "Cargo Document",
                        res_model: "sd_payaneh_nafti.input_info",
                        res_id: document[0].id,
                        views: [[false, "form"]],
                        type: "ir.actions.act_window",
                        view_mode: "form",
//                                domain: domain,
                        target: "new",
                    });
                }else{
                    this.state.openInputInfo.status = 'Not found'
                }
            }else{
                this.state.openInputInfo.status = 'Not found'
            }

//            console.log('openInputInfo value:', e.target.value, this)
        }
    }

})


