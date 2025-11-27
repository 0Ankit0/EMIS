import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

const PUBLIC_PATHS = [
    '/login',
    '/password-reset',
    '/password-reset/confirm',
];

export function proxy(request: NextRequest) {
    const token = request.cookies.get('auth_token')?.value;
    const { pathname } = request.nextUrl;

    // Check if the path is public
    const isPublicPath = PUBLIC_PATHS.some(path => pathname.startsWith(path));

    // If authenticated and trying to access login, redirect to home
    if (token && pathname === '/login') {
        return NextResponse.redirect(new URL('/', request.url));
    }

    // If not authenticated and trying to access protected route, redirect to login
    if (!token && !isPublicPath) {
        return NextResponse.redirect(new URL('/login', request.url));
    }

    return NextResponse.next();
}

export const config = {
    matcher: [
        /*
         * Match all request paths except for the ones starting with:
         * - api (API routes)
         * - _next/static (static files)
         * - _next/image (image optimization files)
         * - favicon.ico (favicon file)
         */
        '/((?!api|_next/static|_next/image|favicon.ico).*)',
    ],
};
