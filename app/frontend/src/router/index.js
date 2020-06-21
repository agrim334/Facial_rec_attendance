import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../views/Home.vue';
import LogForm from '../views/Login.vue';
import UserTable from '../views/UserRUD.vue';
import Reg from '../views/UserAdd.vue';
import UserModify from '../views/UserModify.vue';
import CourseTable from '../views/CourseRUD.vue';
import AddCourse from '../views/CourseAdd.vue';
import CourseModify from '../views/CourseModify.vue';
import DeptTable from '../views/DeptRUD.vue';
import AddDept from '../views/DeptAdd.vue';
import DeptModify from '../views/DeptModify.vue';
import AttdTable from '../views/AttdRUD.vue';
import AddAttd from '../views/AttdAdd.vue';
import AttdModify from '../views/AttdModify.vue';

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
    path: '/register',
    name: 'Register',
    component: Reg,
  },
  {
    path: '/userupd',
    name: 'UserModify',
    component: UserModify,
  },
  {
    path: '/usertable',
    name: 'UserTable',
    component: UserTable,
  },
  {
    path: '/addcourse',
    name: 'AddCourse',
    component: AddCourse,
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
    path: '/adddept',
    name: 'AddDept',
    component: AddDept,
  },
  {
    path: '/deptupd',
    name: 'DeptModify',
    component: DeptModify,
  },
  {
    path: '/depttable',
    name: 'DeptTable',
    component: DeptTable,
  },
  {
    path: '/addattd',
    name: 'AddAttd',
    component: AddAttd,
  },
  {
    path: '/attdupd',
    name: 'AttdModify',
    component: AttdModify,
  },
  {
    path: '/atddtable',
    name: 'AttdTable',
    component: AttdTable,
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
