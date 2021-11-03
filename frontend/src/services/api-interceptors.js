/* eslint no-underscore-dangle: 0 */
/* eslint no-param-reassign: "error" */
/* eslint camelcase: "error" */
/* eslint dot-notation: ["error", { "allowPattern": "^[a-z]+(_[a-z]+)+$" }] */
import axios from 'axios';
import axiosInstance from './api';
import TokenService from './token.service';

const setup = (store) => {
  axiosInstance.interceptors.request.use(
    (config) => {
      const token = TokenService.getLocalAccessToken();
      if (token) {
        // eslint-disable-next-line
        config.headers['Authorization'] = `Bearer ${token}`;
      }
      return config;
    },
    (error) => (Promise.reject(error)),
  );

  axiosInstance.interceptors.response.use(
    (res) => {
      console.log('yes');
      return res;
    },
    async (err) => {
      console.log(err);
      const originalConfig = err.config;
      console.log(originalConfig);
      if (originalConfig.url !== '/auth/login' && err.response) {
        // Access Token was expired
        if (err.response.status === 401 && !originalConfig._retry) {
          originalConfig._retry = true;
          try {
            const rs = await axios.post('http://localhost:5000/refreshtoken', {}, {
              headers: { Authorization: `Bearer ${TokenService.getLocalRefreshToken()}` },
            });

            const { accessToken } = rs.data;

            store.dispatch('auth/refreshToken', accessToken);
            TokenService.updateLocalAccessToken(accessToken);

            return axiosInstance(originalConfig);
          } catch (_error) {
            return Promise.reject(_error);
          }
        }
      }

      return Promise.reject(err);
    },
  );
};

export default setup;
