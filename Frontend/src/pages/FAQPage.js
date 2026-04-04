import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Search, ChevronDown, ChevronUp, HelpCircle, Zap, Smartphone, Shield, Wrench, Info } from 'lucide-react';

const faqData = [
    {
        category: "General",
        icon: Info,
        color: "text-purple-400",
        bgColor: "bg-purple-500/20",
        items: [
            { q: "What is ByteBrief?", a: "ByteBrief is an AI-powered platform that summarizes news into short, easy-to-read content. It helps you stay informed without spending hours reading full articles." },
            { q: "How does ByteBrief work?", a: "It uses advanced AI algorithms to fetch news articles from trusted global sources and generate concise summaries for quick reading." },
            { q: "Is ByteBrief free to use?", a: "Yes, ByteBrief offers free access to all core features including news reading, AI summaries, and category browsing." },
            { q: "Do I need an account to use ByteBrief?", a: "No, you can browse news as a guest. However, creating an account unlocks personalized features like bookmarks, reading history, and custom category preferences." }
        ]
    },
    {
        category: "Features",
        icon: Zap,
        color: "text-cyan-400",
        bgColor: "bg-cyan-500/20",
        items: [
            { q: "How often is the news updated?", a: "News is updated in real-time through our automated scraping pipeline. Our AI agents constantly monitor trusted sources to bring you breaking updates the moment they happen." },
            { q: "Can I customize news categories?", a: "Yes, you can choose from topics like Technology, Sports, Business, Health, Entertainment, Science, and more. Your feed adapts to your selected preferences." },
            { q: "Does ByteBrief support multiple languages?", a: "Currently, ByteBrief supports English. We are actively working on adding support for more languages in future updates." },
            { q: "Can I save articles for later?", a: "Yes, after logging in you can bookmark any article. Access your saved articles anytime from the Bookmarks section in your account settings." }
        ]
    },
    {
        category: "Usage",
        icon: Smartphone,
        color: "text-pink-400",
        bgColor: "bg-pink-500/20",
        items: [
            { q: "Is ByteBrief available on mobile?", a: "Yes, ByteBrief is fully responsive and works seamlessly on both desktop and mobile browsers. A dedicated mobile app is planned for the future." },
            { q: "Why is a news summary different from the original article?", a: "Summaries are AI-generated shortened versions of the original articles, designed for quick understanding. They capture the key points while reducing reading time to under 3 minutes." },
            { q: "Can I share news from ByteBrief?", a: "Yes, you can share articles via social media platforms or copy the direct link to share with anyone." }
        ]
    },
    {
        category: "Account & Privacy",
        icon: Shield,
        color: "text-green-400",
        bgColor: "bg-green-500/20",
        items: [
            { q: "Is my data secure?", a: "Yes, we follow industry-standard security practices including encrypted connections and secure authentication to protect your personal data." },
            { q: "Can I delete my account?", a: "Yes, you can permanently delete your account and all associated data from the Account Settings page under the Danger Zone section." }
        ]
    },
    {
        category: "Support",
        icon: Wrench,
        color: "text-orange-400",
        bgColor: "bg-orange-500/20",
        items: [
            { q: "What should I do if the app is not working?", a: "Try refreshing the page first. If the issue persists, use the \"Report a Problem\" feature in your Account Settings to let us know the details." },
            { q: "How can I contact support?", a: "Use the \"Contact Us\" form in Account Settings, or email us directly at bytebrief2026@gmail.com. We typically respond within 24 hours." },
            { q: "How do I report incorrect news?", a: "Use the \"Report a Problem\" feature in your Account Settings and select \"Incorrect Content\" as the issue type. Our team will review and take action promptly." }
        ]
    }
];

const FAQItem = ({ item, isOpen, onToggle }) => (
    <div className={`border rounded-2xl overflow-hidden transition-all duration-300 mb-3 ${isOpen ? 'border-purple-500/40 bg-gray-800/60' : 'border-gray-800 bg-gray-900/40 hover:bg-gray-800/40'}`}>
        <button onClick={onToggle} className="w-full flex items-center justify-between p-5 sm:p-6 text-left">
            <span className={`text-base sm:text-lg font-semibold pr-4 ${isOpen ? 'text-white' : 'text-gray-200'}`}>{item.q}</span>
            {isOpen
                ? <ChevronUp className="h-5 w-5 text-purple-400 flex-shrink-0" />
                : <ChevronDown className="h-5 w-5 text-gray-500 flex-shrink-0" />
            }
        </button>
        {isOpen && (
            <div className="px-5 sm:px-6 pb-5 sm:pb-6">
                <div className="border-t border-gray-700/50 pt-4">
                    <p className="text-gray-300 text-base leading-relaxed">{item.a}</p>
                </div>
            </div>
        )}
    </div>
);

const FAQPage = () => {
    const navigate = useNavigate();
    const [searchQuery, setSearchQuery] = useState('');
    const [openItems, setOpenItems] = useState({});

    const toggleItem = (key) => {
        setOpenItems(prev => ({ ...prev, [key]: !prev[key] }));
    };

    const filteredData = faqData.map(section => ({
        ...section,
        items: section.items.filter(
            item => item.q.toLowerCase().includes(searchQuery.toLowerCase()) ||
                item.a.toLowerCase().includes(searchQuery.toLowerCase())
        )
    })).filter(section => section.items.length > 0);

    const totalResults = filteredData.reduce((acc, s) => acc + s.items.length, 0);

    return (
        <div className="min-h-screen pt-8 pb-16 px-4 sm:px-6 lg:px-8">
            <div className="max-w-4xl mx-auto">
                {/* Header */}
                <div className="mb-10">
                    <button
                        onClick={() => { if (window.history.state && window.history.state.idx > 0) navigate(-1); else navigate('/settings'); }}
                        className="inline-flex items-center text-gray-400 hover:text-white transition-colors mb-6 group"
                    >
                        <ArrowLeft className="h-4 w-4 mr-2 group-hover:-translate-x-1 transition-transform" />
                        Back
                    </button>
                    <h1 className="text-4xl sm:text-5xl font-bold text-white flex items-center mb-2">
                        <HelpCircle className="h-9 w-9 mr-4 text-purple-400" />
                        FAQs
                    </h1>
                    <p className="text-gray-400 text-lg mt-2">Find answers to commonly asked questions about ByteBrief.</p>
                </div>

                {/* Search Bar */}
                <div className="relative mb-10">
                    <Search className="absolute left-5 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-500" />
                    <input
                        type="text"
                        placeholder="Search questions..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="w-full bg-gray-900/60 border border-gray-700 rounded-2xl pl-14 pr-6 py-4 text-white text-lg placeholder-gray-500 focus:outline-none focus:border-purple-500 backdrop-blur-xl transition-colors"
                    />
                    {searchQuery && (
                        <span className="absolute right-5 top-1/2 -translate-y-1/2 text-sm text-gray-500">
                            {totalResults} result{totalResults !== 1 ? 's' : ''}
                        </span>
                    )}
                </div>

                {/* FAQ Sections */}
                {filteredData.length > 0 ? (
                    filteredData.map((section) => {
                        const Icon = section.icon;
                        return (
                            <div key={section.category} className="mb-10">
                                <div className="flex items-center mb-5">
                                    <div className={`${section.bgColor} p-2.5 rounded-xl mr-4`}>
                                        <Icon className={`h-5 w-5 ${section.color}`} />
                                    </div>
                                    <h2 className="text-xl font-bold text-white tracking-wide">{section.category}</h2>
                                </div>
                                {section.items.map((item, idx) => {
                                    const key = `${section.category}-${idx}`;
                                    return (
                                        <FAQItem
                                            key={key}
                                            item={item}
                                            isOpen={!!openItems[key]}
                                            onToggle={() => toggleItem(key)}
                                        />
                                    );
                                })}
                            </div>
                        );
                    })
                ) : (
                    <div className="text-center py-20 bg-gray-900/30 rounded-3xl border border-dashed border-gray-800">
                        <Search className="h-12 w-12 text-gray-600 mx-auto mb-4" />
                        <p className="text-white text-xl font-medium mb-2">No results found</p>
                        <p className="text-gray-500">Try searching with different keywords.</p>
                    </div>
                )}

                {/* Contact CTA */}
                <div className="mt-8 bg-gradient-to-r from-purple-900/40 to-cyan-900/40 border border-purple-500/20 rounded-2xl p-8 text-center">
                    <h3 className="text-xl font-bold text-white mb-2">Still have questions?</h3>
                    <p className="text-gray-400 mb-5">We're here to help. Reach out to our team directly.</p>
                    <button
                        onClick={() => navigate('/settings')}
                        className="bg-gradient-to-r from-purple-600 to-cyan-600 hover:from-purple-500 hover:to-cyan-500 text-white px-8 py-3 rounded-xl font-semibold transition-all duration-300 transform hover:scale-105"
                    >
                        Contact Support
                    </button>
                </div>
            </div>
        </div>
    );
};

export default FAQPage;
