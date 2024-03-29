const demoButton = document.getElementById('demo-button');
const usernameField = document.getElementById('id_username');
const passwordField= document.getElementById('id_password');
const loginButton = document.getElementById('login-button');

demoButton.addEventListener('click', () => {
    usernameField.value = 'demo_user';
    passwordField.value = 'demo_pass';
    loginButton.click();
})