// AJAX to handle file upload
$('#file-upload').on('change', function(e) {
    var formData = new FormData();
    formData.append('file', e.target.files[0]);

    $.ajax({
        url: '/upload/' + roomName + '/',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(data) {
            // Notify other users via WebSocket after successful file upload
            chatSocket.send(JSON.stringify({
                'file_url': data.file_url,
                'user': data.user
            }));
        },
        error: function(xhr, status, error) {
            console.error('Error uploading file: ' + error);
        }
    });
});
