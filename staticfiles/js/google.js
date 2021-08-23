function onSignIn(googleUser) {
    console.log("Google user Called");
    if (document.querySelector("#custom-error-div")) {
        document.querySelector("#custom-error-div").remove();
    }
    var profile = googleUser.getBasicProfile();
    console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
    console.log('Name: ' + profile.getName());
    console.log('Image URL: ' + profile.getImageUrl());
    console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.
    let url = "/api/accounts/check-google-user-exists"
    const data = {
        email: profile.getEmail(),
        auth_type: "google",
    };
    fetch(url, {
            method: 'POST', // or 'PUT'
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        }).then(response => response.json())
        .then(data => {
            if (data.error) {
                console.log(data.error);
                createCustomErrorBootstrapAlert(data.error);
                showCustomErrorBootstrapAlert();
                var auth2 = gapi.auth2.getAuthInstance();
                auth2.signOut().then(function() {
                    console.log("User signed out.");
                });
                auth2.disconnect();
            } else {
                console.log("else part")
                if (data.success === "User Exists") {
                    //LOGIN GOOGLE USER
                    const data = {
                        email: profile.getEmail(),
                    };
                    fetch("/api/accounts/login-google-user", {
                            method: 'POST', // or 'PUT'
                            headers: {
                                'Content-Type': 'application/json',
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
                                localStorage.setItem('token', data.token)
                                window.location.href = rootUrl
                            }
                        });

                } else {
                    //GENERATE PASSWORD AND REGISTER GOOGLE USER
                    const data = {
                        email: profile.getEmail(),
                        password: String(Math.floor(Math.random() * 1000000000)),
                    };
                    fetch("/api/accounts/register-google-user", {
                            method: 'POST', // or 'PUT'
                            headers: {
                                'Content-Type': 'application/json',
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
                                localStorage.setItem('token', data.token)
                                window.location.href = rootUrl
                            }
                        });

                }

            }
        });
}


function logoutMain() {

    fetch(rootUrl + "/api/accounts/checkuser", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Token ' + localStorage.getItem('token')
            },
        })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            if (data.auth_type === "google") {
                var auth2 = gapi.auth2.getAuthInstance();
                auth2.signOut().then(function() {
                    console.log("User signed out.");
                });
                auth2.disconnect();
                window.location.href = rootUrl + '/logout'
            } else {
                window.location.href = rootUrl + '/logout'
            }
        })

}