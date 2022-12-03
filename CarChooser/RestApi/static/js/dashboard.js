import {check_token_is_alive, get_full_url} from "./useful.js";
import {categoryChart} from "./charts.js"

$(document).ready(
    async () => {
        await check_token_is_alive();
        await graphics_prepare();
    }
)



async function graphics_prepare() {
    const token = localStorage['auth_token'];
    // let all_categories = await make_request(token, '/categories/getAll')
    await categoryChart(token);
}