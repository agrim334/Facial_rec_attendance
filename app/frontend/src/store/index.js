import Vue from 'vue';
import Vuex from 'vuex';
import {
  isValidJwt, login, authenticate, EventBus,
} from '../services';

Vue.use(Vuex);

const actions = {
  login(context, userData) {
    console.log(userData);
    const path = userData.url;
    const userdat = userData.data;
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
};

const mutations = {
  setUserData(state, payload) {
    console.log('setUserData payload = ', payload);
    state.userData = payload.userData;
  },
  setJwtToken(state, payload) {
    console.log('setJwtToken payload = ', payload);
    localStorage.token = payload.jwt.token;
    state.jwt = payload.jwt;
    console.log(state);
  },
};

const getters = {
  isAuthenticated(state) {
    console.log(state);
    return isValidJwt(state.jwt.token);
  },
};
const state = {
  user: {},
  jwt: { token: localStorage.getItem('token') },
};

const store = new Vuex.Store({
  state,
  actions,
  mutations,
  getters,
});

export default store;
