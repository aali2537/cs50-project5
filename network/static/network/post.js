document.addEventListener('DOMContentLoaded', function() {
    add_like_eventHandler();
    add_follow_eventHandler();

});

// Toggles the like value of the post inside the database
function toggle_like(event) {
    //Check to make sure a user is logged in(since non logged in people can view all posts)
    if (event.target.dataset.user !== "") {
        //Grab current post number of clicked event
        currentPost = event.target.dataset.postnumber;

        //Update database with request to toggle like and return result/update page
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

function add_follow_eventHandler() {
    // Grab element node of follow button
    var followButton = document.querySelector('#followButton')

    if (followButton) {

    followButton.addEventListener('click', (e) => {
        fetch(`/follow/${e.target.dataset.owner}`, {
            method: "PUT",
            body: JSON.stringify({
                button: e.target.value
            })
        })
        .then(response => response)
        .then(() => {
            // Swap the value of the button after click
            if (e.target.value === "Follow") {
                followButton.value = "Unfollow"
            } else {
                followButton.value = "Follow"
            }
        });
    });
    }
}