tinymce.init({
    selector: 'textarea',
    plugins: 'a11ychecker advcode casechange export formatpainter linkchecker autolink lists checklist media mediaembed pageembed permanentpen powerpaste table advtable tinycomments tinymcespellchecker',
    toolbar: 'a11ycheck addcomment showcomments casechange checklist code export formatpainter pageembed permanentpen table',
    toolbar_mode: 'floating',
    tinycomments_mode: 'embedded',
    tinycomments_author: 'Author name',
});

function addNewQuestion() {
    const title = document.querySelector("#id_title").value;
    const body = tinymce.get('id_body_main').getBody().innerHTML
    console.log(title);
    console.log(body);
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
                alert(data.error);
            } else {
                alert(data.success);
            }
        })
}