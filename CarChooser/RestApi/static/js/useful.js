export async function check_token_is_alive() {
    const token = localStorage['auth_token'];
    if(token){
        const is_token_alive = await axios.get(
            get_full_url("/auth/status"),
            {
                headers: {
                    'Authorization': 'Bearer ' + token
                }
            }
        );
        if(is_token_alive.data.status === 'success'){
            if(window.location.href.includes('register') || window.location.href.includes('login')){
                window.location.href =  get_full_url("/cars/dashboard");
            }
        }else{
            if(window.location.href.includes('dashboard')){
                window.location.href =  get_full_url("/auth/login");
            }
        }
    }else{
        if(window.location.href.includes('dashboard')){
            window.location.href =  get_full_url("/auth/login");
        }
    }
}
export function get_full_url(urn){
    console.log(location.protocol.concat("//").concat(window.location.host).concat(urn));
    return location.protocol.concat("//").concat(window.location.host).concat(urn);
}