/** @odoo-module */

import { registry } from "@web/core/registry"
//import { loadJS } from "@web/core/assets"
const { Component } = owl
const { useRef, useEnv, onWillStart, onMounted, onWillUnmount } = owl.hooks;
const { loadJS } = owl.utils;
import { useAssets } from "@web/core/assets";
import { useEffect } from "@web/core/utils/hooks";

export class ChartRenderer extends Component {
    setup(){
        this.chartRef = useRef("chart")
        this.chart = null;
//        useAssets({ jsLibs: ["/web/static/lib/Chart/Chart.js"] });
        useAssets({ jsLibs: ["/sd_payaneh_nafti/static/src/lib/plotly-2.35.2.min.js"] });
//        useEffect(() => this.renderChart());
        onMounted(() => this.renderChart())
        this.renderChart = this.renderChart.bind(this)
    }

    renderChart() {
        const config = this.props.config ? JSON.parse(JSON.stringify(this.props.config)) : {}
        console.log('render:', config, config.data, Plotly)
        Plotly.newPlot(this.chartRef.el, config)
    }
    willUnmount() {
        if (this.chart) {
            this.chart.destroy();
        }
    }
}

ChartRenderer.template = "chart_renderer"