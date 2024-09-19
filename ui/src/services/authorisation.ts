import Cookies from "js-cookie";
import jwt from "jwt-decode";
import { AccessToken } from '../interfaces'

class AuthorizationClass {
  protected headers: any = {};
  

  setAccessToken(token: string) {
    Cookies.set("token", token);
  }

  getAccessToken() {
    return Cookies.get("token");
  }
  getHeaders(){
    return {
      Authorization: this.getAccessToken(),
    }
  }
  getAxiosConfig() {
    const config = {
      headers: this.getAccessToken() ? this.getHeaders() : {},
    };
    return config;
  };

  parseToken(token: any) {
    return jwt(token) as AccessToken
  }

  isValid(token: any) {
    if (token !== undefined && token.length > 0) {
      const tokenData = this.parseToken(token);
      if (tokenData?.exp !== undefined && tokenData?.exp > Math.floor(Date.now() / 1000)) {
        return [true, tokenData.role];
      } else {
        return [false, null];
      }
    } else {
      return [false, null];
    }
    // setInterval(() => {
  
    // }, 1000)
  };
}

const Authorization = new AuthorizationClass

export default Authorization