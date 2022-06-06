let birdForm = document.querySelectorAll(".data_type_form")
let container = document.querySelector("#form-container")
let addButton = document.querySelector("#add-form")
let form_data_types = document.getElementById("form-container")
let formNum = birdForm.length-1
let json_obj = get_json()
showHiddenFieldsWhileEdit()
addButton.addEventListener('click', addForm)

form_data_types.onchange = function(event) {
    let target = event.target;
    if (target.nodeName != 'SELECT') {
        return;
    }
    showHiddenObject(target);
}

form_data_types.onclick = function(event) {
    let target = event.target;
    if (target.id == 'delete_column') {
        deleteForm(target);
    }
}

function addForm(e){
    e.preventDefault();
    let newForm = birdForm[0].cloneNode(true);
    let formRegex = RegExp(`form-(\\d){1}-`,'g');
    formNum++;
    newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formNum}-`).replace('d-block', 'd-none');
    container.insertBefore(newForm, addButton);
}

function deleteForm(target){
    let delete_object = target.closest('.data_type_form');
    delete_object.remove();
}

function showHiddenObject(target) {
    let hidden = target.closest(".row").getElementsByClassName('hidden_object')[0];
    let key = target.value;
    if (json_obj[key] == true){
        hidden.classList.remove('d-none');
        hidden.classList.add('d-block');
    } else {
        hidden.classList.remove('d-block');
        hidden.classList.add('d-none');
    }
}

function get_json() {
    var dict_element = document.getElementById('items_have_range');
    var dict_content = dict_element.textContent;
    return JSON.parse(dict_content);
}
function showHiddenFieldsWhileEdit() {
    let hidden_objects = document.getElementsByClassName('hidden_object');
    for (obj of hidden_objects) {
        let selector = obj.closest(".row").getElementsByClassName('form-select')[0];
        if (json_obj[selector.value]) {
            obj.classList.remove('d-none');
            obj.classList.add('d-block');
        } else {
            obj.classList.remove('d-block');
            obj.classList.add('d-none');
        }
    }
}