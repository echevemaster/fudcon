$(document).ready(function(){
    $('.delete').click(function(){
        var answer = confirm("¿Está seguro de querer borrar este item?");
        if (answer){
            return true;
        } else {
            return false;
        }
    });
});

