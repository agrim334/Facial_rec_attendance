import Vue from 'vue';
import axios from 'axios';

export const EventBus = new Vue();
const API_URL = 'http://192.168.43.70:5000/';

export function isValidJwt(jwt) {
  if (!jwt || jwt.split('.').length < 3) {
    return false;
  }
  const data = JSON.parse(atob(jwt.split('.')[1]));
  const exp = new Date(data.exp * 1000); // JS deals with dates in milliseconds since epoch
  const now = new Date();
  return now < exp;
}

export function noauthroute(remain, userData) {
  let finalurl = `${API_URL}`;
  finalurl = finalurl.concat(remain);
  return axios.post(`${finalurl}`, userData);
}

export function authenticate(remain, userData, jwt) {
  let finalurl = `${API_URL}`;
  finalurl = finalurl.concat(remain);
  return axios.post(`${finalurl}`, userData, { headers: { Authorization: `Bearer: ${jwt}` } });
}

export function authenticateimg(remain, userData, jwt) {
  let finalurl = `${API_URL}`;
  finalurl = finalurl.concat(remain);
  const headerdata = {
    Authorization: `Bearer: ${jwt}`, 'Content-Type': 'multipart/form-data',
  };
  return axios.post(`${finalurl}`, userData, { headers: headerdata });
}

export function login(remain, userData) {
  let finalurl = `${API_URL}`;
  finalurl = finalurl.concat(remain);
  return axios.post(`${finalurl}`, userData);
}
