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
    console.log('asdasdasd123123')
};

async function graphics_prepare() {
    const token = localStorage['auth_token'];
    // let all_categories = await make_request(token, '/categories/getAll')
    await countByBrandAndModel(token);
    await CountBy_Value_AndPrice(token, 'category');
    await CountBy_Value_AndPrice(token, 'gearbox');
}