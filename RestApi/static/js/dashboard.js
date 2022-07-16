$(document).ready(
    async () => {
        console.log('asd')
        await grapics_preare()
    }
)

async function make_request(token, uri){
    return await axios.get(
        'http://127.0.0.1:5000/' + uri,
        {
            headers: {
                'Authorization': 'Bearer ' + token
            }
        }
    )
}
async function grapics_preare() {
    const token = localStorage['auth_token'];
    let all_categories = await make_request(token, 'categories/getAll')
    console.log(all_categories)
}