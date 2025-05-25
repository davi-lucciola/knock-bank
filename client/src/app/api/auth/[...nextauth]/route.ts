import NextAuth from "next-auth";
import { nextAuthOptions } from "@/app/api/auth/[...nextauth]/options";

const handler = NextAuth(nextAuthOptions);

export { handler as GET, handler as POST };
