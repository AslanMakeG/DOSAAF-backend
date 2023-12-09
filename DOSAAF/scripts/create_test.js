let questions = document.getElementById('test-questions');
let question_counter = 0;

//Создание вопроса
function create_question(){
    let question_name = document.getElementById('question-name');
    let question_type = document.getElementById('question-type');

    //Создание элементов с названием вопроса и типом (один, много ответов или текст)
    let new_question = document.createElement('div');
    new_question.innerHTML = 
    `<div class="question-top">
        <p class="question-top-title">Название вопроса:</p>
        <input class="question-top-input" type="text" name="question-name" placeholder="Введите название вопроса" value="${question_name.value}">                   
    </div>`; //Добавляем элементы для записи названия вопроса

    new_question.classList.add('question'); //Добавляем класс элементу
    new_question.dataset.type = question_type.value; //Добавляем тип вопроса элементу

    question_content = content_by_type(question_type.value); //Добавляем содержимое в зависимости от типа

    new_question.innerHTML += question_content;
    questions.appendChild(new_question); //Добавляем вопрос на страницу

    close_modal_window(); //Закрываем модальное окно и сбрасываем значения в нём
    question_name.value = '';
    question_type.value = 'one';
}

//Добавить вариант ответа к вопросу
function add_question_answer(type, button){
    let last_answer = button.previousElementSibling;
    let value = parseInt(last_answer.children[0].value) + 1;

    let new_answer = document.createElement('div');
    new_answer.classList.add('answer');

    //Добавлять варианты ответа можно только к одному или множественному ответу
    if(type === 'one'){
        let name = last_answer.children[0].name;

        new_answer.innerHTML = `<input type="radio" name="${name}" value="${value}" />
        <input class="radio-question-text" type="text" placeholder="Введите вариант ответа" />`;
    }

    if(type === 'multiple'){
        let name = last_answer.children[0].name.split('_')[0];

        new_answer.innerHTML = `<input class="checkbox-question" type="checkbox" name="${name}_${value}" value="${value}" />
        <input class="checkbox-question-text" type="text" placeholder="Введите вариант ответа" />`;
    }

    //Вставить новый вариант ответа перед кнопкой "Добавить вариант ответа"
    button.parentNode.insertBefore(new_answer, button);
}

//Содержимое блока по типу вопроса
function content_by_type(type){
    //Если один ответ, то будет два варианта ответа с радиобатонами
    if(type === 'one'){
        return `<div class="question-body">
            <div class="answer">
                <input type="radio" name="answ${question_counter}" value="1" checked />
                <input class="radio-question-text" type="text" placeholder="Введите вариант ответа" />
            </div>
            <div class="answer">
                <input type="radio" name="answ${question_counter++}" value="2" />
                <input class="radio-question-text" type="text" placeholder="Введите вариант ответа" />
            </div>
            <p class="text-button" onclick="add_question_answer('${type}', this)">Добавить вариант ответа</p>
        </div>`;
    }
    //Если множественный ответ, то будет два варианта ответа с чекбоксами
    if(type === 'multiple'){
        return `<div class="question-body">
            <div class="answer">
                <input class="checkbox-question" type="checkbox" name="answ${question_counter}_1" value="1" />
                <input class="checkbox-question-text" type="text" placeholder="Введите вариант ответа" />
            </div>
            <div class="answer">
                <input class="checkbox-question" type="checkbox" name="answ${question_counter++}_2" value="2" />
                <input class="checkbox-question-text" type="text" placeholder="Введите вариант ответа" />
            </div>
            <p class="text-button" onclick="add_question_answer('${type}', this)">Добавить вариант ответа</p>
        </div>`;
    }
    //Если ответ текстом, то будет поле для ввода верного ответа
    if(type === 'text'){
        return `<div class="question-body">
            <div class="answer">
                <input class="text-question-text" type="text" name="answ${question_counter++}" placeholder="Введите правильный ответ"/>
            </div>
        </div>`;
    }
}

//Вывод ошибки при создании теста
function raise_creation_error(error){
    document.getElementById('create-test-error').textContent = error;
    setTimeout(() => {document.getElementById('create-test-error').textContent = '';}, 5000);
    return;
}


//Создать тест (json)
function create_test(){
    try{
        let test_name = document.getElementById('test-name-input').value;
        
        //Проверка на пустоту имени теста
        if(!test_name){
            throw new Error('Заполните название вопроса');
        }

        let test_json = {
            'name' : test_name,
            'questions' : []
        };

        let questions = document.getElementsByClassName('question');
        //Проверка на отсутствие вопросов в тесте
        if(questions.length == 0){
            throw new Error('Создайте хотя бы один вопрос');
        }

        Array.from(questions).forEach((question) => {
            let name = question.children[0].children[1].value; //Получаем имя вопроса
            let question_type = question.dataset.type; //Получаем тип вопроса

            let question_json = {
                'name': name,
                'type': question_type,
                'answers': [],
                'right_answer': []
            }

            //Проверка на пустоту имени вопроса
            if(!name){
                throw new Error('Заполните все названия вопросов');
            }

            let answers = question.children[1].getElementsByClassName('answer');
            let current_answer = 0; //Номер текущего ответа в вопросе, чтобы записать правильные ответы

            //Если множественный выбор, то проверяем, чтобы хотя бы один чекбокс был выделен 
            if(question_type === 'multiple'){
                let inputs = question.children[1].querySelectorAll('input[type=checkbox]');
                let check = false; //Проверка, что хотя бы один чекбокс будет нажат

                for(let i = 0; i < inputs.length; i++){
                    if(inputs[i].checked){
                        check = true;
                        break; //Выходим с цикла, если хотя бы один чекбокс выделен
                    }
                }

                //Если ни один чекбокс не выделен
                if(!check){
                    throw new Error('В вопросах с множественным выбором выберите хотя бы один вариант ответа');
                }
            }

            Array.from(answers).forEach((answer) => {
                let answer_name = answer.lastElementChild.value;
                
                //Проверка на пустоту имени вопроса
                if(!answer_name){
                    throw new Error('Заполните все варианты ответов');
                }

                //Если один или множественный выбор, то записываем ответы в массив ответов
                if(question_type === 'one' || question_type === 'multiple'){
                    question_json['answers'].push(answer_name);
                    
                    //Если этот вопрос оказался правильным, записываем в массив правильных ответов
                    if(answer.firstElementChild.checked){
                        question_json['right_answer'].push(current_answer);
                    }
                }

                //Если ответ текстом, то записываем его сразу в массив правильных ответов
                if(question_type === 'text'){
                    question_json['right_answer'].push(answer_name.toLowerCase());
                }

                current_answer++;
            });

            test_json['questions'].push(question_json); //Записываем вопрос в массив вопросов
        });

        post_test_on_server(test_json);
    }
    catch(e){
        raise_creation_error(e.message);
    }
}

function post_test_on_server(test){
    fetch("http://127.0.0.1:8000/api/create_test", {
        method: "POST",
        body: JSON.stringify(test),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    })
    .then((response) => {
        if(response['status'] == 200){
            window.location.replace('list_of_tests.html');
        }
    });
}