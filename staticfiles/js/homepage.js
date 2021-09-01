function toggleLike(questionid) {
    query = "#span-like-" + questionid
    if (document.querySelector(query).style.display === "none") {
        document.querySelector(query).style.display = "inline-block"
        query = "#span-unlike-" + questionid
        document.querySelector(query).style.display = "none"
        return
    }
    document.querySelector(query).style.display = "none"
    query = "#span-unlike-" + questionid
    document.querySelector(query).style.display = "inline-block"
}

function updateLikeCount(questionid, count) {
    countquery = "#span-likecount-" + questionid
    document.querySelector(countquery).innerHTML = count
}


function addlike(questionid, userid) {
    fetch(rootUrl + "/api/add-like/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Authorization: 'Token ' + localStorage.getItem('token')
            },
            body: JSON.stringify({
                questionid: questionid,
                userid: userid,
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success === "added") {
                toggleLike(questionid)
                updateLikeCount(questionid, data.count)
            } else if (data.error) {
                alert(data.error)
            } else {
                alert(data)
            }
        })
}

function removelike(questionid, userid) {
    fetch(rootUrl + "/api/remove-like/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Authorization: 'Token ' + localStorage.getItem('token')
            },
            body: JSON.stringify({
                questionid: questionid,
                userid: userid,
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success === "removed") {
                toggleLike(questionid)
                updateLikeCount(questionid, data.count)
            } else if (data.error) {
                alert(data.error)
            } else {
                alert(data)
            }
        })
}