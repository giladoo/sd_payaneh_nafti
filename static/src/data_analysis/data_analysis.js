/** @odoo-module */
import { registry } from "@web/core/registry"
const { Component, useState } = owl
const { useEnv, onWillStart, onMounted, onWillUnmount, useRef} = owl.hooks;
import { session } from "@web/session";
import { useService } from "@web/core/utils/hooks"
import { DataAnalysisChart } from "./data_analysis_chart/data_chart"
import { ChartRenderer } from "./chart_renderer/chart_renderer"
import Bus from 'web.Bus';
const { DateTime, Settings } = luxon;
import core from 'web.core';
const _t = core._t;
const SERVER_DATE_FORMAT = "yyyy-MM-dd";
//import { loadJS } from "web.ajax";
const { loadJS } = owl.utils;

export class DataAnalysis extends Component {
    async setup(){
        this.orm = useService("orm")
        this.actionService = useService("action")
        this.meters = useRef("meters_chart")
        this.state = useState({
            charts: {
                meters: '<div class="text-info">Chart 1</div>'
            }
        })
        onWillStart(async () => {
            await this.getCharts()
        })
        onMounted(async () => {
            await this.showChart()
        })


        this.getCharts = this.getCharts.bind(this);
        this.showChart = this.showChart.bind(this);

    }
    async getCharts(){
        let charts = await this.orm.call("sd_payaneh_nafti.input_info", "data_analysis_get_charts", [[]])
        this.state.charts = charts ? JSON.parse(charts) : ''
        console.log('charts:', charts)

    }
    async showChart(){
        try {
            Plotly
        } catch (e) {
            const url = "sd_payaneh_nafti/static/src/lib/plotly-2.35.2.min.js";
            await loadJS(url);
            }

        console.log('plotly:', Plotly, this.meters.el)
        if(this.meters.el){
            Plotly.newPlot(this.meters.el, [{
                x: [1, 2, 3, 4],
                y: [3, 7, 0, 2]
            }], {margin: { t: 0}})
    //        Plotly.newPlot(this.meters.el,[])
        }
    }
}


DataAnalysis.template = "data_analysis"
DataAnalysis.components = { DataAnalysisChart, ChartRenderer }
registry.category("actions").add("data_analysis", DataAnalysis)