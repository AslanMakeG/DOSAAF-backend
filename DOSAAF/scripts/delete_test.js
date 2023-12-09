function delete_test(button){
    let test = button.parentNode.parentNode;
    let test_id = test.dataset.id;

    let status = delete_test_on_server(test_id, test);
}

function delete_test_on_server(id, element){
    fetch('http://127.0.0.1:8000/api/delete_test/' + id, {
        headers: {
            'Accept': 'application/json'
        }
    })
    .then(response => {
        if(response['status'] == 200){
            element.parentNode.removeChild(element);
        }
    });
}