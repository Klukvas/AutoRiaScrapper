import {check_token_is_alive, get_full_url} from './useful.js';

$(document).ready(async function(){

    await check_token_is_alive();

    $("#signUpBtn").click(async() => {
            console.log('register')
            await register_process()
        }
      );


    $("#signInBtn").click(async() => {
            console.log('login')
            await login_process()
        }
      );
});



function validateEmail(email){
    const regex_pattern =/^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return regex_pattern.test(email)
}
async function register_process(){
    let password = $('#password').val();
    let email = $('#email').val();
    const is_email_valid = validateEmail(email);
    if(is_email_valid){
        let response = await auth(email, password, '/auth/register');
        console.log(`response from reg: ${response}`)
        //save received token and do redirect
        if(response.data.status === 'success'){
            console.log(`auth token aft reg: ${response.data.auth_token}`)
            localStorage['auth_token'] = response.data.auth_token;
            window.location.href = get_full_url("/cars/dashboard");
        }
    }else{
        let email_label_error = $(".auth-label-error-email")
        email_label_error.text(
            ()=>{
                return "Email us invalid"
            }
        );
        email_label_error.removeAttr('hidden');
        email_label_error.css("color: red");
    }
    
}
async function auth(email, password, uri){
    try {
        return await axios.post(
            get_full_url(uri),
            {
                "email": email,
                "password": password
            },
            {
                'Content-Type': 'application/json'
            }
        )
    } catch (err) {
        return {
            "message": err,
            "status": "fail"
        }
    }
};


async function login_process() {
    let password = $('#password').val();
    let email = $('#email').val();
    const is_email_valid = validateEmail(email);
    if(is_email_valid){
        let response = await auth(email, password, '/auth/login');
        //save received token and do redirect
        if(response.data.status === 'success'){
            localStorage['auth_token'] = response.data.auth_token;
            window.location.href = get_full_url("/cars/dashboard");
        }
    }else{
        let email_label_error = $(".auth-label-error-email")
        email_label_error.text(
            ()=>{
                return "Email us invalid"
            }
        );
        email_label_error.removeAttr('hidden');
        email_label_error.css("color: red");
    }

}