import React from 'react';
import {
    BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
    LineChart, Line, Legend, Cell
} from 'recharts';
import { Users, Clock, Bookmark, Activity, ArrowUpRight, TrendingUp } from 'lucide-react';
import { categoryViewsData, engagementData, topArticles, kpiStats } from '../data/mockAnalytics';

const Analytics = () => {
    return (
        <div className="min-h-screen bg-black pt-8 pb-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-7xl mx-auto">
                <div className="flex flex-col md:flex-row md:items-center justify-between mb-8">
                    <div>
                        <div className="flex items-center space-x-3 mb-2">
                            <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-400 to-cyan-400 bg-clip-text text-transparent">
                                Internal Analytics Dashboard
                            </h1>
                            {/* Real-time Indicator */}
                            <div className="flex items-center space-x-2 bg-gray-900 border border-gray-800 rounded-full px-3 py-1">
                                <span className="relative flex h-3 w-3">
                                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                                    <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
                                </span>
                                <span className="text-xs text-green-400 font-medium">942 Active Now</span>
                            </div>
                        </div>
                        <p className="text-gray-400">Company insights on user behavior and content performance.</p>
                    </div>
                </div>

                {/* KPI Summary Cards */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                    {kpiStats.map((kpi, idx) => (
                        <div key={idx} className="bg-gray-900/50 p-6 rounded-2xl border border-gray-800 hover:border-purple-500/50 transition-colors">
                            <div className="flex items-center justify-between mb-4">
                                <p className="text-sm font-medium text-gray-400">{kpi.label}</p>
                                <div className="p-2 bg-gray-800 rounded-lg">
                                    {idx === 0 && <Users className="h-5 w-5 text-cyan-400" />}
                                    {idx === 1 && <Clock className="h-5 w-5 text-purple-400" />}
                                    {idx === 2 && <Bookmark className="h-5 w-5 text-pink-400" />}
                                    {idx === 3 && <Activity className="h-5 w-5 text-emerald-400" />}
                                </div>
                            </div>
                            <div className="flex items-baseline space-x-4">
                                <h3 className="text-3xl font-bold text-white">{kpi.value}</h3>
                                <span className="text-sm font-medium text-green-400 flex items-center">
                                    <ArrowUpRight className="h-4 w-4 mr-1" />
                                    {kpi.trend.split(' ')[0]}
                                </span>
                            </div>
                        </div>
                    ))}
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
                    {/* Bar Chart: Views by Category */}
                    <div className="bg-gray-900/50 p-6 rounded-2xl border border-gray-800">
                        <h3 className="text-xl font-bold text-white mb-6">Total Views by Category</h3>
                        <div className="h-80 w-full">
                            <ResponsiveContainer width="100%" height="100%">
                                <BarChart data={categoryViewsData}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" vertical={false} />
                                    <XAxis dataKey="name" stroke="#9CA3AF" />
                                    <YAxis stroke="#9CA3AF" />
                                    <Tooltip
                                        contentStyle={{ backgroundColor: '#111827', border: '1px solid #374151', borderRadius: '8px' }}
                                        itemStyle={{ color: '#E5E7EB' }}
                                    />
                                    <Bar dataKey="views" radius={[4, 4, 0, 0]}>
                                        {categoryViewsData.map((entry, index) => (
                                            <Cell key={`cell-${index}`} fill={entry.color} />
                                        ))}
                                    </Bar>
                                </BarChart>
                            </ResponsiveContainer>
                        </div>
                    </div>

                    {/* Line Chart: User Engagement over time */}
                    <div className="bg-gray-900/50 p-6 rounded-2xl border border-gray-800">
                        <h3 className="text-xl font-bold text-white mb-6">User Engagement (Active vs Returning)</h3>
                        <div className="h-80 w-full">
                            <ResponsiveContainer width="100%" height="100%">
                                <LineChart data={engagementData}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" vertical={false} />
                                    <XAxis dataKey="name" stroke="#9CA3AF" />
                                    <YAxis stroke="#9CA3AF" />
                                    <Tooltip
                                        contentStyle={{ backgroundColor: '#111827', border: '1px solid #374151', borderRadius: '8px' }}
                                    />
                                    <Legend />
                                    <Line type="monotone" dataKey="active" stroke="#a855f7" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 8 }} name="Active Users" />
                                    <Line type="monotone" dataKey="returning" stroke="#06b6d4" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 8 }} name="Returning Users" />
                                </LineChart>
                            </ResponsiveContainer>
                        </div>
                    </div>
                </div>

                {/* Top Viewed Articles List */}
                <div className="bg-gray-900/50 rounded-2xl border border-gray-800 overflow-hidden">
                    <div className="px-6 py-5 border-b border-gray-800">
                        <h3 className="text-xl font-bold text-white flex items-center">
                            <TrendingUp className="mr-2 h-5 w-5 text-purple-400" />
                            Top Viewed Articles This Week
                        </h3>
                    </div>
                    <div className="overflow-x-auto">
                        <table className="w-full text-left text-sm text-gray-400">
                            <thead className="bg-gray-800/50 text-xs uppercase text-gray-300">
                                <tr>
                                    <th scope="col" className="px-6 py-4">Rank</th>
                                    <th scope="col" className="px-6 py-4">Article Title</th>
                                    <th scope="col" className="px-6 py-4">Category</th>
                                    <th scope="col" className="px-6 py-4">Total Views</th>
                                    <th scope="col" className="px-6 py-4">Avg. View Time</th>
                                </tr>
                            </thead>
                            <tbody>
                                {topArticles.map((article, index) => (
                                    <tr key={article.id} className="border-b border-gray-800 hover:bg-gray-800/30 transition-colors">
                                        <td className="px-6 py-4 font-bold text-white">#{index + 1}</td>
                                        <td className="px-6 py-4 font-medium text-white">{article.title}</td>
                                        <td className="px-6 py-4 border-t border-gray-800">
                                            <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-gray-800 text-purple-400 border border-purple-500/20">
                                                {article.category}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 border-t border-gray-800">{article.views.toLocaleString()}</td>
                                        <td className="px-6 py-4 border-t border-gray-800">{article.avgTime}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>

            </div>
        </div>
    );
};

export default Analytics;
