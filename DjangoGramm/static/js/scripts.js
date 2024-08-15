document.addEventListener('DOMContentLoaded', function() {
    var createPostModal = document.getElementById('createPostModal');
    createPostModal.addEventListener('show.bs.modal', function (event) {
        var modalBody = createPostModal.querySelector('.modal-body');
        fetch("{% url 'add_post' %}", {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(response => response.json())
        .then(data => {
            modalBody.innerHTML = data.html;
        });
    });
});
