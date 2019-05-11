$(document).ready(function() {
    validate();
});

/*$.validator.addMethod(
        "regex",
        function(value, element, regexp) {
            var re = new RegExp(regexp);
            return this.optional(element) || re.test(value);
        },
        "Please check your input."
);

$("#pass").rules("add", { regex: "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$" });*/

function validate() {
    $('#reg-form').validate({
    rules: {
        username: {
            required: true,
            minlength: 8
        },
        pass: {
            required: true,
            minlength: 8
        },
        repass: {
            required: true,
            equalTo: "#pass"
        },
        email: {
            required: true,
            email: true
        }
    },
    messages: {
        username: {
            required: "Username cannot be blank",
            minlength: "It should br greater than 8 characters"
        },
        pass: {
            required: "Password cannot be blank",
            minlength: "It should br greater than 8 characters"
        },
        repass: {
            required: "Re-Enter your password",
            equalTo: "Password do not match"
        },
        email: {
            required: "Email cannot be empty",
            email: "Please enter valid email address"
        }
    },
    submitHandler: function(form) {
        form.submit();
    }
});

$('#login-form').validate({
    rules: {
        user: {
            required: true,
            minlength: 8
        },
        password: {
            required: true,
            minlength: 8
        }
    },
    messages: {
        user: {
            required: "Username cannot be blank",
            minlength: "It should br greater than 8 characters"
        },
        password: {
            required: "Password cannot be blank",
            minlength: "It should br greater than 8 characters"
        }
    },
    submitHandler: function(form) {
        form.submit();
    }
});
}