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
import MapTable from '../views/MapRUD.vue';
import AddMap from '../views/MapAdd.vue';
import MapModify from '../views/MapModify.vue';
import store from '../store';

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
    props: true,
  },
  {
    path: '/usertable',
    name: 'UserTable',
    component: UserTable,
    props: true,
    beforeEnter(to, from, next) {
      if (!store.getters.isAuthenticated) next('/login');
      else next();
    },
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
    props: true,
  },
  {
    path: '/coursetable',
    name: 'CourseTable',
    component: CourseTable,
    props: true,
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
    props: true,
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
    props: true,
  },
  {
    path: '/attdtable',
    name: 'AttdTable',
    component: AttdTable,
    props: true,
  },
  {
    path: '/addmap',
    name: 'AddMap',
    component: AddMap,
  },
  {
    path: '/mapupd',
    name: 'MapModify',
    component: MapModify,
    props: true,
  },
  {
    path: '/maptable',
    name: 'MapTable',
    component: MapTable,
    props: true,
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
