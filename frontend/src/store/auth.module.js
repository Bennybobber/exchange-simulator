/* eslint no-shadow: ["error", { "allow": ["user"] }] */
/* eslint-env es6 */
import jwtDecode from 'jwt-decode';
import AuthService from '../services/auth.service';

const user = JSON.parse(localStorage.getItem('user'));
const initialState = user
  ? { status: { loggedIn: true }, user }
  : { status: { loggedIn: false }, user: null };

export const auth = {
  namespaced: true,
  state: initialState,
  actions: {
    login({ commit }, user) {
      return AuthService.login(user).then(
        (user) => {
          commit('loginSuccess', user);
          return Promise.resolve(user);
        },
        (error) => {
          commit('loginFailure');
          return Promise.reject(error);
        },
      );
    },
    logout({ commit }) {
      AuthService.logout();
      commit('logout');
    },
    register({ commit }, user) {
      return AuthService.register(user).then(
        (response) => {
          commit('registerSuccess');
          return Promise.resolve(response.data);
        },
        (error) => {
          commit('registerFailure');
          return Promise.reject(error);
        },
      );
    },
    refreshTokens(context, credentials) {
      // Do whatever you need to do to exchange refresh token for access token
      AuthService.refreshToken();
      // Finally, call autoRefresh to set up the new timeout
      this.dispatch('autoRefresh', credentials);
    },
    autoRefresh(context, credentials) {
      // const user = localStorage.getItem('user');
      const { user, commit, dispatch } = context;
      const { accessToken } = user.accessToken;
      const { exp } = jwtDecode(accessToken);
      const now = Date.now() / 1000; // exp is represented in seconds since epoch
      let timeUntilRefresh = exp - now;
      timeUntilRefresh -= (15 * 60); // Refresh 15 minutes before it expires
      const refreshTask = setTimeout(() => dispatch('refreshTokens', credentials), timeUntilRefresh * 1000);
      commit('refreshTask', refreshTask); // In case you want to cancel this task on logout
    },
  },
  mutations: {
    loginSuccess(state, user) {
      state.status.loggedIn = true;
      state.user = user;
    },
    loginFailure(state) {
      state.status.loggedIn = false;
      state.user = null;
    },
    logout(state) {
      state.status.loggedIn = false;
      state.user = null;
    },
    registerSuccess(state) {
      state.status.loggedIn = false;
    },
    registerFailure(state) {
      state.status.loggedIn = false;
    },
  },
};
