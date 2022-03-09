function comment(plateNum) {
  const myComment = $("#comment").val();
  $.ajax({
    type: "POST",
    url: "/api/comment",
    data: { comment_give: myComment, plate_num: plateNum },
    success: function (response) {
      if (response["msg"] === "success") {
        location.reload();
      }
    },
  });
}
