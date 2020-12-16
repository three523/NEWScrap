function keywordAdd() {
    if (($('.add-list > button').length) + 1 <= 6) {
        keyword = $('#input-emxail-keyword').val()
        iskeyword = false
        $('.add-list').children().each(function () {
            iskeyword = keyword === $(this).text()
            if (iskeyword) {
                return
            }
        })
        if (keyword === '') {
            swal("아무것도 입력이 안되었습니다")
        } else if (iskeyword) {
            swal("이미 입력한 키워드입니다")
        } else {
            $('.add-list').append(`<button onclick="keywordDel(this)" class="keyword-lists">${keyword}</button>`)
        }
    } else {
        swal("키워드는 6개까지만 가능합니다")
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
function addEmail(btn) {
    $('#email-del').attr('disabled', true)
    $('#email-add').attr('disabled', true)
    if ('none' !== $('#input-email-add').css('display')) {
        $('#email-del').attr('disabled', false)
        $('#email-add').attr('disabled', false)
        let email = $('#input-email-add').val()
        let keywords = ""
        $('.add-list').children().each(function () {
            keywords += $(this).text()
            keywords += ","
        })
        if ($('.add-list > button').length < 2) {
            swal("키워드를 두개 이상 입력해야합니다")
        } else if (!isEmail(email)) {
            swal("이메일 형식이 틀립니다(예시: example@example.com)")
        } else {
            $('.swal-overlay').css('display','none')
            $('.loader').css('display', 'block')
            $('.loader-area').css('display','flex')
            setTimeout(function () {
                $.ajax({
                    async: false,
                    type: "POST",
                    url: "/email/save",
                    data: {
                        'email': email,
                        'keywords': keywords
                    },
                    success: function (response) {
                        if (response['result'] === false) {
                            $('.loader').css('display', 'none')
                            $('.loader-area').css('display','none')
                            swal(response['msg'])
                        } else {
                            document.write(response)
                        }
                    }
                })
            }, 100);
        }
    } else if ($('#input-email-del').css('display') !== 'none') {
        $('#input-email-del').animate({
            'width': '-=320'
        }, 500, function () {
            $('#input-email-del').css('display', 'none')
        })
        $('#email-del').animate({
            'left': '-=190'
        }, 500, function () {
            $('.delete-input-area').animate({
                'top': '-=80'
            }, 500, function () {
                subscribe = $('.subscribe-add')
                emailArea = $('.email-input-area')
                keywordBtn = $('#email-keyword')
                subscribe.animate({
                    'top': "+=80"
                }, 500)
                $('#email-del').animate({
                    'margin-left': '10'
                }, 500)
                keywordBtn.css('display', 'block')
                emailArea.animate({
                    'top': "+=80"
                }, 500, function () {
                    $('#email-keyword').animate({
                        'left': "+=320"
                    }, 500, function () {
                        $('#input-emxail-keyword').css('display', 'block')
                        $('#email-del').attr('disabled', false)
                        $('#email-add').attr('disabled', false)
                        $('#input-emxail-keyword').animate({
                            'width': '+=300'
                        }, 500)
                    })
                    $('#email-add').animate({
                        'left': "+=320"
                    }, 500, function () {
                        $('#input-email-add').css('display', 'block')
                        $('#input-email-add').animate({
                            'width': '+=300'
                        }, 500)
                    })

                })
            })
        })

    } else {
        subscribe = $('.subscribe-add')
        emailArea = $('.email-input-area')
        keywordBtn = $('#email-keyword')
        subscribe.animate({
            'top': "+=80"
        }, 500)
        $('#email-del').animate({
            'margin-left': '10'
        }, 500)
        keywordBtn.css('display', 'block')
        emailArea.animate({
            'top': "+=80"
        }, 500, function () {
            $('#email-keyword').animate({
                'left': "+=320"
            }, 500, function () {
                $('#input-emxail-keyword').css('display', 'block')
                $('#email-del').attr('disabled', false)
                $('#email-add').attr('disabled', false)
                $('#input-emxail-keyword').animate({
                    'width': '+=300'
                }, 500)
            })
            $('#email-add').animate({
                'left': "+=320"
            }, 500, function () {
                $('#input-email-add').css('display', 'block')
                $('#input-email-add').animate({
                    'width': '+=300'
                }, 500)
            })

        })
    }
}

function delEmail() {
    $('.add-list').empty()
    $('#email-del').attr('disabled', true)
    $('#email-add').attr('disabled', true)
    if ($('#input-email-add').css('display') === 'none' && $('#input-email-del').css('display') === 'none') {
        $('.delete-input-area').animate({
            'top': '+=80'
        }, 500, function () {
            $('#input-email-del').css('display', 'block')
            $('#email-del').attr('disabled', false)
            $('#email-add').attr('disabled', false)
            $('#input-email-del').animate({
                'width': '+=300'
            }, 500)
            $('#email-del').animate({
                'left': '+=190'
            }, 500)
        })
    } else if ($('#input-email-del').css('display') !== 'none') {
        $('#email-del').attr('disabled', false)
        $('#email-add').attr('disabled', false)
        email = $('#input-email-del').val()
        if (!isEmail(email)) {
            swal("이메일 형식이 틀립니다(예시: example@example.com)");
        } else {
            $.ajax({
                type: "POST",
                url: "/email/del",
                data: {
                    'email': email
                },
                success: function (response) {
                    if (response["result"] === "success") {
                        swal(response['msg'])
                        .then((value => {
                            location.reload()
                    }))
                    }
                }
            })
        }
    } else {
        $('#input-emxail-keyword').animate({
            'width': '0'
        }, 500, function () {
            $('#input-emxail-keyword').css('display', 'none')
            $('#email-keyword').animate({
                'left': '-=320'
            }, 500)
        })
        $('#input-email-add').animate({
            'width': '0'
        }, 500, function () {
            $('#input-email-add').css('display', 'none')
            $('#input-email-add').animate({
                'top': '-=80'
            })
            $('#email-add').animate({
                'left': '-=320'
            }, 500, function () {
                $('#email-add').animate({
                    'top': '-=80'
                }, 500, function () {
                    $('#email-keyword').css('display', 'none')
                    $('#email-del').animate({
                        'margin-left': '140'
                    }, 500)
                    $('.email-input-area').animate({
                        'top': '-=80'
                    }, 500, function () {
                        $('.delete-input-area').animate({
                            'top': '+=80'
                        }, 500, function () {
                            $('#input-email-del').css('display', 'block')
                            $('#email-del').attr('disabled', false)
                            $('#email-add').attr('disabled', false)
                            $('#input-email-del').animate({
                                'width': '+=300'
                            }, 500)
                            $('#email-del').animate({
                                'left': '+=190'
                            }, 500)
                        })
                    })
                    $('.keyword-input-area').animate({
                        'top': '-=80'
                    })
                    $('.add-list').animate({
                        'top': '-=80'
                    })
                    $('#input-emxail-keyword').animate({
                        'top': '-=80'
                    }, 500)
                    $('#email-keyword').animate({
                        'top': '-=80'
                    }, 500)
                })
            })
        })
    }
}
function emailCheck() {
    code = $('#code').val()
    $.ajax({
        type: "POST",
        url: "/email/code",
        data: {
            'code': code,
        },
        success: function (response) {
            if (response['result'] === true) {
                swal(response['msg'])
                    .then((value => {
                        location.reload()
                    }))
            } else {
                swal(response['msg'])
            }
        }
    })
}

function reSender(btn) {
    $('.loader').css('display', 'block')
    $('.loader-area').css('display','flex')
    setTimeout(function () {
        email = $('#email-id').text()
        $.ajax({
            type: "POST",
            url: "/resend",
            data: {
                'email': email,
            },
            success: function (response) {
                $('.loader').css('display', 'none')
                $('.loader-area').css('display','none')
                swal(response['msg']);
                btn.disabled = false;
            }
        })
    }, 0);

}