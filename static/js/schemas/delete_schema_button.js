const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

jQuery(document).ready(function() {
        jQuery(document).on('click', "#delete_schema_button", function () {
         if (confirm("Are you sure you want to delete this schema?")) {
             jQuery.ajax({
                 headers: {"X-CSRFToken": csrftoken},
                 url: this.href,
                 type: "POST",

             });
         }
        });

 })

