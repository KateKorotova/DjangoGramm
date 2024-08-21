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