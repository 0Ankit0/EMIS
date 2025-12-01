import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      // Other API routes are proxied normally
      // /api/exam/process is handled by custom API route in src/app/api/exam/process/route.ts
      {
        source: '/api/:path*/',
        destination: 'http://localhost:8000/api/:path*/',
      },
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*/',
      },
    ];
  },
  allowedDevOrigins: ["192.168.100.107"],
};

export default nextConfig;
