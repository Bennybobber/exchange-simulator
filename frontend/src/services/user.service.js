import api from './api';

const API_URL = 'http://localhost:5000/api/';

class UserService {
  getPublicContent() {
    return api.get(`${API_URL}all`);
  }

  getUser() {
    return api.get(`${API_URL}user`);
  }
}

export default new UserService();
