<template>
  <div id="modify-form">
    <form @submit.prevent="handle">
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
        rolec: this.userrec.role_id,
        deptc: this.userrec.dept_id,
      },
    };
  },
  methods: {
    handle() {
      this.$emit('userupd', this.moduser);
    },
  },
};
</script>
