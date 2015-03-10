

$.getJSON("questions/random/", function(data){
    var source   = $("#entry-template").html();
    var template = Handlebars.compile(source);
    var html     = template(data);
    
    $('body').append(html);
});