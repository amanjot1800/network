window.onpopstate = function (event) {

}

document.addEventListener('DOMContentLoaded', function () {

    if (window.location.pathname.match(/^[\/][{p}][\/][\w]*$/)) {
        //document.getElementById("follow").onclick = () => follow();
        fetch_posts("")
    } else {
        fetch_posts("all");
        document.getElementById("post-submit-button").onclick = () => make_posts();
    }
});

function follow() {

    const puser = document.getElementById("follow").dataset.puser;
    const ruser = document.getElementById("follow").dataset.ruser;

    fetch(`/p/${puser}`, {
        method: 'PUT',
        body: JSON.stringify({
            "start_following": ruser,
        }),
    }).then(response => response.json())
        .then(result => {
            document.getElementById("follow").innerHTML = "Following";
            if (result.error !== undefined) {
                alert(result.error);
            }
        })
}


function fetch_posts(who) {

    document.getElementById('posts-view').innerHTML = "";

    if (who==="all") {
        fetch(`/posts`)
            .then(response => response.json())
            .then(posts => {
                posts.forEach(post => {
                    populate_dom(post)
                })
            })
    } else {
        fetch(`/userposts/${window.location.pathname.substr(3)}`)
            .then(response => response.json())
            .then(posts => {
                posts.forEach(post => {
                    populate_dom(post)
                })
            })
    }
}

function populate_dom(post) {
    const card_body = document.createElement('div');
    card_body.setAttribute('class', 'card-body');

    const card_title = document.createElement('a');
    card_title.setAttribute("href", `/p/${post['user']}`)
    card_title.setAttribute('class', 'card-title');
    card_title.innerHTML = post['user'];
    const card_title_link = document.createElement('h3').appendChild(card_title);


    const card_text = document.createElement('p');
    card_text.setAttribute('class', 'card-text');
    card_text.innerHTML = post['body'];

    const card_timestamp = document.createElement('p');
    card_timestamp.setAttribute('class', 'card-timestamp');
    card_timestamp.innerHTML = post['timestamp'];

    const card_like_image = document.createElement('img');

    if (post['likes_users'].includes(JSON.parse(document.getElementById('current_user').textContent))) {
        card_like_image.setAttribute('src', '../../static/network/heart.png');
        card_like_image.addEventListener('click', () => {
            fetch(`/posts/${post['id']}`, {
                method: 'PUT',
                body: JSON.stringify({
                    "unlikes": true,
                })
            }).then(() => fetch_posts(""))
        })
    } else {
        card_like_image.setAttribute('src', '../../static/network/heartu.png');
        card_like_image.addEventListener('click', () => {
            fetch(`/posts/${post['id']}`, {
                method: 'PUT',
                body: JSON.stringify({
                    "likes": true,
                })
            }).then(() => fetch_posts(""))
        })
    }

    const card_like_count = document.createElement('span');
    card_like_count.innerHTML = " " + post['likes_count'];

    const like_container = document.createElement('p');
    like_container.append(card_like_image, card_like_count);

    if (document.getElementById('current_user').textContent === "\"\"") {
        card_body.append(card_title_link, card_text, card_timestamp);
    } else card_body.append(card_title_link, card_text, card_timestamp, like_container);

    const card = document.createElement('div');
    card.setAttribute('class', 'card');
    card.appendChild(card_body);

    document.getElementById('posts-view').appendChild(card);
}

function make_posts() {

    const text = document.getElementById("post-text").value;
    fetch('/newpost', {
        method: 'POST',
        body: JSON.stringify({
            text: text
        })
    }).then(response => response.json())
        .then(result => {
            fetch_posts("all");
            document.getElementById("post-text").value = "";
            if (result.error !== undefined) {
                alert(result.error);
            }
        })
}