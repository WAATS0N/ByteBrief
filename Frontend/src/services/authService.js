import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api/auth/';

// Configure axios to always send the JWT token if it exists
axios.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

export const authService = {
    // Login with email and password
    login: async (email, password) => {
        try {
            const response = await axios.post(`${API_URL}login/`, { email, password });
            if (response.data && response.data.access) {
                localStorage.setItem('access_token', response.data.access);
                localStorage.setItem('refresh_token', response.data.refresh);
                localStorage.setItem('user', JSON.stringify(response.data.user));
            }
            return response.data;
        } catch (error) {
            throw error.response?.data || { error: 'Login failed' };
        }
    },

    // Register a new user
    register: async (email, password, fullName) => {
        try {
            // dj-rest-auth registration endpoint requires password1, password2, and username
            const response = await axios.post(`${API_URL}registration/`, {
                email,
                password1: password,
                password2: password,
                username: email.split('@')[0] + Math.floor(Math.random() * 10000), // Generate a unique basic username
                first_name: fullName.split(' ')[0],
                last_name: fullName.split(' ').slice(1).join(' '),
            });

            if (response.data && response.data.access) {
                localStorage.setItem('access_token', response.data.access);
                localStorage.setItem('refresh_token', response.data.refresh);
                localStorage.setItem('user', JSON.stringify(response.data.user));
            }
            return response.data;
        } catch (error) {
            throw error.response?.data || { error: 'Registration failed' };
        }
    },

    // Google OAuth Login
    googleLogin: async (accessToken) => {
        try {
            const response = await axios.post(`${API_URL}google/`, { access_token: accessToken });
            if (response.data && response.data.access) {
                localStorage.setItem('access_token', response.data.access);
                localStorage.setItem('refresh_token', response.data.refresh);
                localStorage.setItem('user', JSON.stringify(response.data.user));
            }
            return response.data;
        } catch (error) {
            throw error.response?.data || { error: 'Google login failed' };
        }
    },

    // Reset password
    resetPassword: async (email) => {
        try {
            const response = await axios.post(`${API_URL}password/reset/`, { email });
            return response.data;
        } catch (error) {
            throw error.response?.data || { error: 'Password reset request failed' };
        }
    },

    // Logout
    logout: () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
    },

    // Check auth status
    isAuthenticated: () => {
        return !!localStorage.getItem('access_token');
    },

    // Get current user details
    getCurrentUser: () => {
        const userStr = localStorage.getItem('user');
        return userStr ? JSON.parse(userStr) : null;
    },

    // Get full profile from backend
    getProfile: async () => {
        try {
            const response = await axios.get('http://127.0.0.1:8000/api/user/profile/');
            return response.data;
        } catch (error) {
            throw error.response?.data || { error: 'Failed to fetch profile' };
        }
    },

    // Update profile (first_name, last_name)
    updateProfile: async (data) => {
        try {
            const response = await axios.patch('http://127.0.0.1:8000/api/user/profile/', data);
            // Update local storage with new user info
            const currentUser = JSON.parse(localStorage.getItem('user') || '{}');
            const updatedUser = { ...currentUser, ...response.data };
            localStorage.setItem('user', JSON.stringify(updatedUser));
            return response.data;
        } catch (error) {
            throw error.response?.data || { error: 'Failed to update profile' };
        }
    },

    // Change password
    changePassword: async (oldPassword, newPassword1, newPassword2) => {
        try {
            const response = await axios.post(`${API_URL}password/change/`, {
                old_password: oldPassword,
                new_password1: newPassword1,
                new_password2: newPassword2,
            });
            return response.data;
        } catch (error) {
            throw error.response?.data || { error: 'Password change failed' };
        }
    },

    // Delete account (requires password confirmation)
    deleteAccount: async (password) => {
        try {
            const response = await axios.post('http://127.0.0.1:8000/api/user/delete-account/', { password });
            return response.data;
        } catch (error) {
            throw error.response?.data || { error: 'Account deletion failed' };
        }
    },
};
