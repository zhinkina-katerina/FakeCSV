const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
let element_types = ["input", 'select'];

jQuery(document).ready(function() {
    jQuery(document).on( 'click', "#submit", function(e) {
        e.preventDefault();
        if (validateForm() == false) {
            return;
        }
        let json_object = get_json_object()

        jQuery.ajax({
            headers: {
                "X-CSRFToken": csrftoken
            },
            type: "POST",
            url: this.href,
            dataType: "json",
            data: {
                'json_object':JSON.stringify(json_object)
            },
            success: window.location="/"
        });
    });
});

function get_json_object() {
    let json_object = {};
    let form_schema = document.getElementById('form-schema');
    json_object['schema'] = get_values(form_schema);
    json_object['schema_columns'] = [];
    let form_container = document.getElementById('form-container').querySelectorAll('.row');
    for (row of form_container) {
        json_object['schema_columns'].push(get_values(row));
    }
    return json_object;

}

function get_values(element) {
    let dict = {};
    for (element_type of element_types) {
        let find_element = element.querySelectorAll(element_type);
        for (element_form of find_element) {
            let name = element_form.getAttribute("name");
            let val = element_form.value;
            dict[name]=val;
        }
    }
    return dict;
}

function validateForm() {
    let titles = document.querySelectorAll('[name="title"]');
    for (title of titles) {
        if (!title.value) {
            alert("All fields must be filled out");
            return false;
        }
    }
}