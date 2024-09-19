import { NextResponse, URLPattern } from "next/server";
import type { NextRequest } from "next/server";
import Authorization from "./services/authorisation";

// This function can be marked `async` if using `await` inside
export function middleware(req: NextRequest) {
  const [valid, role] = Authorization.isValid(req.cookies.get("token")?.value);
  if (
    req.nextUrl.pathname.startsWith('/_next') ||
    req.nextUrl.pathname.includes('/api/') ||
    req.nextUrl.pathname === '/'
  ) {
    return;
  }

  if (valid === true) {
    return NextResponse.next()
  } else {
    return NextResponse.redirect(new URL("/", req.url));
  }
}

// See "Matching Paths" below to learn more
export const config = {
  matcher: ['/:workspace*'],
};
