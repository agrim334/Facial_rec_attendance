import axios from 'axios';

const API_URL = 'http://localhost:8080/'

export function authenticate (userData) {
  return axios.post(`${API_URL}/login/`, userData)
}

export function register (userData) {
  return axios.post(`${API_URL}/register/`, userData)
}