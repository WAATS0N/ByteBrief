import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ArrowLeft, Clock } from 'lucide-react';
import { fetchReadingHistory } from '../services/api';

const History = () => {
    const [history, setHistory] = useState([]);
    const navigate = useNavigate();
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const loadHistory = async () => {
            setIsLoading(true);
            try {
                const token = localStorage.getItem('access_token');
                if (token) {
                    const res = await fetchReadingHistory(token);
                    if (res && Array.isArray(res)) setHistory(res);
                }
            } catch (error) {
                console.error("Error loading history:", error);
            } finally {
                setIsLoading(false);
            }
        };
        loadHistory();
    }, []);

    return (
        <div className="min-h-screen bg-black pt-8 pb-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-4xl mx-auto">
                <div className="mb-8">
                    <button onClick={() => { if (window.history.state && window.history.state.idx > 0) { navigate(-1); } else { navigate('/home'); } }} className="inline-flex items-center text-gray-400 hover:text-white transition-colors mb-4 group">
                        <ArrowLeft className="h-4 w-4 mr-2 group-hover:-translate-x-1 transition-transform" />
                        Back
                    </button>
                    <h1 className="text-4xl font-bold text-white flex items-center">
                        <Clock className="h-8 w-8 mr-3 text-blue-400" />
                        Reading History
                    </h1>
                    <p className="text-gray-400 mt-2">Articles you've recently viewed.</p>
                </div>

                {isLoading ? (
                    <div className="flex justify-center items-center h-64"><div className="text-blue-400 text-xl animate-pulse">Loading history...</div></div>
                ) : (
                    history.length > 0 ? (
                        <div className="space-y-4">
                            {history.map((item, idx) => (
                                <Link to={`/article/${item.id}`} key={idx} className="block bg-gray-900/60 border border-gray-800 rounded-xl p-5 hover:bg-gray-800 transition-colors">
                                    <div className="flex justify-between items-start">
                                        <div>
                                            <h3 className="text-lg font-bold text-white mb-2">{item.title}</h3>
                                            <div className="flex items-center text-sm text-gray-400">
                                                <span className="bg-red-900/50 text-red-200 px-2 py-0.5 rounded text-xs mr-3">{item.source}</span>
                                                <span>Viewed at {new Date(item.viewed_at).toLocaleString()}</span>
                                            </div>
                                        </div>
                                    </div>
                                </Link>
                            ))}
                        </div>
                    ) : (
                        <div className="text-center py-20 bg-gray-900/30 rounded-3xl border border-dashed border-gray-800">
                            <Clock className="h-12 w-12 text-gray-500 mx-auto mb-4" />
                            <p className="text-white text-xl font-medium mb-2">No history yet</p>
                            <p className="text-gray-500">Read some articles to see them here.</p>
                        </div>
                    )
                )}
            </div>
        </div>
    );
};

export default History;
