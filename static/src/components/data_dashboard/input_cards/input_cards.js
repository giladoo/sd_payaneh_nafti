/** @odoo-module */
    const { Component, useState } = owl
const { onMounted, useRef } = owl.hooks
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
        this.inputRef = useRef('input_ref');
        this.toOpenInputInfo = this.toOpenInputInfo.bind(this);
        this.onChange = this.onChange.bind(this);

//        console.log('data_dashboard_input', this.inputRef.el)
    },
    onChange(e){
        console.log('onchange:', e.target.value, e.target.value.split('_'))
        let value = e.target.value.split('_')
        value = value.length == 2 ? value[1] : value[0]
        let ev = {'target':{'value': value, 'tagName': 'BUTTON', 'previousSibling':{'value': value}}}
        e.target.value = ''
        console.log('onchange ev:', ev)
        this.toOpenInputInfo(ev)
    },
    async toOpenInputInfo(e){
        console.log('openInputInfo', e, e.target.value)
        let value = e.target.value;
        if (e.target.tagName == 'BUTTON'){
            value = e.target.previousSibling.value
        }
        if( e.keyCode == 13 || e.target.tagName == 'BUTTON'){
            if(Number.isInteger(Number(value))){
                this.state.openInputInfo.status = value
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
                    this.state.openInputInfo.status = `${value} ${_t("Not found")}`
                }
            }else{
                this.state.openInputInfo.status = `${value} ${_t("Not found")}`
            }

//            console.log('openInputInfo value:', e.target.value, this)
        }
    }

})


