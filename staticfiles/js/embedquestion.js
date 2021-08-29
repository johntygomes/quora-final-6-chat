fetch(rootUrl + "api/get-question-data/")
    .then(response => response.json())
    .then(data => {
        console.log(data)
        document.querySelector("#embed-question-body").innerHTML = data.body;
    })