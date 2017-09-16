$(function () {
    var $userName = $("#user_name");
    var $pwd = $("#pwd");
    var $cpwd = $("#cpwd");
    var $email = $("#email");
    var $allow = $("#allow");

    var is_error_username = true;
    var is_error_pwd = true;
    var is_error_cpwd = true;
    var is_error_email = true;
    var is_error_allow = false;

    // 数字字母或下划线6到20位
    var reg_name = /^\w{6,20}$/;
    var reg_psw = /^[\w!@#$%^&*]{6,20}$/;

    // 6~18个字符，可使用字母、数字、下划线，需以字母开头

    var reg_email = /^[A-Za-z0-9]\w{4,16}[A-Za-z0-9]@[a-z0-9]+(\.[a-z]{2,5}){1,2}$/i;


    //-----------------------------------------------------验证用户名
    $userName.blur(function () {
        //验证用户名
        checkUserName();
    });
    $userName.focus(function () {
        //获取焦点 隐藏提示
        $(this).next().hide();
    });

    //用户重名判断
    function checkIsName() {
        var username = $userName.val();
         $.ajax({
            url:'/user/has_user/',
            type:'get',
            dataType:'json',
            data:{'uname':username},
            success:function (data) {
                if (data.reg_name){
                    $('#user_name').next().html('用户名已存在！').show();
                    is_error_username = true;
                }
                else {
                    $('#user_name').next().hide();
                    is_error_username = false;
                }

            }
        })
    }

    //验证用户名
    function checkUserName() {
        // console.log("checkUserName");
        var username = $userName.val();
        if (username == "") {
            $userName.next().html("用户名不能为空").show();
            is_error_username = true;
            return;
        }
        if (reg_name.test(username)) {
            checkIsName();
        } else {
            $userName.next().html("用户名6到20位数字字母或下划线").show();
            is_error_username = true;
        }

    }
    //-----------------------------------------------------验证密码

    $pwd.focus(function () {
        $pwd.next().hide();
    });
    $pwd.blur(function () {
        checkPsw();
    });

    function checkPsw() {
        var psw = $pwd.val();
        if (psw == "") {
            $pwd.next().html("密码不能为空").show();
            is_error_pwd = true;
            return;
        }

        if (reg_psw.test(psw)) {
            is_error_pwd = false;
        } else {
            $pwd.next().html("密码是6到20位数字字母下划线和!@#$%^&*").show();
            is_error_pwd = true;
        }
    }
    //-----------------------------------------------------验证重复密码


    $cpwd.focus(function () {
        $cpwd.next().hide();
    });


    $cpwd.blur(function () {
        checkCPsw();
    });

    function checkCPsw() {
        var psw = $pwd.val();
        var cpwd = $cpwd.val();
        if (cpwd != psw) {
            $cpwd.next().html("两次密码不一致").show();
            is_error_cpwd = true;
        } else {
            is_error_cpwd = false;
        }
    }


    //-----------------------------------------------------验证邮箱

    $email.focus(function () {
        $email.next().hide();
    });
    $email.blur(function () {
        checkEmail();
    });


    function checkEmail() {
        var email = $email.val();
        if (email == "") {
            $email.next().html("邮箱不能为空").show();
            is_error_email = true;
            return;
        }
        if (reg_email.test(email)) {
            is_error_email = false

        } else {
            $email.next().html("邮箱格式错误").show();
            is_error_email = true;
        }
    }

    //-------------------------------checkbox验证

    $allow.click(function () {
        // var isChecked = $allow.prop("checked");
        var isChecked = $allow.is(":checked");
        if (isChecked) {
            $allow.siblings("span").hide();
            is_error_allow = false;
        } else {
            $allow.siblings("span").html("必须勾选").show();
            is_error_allow = true;
        }

    });

    // 表单的提交事件
    $("#myform").submit(function () {
        console.log("myform");
        checkUserName();
        checkPsw();
        checkCPsw();
        checkEmail();
//
        if (is_error_username || is_error_pwd || is_error_cpwd || is_error_email || is_error_allow) {
            //  有一个表单有错误 就不提交
            console.log("false");
            return false;
        } else {
            console.log("true");
            return true;
        }

    })


});