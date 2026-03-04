// src/data/mockAnalytics.js
export const categoryViewsData = [
    { name: 'Business', views: 4200, color: '#3b82f6' }, // blue-500
    { name: 'Tech', views: 3800, color: '#a855f7' }, // purple-500
    { name: 'Global', views: 3100, color: '#06b6d4' }, // cyan-500
    { name: 'Health', views: 2400, color: '#10b981' }, // emerald-500
    { name: 'Breaking', views: 5100, color: '#ef4444' }, // red-500
    { name: 'Sports', views: 2100, color: '#f59e0b' }, // amber-500
];

export const engagementData = [
    { name: 'Mon', active: 1200, returning: 800 },
    { name: 'Tue', active: 1400, returning: 900 },
    { name: 'Wed', active: 1100, returning: 850 },
    { name: 'Thu', active: 1600, returning: 1100 },
    { name: 'Fri', active: 1800, returning: 1300 },
    { name: 'Sat', active: 2200, returning: 1600 },
    { name: 'Sun', active: 2500, returning: 1800 },
];

export const topArticles = [
    { id: 1, title: 'AI Startup Raises $100M Series B', category: 'Tech', views: 1240, avgTime: '4m 12s' },
    { id: 2, title: 'Global Markets Rally on Rate Hopes', category: 'Business', views: 980, avgTime: '3m 45s' },
    { id: 3, title: 'New Breakthrough in Quantum Tech', category: 'Tech', views: 940, avgTime: '5m 05s' },
    { id: 4, title: 'Major Sports Event Concludes', category: 'Sports', views: 820, avgTime: '2m 30s' },
    { id: 5, title: 'Health Committee Releases New Guidelines', category: 'Health', views: 760, avgTime: '3m 15s' },
];

export const kpiStats = [
    { label: 'Total active users', value: '14,800', trend: '+12% vs last week' },
    { label: 'Avg read time', value: '3m 42s', trend: '+5% vs last week' },
    { label: 'Bookmarks created', value: '3,210', trend: '+18% vs last week' },
    { label: 'Returning users', value: '68%', trend: '+2% vs last week' }
];
