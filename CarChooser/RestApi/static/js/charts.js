import {make_request, check_token_is_alive} from "./useful.js";

export async function categoryChart(token){
    try{
        const chartData = await make_request(token, "/cars/brands/getcounByCategory");
        const chartConfig = {
            type: 'column2d',
            renderAt: 'chart-countByCategory',
            width: '100%',
            height: '400',
            dataFormat: 'json',
            dataSource: {
                "chart": {
                    "caption": "Count cars by categories",
                    "subCaption": "",
                    "xAxisName": "Category",
                    "theme": "fusion",
                    },
                "data": chartData.data.data
                }
            };
            FusionCharts.ready(function(){
                var fusioncharts = new FusionCharts(chartConfig);
                fusioncharts.render();
            });
    }catch (err){
        if(err.response.status === 498){
            await check_token_is_alive();
        }
    }
    
}