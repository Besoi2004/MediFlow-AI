import { NextResponse, type NextRequest } from "next/server";

// Chỉ chặn sớm cho dễ dùng: phân quyền thật nằm ở backend.
export function proxy(request: NextRequest) {
  if (request.cookies.has("access_token")) return NextResponse.next();
  const { pathname, search } = request.nextUrl;
  const login = new URL("/login", request.url);
  login.searchParams.set("next", pathname + search);
  return NextResponse.redirect(login);
}

export const config = { matcher: ["/bookings", "/book/:path*", "/consultant/:path*"] };
