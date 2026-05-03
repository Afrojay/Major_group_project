async function checkAuth() {
    try {
        const response = await fetch('/api/auth/status');
        const data = await response.json();
        
        const authNav = document.getElementById('authNav');
        if (!authNav) return;
        
        if (data.authenticated) {
            authNav.innerHTML = `
                <span style="color: white;">Welcome, ${data.username}</span>
                ${data.role === 'admin' ? '<a href="admin.html" class="btn btn-small">Admin Panel</a>' : ''}
                <button onclick="logout()" class="btn btn-small">Logout</button>
            `;
        } else {
            authNav.innerHTML = `
                <a href="login.html" class="btn btn-small">Login</a>
                <a href="signup.html" class="btn btn-small">Sign Up</a>
            `;
        }
    } catch (error) {
        console.error('Auth check failed:', error);
    }
}

async function logout() {
    try {
        const response = await fetch('/api/logout', {
            method: 'POST'
        });
        
        if (response.ok) {
            window.location.href = 'index.html';
        }
    } catch (error) {
        alert('Logout failed');
    }
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', checkAuth);
} else {
    checkAuth();
}
