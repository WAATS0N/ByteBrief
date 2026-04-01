import {
    Zap, Bot, TrendingUp, Globe, Heart, Trophy,
    Briefcase, Car, Gamepad2, Music, Camera,
    Plane, DollarSign, Users, Shield, Clock, Sparkles,
    Rocket, Cpu, Leaf, Smartphone, Satellite, Brain
} from 'lucide-react';

const iconMap = {
    Zap, Bot, TrendingUp, Globe, Heart, Trophy,
    Briefcase, Car, Gamepad2, Music, Camera,
    Plane, DollarSign, Users, Shield, Clock, Sparkles,
    Rocket, Cpu, Leaf, Smartphone, Satellite, Brain
};

export const getIcon = (iconName) => {
    return iconMap[iconName] || Globe; // Default to Globe if not found
};
