let tests = document.getElementById('tests');

function load_from_json(json){
   json['tests'].forEach(element => {
      tests.innerHTML += `<div class="test" data-id="${element['id']}">
                              <p class="test-name">${element['name']}</p>
                              <div class="buttons">
                                 <p class="solve-test">Пройти тест</p>
                                 <p class="delete-test" onclick="delete_test(this)">Удалить тест</p>
                              </div>
                        </div>`
   });
}

fetch('http://127.0.0.1:8000/api/get_tests', {
   headers: {
      'Accept': 'application/json'
   }
})
.then(response => response.json())
.then(text => load_from_json(text));