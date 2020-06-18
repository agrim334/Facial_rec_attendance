import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../views/Home.vue';
import LogForm from '../views/Login.vue';
import UserTable from '../views/UserRUD.vue';
import Reg from '../views/Register.vue';
import UserModify from '../views/UserModify.vue';
import CourseTable from '../views/CourseRUD.vue';
import AddCourse from '../views/AddCourse.vue';
import CourseModify from '../views/CourseModify.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/logform',
    name: 'LogForm',
    component: LogForm,
  },
  {
    path: '/usertable',
    name: 'UserTable',
    component: UserTable,
  },
  {
    path: '/register',
    name: 'Register',
    component: Reg,
  },
  {
    path: '/courseupd',
    name: 'CourseModify',
    component: CourseModify,
  },
  {
    path: '/coursetable',
    name: 'CourseTable',
    component: CourseTable,
  },
  {
    path: '/addcourse',
    name: 'AddCourse',
    component: AddCourse,
  },
  {
    path: '/userupd',
    name: 'UserModify',
    component: UserModify,
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue'),
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
