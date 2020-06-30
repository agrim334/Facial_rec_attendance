import Vue from 'vue';
import Vuex from 'vuex';
import VueRouter from 'vue-router';
import Home from '../views/Home.vue';
import Login from '../views/Login.vue';
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
import PasswordChange from '../views/PasswordChange.vue';
import PasswordReset from '../views/PasswordReset.vue';
import RequestReset from '../views/PasswordResetRequest.vue';
import store from '../store';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    beforeEnter(to, from, next) {
      let t = 1;
      const role = store.state.userrole;
      console.log(process.env.BASE_URL);
      if (!role || (role !== 'Admin' && role !== 'Prof' && role !== 'TA' && role !== 'Student')) {
        t = 0;
      }
      if (!store.getters.isAuthenticated || t === 0) next('/login');
      else next();
    },
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    beforeEnter(to, from, next) {
      if (store.getters.isAuthenticated) next('/');
      else next();
    },
  },
  {
    path: '/register',
    name: 'Register',
    component: Reg,
    beforeEnter(to, from, next) {
      let t = 1;
      const role = store.state.userrole;
      if (!role || role !== 'Admin') {
        t = 0;
      }
      if (!store.getters.isAuthenticated) next('/login');
      else if (!t) next('/');
      else next();
    },
  },
  {
    path: '/resetreq',
    name: 'RequestReset',
    component: RequestReset,
    beforeEnter(to, from, next) {
      if (store.getters.isAuthenticated) next('/');
      else next();
    },
  },
  {
    path: '/resetpwd/:token',
    name: 'PasswordReset',
    component: PasswordReset,
    beforeEnter(to, from, next) {
      if (store.getters.isAuthenticated) next('/');
      else next();
    },
  },
  {
    path: '/pwdchg',
    name: 'PasswordChange',
    component: PasswordChange,
    beforeEnter(to, from, next) {
      if (!store.getters.isAuthenticated) next('/login');
      else next();
    },
  },
  {
    path: '/userupd',
    name: 'UserModify',
    component: UserModify,
    props: true,
    beforeEnter(to, from, next) {
      let t = 1;
      const role = store.state.userrole;
      if (!role || role !== 'Admin') {
        t = 0;
      }
      if (!store.getters.isAuthenticated) next('/login');
      else if (t === 0) next('/');
      else next();
    },
  },
  {
    path: '/usertable',
    name: 'UserTable',
    component: UserTable,
    props: true,
    beforeEnter(to, from, next) {
      let t = 1;
      const role = store.state.userrole;
      if (!role || (role !== 'Admin' && role !== 'Prof' && role !== 'Student' && role !== 'TA')) {
        t = 0;
      }
      if (!store.getters.isAuthenticated) next('/login');
      else if (t === 0) next('/');
      else next();
    },
  },
  {
    path: '/addcourse',
    name: 'AddCourse',
    component: AddCourse,
    beforeEnter(to, from, next) {
      let t = 1;
      const role = store.state.userrole;
      if (!role || role !== 'Admin') {
        t = 0;
      }
      if (!store.getters.isAuthenticated) next('/login');
      else if (t === 0) next('/');
      else next();
    },
  },
  {
    path: '/courseupd',
    name: 'CourseModify',
    component: CourseModify,
    props: true,
    beforeEnter(to, from, next) {
      let t = 1;
      const role = store.state.userrole;
      if (!role || role !== 'Admin') {
        t = 0;
      }
      if (!store.getters.isAuthenticated) next('/login');
      else if (t === 0) next('/');
      else next();
    },
  },
  {
    path: '/coursetable',
    name: 'CourseTable',
    component: CourseTable,
    props: true,
    beforeEnter(to, from, next) {
      let t = 1;
      const role = store.state.userrole;
      if (!role || (role !== 'Admin' && role !== 'Prof' && role !== 'Student' && role !== 'TA')) {
        t = 0;
      }
      if (!store.getters.isAuthenticated) next('/login');
      else if (t === 0) next('/');
      else next();
    },
  },
  {
    path: '/adddept',
    name: 'AddDept',
    component: AddDept,
    beforeEnter(to, from, next) {
      let t = 1;
      const role = store.state.userrole;
      if (!role || role !== 'Admin') {
        t = 0;
      }
      if (!store.getters.isAuthenticated) next('/login');
      else if (t === 0) next('/');
      else next();
    },
  },
  {
    path: '/deptupd',
    name: 'DeptModify',
    component: DeptModify,
    props: true,
    beforeEnter(to, from, next) {
      let t = 1;
      const role = store.state.userrole;
      if (!role || role !== 'Admin') {
        t = 0;
      }
      if (!store.getters.isAuthenticated) next('/login');
      else if (t === 0) next('/');
      else next();
    },
  },
  {
    path: '/depttable',
    name: 'DeptTable',
    component: DeptTable,
    beforeEnter(to, from, next) {
      let t = 1;
      const role = store.state.userrole;
      if (!role || (role !== 'Admin' && role !== 'Prof' && role !== 'Student' && role !== 'TA')) {
        t = 0;
      }
      if (!store.getters.isAuthenticated) next('/login');
      else if (t === 0) next('/');
      else next();
    },
  },
  {
    path: '/addattd',
    name: 'AddAttd',
    component: AddAttd,
    beforeEnter(to, from, next) {
      let t = 1;
      const role = store.state.userrole;
      console.log(role);
      if (!role || (role !== 'Admin' && role !== 'Prof' && role !== 'TA')) {
        t = 0;
      }
      if (!store.getters.isAuthenticated) next('/login');
      else if (t === 0) next('/');
      else next();
    },
  },
  {
    path: '/attdupd',
    name: 'AttdModify',
    component: AttdModify,
    props: true,
    beforeEnter(to, from, next) {
      let t = 1;
      const role = store.state.userrole;
      if (!role || (role !== 'Admin' && role !== 'Prof' && role !== 'TA')) {
        t = 0;
      }
      if (!store.getters.isAuthenticated) next('/login');
      else if (t === 0) next('/');
      else next();
    },
  },
  {
    path: '/attdtable',
    name: 'AttdTable',
    component: AttdTable,
    props: true,
    beforeEnter(to, from, next) {
      let t = 1;
      const role = store.state.userrole;
      if (!role || (role !== 'Admin' && role !== 'Prof' && role !== 'Student' && role !== 'TA')) {
        t = 0;
      }
      if (!store.getters.isAuthenticated) next('/login');
      else if (t === 0) next('/');
      else next();
    },
  },
  {
    path: '/addmap',
    name: 'AddMap',
    component: AddMap,
    beforeEnter(to, from, next) {
      let t = 1;
      const role = store.state.userrole;
      if (!role || role !== 'Admin') {
        t = 0;
      }
      if (!store.getters.isAuthenticated) next('/login');
      else if (t === 0) next('/');
      else next();
    },
  },
  {
    path: '/mapupd',
    name: 'MapModify',
    component: MapModify,
    props: true,
    beforeEnter(to, from, next) {
      let t = 1;
      const role = store.state.userrole;
      if (!role || role !== 'Admin') {
        t = 0;
      }
      if (!store.getters.isAuthenticated) next('/login');
      else if (t === 0) next('/');
      else next();
    },
  },
  {
    path: '/maptable',
    name: 'MapTable',
    component: MapTable,
    props: true,
    beforeEnter(to, from, next) {
      let t = 1;
      const role = store.state.userrole;
      if (!role || (role !== 'Admin' && role !== 'Prof' && role !== 'Student' && role !== 'TA')) {
        t = 0;
      }
      if (!store.getters.isAuthenticated) next('/login');
      else if (t === 0) next('/');
      else next();
    },
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
