$(document).ready(function () {
    $("#register").click(function () {
        var name = $("#name").val();
        var password_ = $("#password").val();
        if (name == '' || password_ == '') {
            alert("Please fill all fields...!!!!!!");
        } else if ((password.length) < 3) {
            alert("Password should atleast 3 character in length...!!!!!!");
        } else {
            $.post("0.0.0.0:5050/api/registration", {
                username: name,
                password: password_
            }, function (data) {
                if (data == 'You have Successfully Registered.....') {
                    $("form")[0].reset();
                }
                alert(data);
            });
        }
    });
});