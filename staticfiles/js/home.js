window.onload = function() {
    console.log("onload");
    if (localStorage.getItem("token")) {
        console.log(localStorage.getItem("token"));
    }
}