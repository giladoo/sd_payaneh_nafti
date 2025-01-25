/** @odoo-module */

import { registry } from "@web/core/registry"
import { ChartRenderer } from "../chart_renderer/chart_renderer"
import { loadJS } from "@web/core/assets"
import { useService } from "@web/core/utils/hooks"
import { _t } from 'web.core';

const { Component, useRef, useState } = owl
const { useEnv, onWillStart, onMounted, onWillUnmount } = owl.hooks;

export class MetersDashboard extends Component {
    setup(){
        this.state = useState({
            meter_this_day: {title: _t('Meter Loading Count'), type: 'bar', config: {}},
            meter_weeks: {title: _t('Meters in 6 weeks'), type: 'line', config: {}},
            meter_months: {title: _t('Meters in 6 months'), type: 'line', config: {}},
        })
        this.orm = useService("orm")
        this.actionService = useService("action")
        onWillStart(async ()=>{
            await this.getMetersThisDay()
        })
    }
    async getMetersThisDay(){
        let meter_data = await this.orm.call('sd_payaneh_nafti.input_info', 'get_meter_charts', [[]])
        meter_data = JSON.parse(meter_data)
//        console.log('meter_this_day:', meter_data)
        this.state.meter_this_day.config = meter_data.data_this_day
        this.state.meter_weeks.config = meter_data.data_weeks
        this.state.meter_months.config = meter_data.data_months
    }
}

MetersDashboard.template = "meters_dashboard_template"
MetersDashboard.components = { ChartRenderer }
registry.category("actions").add("meters_dashboard", MetersDashboard)