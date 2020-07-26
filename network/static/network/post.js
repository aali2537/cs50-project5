document.addEventListener('DOMContentLoaded', function() {
    add_like_eventHandler();

});

function toggle_like(event) {
    //Check to make sure a user is logged in(since non logged in people can view all posts)
    if (event.target.dataset.user !== "") {
        //Grab current post number of clicked event
        currentPost = event.target.dataset.postnumber;

        //Update database with request to toggle like and return result
        fetch(`/likes/${currentPost}`)
        .then(response => response.json())
        .then(email => {
            event.target.innerHTML = ` ${email.likes}`;
        });
    }
}

// Adds event handlers too all like buttons currently on the page
function add_like_eventHandler() {
    //Grab nodelist of all like buttons of posts
    var buttonList = document.querySelectorAll('.fa-heart');

    //Loop through node list of buttons and add an like event handler to each one
    for (var button of buttonList) {
        button.addEventListener('click', (e) => toggle_like(e));
    }
}