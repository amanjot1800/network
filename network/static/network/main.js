window.onpopstate = function(event) {

}

document.addEventListener('DOMContentLoaded', function () {

    document.getElementById('test').addEventListener('click', () => {
        window.alert("It works!!");
    })
    fetch_posts();

});

function fetch_posts() {

    fetch(`/posts`)
        .then(response => response.json())
        .then(posts => {
            posts.forEach(post => {
                const card_body = document.createElement('div');
                card_body.setAttribute('class', 'card-body');

                const card_title = document.createElement('h3');
                card_title.setAttribute('class', 'card-title');
                card_title.innerHTML = post['title'];

                const card_text = document.createElement('p');
                card_text.setAttribute('class', 'card-text');
                card_text.innerHTML = post['body'];

                const card_timestamp = document.createElement('p');
                card_timestamp.setAttribute('class', 'card-timestamp' );
                card_timestamp.innerHTML = post['timestamp'];

                const card_like_image = document.createElement('img');
                card_like_image.setAttribute('src', '../../static/network/heart.png');

                const card_like_count = document.createElement('span');
                card_like_count.innerHTML = post['likes'];

                const like_container = document.createElement('p');
                like_container.append(card_like_image, card_like_count);

                card_body.append(card_title, card_text, card_timestamp, like_container);

                const card = document.createElement('div');
                card.setAttribute('class', 'card');
                card.appendChild(card_body);

                document.getElementById('posts-view').appendChild(card);

            })
        })

}