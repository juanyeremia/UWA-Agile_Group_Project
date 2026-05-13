// JavaScript for client-side validation on login and sign-up forms

function setError(elementId, message) {
    const errorElement = document.getElementById(elementId);
    if (errorElement) {
        errorElement.textContent = message;
    }
}
function clearError(elementId) {
    setError(elementId, '');
}

function isValidUsername(username) {
    const usernameRegex = /^[a-zA-Z0-9_]{3,80}$/;
    return usernameRegex.test(username);
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function isValidPassword(password) {
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$/;
    return passwordRegex.test(password);
}

// Validate login form
function validateLoginForm() {
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();
    let isValid = true;
    clearError('emailError');
    clearError('passwordError');

    // Validate email
    if (!email) {
        setError('emailError', 'Email is required.');
        isValid = false;
    } else if (!isValidEmail(email)) {
        setError('emailError', 'Please enter a valid email address.');
        isValid = false;
    }

    // Validate password
    if (!password) {
        setError('passwordError', 'Password is required.');
        isValid = false;
    }
    return isValid;
} 

function validateSignUpForm() {
    const username = document.getElementById('username').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();
    const confirmPassword = document.getElementById('confirm_password').value.trim();
    let isValid = true;
    
    clearError('usernameError');
    clearError('emailError');
    clearError('passwordError');
    clearError('confirmPasswordError');
    // Validate username
    if (!username) {
        setError('usernameError', 'Username is required.');
        isValid = false;
    } else if (username.length < 3 || username.length > 80) {
        setError('usernameError', 'Username must be at least 3 characters long.');
        isValid = false;
    } else if (!isValidUsername(username)) {
        setError('usernameError', 'Username can only contain letters, numbers, and underscores.');
        isValid = false;
    }

    // Validate email
    if (!email) {
        setError('emailError', 'Email is required.');
        isValid = false;
    } else if (!isValidEmail(email)) {   
        setError('emailError', 'Please enter a valid email address.');
        isValid = false;
    }

    // Validate password
    if (!password) {
        setError('passwordError', 'Password is required.');
        isValid = false;
    } else if (!isValidPassword(password)) {
        setError('passwordError', 'Password must be at least 6 characters long and include uppercase, lowercase, number, and special character.');
        isValid = false;
    }
    // Validate confirm password
    if (!confirmPassword) {
        setError('confirmPasswordError', 'Confirm Password is required.');
        isValid = false;
    } else if (password !== confirmPassword) {
        setError('confirmPasswordError', 'Passwords do not match.');
        isValid = false;
    }
    return isValid;
}

const usernameInput = document.getElementById('username');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const confirmPasswordInput = document.getElementById('confirm_password');

if (usernameInput) {
    usernameInput.addEventListener('blur', function() {
        const username = usernameInput.value.trim();
        if (!username) {
            setError('usernameError', 'Username is required.');
        } else if (username.length < 3 || username.length > 80) {
            setError('usernameError', 'Username must be at least 3 characters long.');
        } else if (!isValidUsername(username)) {
            setError('usernameError', 'Username can only contain letters, numbers, and underscores.');
        } else {
            clearError('usernameError');
        }
    });
}

if (emailInput) {
    emailInput.addEventListener('blur', function() {
        const email = emailInput.value.trim();
        if (!email) {
            setError('emailError', 'Email is required.');
        } else if (!isValidEmail(email)) {
            setError('emailError', 'Please enter a valid email address.');
        } else {
            clearError('emailError');
        }
    });
}

if (passwordInput) {
    passwordInput.addEventListener('blur', function() {
        const password = passwordInput.value.trim();
        if (!password) {
            setError('passwordError', 'Password is required.');
        } else if (!isValidPassword(password)) {
            setError('passwordError', 'Password must be at least 6 characters long and include uppercase, lowercase, number, and special character.');
        } else {
            clearError('passwordError');
        }  
    });
}

if (confirmPasswordInput) {
    confirmPasswordInput.addEventListener('blur', function() {
        const password = passwordInput.value.trim();
        const confirmPassword = confirmPasswordInput.value.trim();
        if (!confirmPassword) {
            setError('confirmPasswordError', 'Confirm Password is required.');
        } else if (password !== confirmPassword) {
            setError('confirmPasswordError', 'Passwords do not match.');
        } else {
            clearError('confirmPasswordError');
        }
    });
}


const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', function(event) { 
        if (!validateLoginForm()) {
            event.preventDefault(); 
        }
    });
}

const signUpForm = document.getElementById('signUpForm');
if (signUpForm) {
    signUpForm.addEventListener('submit', function(event) {
        if (!validateSignUpForm()) {
            event.preventDefault(); 
        }
    });
}

const togglePasswordBtn = document.getElementById('toggle-password');

if (togglePasswordBtn && passwordInput) {
    const showPassword = function(event) {
        event.preventDefault();
        passwordInput.type = 'text';
    };
    const hidePassword = function(event) {
        event.preventDefault();
        passwordInput.type = 'password';
    };

    togglePasswordBtn.addEventListener('mousedown', showPassword);
    togglePasswordBtn.addEventListener('mouseup', hidePassword);
    togglePasswordBtn.addEventListener('mouseleave', hidePassword);
}
