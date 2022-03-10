function search() {
  const keyword = $("#keyword").val();
  const searchSelect = $("#searchSelect").val();
  window.location.href = `/search?select=${searchSelect}&keyword=${keyword}`;
}
 // search 함수 만들어서  search로 보냄
function detail(plate_num) {
  window.location.href = `/detail?plate_num=${plate_num}`;
}
