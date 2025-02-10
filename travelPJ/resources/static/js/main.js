

window.onload = function() {
    // 검색 완료 후 검색창 초기화
    function clearInput() {
        fetch('/clearInput', { method: 'POST' })  // Flask에 요청 보내기
            .then(response => response.json())
            .then(data => {
                document.getElementById("searchInput").value = data.new_value;  // 값을 변경
            });
    }
}