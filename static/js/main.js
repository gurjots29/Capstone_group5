      document.addEventListener("DOMContentLoaded", function() {
    
      // Event listener for postForm
       document.getElementById('postForm').addEventListener('submit', function(event) {
        event.preventDefault();  
        
        let formData = new FormData(this);
        
        // Verifica si los datos están siendo agregados al formData
        for(let pair of formData.entries()) {
            console.log(pair[0] + ', ' + pair[1]);
        }
    
        // Configura el header para el token CSRF
        let headers = new Headers();
        headers.append('X-CSRFToken', getCookie('csrftoken'));  // Asumiendo que tienes una función que obtiene el valor del cookie csrftoken
    
        fetch("/api/posts/", {
            method: "POST",
            headers: headers,
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.id) {
                alert("Post created successfully!");
                window.location.href = "/";
            } else {
                alert("Error: " + JSON.stringify(data));
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred. Please try again.");
        });
    });
    
    // Función para obtener el valor de un cookie
    function getCookie(name) {
        let value = "; " + document.cookie;
        let parts = value.split("; " + name + "=");
        if (parts.length == 2) return parts.pop().split(";").shift();
    }

    // Event listeners for each commentForm
    let commentForms = document.querySelectorAll('.commentForm');
    commentForms.forEach(form => {
        form.addEventListener("submit", function(event) {
            event.preventDefault();  
            let postId = this.getAttribute('data-post-id');
            let formData = new FormData();
            formData.append('csrfmiddlewaretoken', getCSRFToken());
            formData.append('text', this.querySelector('textarea[name="text"]').value);
            formData.append('post', postId);

            fetch("/api/post/comments/", {
                method: "POST",
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.id) {  
                    alert("Comment added successfully!");
                    location.reload();  
                } else {
                    alert("Error: " + JSON.stringify(data));
                }
            })
            .catch(error => {
                console.error("Error:", error);
                alert("An error occurred. Please try again.");
            });
        });
    });

    // Function to get CSRF token
    function getCSRFToken() {
        const name = "csrftoken=";
        const decodedCookie = decodeURIComponent(document.cookie);
        const cookieArray = decodedCookie.split(';');

        for (let i = 0; i < cookieArray.length; i++) {
            let cookie = cookieArray[i];
            while (cookie.charAt(0) === ' ') {
                cookie = cookie.substring(1);
            }
            if (cookie.indexOf(name) === 0) {
                return cookie.substring(name.length, cookie.length);
            }
        }
        return "";
    }

    // Event listeners for each comment button
    let commentButtons = document.querySelectorAll('.add-comment-btn');
    commentButtons.forEach(btn => {
        btn.addEventListener("click", function() {
            let postId = this.getAttribute('data-post-id');
            let form = document.querySelector(`.commentForm[data-post-id="${postId}"]`);
            form.classList.remove('hidden');
        });
    });
    
});
