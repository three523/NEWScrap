$(document).ready(function () {
    $('.news-list').empty()
    showNewslist();
});

function addModalshow() {
    $('#add-modal').css('visibility', 'visible')
    $('#add-exit-btn').css('visibility', 'visible')
    $('.slider-btn').css('visibility', 'hidden')
    $('.add-list').empty()
}

function delModalshow() {
    $('#del-modal').css('visibility', 'visible')
    $('#del-exit-btn').css('visibility', 'visible')
    $('.slider-btn').css('visibility', 'hidden')
}



function keywordAdd() {
    if (($('.add-list > button').length) + 1 <= 3) {
        keyword = $('#keyword-add').val()
        $('.add-list').append(`<button onclick="keywordDel(this)" class="keyword-lists">${keyword}</button>`)
    } else {
        alert("키워드는 3개까지만 가능합니다")
    }
}

function keywordDel(delBtn) {
    delBtn.remove()
}
function isEmail(asValue) {
    let regExp = /^([0-9a-zA-Z_\.-]+)@([0-9a-zA-Z_-]+)(\.[0-9a-zA-Z_-]+){1,2}$/
    console.log(regExp.test(asValue))
    return regExp.test(asValue);
}
function addEmail() {
    let email = $('#email-input-add').val()
    let keywords = ""
    $('.add-list').children().each(function () {
        keywords += $(this).text()
        keywords += ","
    })
    if ($('.add-list > button').length === 0) {
        alert("키워드를 하나 이상 입력해야합니다")
    } else if (!isEmail(email)) {
        alert("이메일 형식이 틀립니다(예시: example@example.com)")
    } else {
        $.ajax({
            type: "POST",
            url: "/email/save",
            data: {
                'email': email,
                'keywords': keywords
            },
            success: function (response) {
                console.log(response)
                if (response["result"] === "success") {
                    alert(response["msg"]);
                    location.reload()
                }
            }
        })
    }
}

function delEmail() {
    email = $('#email-input-del').val()
    if (!isEmail(email)) {
        alert("이메일 형식이 틀립니다(예시: example@example.com)")
    } else {
        $.ajax({
            type: "POST",
            url: "/email/del",
            data: {
                'email': email
            },
            success: function (response) {
                if (response["result"] === "success") {
                    alert(response["msg"]);
                    location.reload()
                }
            }
        })
    }
}

function slider() {
    if ($('.slider-img').attr('src') === 'static/up-arrow.png') {
        $('.news-content').css('height', '100%')
        $('.main').css('height', '0%')
        $('.slider-img').attr('src', 'static/down-arrow.png')
    } else {
        $('.news-content').css('height', '60%')
        $('.main').css('height', '40%')
        $('.slider-img').attr('src', 'static/up-arrow.png')
    }
}

function modalExit(modal_btn) {
    modal = modal_btn.parentElement.parentElement
    modal.style.visibility = 'hidden'
    modal_btn.style.visibility = 'hidden'
    $('.slider-btn').css('visibility', 'visible')
}

function showNewslist() {
    $.ajax({
        type: "GET",
        url: "/news/list",
        data: {},
        success: function (response) {
            if (response["result"] === "success") {
                news = response['news']
                for (let i = 0; i < news.length; i++) {
                    console.log(news)
                    title = news[i]['title']
                    img = news[i]['image']
                    dec = news[i]['description']
                    url = news[i]['link']

                    $('.news-list').append(`
                                            <a href="${url}" class="news-item">
                                                <img src="${img}" alt="" class="image">
                                                <h3 class="title">${title}</h3>
                                                <div class="dec">${dec}</div>
                                            </a>`)
                }
            }
        }
    })
}