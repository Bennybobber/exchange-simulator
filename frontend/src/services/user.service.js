import api from './api';

const API_URL = 'http://localhost:5000/api/';

class UserService {
  getPublicContent() {
    return api.get(`${API_URL}all`);
  }

  updateUser(userData) {
    return api.put(`${API_URL}user`, { data: userData });
  }

  deleteUser(userData) {
    return api.delete(`${API_URL}user`, { data: userData });
  }

  getUser() {
    return api.get(`${API_URL}user`);
  }
}

export default new UserService();
