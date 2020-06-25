<template>
  <div id="register-form">
    <form @submit.prevent="validate">
    <label>User ID</label>
    <input type="text" placeholder = "Enter UID" v-model = 'newuser.username' />
    <br>

    <label>First name</label>
    <input type="text" placeholder = "Enter first name" v-model = 'newuser.fname' />
    <br>

    <label>Last name</label>
    <input type="text" placeholder = "Enter last name" v-model = 'newuser.lname' />
    <br>

    <label> User Email </label>
    <input type="text" placeholder = "Enter email id" v-model = 'newuser.email' />
    <br>

    <label> Role </label>
    <div id = 'rolerad' v-for='role in roles' :key='role.id'>
      <input type="radio" name= 'role.name' :value = 'role.id' v-model = 'newuser.rolec'>
      <label> {{role.name}} </label>
    </div>
    <br>

    <label> Department </label>
    <div id = 'deptrad' v-for='dept in depts' :key='dept.id'>
      <input type="radio"  name= 'dept.name' :value = 'dept.id' v-model = 'newuser.deptc'>
      <label> {{dept.name}} </label>
    </div>
    <br>
    <label> Enter Password </label>
    <input type="password" v-model = 'newuser.pass' />
    <br>

    <label> Confirm Password </label>
    <input type="password" v-model = 'newuser.confirmpass' />
    <br>
    <input type="submit" value="Add user" />
    </form>
  </div>
</template>

<script>
const validator = require('email-validator');

export default {
  name: 'RegisterForm',
  props: { depts: Array, roles: Array },
  data() {
    return {
      newuser: {
        username: '', fname: '', lname: '', email: '', rolec: '', deptc: '', pass: '', confirmpass: '',
      },
    };
  },
  methods: {
    validate() {
      let f = 0;
      let ad = -1;
      for (let i = 0; i < this.roles.length; i += 1) {
        if (this.roles[i].name === 'Admin') {
          ad = this.roles[i].id;
          break;
        }
      }
      if (this.newuser.username === null || this.newuser.username === '') {
        alert('Fill in user name');
        f = 1;
      }
      if (this.newuser.fname === null || this.newuser.fname === '') {
        alert('Fill in first name');
        f = 1;
      }
      if (this.newuser.lname === null || this.newuser.lname === '') {
        alert('Fill in last name');
        f = 1;
      }
      if (this.newuser.email === null || this.newuser.email === '' || validator.validate(this.newuser.email) === false) {
        alert('email format incorrect');
        f = 1;
      }
      if (this.newuser.rolec === null || this.newuser.rolec === '') {
        alert('Choose a role');
        f = 1;
      }
      if (this.newuser.rolec !== ad && (this.newuser.deptc === '' || this.newuser.deptc === null)) {
        alert('Choose a department');
        f = 1;
      }
      if (this.newuser.pass !== this.newuser.confirmpass) {
        alert('Password no match');
        f = 1;
      }
      if (f === 0) {
        this.$emit('userreg', this.newuser);
      }
    },
  },
};
</script>
