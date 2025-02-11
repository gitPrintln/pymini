

window.addEventListener('DOMContentLoaded', () => {
    enter();
});
// 검색창 검색 버튼 클릭했을 때
function searchSubmit() {
    selection = document.getElementById("selected").value;
    query = document.getElementById("searchInput").value;
    fetch('/search', { method: 'post',
        headers: {
            'Content-Type': 'application/json'  // JSON 형식
        },
        body: JSON.stringify({ selection: selection, query: query })
     })  // Flask에 요청 보내기
        .then(response => response.json())
        .then(data => {
            if(data.message === 'success'){
                // 검색창 초기화
                clearInput();
            } else{
                alert("검색어를 입력해주세요!!")
            }
        }).catch(error => {
            // 에러가 발생한 경우 catch 블록에서 처리
            console.error('Error:', error);
            clearInput(); // 검색 결과가 없을 때도 초기화
        });
}

// 검색 완료 후 검색창 초기화
function clearInput() {
    document.getElementById("searchInput").value = '';  // 빈 값으로 변경
}

// Enter로 동작 가능하게 하기
function enter() {
    searchInput = document.getElementById("searchInput");
    submitBtn = document.getElementById("submitBtn");
    searchInput.addEventListener('keydown', function(event) {
        // 엔터 키(키 코드 13)가 눌렸을 때
        if (event.key === 'Enter') {
            submitBtn.click();
        }
    });
}