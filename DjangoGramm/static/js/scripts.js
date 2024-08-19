$(document).ready(function () {
    $('.like-button').click(function () {
        var button = $(this);
        var post_id = button.data('post-id');
        var url = button.data('url');
        var csrf_token = button.data('csrf');

        $.ajax({
            url: url,
            method: 'POST',
            data: {
                'post_id': post_id,
                'csrfmiddlewaretoken': csrf_token
            },
            success: function (response) {
                if (response.liked) {
                    button.find('i').removeClass('bi-heart').addClass('bi-heart-fill');
                } else {
                    button.find('i').removeClass('bi-heart-fill').addClass('bi-heart');
                }
                button.find('.like-count').text(response.like_count);
            },
            error: function (response) {
                alert('An error occurred. Please try again.');
            }
        });
    });
});

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
