<template>
  <div id="register-form">
    <form @submit.prevent="handle">
    <label>User ID</label>
    <input type="text" placeholder = "Enter UID" v-model = 'newuser.userid' />
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
    <input type="passsword" v-model = 'newuser.pass' />
    <br>

    <label> Confirm Password </label>
    <input type="passsword" v-model = 'newuser.confirmpass' />
    <br>

    <button>Add User</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'RegisterForm',
  props: { depts: Array, roles: Array },
  data() {
    return {
      newuser: {
        userid: '', fname: '', lname: '', email: '', rolec: '', deptc: '', pass: '', confirmpass: '',
      },
    };
  },
  methods: {
    handle() {
      this.$emit('userreg', this.newuser);
    },
  },
};
</script>
