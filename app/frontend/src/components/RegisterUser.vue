<template>
  <div id="register-form">
    <form>
    <label>User ID</label>
    <input type="text" placeholder = "Enter UID" v-model = 'userid' />
    <br>

    <label>First name</label>
    <input type="text" placeholder = "Enter first name" v-model = 'fname' />
    <br>

    <label>Last name</label>
    <input type="text" placeholder = "Enter last name" v-model = 'lname' />
    <br>

    <label> User Email </label>
    <input type="text" placeholder = "Enter email id" v-model = 'email' />
    <br>

    <label> Role </label>
    <div id = 'rolerad' v-for='role in roles' :key='role.id'>
      <input type="radio" name= 'role.name' :value = 'role.id' v-model = 'rolec'>
      <label> {{role.name}} </label>
    </div>
    <br>

    <label> Department </label>
    <div id = 'deptrad' v-for='dept in depts' :key='dept.id'>
      <input type="radio"  name= 'dept.name' :value = 'dept.id' v-model = 'deptc'>
      <label> {{dept.name}} </label>
    </div>
    <br>
    <p> {{deptc}} </p>
    <label> Enter Password </label>
    <input type="passsword" v-model = 'pass' />
    <br>

    <label> Confirm Password </label>
    <input type="passsword" v-model = 'confirmpass' />
    <br>

    <button>Add User</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'RegisterForm',
  data() {
    return {
      userid: '',
      fname: '',
      lname: '',
      email: '',
      roles: [{ id: 1, name: 'Student' }, { id: 2, name: 'Admin' }, { id: 3, name: 'Prof' }, { id: 4, name: 'TA' }],
      depts: [{ id: 1, name: 'EE' }, { id: 2, name: 'ECE' }, { id: 3, name: 'Prod' }, { id: 4, name: 'CSE' }],
      rolec: '',
      deptc: '',
      pass: '',
      confirmpass: '',
    };
  },
};
</script>
