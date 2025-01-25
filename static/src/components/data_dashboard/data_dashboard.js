/** @odoo-module */
import { registry } from "@web/core/registry"
const { Component, useRef, useState } = owl
const { useEnv, onWillStart, onMounted, onWillUnmount } = owl.hooks;
import { session } from "@web/session";
import { useService } from "@web/core/utils/hooks"
import { DataCards } from "./data_cards/data_cards"
import { DataPlans } from "./data_plans/data_plans"
import { DataLockers } from "./data_lockers/data_lockers"
import Bus from 'web.Bus';
const { DateTime, Settings } = luxon;
import core from 'web.core';
const _t = core._t;
const SERVER_DATE_FORMAT = "yyyy-MM-dd";

export class DataDashboard extends Component {
    setup(){
        let self = this;
        let loadingEvent;
        let loadingPlanCard;
        this.legacyEnv = Component.env;
        this.state = useState({
            title: {
                name: _t('Payaneh Data Dashboard'),
            },
            username: {
                value: '',
                status: session.name
            },
            load_plan: {
                name: _t('Loading Plan'),
                value: '',
                link: '<a href="https://google.com">12/17</a>'
            },
            plan_detail:{
                name: _t('Plan Detail'),
                status: ''
            },
            spgr: {
                value: 0.7722,
                status: "1402/10/01",
            },
            contracts: {
                name: _t('Open Contracts'),
                value: 0,
                status: "",
            },
            remain_amount: {
                value: 0,
                status: "",
            },
            open_requests: {
                value: 0,
                status: "",
            },
            newRequest: {
                status: _t("Create Loading"),
            },
            lockers: {
                name: _t('Lockers'),
                status: [
                {"box_no": 1, "start_no": "SPT100", "end_no": "SPT199", "available": 350},
                {"box_no": 2, "start_no": "SPT200", "end_no": "SPT299", "available": 500},
                ],
            },
            this_day_requests_count: {
                value: 0,
                status: "",
            },
            one_day_ago_count: {
                value: 0,
                status: "",
            },
            two_days_ago_count: {
                value: 0,
                status: "",
            },
            three_days_ago_count: {
                value: 0,
                status: "",
            },
            this_day_requests_amount: {
                value: 110,
                status: "",
            },
            delivered_month_amount: {
                value: 2110,
                status: "",
            },
            new_requests: {
                name: _t('New Loadings'),
                value: 0,
                status: "",
            },
            loading_permit: {
                name: _t('Loading Permit'),
                value: 0,
                status: "",
            },
            loading_info: {
                name: _t('Loading Info'),
                value: 0,
                status: "",
            },
            cargo_document: {
                name: _t('Cargo Document'),
                value: 0,
                status: "",
            },
            meter_data: {
                value: 0,
            },
        })
        this.orm = useService("orm")
        this.actionService = useService("action")
        let getRequestsInterval;
        onWillStart(async ()=>{
            await this.getSpgr()
            await this.loadPlan()
            await this.getContracts()
            await this.getRequests()
            await this.getLockerPackage()
        })
        onMounted(()=> {
            loadingPlanCard = document.querySelector('.loading_plan_card')
            loadingEvent = loadingPlanCard.addEventListener('click', self._onLoadingPlanCard)
            self.legacyEnv.services.bus_service.call( 'bus_service', 'addChannel', 'payaneh_operation_channel');
            self.legacyEnv.services.bus_service
                .on('notification', 'payaneh_operation' , notifications => self._onNotif(notifications));
        })
        onWillUnmount(function(){
            loadingPlanCard.removeEventListener('click', loadingEvent)
            self.legacyEnv.services.bus_service.call( 'bus_service', 'deleteChannel', 'payaneh_operation_channel');
            self.legacyEnv.services.bus_service.off('notification', self._onNotif);


        })
        this.viewSpgr = this.viewSpgr.bind(this);
        this.loadPlan = this.loadPlan.bind(this);
        this.getRequests = this.getRequests.bind(this);
        this.viewContracts = this.viewContracts.bind(this);
        this.viewThisDayRequests = this.viewThisDayRequests.bind(this);
        this.viewNewRequests = this.viewNewRequests.bind(this);
        this.newRequestCreation = this.newRequestCreation.bind(this);
        this.viewLoadingPermit = this.viewLoadingPermit.bind(this);
        this.viewLoadingInfo = this.viewLoadingInfo.bind(this);
        this.viewCargoDocument = this.viewCargoDocument.bind(this);
        this._onLoadingPlanCard = this._onLoadingPlanCard.bind(this);
        this.viewTodayLoadingPlan = this.viewTodayLoadingPlan.bind(this);
        this.viewLockerPackage = this.viewLockerPackage.bind(this);


    }
    async getLockerPackage(){
        const packages = await this.orm.call("sd_payaneh_nafti.locker_package", "get_locker_package", [[]])
        this.state.lockers.status = JSON.parse(packages).ids
    }
    async viewLockerPackage(){
        let domain = [['state', '=', 'published']]
        this.actionService.doAction({
            name: _t("Locker Package"),
            res_model: "sd_payaneh_nafti.locker_package",
            views: [[false, "list"]],
            type: "ir.actions.act_window",
            view_mode: "list",
            domain: domain,
            create: false,
            target: "current",
        });
    }
    async getSpgr(){
        let dateFormat = session.user_context.lang == 'fa_IR' ? "jYYYY/jMM/jDD" : "YYYY-MM-DD"
        const spgr = await this.orm.searchRead("sd_payaneh_nafti.spgr", [['active', '=', 'True']],['spgr', 'spgr_date'])
        this.state.spgr.status = moment(spgr[0].spgr_date).format(dateFormat);
        this.state.spgr.value = spgr[0].spgr;
    }
    viewTodayLoadingPlan(theDate){
        let today = moment().locale('en').format('YYYY/MM/DD')
        let domain = [['record_date', '=', today]]
        this.actionService.doAction({
            name: _t("Loading Plan"),
            res_model: "sd_payaneh_nafti.loading_plan",
            views: [[false, "list"],],
            type: "ir.actions.act_window",
            view_mode: "list",
            domain: domain,
            target: "current",
        });

    }
    _onLoadingPlanCard(ev){
        if(ev.target.classList.contains('loading_plan') || ev.target.parentElement.classList.contains('loading_plan') ){
            if(ev.target.parentElement.dataset.date){
                let domain = [['record_date', '=', ev.target.parentElement.dataset.date]]
                this.actionService.doAction({
                    name: _t("Loading Plan"),
                    res_model: "sd_payaneh_nafti.loading_plan",
                    views: [[false, "list"],],
                    type: "ir.actions.act_window",
                    view_mode: "list",
                    domain: domain,
                    target: "current",
                });
            }

        }
    }
    async loadPlan(){
        let self = this;
        let plans = await this.orm.call("sd_payaneh_nafti.loading_plan", "loading_plans", [],{})
        plans = JSON.parse(plans)
        this.state.plan_detail.status = plans.plan_detail
        let link = ''
            link += `
            <div class="col">
                <div class="row small border-bottom">
                    <div class="col-6  px-1">${_t('Date')}</div>
                    <div class="col-3  px-1">${_t('Total')}</div>
                    <div class="col-3  px-1">${_t('Plan')}</div>
                </div>
            </div>
            `;
        plans.data.forEach( r => {
            link += `
            <div class="col" style="cursor: pointer;">
                <div class="row small border-bottom plans_row loading_plan" data-date="${r.date}"  >
                    <div class="col-6  px-1">${r.s_date}</div>
                    <div class="col-3  px-1">${r.remain_amount}</div>
                    <div class="col-3  px-1">${r.allocated}</div>
                </div>
            </div>
            `;
        } )
        this.state.load_plan.link = link
    }
    async getContracts(){
        let contracts = await this.orm.call("sd_payaneh_nafti.contract_registration", "get_contracts", [],{})
        contracts = JSON.parse(contracts)
        this.state.contracts.value = contracts.open_contracts;
        this.state.remain_amount.value = contracts.remain_amount;
    }
    async getRequests(){
        let dateFormat = session.user_context.lang == 'fa_IR' ? "jYYYY/jMM/jDD" : "YYYY-MM-DD"
        let requests = await this.orm.call("sd_payaneh_nafti.input_info", "get_requests", [],{})
        requests = JSON.parse(requests)
        this.state.open_requests.value = requests.open_requests;
        this.state.this_day_requests_count.value = requests.this_day_requests_count;
        this.state.one_day_ago_count.value = requests.one_day_ago_count;
        this.state.two_days_ago_count.value = requests.two_days_ago_count;
        this.state.three_days_ago_count.value = requests.three_days_ago_count;
        this.state.this_day_requests_amount.value = requests.this_day_requests_amount;
        this.state.new_requests.value = requests.new_requests;
        this.state.loading_permit.value = requests.loading_permit;
        this.state.loading_info.value = requests.loading_info;
        this.state.cargo_document.value = requests.cargo_document;
        this.state.meter_data.name = [_t("Meter No"), _t("First Totalizer"), _t("Last Totalizer"), _t("Amount"), _t("Trucks")];
        this.state.meter_data.value = requests.meter_data;
        this.state.this_day_requests_count.status = moment().format(dateFormat);
        this.state.one_day_ago_count.status = moment().subtract(1, 'days').format(dateFormat);
        this.state.two_days_ago_count.status = moment().subtract(2, 'days').format(dateFormat);
        this.state.three_days_ago_count.status = moment().subtract(3, 'days').format(dateFormat);
        this.loadPlan()
    }
    _onNotif(notifications){
        let self = this;
        let payaneh = notifications.filter(({payload, type}) => type == "payaneh_operation" )
        if (payaneh.length > 0){
            setTimeout(() =>{
                self.legacyEnv.services.bus_service._channels.includes('payaneh_operation_channel')
                    ? self.getRequests() : '';
            } , 100);
        }
    }
    viewSpgr(){
        let domain = ['|',['active', '=', true], ['active', '=', false], ]
        let context = {'search_default_show_active': 1}
        this.actionService.doAction({
            name: _t("SPGR"),
            res_model: "sd_payaneh_nafti.spgr",
            views: [[false, "list"], [false, "form"]],
            type: "ir.actions.act_window",
            view_mode: "list",
            domain: domain,
            context: context,
            target: "current",
        });
    }
    viewContracts(){
        let today = moment().locale('en').format('YYYY/MM/DD')
        let domain = ['|','|',['end_date', '>=', today],
        ['first_extend_end_date', '>=', today],
        ['second_extend_end_date', '>=', today],
        ]

        this.actionService.doAction({
            name: _t("Ongoing Contracts"),
            res_model: "sd_payaneh_nafti.contract_registration",
            views: [[false, "list"], [false, "form"]],
            type: "ir.actions.act_window",
            view_mode: "list",
            domain: domain,
            target: "current",
        });
    }
    newRequestCreation(){
        this.actionService.doAction({
            res_model: "sd_payaneh_nafti.input_info",
            views: [[false, "form"]],
            type: "ir.actions.act_window",
            view_mode: "form",
            target: "new",
        });
    }
    viewThisDayRequests(day=0){
        let today = moment().locale('en').add(day, 'days')
        let dateFormat = session.user_context.lang == 'fa_IR' ? "jYYYY/jMM/jDD" : "YYYY-MM-DD"
        let theDay = today.format(dateFormat)
        today = today.format('YYYY/MM/DD')
        let domain = [['request_date', '=', today]]
        this.actionService.doAction({
            name: `${_t("Loadings")} [${theDay}]`,
            res_model: "sd_payaneh_nafti.input_info",
            views: [[false, "list"], [false, "form"]],
            type: "ir.actions.act_window",
            view_mode: "list",
            domain: domain,
            context: {'search_default_meter_no_group': 1},
            target: "current",
        });
    }
    viewNewRequests(){
        let domain = [['state', '=', 'draft']]
        this.actionService.doAction({
            name: _t("New Loadings"),
            res_model: "sd_payaneh_nafti.input_info",
            views: [[false, "list"], [false, "form"]],
            type: "ir.actions.act_window",
            view_mode: "list",
            domain: domain,
            target: "current",
        });
        }
    viewLoadingPermit(){
        let domain = [['state', '=', 'loading_permit']]
        this.actionService.doAction({
            name: _t("Loading Permit"),
            res_model: "sd_payaneh_nafti.input_info",
            views: [[false, "list"], [false, "form"]],
            type: "ir.actions.act_window",
            view_mode: "list",
            domain: domain,
            target: "current",
        });
        }
    viewLoadingInfo(){
        let domain = [['state', '=', 'loading_info']]

        this.actionService.doAction({
            name: _t("Loading Info"),
            res_model: "sd_payaneh_nafti.input_info",
            views: [[false, "list"], [false, "form"]],
            type: "ir.actions.act_window",
            view_mode: "list",
            domain: domain,
            target: "current",
        });
        }
    viewCargoDocument(){
        let domain = [['state', '=', 'cargo_document']]
        this.actionService.doAction({
            name: _t("Cargo Document"),
            res_model: "sd_payaneh_nafti.input_info",
            views: [[false, "list"], [false, "form"]],
            type: "ir.actions.act_window",
            view_mode: "list,form",
            domain: domain,
            target: "current",
        });
        }
    onSubDashboardClick(e){
        console.log('onSubDashboardClick', e)
        this.actionService.doAction({
            type: "ir.actions.client",
            tag: "meters_dashboard",
            target: "current",
        });
    }
}

DataDashboard.template = "data_dashboard"
DataDashboard.components = { DataCards, DataPlans, DataLockers }
registry.category("actions").add("data_dashboard", DataDashboard)
