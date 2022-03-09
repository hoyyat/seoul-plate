function search() {
  const keyword = $("#keyword").val();
  const searchSelect = $("#searchSelect").val();

  window.location.href = `/search?select=${searchSelect}&keyword=${keyword}`;
}