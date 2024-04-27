/** @odoo-module */
    import { registry } from "@web/core/registry"
    const { Component, useRef, useState } = owl
    const { useEnv, onWillStart, onMounted, onWillUnmount } = owl.hooks;
    import { session } from "@web/session";
    import { useService } from "@web/core/utils/hooks"
    import { DataCards } from "./data_cards/data_cards"
    import { DataPlans } from "./data_plans/data_plans"
//    import { InputCards } from "./input_cards/input_cards"
    const { DateTime, Settings } = luxon;
    import core from 'web.core';
    const _t = core._t;

    const SERVER_DATE_FORMAT = "yyyy-MM-dd";

export class DataDashboard extends Component {
    setup(){
        let self = this;
        let loadingEvent;
        let loadingPlanCard;
//        console.log('session:', session)

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
                name: _t('New Request'),
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
//            openInputInfo: {
//                value: 0,
//                status: "",
//            },
        })
        this.orm = useService("orm")
        this.actionService = useService("action")
        let getRequestsInterval;
        onWillStart(async ()=>{
            await this.getSpgr()
            await this.loadPlan()
            await this.getContracts()
            await this.getRequests()
            getRequestsInterval = setInterval(this.getRequests, 30000)
//            console.log('onWillStart', getRequestsInterval)
        })
        onMounted(()=> {
            loadingPlanCard = document.querySelector('.loading_plan_card')
//            console.log('class DataDashboard',)
            loadingEvent = loadingPlanCard.addEventListener('click', self._onLoadingPlanCard)
//            self.loading_plan_detail()

        })
        onWillUnmount(function(){
//            console.log('onWillUnmount', getRequestsInterval)
            clearInterval(getRequestsInterval)
            loadingPlanCard.removeEventListener('click', loadingEvent)
        })
        this.viewSpgr = this.viewSpgr.bind(this);
        this.loadPlan = this.loadPlan.bind(this);
        this.getRequests = this.getRequests.bind(this);
        this.viewContracts = this.viewContracts.bind(this);
        this.viewThisDayRequests = this.viewThisDayRequests.bind(this);
        this.viewNewRequests = this.viewNewRequests.bind(this);
        this.viewLoadingPermit = this.viewLoadingPermit.bind(this);
        this.viewLoadingInfo = this.viewLoadingInfo.bind(this);
        this.viewCargoDocument = this.viewCargoDocument.bind(this);
//        this.toOpenInputInfo = this.toOpenInputInfo.bind(this);
        this._onLoadingPlanCard = this._onLoadingPlanCard.bind(this);
        this.viewTodayLoadingPlan = this.viewTodayLoadingPlan.bind(this);


    }
    async getSpgr(){
        const spgr = await this.orm.searchRead("sd_payaneh_nafti.spgr", [['active', '=', 'True']],['spgr', 'spgr_date'])
//        console.log('spgr:', spgr, spgr[0].spgr, spgr[0].spgr_date)
        this.state.spgr.status = moment(spgr[0].spgr_date).format("jYYYY/jMM/jDD");
        this.state.spgr.value = spgr[0].spgr;
    }
    loadingPlan(e){
        console.log('date:', e);
    }
    async loading_plan_detail(){
        let loadingPlanDetail = document.querySelector('.loading_plan_detail')
        let plans = await this.orm.call("sd_payaneh_nafti.loading_plan", "loading_plans_detail", [],{})
    }
    viewTodayLoadingPlan(theDate){
    let today = moment().locale('en').format('YYYY/MM/DD')
        let domain = [['record_date', '=', today]]
        this.actionService.doAction({
            name: "Loading Plan",
            res_model: "sd_payaneh_nafti.loading_plan",
//            res_id: this.actionId,
            views: [[false, "list"],],
            type: "ir.actions.act_window",
            view_mode: "list",
            domain: domain,
//                    context: {'search_default_meter_no_group': 1},
            target: "current",
        });

    }
    _onLoadingPlanCard(ev){
        if(ev.target.classList.contains('loading_plan') || ev.target.parentElement.classList.contains('loading_plan') ){
            if(ev.target.parentElement.dataset.date){
                let domain = [['record_date', '=', ev.target.parentElement.dataset.date]]
                this.actionService.doAction({
                    name: "Loading Plan",
                    res_model: "sd_payaneh_nafti.loading_plan",
        //            res_id: this.actionId,
                    views: [[false, "list"],],
                    type: "ir.actions.act_window",
                    view_mode: "list",
                    domain: domain,
//                    context: {'search_default_meter_no_group': 1},
                    target: "current",
                });
            }

        }
    }
    async loadPlan(){
        let self = this;
        let plans = await this.orm.call("sd_payaneh_nafti.loading_plan", "loading_plans", [],{})
        plans = JSON.parse(plans)
//        console.log('plans:', plans)
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
//        console.log('plans:', r)

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
//        this.state.load_plan.link = `<div class="row">${link}</div>`
        this.state.load_plan.link = link
    }
    async getContracts(){
        let contracts = await this.orm.call("sd_payaneh_nafti.contract_registration", "get_contracts", [],{})
        contracts = JSON.parse(contracts)
//        console.log('contracts:', contracts, typeof contracts, )
//        this.state.spgr.status = moment(spgr[0].spgr_date).format("jYYYY/jMM/jDD");
        this.state.contracts.value = contracts.open_contracts;
        this.state.remain_amount.value = contracts.remain_amount;
    }
    async getRequests(){
//            console.log('getRequests:',  )

        let requests = await this.orm.call("sd_payaneh_nafti.input_info", "get_requests", [],{})
        requests = JSON.parse(requests)
//        console.log('requests:', requests,  )
//        this.state.spgr.status = moment(spgr[0].spgr_date).format("jYYYY/jMM/jDD");
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
        this.state.this_day_requests_count.status = moment().format("jYYYY/jMM/jDD");
        this.state.one_day_ago_count.status = moment().subtract(1, 'days').format("jYYYY/jMM/jDD");
        this.state.two_days_ago_count.status = moment().subtract(2, 'days').format("jYYYY/jMM/jDD");
        this.state.three_days_ago_count.status = moment().subtract(3, 'days').format("jYYYY/jMM/jDD");

        this.loadPlan()
    }
    viewSpgr(){
//        console.log('viewSpgr', this)
//            this.actionService = useService("action")

        this.actionService.doAction({
            name: "SPGR",
            res_model: "sd_payaneh_nafti.spgr",
//            res_id: this.actionId,
            views: [[false, "list"], [false, "form"]],
            type: "ir.actions.act_window",
            view_mode: "list",
//            domain: domain,
            target: "current",
        });
        }
    viewContracts(){
//        this.actionService = useService("action")
        let today = moment().locale('en').format('YYYY/MM/DD')
        console.log('today:',  today, moment.locale())
        let domain = ['|','|',['end_date', '>=', today],
        ['first_extend_end_date', '>=', today],
        ['second_extend_end_date', '>=', today],
        ]
//        this.orm = useService("orm")
//        this.orm.call("sd_payaneh_nafti.contract_registration", "dash_get_inputs", [],{})
//        console.log('viewContracts', this.orm, this.actionService, )
//          this.actionService.doAction("sd_payaneh_nafti.action_window_contract_registration")
        this.actionService.doAction({
            name: "Ongoing Contracts",
            res_model: "sd_payaneh_nafti.contract_registration",
//            res_id: this.actionId,
            views: [[false, "list"], [false, "form"]],
            type: "ir.actions.act_window",
            view_mode: "list",
            domain: domain,
            target: "current",
        });
    }
    viewThisDayRequests(day=0){
//        this.actionService = useService("action")
//        console.log('viewThisDayRequests', day)
        let today = moment().locale('en').add(day, 'days').format('YYYY/MM/DD')
        let domain = [['request_date', '=', today]]
        this.actionService.doAction({
            name: "This day Requests",
            res_model: "sd_payaneh_nafti.input_info",
//            res_id: this.actionId,
            views: [[false, "list"], [false, "form"]],
            type: "ir.actions.act_window",
            view_mode: "list",
            domain: domain,
            context: {'search_default_meter_no_group': 1},
            target: "current",
        });
    }
    viewNewRequests(){
//            this.actionService = useService("action")
        let domain = [['state', '=', 'draft']]

        this.actionService.doAction({
            name: "New Requests",
            res_model: "sd_payaneh_nafti.input_info",
//            res_id: this.actionId,
            views: [[false, "list"], [false, "form"]],
            type: "ir.actions.act_window",
            view_mode: "list",
            domain: domain,
            target: "current",
        });
        }
    viewLoadingPermit(){
//            this.actionService = useService("action")
        let domain = [['state', '=', 'loading_permit']]

        this.actionService.doAction({
            name: "Loading Permit",
            res_model: "sd_payaneh_nafti.input_info",
//            res_id: this.actionId,
            views: [[false, "list"], [false, "form"]],
            type: "ir.actions.act_window",
            view_mode: "list",
            domain: domain,
            target: "current",
        });
        }
    viewLoadingInfo(){
//            this.actionService = useService("action")
        let domain = [['state', '=', 'loading_info']]

        this.actionService.doAction({
            name: "Loading Permit",
            res_model: "sd_payaneh_nafti.input_info",
//            res_id: this.actionId,
            views: [[false, "list"], [false, "form"]],
            type: "ir.actions.act_window",
            view_mode: "list",
            domain: domain,
            target: "current",
        });
        }
    viewCargoDocument(){
//            this.actionService = useService("action")
        let domain = [['state', '=', 'cargo_document']]

        this.actionService.doAction({
            name: "Cargo Document",
            res_model: "sd_payaneh_nafti.input_info",
//            res_id: this.actionId,
            views: [[false, "list"], [false, "form"]],
            type: "ir.actions.act_window",
            view_mode: "list,form",
            domain: domain,
            target: "current",
        });
        }
}

DataDashboard.template = "data_dashboard"
DataDashboard.components = { DataCards, DataPlans }
registry.category("actions").add("data_dashboard", DataDashboard)
