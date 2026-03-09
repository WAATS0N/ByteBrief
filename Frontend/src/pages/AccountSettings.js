import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { User, Lock, LogOut, Trash2, AlertCircle, Check, Loader, Mail, Calendar, Edit3, X, Shield, ChevronRight } from 'lucide-react';
import { authService } from '../services/authService';

const AccountSettings = () => {
    const navigate = useNavigate();
    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(true);

    // Edit profile state
    const [isEditing, setIsEditing] = useState(false);
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [profileMsg, setProfileMsg] = useState({ type: '', text: '' });

    // Change password state
    const [oldPassword, setOldPassword] = useState('');
    const [newPassword1, setNewPassword1] = useState('');
    const [newPassword2, setNewPassword2] = useState('');
    const [passwordMsg, setPasswordMsg] = useState({ type: '', text: '' });
    const [passwordLoading, setPasswordLoading] = useState(false);

    // Delete account state
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [deletePassword, setDeletePassword] = useState('');
    const [deleteMsg, setDeleteMsg] = useState({ type: '', text: '' });
    const [deleteLoading, setDeleteLoading] = useState(false);

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                const data = await authService.getProfile();
                setProfile(data);
                setFirstName(data.first_name || '');
                setLastName(data.last_name || '');
            } catch {
                setProfileMsg({ type: 'error', text: 'Failed to load profile.' });
            } finally {
                setLoading(false);
            }
        };
        fetchProfile();
    }, []);

    const handleUpdateProfile = async () => {
        setProfileMsg({ type: '', text: '' });
        try {
            const data = await authService.updateProfile({ first_name: firstName, last_name: lastName });
            setProfile(data);
            setIsEditing(false);
            setProfileMsg({ type: 'success', text: 'Profile updated successfully!' });
        } catch (err) {
            setProfileMsg({ type: 'error', text: err?.error || 'Update failed.' });
        }
    };

    const handleChangePassword = async (e) => {
        e.preventDefault();
        setPasswordMsg({ type: '', text: '' });
        if (newPassword1 !== newPassword2) {
            setPasswordMsg({ type: 'error', text: 'New passwords do not match.' });
            return;
        }
        setPasswordLoading(true);
        try {
            await authService.changePassword(oldPassword, newPassword1, newPassword2);
            setPasswordMsg({ type: 'success', text: 'Password changed successfully!' });
            setOldPassword('');
            setNewPassword1('');
            setNewPassword2('');
        } catch (err) {
            const msg = err?.old_password?.[0] || err?.new_password2?.[0] || err?.new_password1?.[0] || err?.error || 'Password change failed.';
            setPasswordMsg({ type: 'error', text: msg });
        } finally {
            setPasswordLoading(false);
        }
    };

    const handleLogout = () => {
        authService.logout();
        navigate('/');
    };

    const handleDeleteAccount = async () => {
        setDeleteMsg({ type: '', text: '' });
        if (!deletePassword) {
            setDeleteMsg({ type: 'error', text: 'Please enter your password to confirm.' });
            return;
        }
        setDeleteLoading(true);
        try {
            await authService.deleteAccount(deletePassword);
            authService.logout();
            navigate('/');
        } catch (err) {
            setDeleteMsg({ type: 'error', text: err?.error || 'Deletion failed.' });
        } finally {
            setDeleteLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-black flex items-center justify-center pt-8">
                <Loader className="h-8 w-8 text-purple-400 animate-spin" />
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-black pt-8 pb-16 px-4 sm:px-6 relative overflow-hidden">
            {/* Background Glows */}
            <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-600/10 rounded-full blur-[120px] pointer-events-none" />
            <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-cyan-600/10 rounded-full blur-[120px] pointer-events-none" />

            <div className="max-w-2xl mx-auto relative z-10">
                <h1 className="text-3xl font-bold text-white mb-2">Account Settings</h1>
                <p className="text-gray-400 mb-8">Manage your profile, security, and preferences.</p>

                {/* ── Profile Section ── */}
                <div className="bg-gray-900/60 border border-gray-800 rounded-2xl p-6 mb-6 backdrop-blur-xl">
                    <div className="flex items-center justify-between mb-5">
                        <div className="flex items-center gap-3">
                            <div className="bg-gradient-to-br from-purple-500 to-cyan-500 p-2.5 rounded-xl">
                                <User className="h-5 w-5 text-white" />
                            </div>
                            <h2 className="text-xl font-semibold text-white">Profile Information</h2>
                        </div>
                        {!isEditing && (
                            <button
                                onClick={() => setIsEditing(true)}
                                className="flex items-center gap-1.5 text-sm text-purple-400 hover:text-purple-300 transition-colors"
                            >
                                <Edit3 className="h-4 w-4" /> Edit
                            </button>
                        )}
                    </div>

                    {profileMsg.text && (
                        <div className={`mb-4 p-3 rounded-xl flex items-center text-sm ${profileMsg.type === 'success' ? 'bg-green-500/10 border border-green-500/50 text-green-400' : 'bg-red-500/10 border border-red-500/50 text-red-400'}`}>
                            {profileMsg.type === 'success' ? <Check className="h-4 w-4 mr-2 flex-shrink-0" /> : <AlertCircle className="h-4 w-4 mr-2 flex-shrink-0" />}
                            {profileMsg.text}
                        </div>
                    )}

                    {isEditing ? (
                        <div className="space-y-4">
                            <div>
                                <label className="block text-sm text-gray-400 mb-1">First Name</label>
                                <input type="text" value={firstName} onChange={(e) => setFirstName(e.target.value)}
                                    className="w-full bg-gray-950 border border-gray-700 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-purple-500 transition-colors" />
                            </div>
                            <div>
                                <label className="block text-sm text-gray-400 mb-1">Last Name</label>
                                <input type="text" value={lastName} onChange={(e) => setLastName(e.target.value)}
                                    className="w-full bg-gray-950 border border-gray-700 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-purple-500 transition-colors" />
                            </div>
                            <div className="flex gap-3 pt-1">
                                <button onClick={handleUpdateProfile}
                                    className="bg-gradient-to-r from-purple-600 to-cyan-600 hover:from-purple-500 hover:to-cyan-500 text-white px-5 py-2 rounded-xl font-medium transition-all text-sm">
                                    Save Changes
                                </button>
                                <button onClick={() => { setIsEditing(false); setFirstName(profile?.first_name || ''); setLastName(profile?.last_name || ''); }}
                                    className="text-gray-400 hover:text-white px-4 py-2 rounded-xl border border-gray-700 hover:border-gray-500 transition-colors text-sm flex items-center gap-1.5">
                                    <X className="h-4 w-4" /> Cancel
                                </button>
                            </div>
                        </div>
                    ) : (
                        <div className="space-y-3">
                            <div className="flex items-center gap-3 text-gray-300">
                                <User className="h-4 w-4 text-gray-500" />
                                <span>{profile?.first_name || profile?.username || '—'} {profile?.last_name || ''}</span>
                            </div>
                            <div className="flex items-center gap-3 text-gray-300">
                                <Mail className="h-4 w-4 text-gray-500" />
                                <span>{profile?.email}</span>
                            </div>
                            <div className="flex items-center gap-3 text-gray-300">
                                <Calendar className="h-4 w-4 text-gray-500" />
                                <span>Joined {new Date(profile?.date_joined).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}</span>
                            </div>
                        </div>
                    )}
                </div>

                {/* ── Change Password Section ── */}
                <div className="bg-gray-900/60 border border-gray-800 rounded-2xl p-6 mb-6 backdrop-blur-xl">
                    <div className="flex items-center gap-3 mb-5">
                        <div className="bg-gradient-to-br from-blue-500 to-indigo-500 p-2.5 rounded-xl">
                            <Shield className="h-5 w-5 text-white" />
                        </div>
                        <h2 className="text-xl font-semibold text-white">Security</h2>
                    </div>

                    {passwordMsg.text && (
                        <div className={`mb-4 p-3 rounded-xl flex items-center text-sm ${passwordMsg.type === 'success' ? 'bg-green-500/10 border border-green-500/50 text-green-400' : 'bg-red-500/10 border border-red-500/50 text-red-400'}`}>
                            {passwordMsg.type === 'success' ? <Check className="h-4 w-4 mr-2 flex-shrink-0" /> : <AlertCircle className="h-4 w-4 mr-2 flex-shrink-0" />}
                            {passwordMsg.text}
                        </div>
                    )}

                    <form onSubmit={handleChangePassword} className="space-y-4">
                        <div>
                            <label className="block text-sm text-gray-400 mb-1">Current Password</label>
                            <div className="relative">
                                <Lock className="absolute left-3 top-3 h-4 w-4 text-gray-500" />
                                <input type="password" value={oldPassword} onChange={(e) => setOldPassword(e.target.value)}
                                    placeholder="Enter current password"
                                    className="w-full bg-gray-950 border border-gray-700 rounded-xl pl-10 pr-4 py-2.5 text-white placeholder-gray-600 focus:outline-none focus:border-purple-500 transition-colors" required />
                            </div>
                        </div>
                        <div>
                            <label className="block text-sm text-gray-400 mb-1">New Password</label>
                            <div className="relative">
                                <Lock className="absolute left-3 top-3 h-4 w-4 text-gray-500" />
                                <input type="password" value={newPassword1} onChange={(e) => setNewPassword1(e.target.value)}
                                    placeholder="Enter new password"
                                    className="w-full bg-gray-950 border border-gray-700 rounded-xl pl-10 pr-4 py-2.5 text-white placeholder-gray-600 focus:outline-none focus:border-purple-500 transition-colors" required />
                            </div>
                        </div>
                        <div>
                            <label className="block text-sm text-gray-400 mb-1">Confirm New Password</label>
                            <div className="relative">
                                <Lock className="absolute left-3 top-3 h-4 w-4 text-gray-500" />
                                <input type="password" value={newPassword2} onChange={(e) => setNewPassword2(e.target.value)}
                                    placeholder="Confirm new password"
                                    className="w-full bg-gray-950 border border-gray-700 rounded-xl pl-10 pr-4 py-2.5 text-white placeholder-gray-600 focus:outline-none focus:border-purple-500 transition-colors" required />
                            </div>
                        </div>
                        <button type="submit" disabled={passwordLoading}
                            className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white px-5 py-2.5 rounded-xl font-medium transition-all text-sm flex items-center gap-2 disabled:opacity-50">
                            {passwordLoading ? <Loader className="h-4 w-4 animate-spin" /> : <Lock className="h-4 w-4" />}
                            Change Password
                        </button>
                    </form>
                </div>

                {/* ── Session / Logout ── */}
                <div className="bg-gray-900/60 border border-gray-800 rounded-2xl p-6 mb-6 backdrop-blur-xl">
                    <div className="flex items-center gap-3 mb-4">
                        <div className="bg-gradient-to-br from-amber-500 to-orange-500 p-2.5 rounded-xl">
                            <LogOut className="h-5 w-5 text-white" />
                        </div>
                        <h2 className="text-xl font-semibold text-white">Session</h2>
                    </div>
                    <p className="text-gray-400 text-sm mb-4">Sign out of your current session on this device.</p>
                    <button onClick={handleLogout}
                        className="flex items-center gap-2 text-white bg-gray-800 hover:bg-gray-700 border border-gray-700 hover:border-gray-600 px-5 py-2.5 rounded-xl font-medium transition-all text-sm">
                        <LogOut className="h-4 w-4" /> Logout
                        <ChevronRight className="h-4 w-4 ml-auto opacity-50" />
                    </button>
                </div>

                {/* ── Danger Zone ── */}
                <div className="bg-red-950/20 border border-red-900/40 rounded-2xl p-6 backdrop-blur-xl">
                    <div className="flex items-center gap-3 mb-4">
                        <div className="bg-gradient-to-br from-red-500 to-rose-600 p-2.5 rounded-xl">
                            <Trash2 className="h-5 w-5 text-white" />
                        </div>
                        <h2 className="text-xl font-semibold text-red-400">Danger Zone</h2>
                    </div>
                    <p className="text-gray-400 text-sm mb-4">
                        Permanently delete your account and all associated data. <span className="text-red-400 font-medium">This action cannot be undone.</span>
                    </p>
                    <button onClick={() => setShowDeleteModal(true)}
                        className="flex items-center gap-2 text-red-400 bg-red-500/10 hover:bg-red-500/20 border border-red-500/30 hover:border-red-500/50 px-5 py-2.5 rounded-xl font-medium transition-all text-sm">
                        <Trash2 className="h-4 w-4" /> Delete My Account
                    </button>
                </div>
            </div>

            {/* ── Delete Confirmation Modal ── */}
            {showDeleteModal && (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm px-4">
                    <div className="bg-gray-900 border border-gray-700 rounded-2xl p-6 max-w-md w-full relative">
                        <button onClick={() => { setShowDeleteModal(false); setDeletePassword(''); setDeleteMsg({ type: '', text: '' }); }}
                            className="absolute top-4 right-4 text-gray-500 hover:text-white transition-colors">
                            <X className="h-5 w-5" />
                        </button>

                        <div className="flex items-center gap-3 mb-4">
                            <div className="bg-red-500/20 p-2.5 rounded-xl">
                                <AlertCircle className="h-5 w-5 text-red-400" />
                            </div>
                            <h3 className="text-lg font-semibold text-white">Confirm Account Deletion</h3>
                        </div>

                        <p className="text-gray-400 text-sm mb-4">Enter your password to permanently delete your account. All your data will be lost forever.</p>

                        {deleteMsg.text && (
                            <div className="mb-4 p-3 rounded-xl flex items-center text-sm bg-red-500/10 border border-red-500/50 text-red-400">
                                <AlertCircle className="h-4 w-4 mr-2 flex-shrink-0" />
                                {deleteMsg.text}
                            </div>
                        )}

                        <div className="relative mb-4">
                            <Lock className="absolute left-3 top-3 h-4 w-4 text-gray-500" />
                            <input type="password" value={deletePassword} onChange={(e) => setDeletePassword(e.target.value)}
                                placeholder="Enter your password"
                                className="w-full bg-gray-950 border border-gray-700 rounded-xl pl-10 pr-4 py-2.5 text-white placeholder-gray-600 focus:outline-none focus:border-red-500 transition-colors" />
                        </div>

                        <div className="flex gap-3">
                            <button onClick={handleDeleteAccount} disabled={deleteLoading}
                                className="flex-1 bg-red-600 hover:bg-red-500 text-white px-5 py-2.5 rounded-xl font-medium transition-all text-sm flex items-center justify-center gap-2 disabled:opacity-50">
                                {deleteLoading ? <Loader className="h-4 w-4 animate-spin" /> : <Trash2 className="h-4 w-4" />}
                                Delete Forever
                            </button>
                            <button onClick={() => { setShowDeleteModal(false); setDeletePassword(''); setDeleteMsg({ type: '', text: '' }); }}
                                className="flex-1 text-gray-300 bg-gray-800 hover:bg-gray-700 border border-gray-700 px-5 py-2.5 rounded-xl font-medium transition-all text-sm">
                                Cancel
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default AccountSettings;
