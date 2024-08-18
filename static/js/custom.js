function fillParentForComments(id) {
    $('#parentforcomments').val(id)
}


function sendArticleComment(blog_id) {
    var text = $('#ssmmdd').val()
    var username = $('#username').val()


    $.get('add-blog-comments', {
        text: text,
        username: username,
        blog_id: blog_id,
        parent: $('#parentforcomments').val()
    })
        .then(res => {
            $('#sucess_comment').addClass('alert alert-success').text('کامنت شما با موفقیت ارسال شد')
            $('#response_area').html(res)
            var text = $('#ssmmdd').val('')
            var username = $('#username').val('')
            document.getElementById('response_area').scrollIntoView({behavior: "smooth"})
        })
}