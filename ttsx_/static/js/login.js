/**
 * Created by python on 17-9-11.
 */
$(function () {
    var is_error_name = true;
    var is_error_password = true;

    var reg_username = /^\w{6,20}$/;
    var reg_pwd = /^[\w!@#$%^&*]{6,20}$/;

    var $name_input = $('#n_input');
    var $pass_input = $('#p_input');

    //判断用户名是否正确
    $name_input.focus(function () {
        $(this).next().hide();
    });

    $name_input.blur(function () {
       check_username();
    });

    //判断密码是否正确

     $pass_input.focus(function () {
        $(this).next().hide();
    });

    $pass_input.blur(function () {
        check_pwd();
    });

    //判断用户是否存在
    function checkIsName() {
        var username = $name_input.val();
        $.ajax({
            url:'/user/has_user/',
            type:'get',
            dataType:'json',
            data:{'uname':username},
            success:function (data) {
                if (data.reg_name){
                    $('#n_input').next().hide();
                    is_error_name = false;
                }
                else {
                    $('#n_input').next().html('不存在的用户名,请先前往注册页面注册！').show();

                    is_error_name = true;
                }

            }
        })
    }

    function check_username() {
        var uname = $name_input.val();
        var check = reg_username.test(uname);
        if(uname == ''){
            $name_input.next().html('用户名不能为空').show();
            is_error_name = true;
            return;
        }

        if (check){
            // $name_input.next().hide();
            checkIsName();
        }else {
            $name_input.next().html('请输入6-20个字符的用户名!').show();
            is_error_name = true;
        }
    }

    function check_pwd() {
        var upwd = $pass_input.val();
        var check = reg_pwd.test(upwd);
        if (upwd == ""){
            $pass_input.next().html('密码不能为空!').show();
            is_error_password = true;
            return
        }


        if (check){
            $pass_input.next().hide();
            is_error_password = false;
            // checkIsPwd();
        } else {
            $pass_input.next().html("密码是6到20位数字字母下划线和!@#$%^&*").show();
            is_error_password = true;
        }
    }

    //登录

    $('#myform').submit(function () {
        check_pwd();
        check_username();

        if(is_error_password || is_error_name){
            return false;
        } else {
            return true;
        }
    });

});