function toggleLike(responseid) {
    query = "#span-like-" + responseid
    if (document.querySelector(query).style.display === "none") {
        document.querySelector(query).style.display = "inline-block"
        query = "#span-unlike-" + responseid
        document.querySelector(query).style.display = "none"
        return
    }
    document.querySelector(query).style.display = "none"
    query = "#span-unlike-" + responseid
    document.querySelector(query).style.display = "inline-block"
}

function updateLikeCount(responseid, count) {
    countquery = "#span-likecount-" + responseid
    document.querySelector(countquery).innerHTML = count
}


function addlike(responseid, userid) {
    if (userid === 'None') {
        alert('You Need To Login To Like')
        return
    }
    fetch(rootUrl + "/api/add-response-like/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Authorization: 'Token ' + localStorage.getItem('token')
            },
            body: JSON.stringify({
                responseid: responseid,
                userid: userid,
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success === "added") {
                toggleLike(responseid)
                updateLikeCount(responseid, data.count)
            } else if (data.error) {
                alert(data.error)
            } else {
                alert(data)
            }
        })
}

function removelike(responseid, userid) {
    fetch(rootUrl + "/api/remove-response-like/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Authorization: 'Token ' + localStorage.getItem('token')
            },
            body: JSON.stringify({
                responseid: responseid,
                userid: userid,
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success === "removed") {
                toggleLike(responseid)
                updateLikeCount(responseid, data.count)
            } else if (data.error) {
                alert(data.error)
            } else {
                alert(data)
            }
        })
}