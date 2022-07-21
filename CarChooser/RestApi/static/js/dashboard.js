import {check_token_is_alive, get_full_url} from "./useful.js";
$(document).ready(
    async () => {
        await check_token_is_alive();
        await graphics_prepare();
    }
)

async function make_request(token, uri){
    return await axios.get(
        get_full_url(uri),
        {
            headers: {
                'Authorization': 'Bearer ' + token
            }
        }
    )
}
async function graphics_prepare() {
    const token = localStorage['auth_token'];
    let all_categories = await make_request(token, '/categories/getAll')
    console.log(all_categories)
}