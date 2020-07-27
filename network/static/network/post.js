document.addEventListener('DOMContentLoaded', function() {
    add_like_eventHandler();
    add_follow_eventHandler();
    add_edit_eventHandler();
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

//Handles follow/unfollow button click events
function add_follow_eventHandler() {
    // Grab element node of follow button
    var followButton = document.querySelector('#followButton')

    // Only run if there is an actual follow button avaialable (case of no user logged in)
    if (followButton) {
        followButton.addEventListener('click', (e) => {
            //Use api to either follow/unfollow depending on which button was available
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

//Adds event handlers to all edit buttons on page
function add_edit_eventHandler() {
    //Grab nodeslist of edit buttons
    var buttonList = document.querySelectorAll('.editButton');
    var boxElement, contentElement;

    //Only proceed if there if an edit button avaialable
    if (buttonList) {
        //Loop through list of avaialable edit buttons and add event handlers to all of them
        for (var button of buttonList) {
            button.addEventListener('click', (e) => {
                //Current structure of each post has a box parent element that is three elements above the edit button
                boxElement = e.target.parentElement.parentElement.parentElement;

                //Button is edit so replace content with text area logic
                if (e.target.value == "Edit") {
                    contentElement = boxElement.querySelector('.content');

                    //Create textarea element and fill its content with what's currently inside the post
                    var textArea = document.createElement('textarea');
                    var text = document.createTextNode(contentElement.innerHTML.trim());
                    textArea.appendChild(text);
                
                    //Replace content divtag with new textarea element
                    contentElement.replaceWith(textArea);

                    //Change button to 'save' instead
                    e.target.value = "Save";
                //Button is save so add submit handler logic
                } else {
                    //Current structure has the like button contain a data attr which has the current post number
                    var commonParent = e.target.parentElement.parentElement;
                    var likeElement = commonParent.querySelector('.fa');
                    var postId = likeElement.dataset.postnumber;
                    var textElement = boxElement.querySelector('textarea');
                    
                    fetch(`/edit/${postId}`, {
                        method: "PUT",
                        body: JSON.stringify({
                            content: textElement.value.trim()
                        })
                    })
                    .then(response => response)
                    .then(response => {
                    //Create div and grab content from textarea
                    var divContent = document.createElement('div');
                    var content = textElement.value.trim();
                    
                    //Add class content so div can be selected later and replace textarea
                    divContent.classList.add("content");
                    divContent.innerHTML = content;
                    textElement.replaceWith(divContent);

                    //Switch button back to edit now
                    e.target.value = "Edit";
                    })
                }
            });
        }
    }
}