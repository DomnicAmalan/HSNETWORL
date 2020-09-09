
$("#updateModal").modal({
  show: false
});

$(".update_user_button").click(function () {
  var userId = +$(this).val();
  $.get('${pageContext.request.contextPath}/ajax/' + userId, function (user) {
      $("#updateModal #id").val(user.id);
      $("#updateModal #name").val(user.name);
      $("#updateModal #username").val(user.username);
      $("#updateModal #email").val(user.email);
      $("#updateModal #authority").val(user.authority);
  });
  $("#updateModal").modal('show');
  $("#alert").hide();
  $("#error_name").hide();
});