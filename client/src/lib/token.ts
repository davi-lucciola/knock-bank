import { getCookie, deleteCookie } from "cookies-next";

export const TOKEN_KEY = "knockbank.token";

export class Token {
  static get() {
    return getCookie(TOKEN_KEY)?.toString();
  }

  static clean() {
    deleteCookie(TOKEN_KEY);
  }
}
