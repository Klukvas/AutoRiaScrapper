import {check_token_is_alive} from "./useful.js";
import {CountBy_Value_AndPrice, countByBrandAndModel} from "./charts.js"


$(document).ready(
    async () => {
        await check_token_is_alive();
        await graphics_prepare();
    }
)
document.getElementById("a_filter_show").addEventListener("click", showFilter);
async function showFilter(){
    let categoryChart = FusionCharts('category');
    let gearboxChart = FusionCharts('gearbox');
    let countByBrandAndModelChart = FusionCharts('countByBrandAndModel');
    // let jsonData = revenueChart.getChartData('json');
    // console.log(`jsonData: ${JSON.stringify( jsonData )}`);
};

async function graphics_prepare() {
    const token = localStorage['auth_token'];
    // let all_categories = await make_request(token, '/categories/getAll')
    await countByBrandAndModel(token);
    await CountBy_Value_AndPrice(token, 'category');
    await CountBy_Value_AndPrice(token, 'gearbox');
}