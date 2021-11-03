import api from './api';

const API_URL = 'http://localhost:5000/api/';

class UserService {
  getPublicContent() {
    return api.get(`${API_URL}all`);
  }

  getUser() {
    return api.get(`${API_URL}user`);
  }

  getModeratorBoard() {
    return api.get(`${API_URL}mod`);
  }

  getAdminBoard() {
    return api.get(`${API_URL}admin`);
  }
}

export default new UserService();
