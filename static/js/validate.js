$(document).ready(function() {
    validate();
});

function validate() {
    $('#reg-form').validate({
    rules: {
        oldpass: {
            required: true,
            minlength: 8
        },
        newpass: {
            required: true,
            minlength: 8
        },
        repass: {
            required: true,
            equalTo: "#newpass"
        }
    },
    messages: {
        oldpass: {
            required: "Username cannot be blank",
            minlength: "It should br greater than 8 characters"
        },
        newpass: {
            required: "Password cannot be blank",
            minlength: "It should br greater than 8 characters"
        },
        repass: {
            required: "Re-Enter your password",
            equalTo: "Password do not match"
        }
    },
    submitHandler: function(form) {
        form.submit();
    }
});

$('#login-form').validate({
    rules: {
        olduser: {
            required: true,
            minlength: 8
        },
        newuser: {
            required: true,
            minlength: 8
        }
    },
    messages: {
        olduser: {
            required: "Username cannot be blank",
            minlength: "It should br greater than 8 characters"
        },
        newuser: {
            required: "Username cannot be blank",
            minlength: "It should br greater than 8 characters"
        }
    },
    submitHandler: function(form) {
        form.submit();
    }
});
}