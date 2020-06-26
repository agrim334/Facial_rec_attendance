<template>
  <div id="modify-form">
    <form @submit.prevent="validate">
    <label>User ID</label>
    <input type="text" placeholder = "Enter UID" v-model = 'moduser.username'/>
    <br>

    <label>First name</label>
    <input type="text" placeholder = "Enter first name" v-model = 'moduser.fname'/>
    <br>

    <label>Last name</label>
    <input type="text" placeholder = "Enter last name" v-model = 'moduser.lname'/>
    <br>

    <label> User Email </label>
    <input type="text" placeholder = "Enter email id" v-model = 'moduser.email'/>
    <br>

    <label> Role </label>
    <div id = 'rolerad' v-for='role in roles' :key='role.id'>
      <input type="radio" name= 'role.name' :value = 'role.id' v-model = 'moduser.rolec'>
      <label> {{role.name}} </label>
    </div>
    <br>

    <label> Department </label>
    <div id = 'deptrad' v-for='dept in depts' :key='dept.id'>
      <input type="radio"  name= 'dept.name' :value = 'dept.id' v-model = 'moduser.deptc'>
      <label> {{dept.name}} </label>
    </div>
    <br>
    <input type="submit" value="Modify user" />
    </form>
  </div>
</template>

<script>
const validator = require('email-validator');

export default {
  name: 'ModifyUser',
  props: { userrec: Array, depts: Array, roles: Array },
  data() {
    return {
      moduser: {
        username: this.userrec.username,
        fname: this.userrec.fname,
        lname: this.userrec.lname,
        email: this.userrec.email,
        rolec: this.userrec.role,
        deptc: this.userrec.dept,
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
      if (this.moduser.username === null || this.moduser.username === '') {
        alert('Fill in user name');
        f = 1;
      }
      if (this.moduser.fname === null || this.moduser.fname === '') {
        alert('Fill in first name');
        f = 1;
      }
      if (this.moduser.lname === null || this.moduser.lname === '') {
        alert('Fill in last name');
        f = 1;
      }
      if (this.moduser.email === null || this.moduser.email === '' || validator.validate(this.moduser.email) === false) {
        alert('email format incorrect');
        f = 1;
      }
      if (this.moduser.rolec === null || this.moduser.rolec === '') {
        alert('Choose a role');
        f = 1;
      }
      if (this.moduser.rolec !== ad && (this.moduser.deptc === '' || this.moduser.deptc === null)) {
        alert('Choose a department');
        f = 1;
      }
      if (f === 0) {
        this.$emit('userupd', this.moduser);
      }
    },
  },
};
</script>
