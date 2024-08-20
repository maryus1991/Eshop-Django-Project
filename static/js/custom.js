function fillParentForComments(id) {
    $('#parentforcomments').val(id)
}

function addProductToOrder(product_id) {
    let Product_count = $('#Product_count').val()
    $.get('/order/add-Product-To-Order?pid=' + product_id + '&count=' + Product_count).then(res => {
        if (res.status === 200) {
            document.getElementById('successfororder').removeAttribute('hidden')
        } else {
            // console.log('ssssssssssssssss')
            $('#resultreq').text(res.status)
            $('#successfororder').removeClass('alert-success').addClass('alert-danger')
            document.getElementById('successfororder').removeAttribute('hidden')
        }
    })
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

function remove_item_content(detail_id) {
    $.get('/order/remove?detail_id=' + detail_id).then(res => {
            if (res.status === 200) {
                $('#order').html(res.data)
            }
        }
    )
}

function ChangeOrderCount(detail_id, state) {
    $.get('/order/Change-Count?detail_id=' + detail_id + '&state=' + state).then(res => {
            if (res.status === 200) {
                $('#order').html(res.data)
            } else {
                $('#problem').removeClass('hidden').text(res.status)
            }
        }
    )
}