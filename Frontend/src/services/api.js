const API_BASE_URL = 'http://127.0.0.1:8000/api';

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
        
        if (!response.ok) throw new Error('Failed to toggle bookmark');
        return await response.json();
    } catch (error) {
        console.error("Failed to toggle bookmark:", error);
        return { status: 'error' };
    }
};
