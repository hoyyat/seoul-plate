function search() {
  const keyword = $("#keyword").val();
  const searchSelect =$("#searchSelect").val();
    $.ajax({
    type: "POST",
    url: "/api/search_title_place",
    data: { key_give : keyword, select_give : searchSelect },
    success: function (response) {
      console.log(response)
      location.reload();
    },
  });
}// const var let 차이점 알아보기



