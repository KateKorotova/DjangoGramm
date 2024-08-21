document.addEventListener('DOMContentLoaded', function() {
    var createPostModal = document.getElementById('createPostModal');
    createPostModal.addEventListener('show.bs.modal', function (event) {
        var button = event.relatedTarget; // Button that triggered the modal
        var url = button.getAttribute('data-url'); // Extract the URL from data-url attribute
        var csrfToken = button.getAttribute('data-csrf'); // Extract the CSRF token from data-csrf attribute

        var modalBody = createPostModal.querySelector('.modal-body');

        fetch(url, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrfToken // Add CSRF token to the headers
            }
        })
        .then(response => response.json())
        .then(data => {
            modalBody.innerHTML = data.html;
        });
    });
});
