function search() {
  const keyword = $("#keyword").val();
  const searchSelect = $("#searchSelect").val();
  window.location.href = `/search?select=${searchSelect}&keyword=${keyword}`;
}

function detail(plate_num) {
  window.location.href = `/detail?plate_num=${plate_num}`;
}
