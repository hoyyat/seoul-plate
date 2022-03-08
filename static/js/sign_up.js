function signup(){
    // const formData = $('.joinForm').serialize();
    // console.log(formData.get('email')

    $.ajax({
        type:"POST",
        url:"/api/signup",
        data:{'id_give': $('.email').val(), 'pw_give': $('input[name=loginPw]').val()},
        success: function (response) {
            if (response['result'] === 'success') {
                alert('회원가입 완료!')
                window.location.href = '/login'
            }else{
                alert(response['msg'])
            }
        }
    })
}