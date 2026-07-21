import { motion } from 'framer-motion';

interface Props {
  children: React.ReactNode;
  className?: string;
  hover?: boolean;
  shimmer?: boolean;
}

export default function LiquidGlassCard({ 
  children, 
  className = "", 
  hover = false, 
  shimmer = false 
}: Props) {
  return (
    <motion.div
      whileHover={hover ? { 
        y: -2, 
        scale: 1.01,
        boxShadow: "0 24px 60px rgba(0,0,0,0.6), inset 0 0 0 1px rgba(255,255,255,0.12)",
        transition: { 
          type: "spring", 
          stiffness: 400, 
          damping: 20 
        }
      } : {}}
      className={`
        relative overflow-hidden
        bg-white/[0.06] 
        backdrop-blur-2xl
        border border-white/[0.08] 
        rounded-2xl 
        shadow-clay
        transition-all duration-200
        ${className}
      `}
      style={{ willChange: 'transform, box-shadow' }}
    >
      {/* Glass refraction highlight */}
      <div className="absolute inset-0 bg-gradient-to-br from-white/5 via-transparent to-white/0 pointer-events-none" />
      
      {/* Top highlight line */}
      <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-white/20 to-transparent pointer-events-none" />
      
      {shimmer && <div className="shimmer-overlay pointer-events-none" />}
      
      <div className="relative z-10">
        {children}
      </div>
    </motion.div>
  );
}