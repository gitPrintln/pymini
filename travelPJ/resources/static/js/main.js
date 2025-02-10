

window.addEventListener('DOMContentLoaded', () => {
    
});
// 검색창 검색 버튼 클릭했을 때
function searchSubmit() {
    query = document.getElementById("searchInput").value;
    fetch('/search', { method: 'post',
        headers: {
            'Content-Type': 'application/json'  // JSON 형식
        },
        body: JSON.stringify({ query: query })
     })  // Flask에 요청 보내기
        .then(response => response.json())
        .then(data => {
            console.log(data)
            if(data.message === 'success'){
                // 검색창 초기화
                clearInput();
            } else{
                alert("검색어를 입력해주세요!!")
            }
        }).catch(error => {
            // 에러가 발생한 경우 catch 블록에서 처리
            console.error('Error:', error);
        });
}

// 검색 완료 후 검색창 초기화
function clearInput() {
    document.getElementById("searchInput").value = '';  // 빈 값으로 변경
}