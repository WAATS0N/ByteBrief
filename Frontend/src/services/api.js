let rawUrl = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000/api';
rawUrl = rawUrl.replace(/\/+$/, ''); // Remove trailing slashes
if (!rawUrl.endsWith('/api')) {
    rawUrl += '/api';
}
export const API_BASE_URL = rawUrl;

export const generateDigest = async (keywords = [], categories = [], sources = []) => {
    try {
        const response = await fetch(`${API_BASE_URL}/generate-digest/`, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                keywords,
                categories,
                sources
            }),
        });

        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Failed to fetch digest:", error);
        throw error;
    }
};

export const fetchMetadata = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/metadata/`);
        if (!response.ok) throw new Error('Failed to fetch metadata');
        return await response.json();
    } catch (error) {
        console.error("Failed to fetch metadata:", error);
        return null;
    }
};

export const fetchPreferences = async (token) => {
    try {
        const headers = { 'Content-Type': 'application/json' };
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const response = await fetch(`${API_BASE_URL}/user/preferences/`, { headers });
        if (response.status === 401) {
            localStorage.removeItem('access_token');
            localStorage.removeItem('user');
            window.location.href = '/login';
            throw new Error('Session expired');
        }
        if (!response.ok) throw new Error('Failed to fetch preferences');
        return await response.json();
    } catch (error) {
        console.error("Failed to fetch preferences:", error);
        return null;
    }
};

export const savePreferences = async (token, categories) => {
    try {
        const headers = { 'Content-Type': 'application/json' };
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const response = await fetch(`${API_BASE_URL}/user/preferences/`, {
            method: 'POST',
            headers,
            body: JSON.stringify({ categories })
        });
        if (response.status === 401) {
            localStorage.removeItem('access_token');
            localStorage.removeItem('user');
            window.location.href = '/login';
            throw new Error('Session expired');
        }
        if (!response.ok) throw new Error('Failed to save preferences');
        return await response.json();
    } catch (error) {
        console.error("Failed to save preferences:", error);
        return null;
    }
};

export const fetchBookmarks = async (token) => {
    try {
        const headers = { 'Content-Type': 'application/json' };
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const response = await fetch(`${API_BASE_URL}/user/bookmarks/`, { headers });
        if (response.status === 401) {
            localStorage.removeItem('access_token');
            localStorage.removeItem('user');
            window.location.href = '/login';
            throw new Error('Session expired');
        }
        if (!response.ok) throw new Error('Failed to fetch bookmarks');
        return await response.json();
    } catch (error) {
        console.error("Failed to fetch bookmarks:", error);
        return { status: 'error', bookmarks: [] };
    }
};

export const toggleBookmark = async (token, articleUrl, isBookmarked) => {
    try {
        const headers = { 'Content-Type': 'application/json' };
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const method = isBookmarked ? 'DELETE' : 'POST';
        const response = await fetch(`${API_BASE_URL}/user/bookmarks/`, {
            method,
            headers,
            body: JSON.stringify({ article_url: articleUrl })
        });

        if (response.status === 401) {
            localStorage.removeItem('access_token');
            localStorage.removeItem('user');
            window.location.href = '/login';
            throw new Error('Session expired');
        }
        if (!response.ok) throw new Error('Failed to toggle bookmark');
        return await response.json();
    } catch (error) {
        console.error("Failed to toggle bookmark:", error);
        return { status: 'error' };
    }
};

export const fetchUserSettings = async (token) => {
    try {
        const response = await fetch(`${API_BASE_URL}/user/settings/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) throw new Error('Fetch settings failed');
        return await response.json();
    } catch (e) { return null; }
};

export const updateUserSettings = async (token, settings) => {
    try {
        const response = await fetch(`${API_BASE_URL}/user/settings/`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
            body: JSON.stringify(settings)
        });
        if (!response.ok) throw new Error('Update settings failed');
        return await response.json();
    } catch (e) { return null; }
};

export const fetchReadingHistory = async (token) => {
    try {
        const response = await fetch(`${API_BASE_URL}/user/history/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) throw new Error('Fetch history failed');
        return await response.json();
    } catch (e) { return []; }
};

export const recordReadingHistory = async (token, articleId) => {
    try {
        const response = await fetch(`${API_BASE_URL}/user/history/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ article_id: articleId })
        });
        if (!response.ok) throw new Error('Record history failed');
        return await response.json();
    } catch (e) { return { status: 'error' }; }
};

export const fetchNotifications = async (token) => {
    try {
        const response = await fetch(`${API_BASE_URL}/user/notifications/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) throw new Error('Fetch notifications failed');
        return await response.json();
    } catch (e) { return []; }
};

export const markNotificationRead = async (token, notificationId) => {
    try {
        const response = await fetch(`${API_BASE_URL}/user/notifications/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ notification_id: notificationId })
        });
        return await response.json();
    } catch (e) { return { status: 'error' }; }
};

export const submitSupportTicket = async (token, subject, message, type = 'General') => {
    try {
        const response = await fetch(`${API_BASE_URL}/support/ticket/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
            body: JSON.stringify({ subject, message, type })
        });
        if (!response.ok) throw new Error('Submit ticket failed');
        return await response.json();
    } catch (e) { return { status: 'error' }; }
};
