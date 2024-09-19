/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
  // env: {
  //   NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5001',
  // },
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: "http://127.0.0.1:5001/api/:path*",
      },
      {
        source: "/parse/:path*",
        destination: "http://127.0.0.1:5173/parse/:path*",
      },
    ];
  },
};

module.exports = nextConfig;
