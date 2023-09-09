// fetch('https://verdant-sfogliatella-d6a167.netlify.app/main', {
//     method: 'POST',
//     headers: {
//         'Content-Type': 'application/json',
//     },
//     body: JSON.stringify({
//         data: paragraphContents,
//     }),
// })
//     .then(response => response.json())
//     .then(data => {
//         // 서버 응답 처리
//         console.log(data);
//         appendDataToContainer(data.result);  // 데이터를 컨테이너에 추가하는 함수 호출
//     })
//     .catch(error => {
//         // 에러 처리
//         console.error('Error:', error);
//     });

// function appendDataToContainer(data) {
//     var container = document.getElementById('dataContainer');
//     var paragraph = document.createElement('p');
//     paragraph.textContent = data;
//     container.appendChild(paragraph);
// }

// script.js

document.addEventListener('DOMContentLoaded', function() {
    // var paragraphContents = {data};
    // var test = document.getElementById('test');

    // var answer=document.createElement('p');
    // answer.context=data;
    // test.appendChild(paragraph);
  
    // paragraphContents.forEach(function(content) {
    //   var paragraph = document.createElement('p');
    //   paragraph.textContent = content;
    //   markdownDiv.appendChild(paragraph);
    // });

    var data=JSON.parse(document.getElementById('data').textContent);
    var dataContainer=document.getElementById('data-container');

    dataContainer.innerText=data;
  });
  