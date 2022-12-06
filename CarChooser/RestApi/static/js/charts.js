import {make_request, check_token_is_alive} from "./useful.js";

export async function CountBy_Value_AndPrice(token, data_value){
    try{
        const chartData = await make_request(token, `/cars/getDataByPriceAndCount?dataType=${data_value}`);
        let lables = [], line_data = [], column_data = [];
        
        for(const item of chartData.data.data){
            lables.push({'label': item.label});
            line_data.push({"value": item.line_value});
            column_data.push({"value": item.column_value * 150}); //типу много данных
        };
        
        const chartConfig = {
            type: 'logmscolumn2d',
            renderAt: `chart-countBy_${data_value}`,
            width: '50%',
            height: '400',
            dataFormat: 'json',
            dataSource: {
                "chart": {
                    "borderColor": "#666666",
                    "borderThickness": "4",
                    "showBorder": "1",

                    "rotateValues": "0",
                    
                    "pRotateValues": "0",
                    "showValues": "1",
                    "caption": `Count of cars by ${data_value} with avg price for every ${data_value}`,
                    "xAxisname": data_value,
                    "sAxisName": "Amount (In USD)",
                    "pAxisName": "Count of cars",
                    // "numberPrefix": "$",
                    "sNumberPrefix": "items",
                    "divlineColor": "#999999",
                    "divLineIsDashed": "1",
                    "divLineDashLen": "1",
                    "divLineGapLen": "1",
                    "toolTipColor": "#ffffff",
                    "toolTipBorderThickness": "0",
                    "toolTipBgColor": "#000000",
                    "toolTipBgAlpha": "80",
                    "toolTipBorderRadius": "2",
                    "toolTipPadding": "5",
                    "theme": "fusion"
                },
                "categories": [
                    {
                        "category": lables
                    }
                ],
                "dataset": [
                    {
                        "seriesName": "Count of cars in category",
                        "showValues": "1",
                        "data": column_data
                    },
                    {
                        "seriesName": "Avg price of car category",
                        "numberPrefix": "$",
                        "renderAs": "line",
                        "data": line_data
                    }
                ]
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
    
};

export async function countByBrandAndModel(token){
    //countByBrandModel
    try{
        const chartData = await make_request(token, "/cars/brands/getBrandCount");
        const chartConfig = {
            type: 'pie2d',
            renderAt: 'chart-countByBrandModel',
            width: '100%',
            height: '500',
            dataFormat: 'json',
            dataSource: {
                "chart": {
                    "caption": "Count of brands on the market",
                    "legendPosition": "right",
                    "legendNumColumns": "4",
                    "showPercentInTooltip": "0",
                    "decimals": "1",
                    "useDataPlotColorForLabels": "1",
                    "theme": "fusion"
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
};