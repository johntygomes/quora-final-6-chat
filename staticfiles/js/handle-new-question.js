tinymce.init({
    selector: 'textarea',
    plugins: 'a11ychecker image lists advcode casechange export formatpainter linkchecker autolink lists checklist media mediaembed pageembed permanentpen powerpaste table advtable tinycomments tinymcespellchecker',
    toolbar: 'a11ycheck image numlist bullist addcomment showcomments casechange checklist code export formatpainter pageembed permanentpen table',
    toolbar_mode: 'floating',
    tinycomments_mode: 'embedded',
    tinycomments_author: 'Author name',
});
checkIfAnyErrors()
document.querySelector("#submit-btn").disabled = checkIfAnyErrors()

document.querySelector("#id_title").onkeyup = function() {
    document.querySelector("#submit-btn").disabled = checkIfAnyErrors()
}
document.querySelector('#id_title').onkeyup = function() {
    document.querySelector("#submit-btn").disabled = checkIfAnyErrors()
}

function checkIfAnyErrors() {
    if (document.querySelector("#id_title").value === "") {
        return true;
    }
    return false;
}



function addNewQuestion() {
    activateLoader()
    const title = document.querySelector("#id_title").value;
    const body = tinymce.get('id_body_main').getBody().innerHTML
    fetch(rootUrl + "/api/add-new-question/", {
            method: 'POST',
            headers: {
                'Content-Type': "application/json",
                Authorization: "Token " + localStorage.getItem("token"),
            },
            body: JSON.stringify({
                title: title,
                body: body,
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                deactivateLoader()
                createCustomErrorBootstrapAlert(data.error);
                showCustomErrorBootstrapAlert();
            } else {
                deactivateLoader()
                window.location.href = "/"
            }
        })
}


////////////////////////////////////////////////////////////
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