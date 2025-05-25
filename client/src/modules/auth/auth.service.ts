import { Api } from "@/lib/api";
import { LoginUserPayload, LoginUserResponse } from "@/modules/auth/auth.type";

export class AuthService {
  constructor(private api: Api = new Api()) {}

  async login(payload: LoginUserPayload): Promise<LoginUserResponse> {
    const data = this.api.post<LoginUserResponse, LoginUserPayload>(
      "/login",
      payload
    );
    return data;
  }

  async logout() {
    this.api.delete("/logout");
  }
}
