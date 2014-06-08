function action_params(){
    selectBox = document.getElementById("wordlist");
    for (var i = 0; i < selectBox.options.length; i++) 
        { 
             selectBox.options[i].selected = true; 
        } 
    };

/*
 * jQuery functions
 */

$(document).ready(function() {
    /*
     * HTML related jQuery functions
     */

    ////////////////
    // During Use //
    ////////////////

    // General functions for all webpages
    $(".nav ul li").hover(function() {
        $(this).find('a').css('color', 'yellow');
        $(this).addClass("hovered_link");
    },
        function() {
            $(this).find('a').css('color', 'white');
            $(this).removeClass("hovered_link");
    });

    // index.html
    $(".puzzle_btn").mousedown(function(event) {
        /* Act on the event */
        $( this ).css("box-shadow", "inset 2px 2px 3px 0 #000000");
    });
    $("puzzle_btn").mouseup(function(event) {
        $( this ).css("box-shadow", "");
    });

    //wordsearch
    $("#wordlist").dblclick(function(event) {
        /* Act on the event */
        var value = window.prompt("Please enter one or multiple words (separated by comma with no space. E.g. word,search,awesome");
        //hello,world
        var list = value.split(",");
        for (var i = 0; i < list.length; i++) {
            var word = document.createElement("option");
            var text = document.createTextNode(list[i]);
            word.appendChild(text);
            $(word).appendTo(this);
        }
    });

    // Remove options from list
    $('html').keyup(function(e){
        if(e.keyCode == 46){
            $('#wordlist option:selected').each(function(){
                $(this).remove();
            });
        }
    });
});