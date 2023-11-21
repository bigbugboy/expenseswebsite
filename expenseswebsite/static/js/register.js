const usernameField = document.getElementById('usernameField');
const usernameFeedbackArea = document.getElementById('usernameFeedbackArea');
const emailField = document.getElementById('emailField');
const emailFeedbackArea = document.getElementById('emailFeedbackArea');
const passwordField = document.getElementById('passwordField');
const pwdFeedbackArea = document.getElementById('pwdFeedbackArea');
const repasswordField = document.getElementById('repasswordField');
const repwdFeedbackArea = document.getElementById('repwdFeedbackArea');
const showPasswordToggles = document.getElementsByClassName('showPasswordToggle');


// 显示/隐藏密码
function handleToggleInput(e) {
    let show = '显示'
    let hide = '隐藏'
    let toggle = e.target
    let inputField = toggle.parentNode.children[1]
    if (toggle.textContent === show) {
        toggle.textContent = hide;
        inputField.setAttribute("type", "text");
    } else {
        toggle.textContent = show;
        inputField.setAttribute("type", "password");
    }
};

for (let index = 0; index < showPasswordToggles.length; index++) {
    showPasswordToggles[index].addEventListener("click", handleToggleInput);
}


// 确认密码校验
repasswordField.addEventListener('keyup', (e) => {
    const pwdValue = e.target.value;
    console.log(pwdValue)
    repasswordField.classList.remove("is-invalid")
    if (pwdValue.length > 0) {
        fetch("/authentication/validate-pwd", {
            body: JSON.stringify({ password: pwdValue }),
            method: "POST",
        }).then((res) => res.json()).then((data) => {
            if (data.password_error) {
                repasswordField.classList.add("is-invalid");
                repwdFeedbackArea.classList.add("invalid-feedback")
                repwdFeedbackArea.innerText = data.password_error;
            } else {
                repasswordField.classList.add("is-valid");
            }
        })
    }
})


// 密码校验
passwordField.addEventListener('keyup', (e) => {
    const pwdValue = e.target.value;
    console.log(pwdValue)
    passwordField.classList.remove("is-invalid")
    if (pwdValue.length > 0) {
        fetch("/authentication/validate-pwd", {
            body: JSON.stringify({ password: pwdValue }),
            method: "POST",
        }).then((res) => res.json()).then((data) => {
            if (data.password_error) {
                passwordField.classList.add("is-invalid");
                pwdFeedbackArea.classList.add("invalid-feedback")
                pwdFeedbackArea.innerText = data.password_error;
            } else {
                passwordField.classList.add("is-valid");
            }
        })
    }
})


// 邮箱校验
emailField.addEventListener('keyup', (e) => {
    const emailValue = e.target.value;
    console.log(emailValue)
    emailField.classList.remove("is-invalid")
    if (emailValue.length > 0) {
        fetch("/authentication/validate-email", {
            body: JSON.stringify({ email: emailValue }),
            method: "POST",
        }).then((res) => res.json()).then((data) => {
            if (data.email_error) {
                emailField.classList.add("is-invalid");
                emailFeedbackArea.classList.add("invalid-feedback")
                emailFeedbackArea.innerText = data.email_error;
            } else {
                emailField.classList.add("is-valid");
            }
        })
    }
})


// 用户名校验
usernameField.addEventListener('keyup', (e) => {
    const nameValue = e.target.value;
    usernameField.classList.remove("is-invalid")
    if (nameValue.length > 0) {
        fetch("/authentication/validate-username", {
            body: JSON.stringify({ username: nameValue }),
            method: "POST",
        }).then((res) => res.json()).then((data) => {
            if (data.username_error) {
                usernameField.classList.add("is-invalid");
                usernameFeedbackArea.classList.add("invalid-feedback")
                usernameFeedbackArea.innerText = data.username_error;
            } else {
                usernameField.classList.add("is-valid");
            }
        })
    }
})