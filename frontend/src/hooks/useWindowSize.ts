import { useState, useEffect } from 'react';

interface WindowSize {
  width: number;
  height: number;
  aspectRatio: number;
  isUltraWide: boolean;
  isMobile: boolean;
  isTablet: boolean;
  isDesktop: boolean;
}

export const useWindowSize = (): WindowSize => {
  const [windowSize, setWindowSize] = useState<WindowSize>({
    width: typeof window !== 'undefined' ? window.innerWidth : 1200,
    height: typeof window !== 'undefined' ? window.innerHeight : 800,
    aspectRatio: typeof window !== 'undefined' ? window.innerWidth / window.innerHeight : 1.5,
    isUltraWide: typeof window !== 'undefined' ? (window.innerWidth / window.innerHeight) > 2.1 : false,
    isMobile: typeof window !== 'undefined' ? window.innerWidth < 768 : false,
    isTablet: typeof window !== 'undefined' ? window.innerWidth >= 768 && window.innerWidth < 1024 : false,
    isDesktop: typeof window !== 'undefined' ? window.innerWidth >= 1024 : false,
  });

  useEffect(() => {
    const handleResize = () => {
      const width = window.innerWidth;
      const height = window.innerHeight;
      const aspectRatio = width / height;
      setWindowSize({
        width,
        height,
        aspectRatio,
        isUltraWide: aspectRatio > 2.1,
        isMobile: width < 768,
        isTablet: width >= 768 && width < 1024,
        isDesktop: width >= 1024,
      });
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return windowSize;
};
