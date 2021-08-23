const emailInput = document.getElementById("email");
const csrftoken = getCookie('csrftoken');
let anyError = false;
emailInput.onkeyup = function() {
    if (!(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(emailInput.value))) {
        createCustomErrorBootstrapAlert("Invalid Email")
        showCustomErrorBootstrapAlert()
    } else {
        hideGoogleAlert()
    }
}

const passwordInput = document.getElementById("password");
passwordInput.onkeyup = function() {
    if (passwordInput.value.length < 8) {
        createCustomErrorBootstrapAlert("Password Cannot Have Less Than 8 Characters")
        showCustomErrorBootstrapAlert()
    } else {
        hideGoogleAlert()
    }
}

const confirmPasswordInput = document.getElementById("confirmPassword");
confirmPasswordInput.onkeyup = function() {
    if (passwordInput.value !== confirmPasswordInput.value) {
        createCustomErrorBootstrapAlert("Passwords Do Not Match")
        showCustomErrorBootstrapAlert()
    } else {
        hideGoogleAlert()
    }
}

function createUser(email, username, password, auth_type = "email") {
    if (document.querySelector("#custom-error-div")) {
        document.querySelector("#custom-error-div").remove();
    }
    console.log("createUsernew default updated");
    const data = {
        email: email,
        username: username,
        password: password,
        auth_type: auth_type,
    };

    fetch("/api/accounts/register", {
            method: 'POST', // or 'PUT'
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(data),
        }).then(response => response.json())
        .then(data => {
            if (data.error) {
                console.log(data.error);
                createCustomErrorBootstrapAlert(data.error);
                showCustomErrorBootstrapAlert();
            } else {
                console.log("else part")
                console.log(data)
                createCustomSuccessBootstrapAlert("A verification Email was sent. It Will Expire Within 5 Minutes.")
                showCustomSuccessBootstrapAlert()
            }
        });
}



function signOut() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function() {
        console.log("User signed out.");
    });
    auth2.disconnect();
}

function hideGoogleAlert() {
    if (document.querySelector("#custom-error-div")) {
        document.querySelector("#custom-error-div").remove();
    }
}


function createCustomErrorBootstrapAlert(message) {
    if (document.querySelector("#custom-error-div")) {
        document.querySelector("#custom-error-div").remove();
    }
    errorStuff = '<div id="custom-error-div" style="display:none;" class="alert alert-danger alert-dismissible fade show" role="alert">'
    errorStuff += '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-exclamation-triangle-fill flex-shrink-0 me-2" viewBox="0 0 16 16" role="img" aria-label="Warning:">'
    errorStuff += '<path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/>'
    errorStuff += '</svg>'
    errorStuff += message
    errorStuff += '<button type="button" class="btn-close" onclick="hideGoogleAlert()" aria-label="Close">'
    errorStuff += '<span aria-hidden="true">&times;</span>'
    errorStuff += '</button>'
    errorStuff += '</div>'
    document.querySelector('#mainErrorDiv').innerHTML += errorStuff;
}

function showCustomErrorBootstrapAlert() {
    document.querySelector('#custom-error-div').style.display = 'block';
}

////////////////////////////////////////////////////////////////
function hideSuccessAlert() {
    if (document.querySelector("#custom-error-div")) {
        document.querySelector("#custom-error-div").remove();
    }
}

function createCustomSuccessBootstrapAlert(message) {
    if (document.querySelector("#custom-error-div")) {
        document.querySelector("#custom-error-div").remove();
    }
    errorStuff = '<div id="custom-error-div" style="display:none;">'
    errorStuff += '<div class="alert alert-success d-flex align-items-center" role="alert">'
    errorStuff += '<svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Success:"><use xlink:href="#check-circle-fill"/></svg>'
    errorStuff += '<div>'
    errorStuff += message
    errorStuff += '</div>'
    errorStuff += '<button type="button" style="position:absolute;right:0;top:0;padding: 1.25rem 1rem;" class="btn-close" onclick="hideGoogleAlert()" aria-label="Close">'
    errorStuff += '<span aria-hidden="true">&times;</span>'
    errorStuff += '</button>'
    errorStuff += "</div>"
    errorStuff += "</div>"
    document.querySelector('#mainErrorDiv').innerHTML += errorStuff;
}

function showCustomSuccessBootstrapAlert() {
    document.querySelector('#custom-error-div').style.display = 'block';
}

function getCookie(name) {
    if (!document.cookie) {
        return null;
    }

    const xsrfCookies = document.cookie.split(';')
        .map(c => c.trim())
        .filter(c => c.startsWith(name + '='));

    if (xsrfCookies.length === 0) {
        return null;
    }
    return decodeURIComponent(xsrfCookies[0].split('=')[1]);
}