import api from './api';

const API_URL = 'http://localhost:5000/api/';

class UserService {
  getPublicContent() {
    return api.get(`${API_URL}all`);
  }

  updateUser(userData) {
    console.log('attempting to update...');
    return api.post(`${API_URL}user`, { data: userData });
  }

  getUser() {
    console.log('getting user...');
    return api.get(`${API_URL}user`);
  }
}

export default new UserService();
