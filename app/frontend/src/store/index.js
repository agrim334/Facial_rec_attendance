import Vue from 'vue';
import Vuex from 'vuex';
import {
  isValidJwt, login, authenticate, authenticateimg, noauthroute, EventBus,
} from '../services';

Vue.use(Vuex);

const jwtDecode = require('jwt-decode');

const actions = {
  login(context, userData) {
    const path = userData.url;
    const userdat = userData.data;
    console.log(process.argv.VUE_APP_FLASK_URL);
    context.commit('setUserData', { userdat });
    return login(path, userdat)
      .then((response) => context.commit('setJwtToken', { jwt: response.data }))
      .catch((error) => {
        console.log('Error Authenticating: ', error);
        EventBus.$emit('failedAuthentication', error);
      });
  },
  authrequest(context, userData) {
    const path = userData.url;
    const userdat = userData.data;
    return authenticate(path, userdat, context.state.jwt.token);
  },
  authrequestimg(context, userData) {
    const path = userData.url;
    const userdat = userData.data;
    return authenticateimg(path, userdat, context.state.jwt.token);
  },
  noauthroutrereq(context, userData) {
    const path = userData.url;
    const userdat = userData.data;
    return noauthroute(path, userdat);
  },
  logout(context) {
    context.commit('resetJwtToken');
    return 0;
  },
};

const mutations = {
  setUserData(state, payload) {
    state.userData = payload.userData;
  },
  setJwtToken(state, payload) {
    localStorage.token = payload.jwt.token;
    state.jwt = payload.jwt;
    state.userrole = jwtDecode(payload.jwt.token).role;
  },
  resetJwtToken(state) {
    localStorage.removeItem('token');
    state.jwt = '';
    state.userrole = '';
  },
};

const getters = {
  isAuthenticated(state) {
    return isValidJwt(state.jwt.token);
  },
};
const state = {
  jwt: { token: localStorage.getItem('token') },
  userrole: localStorage.getItem('token') ? jwtDecode(localStorage.getItem('token')).role : '',
};

const store = new Vuex.Store({
  state,
  actions,
  mutations,
  getters,
});

export default store;
