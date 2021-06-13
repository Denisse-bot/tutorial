$(function() {
    let nameState = false
    let emailState = false
    let venueState = false
    let phoneState = false
    let bodyState = false
    let formState = false

    // function checkInputs(){
    //     if (nameState && emailState && venueState && phoneState && bodyState) {
    //         formState = true
    //         $("#submit").addClass("active")
    //     } else {
    //         formState = false
    //         $("#submit").removeClass("active")
    //     }
    // }

    function validateEmail(email){
        var reg = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
        return reg.test(email);
    }

    function validatePhone(phone){
        var mobile_regex = /^((\+?\s?56\s?)?(9)(\s?)[4-9]\d{7})$/;
        return reg.test(phone)
    }

    function adjustForm(){
        $("form").submit(function(e){
            if (!formState) {
                e.preventDefault()
            }
        })

        $("#nombre").keyup(function(){
            if ($(this).val().length > 2) {
                nameState = true
                $("#nombre").addClass("ok")
                $("#nombre").removeClass("error")
            } else if ($(this).val() == "") {
                nameState = false
                $("#nombre").addClass("error")
                $("#nombre").removeClass("ok")
            } else {
                $("#nombre").removeClass("ok")
            }

        })

        $("#email").keyup(function(){
            if ($(this).val().length > 0) {
                if (validateEmail($(this).val())){
                    emailState = true
                    $("#email-field").addClass("ok")
                    $("#email-field").removeClass("error")
                } else {
                    emailState = false
                    $("#email-field").addClass("error")
                    $("#email-field").removeClass("ok")
                }
            } else {
                $("#email-field").removeClass("ok")
            }

        })

        $("#phone").keyup(function(){
            if ($(this).val().length > 6) {
                if (validatePhone($(this).val())){
                    phoneState = true
                    $("#phone-field").addClass("ok")
                    $("#phone-field").removeClass("error")
                } else {
                    phoneState = false
                    $("#phone-field").addClass("error")
                    $("#phone-field").removeClass("ok")
                }
            } else {
                $("#phone-field").removeClass("ok")
            }

        })

        // $("#body").keyup(function(){
        //     if ($(this).val().length > 5) {
        //         bodyState = true
        //         $("#body-field").addClass("ok")
        //         $("#body-field").removeClass("error")
        //     } else if ($(this).val() == "") {
        //         bodyState = false
        //         $("#body-field").addClass("error")
        //         $("#body-field").removeClass("ok")
        //     } else {
        //         $("#body-field").removeClass("ok")
        //     }

        //     checkInputs()
        // })
    }

    
    function init(){
        adjustForm()

    }

    init()
})