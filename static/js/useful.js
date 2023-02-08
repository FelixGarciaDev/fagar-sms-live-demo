
//inicializa el modal
document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.modal');
    var instances = M.Modal.init(elems);
  });

  //inicializa el modal con jquery
  $(document).ready(function(){
    $('.modal').modal();
  });

  //inicializa el modal con jqury y ademas agrega al .modal-content la url de create o update para django
  $( document ).ready(function() {
    $('.modal').modal();
    $('.modal-content').load("{% url 'books:create' %}");
  });


      