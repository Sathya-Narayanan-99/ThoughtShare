// Add comment
var addForm = document.getElementById('comment-form');

addForm.addEventListener("submit",function(e){
    e.preventDefault();

    if (user == 'AnonymousUser'){
        var commentFormData = {
            'username' : addForm.username.value,
            'email' : addForm.email.value,
            'content' : addForm.content.value,
        }
    }else{
        var commentFormData = {
            'content' : addForm.content.value,
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
addForm.reset();

// delete comment
var deleteComments = document.getElementsByClassName("delete-comment")

for (var i = 0; i < deleteComments.length; i++) {
    deleteComments[i].addEventListener("click", function(e){
        e.preventDefault()
        commentId = this.dataset.comment
        
        var url = "/delete_comment/"
        fetch(url,{
            method: 'POST',
            headers:{
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf
            },
            body:JSON.stringify({'commentId':commentId})
        })
        .then((response) =>{
            return response.json()
        })
    
        .then((data) => {
            location.reload();
        })
    })   
}

// load more
var comments = document.getElementsByClassName("d-none");

if (comments.length < 3){
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
