import axios from 'axios';
import api from './api';
import tokenService from './token.service';

const API_URL = 'http://localhost:5000/';

class AuthService {
  login(user) {
    return axios
      .post(`${API_URL}login`, {
        username: user.username,
        password: user.password,
      })
      .then((response) => {
        if (response.data.accessToken) {
          tokenService.setUser(response.data);
        }

        return response.data;
      });
  }

  logout() {
    localStorage.removeItem('user');
    return { message: 'Logout Successful' };
  }

  refreshToken() {
    const user = localStorage.getItem('user');
    return api.post(`${API_URL}refreshtoken`, { headers: user.refreshToken })
      .then((response) => {
        if (response.data.accessToken) {
          tokenService.updateLocalAccessToken(response.data.accessToken);
        }
      });
  }

  register(user) {
    return axios
      .post(`${API_URL}register`, {
        username: user.username,
        password: user.password,
      });
  }
}

export default new AuthService();
