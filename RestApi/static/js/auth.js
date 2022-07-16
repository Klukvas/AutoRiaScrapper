$(document).ready(async function(){

    await check_token_is_alive();

    $("#signUpBtn").click(async() => {
      console.log("asd1")
            await register_process()
        }
      );


    $("#signInBtn").click(async() => {
            await login_process()
        }
      );
});

async function check_token_is_alive() {
    const token = localStorage['auth_token'];
    if(token){
        const is_token_alive = await axios.get(
            'http://127.0.0.1:5000/auth/status',
            {
                headers: {
                    'Authorization': 'Bearer ' + token
                }
            }
        );
        console.log(is_token_alive)
        if(is_token_alive.data.status === 'success'){
            window.location.href = "http://127.0.0.1:5000/cars/dashboard";
        }
    }
}


function validateEmail(email){
    const regex_pattern =/^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return regex_pattern.test(email)
}
async function register_process(){
    let password = $('#password').val();
    let email = $('#email').val();
    const is_email_valid = validateEmail(email);
    if(is_email_valid){
        let response = await auth(email, password, 'auth/register');
        //save received token and do redirect
        if(response.data.status === 'success'){
            localStorage['auth_token'] = response.data.auth_token;
            window.location.href = "http://127.0.0.1:5000/cars/dashboard";
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
        console.log("asd")
        //send auth request
        return await axios.post(
            'http://127.0.0.1:5000/' + uri,
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
        let response = await auth(email, password, 'auth/login');
        //save received token and do redirect
        if(response.data.status === 'success'){
            localStorage['auth_token'] = response.data.auth_token;
            window.location.href = "http://127.0.0.1:5000/cars/dashboard";
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