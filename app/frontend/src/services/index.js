import Vue from 'vue';
import axios from 'axios';

export const EventBus = new Vue();

export function isValidJwt(jwt) {
  if (!jwt || jwt.split('.').length < 3) {
    return false;
  }
  const data = JSON.parse(atob(jwt.split('.')[1]));
  const exp = new Date(data.exp * 1000); // JS deals with dates in milliseconds since epoch
  const now = new Date();
  return now < exp;
}

export function authenticate(API_URL, userData, jwt) {
  return axios.post(`${API_URL}`, userData, { headers: { Authorization: `Bearer: ${jwt}` } });
}

export function login(API_URL, userData) {
  return axios.post(`${API_URL}`, userData);
}
