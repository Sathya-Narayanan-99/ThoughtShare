form = document.getElementById('comment-form');

form.addEventListener("submit",function(e){
    e.preventDefault();

    var commentFormData = {
        'username' : form.username.value,
        'email' : form.email.value,
        'content' : form.content.value,
    }
    
    url = '/add_comment/'
    fetch(url,{
        method: 'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf
        },
        body:JSON.stringify({'form':commentFormData,'postId':postId})
    })

    .then((response) =>{
        return response.json()
    })

    .then((data) => {
        location.reload();
    })
})
form.reset();