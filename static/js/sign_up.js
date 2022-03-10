var joinCheck = false;
// 자바스크립트 전체에서 사용하는 변수 (전역변수)
function signup() {
    var signCHeck = false;
    // const formData = $('.joinForm').serialize();
    // console.log(formData.get('email')
    if (!joinCheck) {
        alert("이메일 중복체크를 해주세요.")
        return;
    }

    var password = $("#loginPw").val();
    var password2 = $("#loginPwConfirm").val();

    if (password == "") {
        $("#help-password").text("비밀번호를 입력해주세요.").removeClass("is-safe").addClass("is-danger")
        $("#loginPw").focus()
        return;
    } else if (!is_password(password)) {
        $("#help-password").text("비밀번호의 형식을 확인해주세요. 영문과 숫자 필수 포함, 특수문자(!@#$%^&*) 사용가능 8-20자").removeClass("is-safe").addClass("is-danger")
        $("#loginPw").focus()
        return;
    } else {
        $("#help-password").text("사용할 수 있는 비밀번호입니다.").removeClass("is-danger").addClass("is-success")
    }
    //위에 비밀번호
    if (password2 == "") {
        $("#help-password2").text("비밀번호를 입력해주세요.").removeClass("is-safe").addClass("is-danger")
        $("#loginPwConfirm").focus()
        return;
    } else if (password2 != password) {
        $("#help-password2").text("비밀번호가 일치하지 않습니다.").removeClass("is-safe").addClass("is-danger")
        $("#loginPwConfirm").focus()
        return;
    } else {
        $("#help-password2").text("비밀번호가 일치합니다.").removeClass("is-danger").addClass("is-success")
    }
    $.ajax({
        type: "POST",
        url: "/api/signup",
        data: {
            id_give: $(".email").val(),
            pw_give: $("input[name=loginPw]").val(),
        },
        success: function (response) {
            if (response["result"] === "success") {
                alert(response["msg"]);
                window.location.href = "/";
            } else {
                alert(response["msg"]);
            }
        },
    });
}

function is_nickname(asValue) {
    var regExp = /[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]$/i;
    return regExp.test(asValue);
}

function check_dup() {
    let email = $("#email").val() //id로 가져온거
    //console.log($("#email"))
    // $("div[name=email]").val() name
    // $(".email").val() class로 가져오는법
    console.log(email)
    if (email == "") {
        $("#help-email").text("이메일를 입력해주세요.").removeClass("is-safe").addClass("is-danger")
        $("#email").focus()
        return;
    }
    if (!is_nickname(email)) {
        $("#help-email").text("이메일 형식으로 써주세요.").removeClass("is-safe").addClass("is-danger")
        $("#email").focus()
        return;
    }


    $("#help-email").addClass("is-loading")
    $.ajax({
        type: "POST",
        url: "/sign_up/check_dup",
        data: {
            id_give: email
        },
        success: function (response) {
            console.log('1', response)
            if (response["exists"]) {
                $("#help-email").text("이미 존재하는 이메일입니다.").removeClass("is-safe").addClass("is-danger")
                $("#email").focus()
                joinCheck = false
            } else {
                $("#help-email").text("사용할 수 있는 이메일입니다.").removeClass("is-danger").addClass("is-success")
                joinCheck = true
            }
            $("#help-email").removeClass("is-loading")
        }
    });
}

function is_password(asValue) {
    var regExp = /^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z!@#$%^&*]{8,20}$/;
    return regExp.test(asValue);
}











