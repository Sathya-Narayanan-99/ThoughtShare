form = document.getElementById('comment-form');

form.addEventListener("submit",function(e){
    e.preventDefault();

    if (user == 'AnonymousUser'){
        var commentFormData = {
            'username' : form.username.value,
            'email' : form.email.value,
            'content' : form.content.value,
        }
    }else{
        var commentFormData = {
            'content' : form.content.value,
        }        
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

var comments = document.getElementsByClassName("d-none");

if (comments.length === 0){
    document.getElementById("load-comments-div").innerHTML='';
}

try {
    document.getElementById("load-comments").addEventListener('click',function(){
        for(var i=0;i<3;i++){
            if (comments[0] != undefined){
                comments[0].classList.remove("d-none")
            }
        }
        if (comments.length === 0){
            document.getElementById("load-comments-div").innerHTML='';
        }
    })    
}catch{
    
}
