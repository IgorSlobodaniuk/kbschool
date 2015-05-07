var myArray = [];
var MyjQuery123 = jQuery.noConflict();
MyjQuery123.getJSON('/static/json/subjects_list.json', function(json) {
    myArray=json;


MyjQuery123( "#id_subject_field" ).autocomplete({
source: myArray,
});
});
