
function login() { // 로그인 함수 만들어서 데이터 넘겨줌
  $.ajax({
    type: "POST",
    url: "api/login",
    data: { id_give: $("#id").val(), pw_give: $("#pw").val() },
    success: function (response) {
      if (response["result"] === "success") {
        $.cookie("mytoken", response["token"]);
        alert("로그인 완료!");
        window.location.href = "/main2";
      } else {
        alert(response["msg"]);
      }
    },
  });
}
