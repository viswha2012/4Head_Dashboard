$(document).ready(function () {
  $("#inputForm").submit(function (event) {
    event.preventDefault();
    var inputData = $("#textInput").val();
    $.ajax({
      type: "POST",
      url: "/submit_concern",
      contentType: "application/json",
      data: JSON.stringify({ input_data: inputData }),
      success: function (response) {
        $("#textInput").val("");
      },
      error: function (error) {
        console.error(error);
      },
    });
  });
});
