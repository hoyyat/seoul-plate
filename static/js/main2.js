function search() {
  const keyword = $("#keyword").val();
  const searchSelect = $("#searchSelect").val();
  $.ajax({
    type: "POST",
    url: "/api/search_title_place",
    data: { key_give: keyword, select_give: searchSelect },
    success: function (response) {
      window.location.href = `/search?select=${response["select"]}&keyword=${response["keyword"]}`;
    },
  });
} // const var let 차이점 알아보기
