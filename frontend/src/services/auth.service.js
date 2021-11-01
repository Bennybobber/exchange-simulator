import axios from 'axios';

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
          localStorage.setItem('user', JSON.stringify(response.data));
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
    return axios.post(`${API_URL}refresh`, { headers: user.refreshToken })
      .then((response) => {
        if (response.data.accessToken) {
          localStorage.setItem('user', JSON.stringify(response.data));
          this.$store.state.auth.user.accessToken = response.data.accessToken;
        }
      });
  }

  register(user) {
    return axios.post(`${API_URL}register`, {
      username: user.username,
      password: user.password,
    });
  }
}

export default new AuthService();
