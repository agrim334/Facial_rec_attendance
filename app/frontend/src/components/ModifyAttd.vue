<template>
  <div id="modify-form">
    <form @submit.prevent="handle">
    <label>User ID</label>
    <input type="text" placeholder = "Enter UID" v-model = 'moduser.userid'
    value = 'userrec.userid' />
    <br>

    <label>First name</label>
    <input type="text" placeholder = "Enter first name" v-model = 'moduser.fname'
    value = 'userrec.fname'/>
    <br>

    <label>Last name</label>
    <input type="text" placeholder = "Enter last name" v-model = 'moduser.lname'
    value = 'userrec.lname'/>
    <br>

    <label> User Email </label>
    <input type="text" placeholder = "Enter email id" v-model = 'moduser.email'
    value = 'userrec.email'/>
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
        userid: '', fname: '', lname: '', email: '', rolec: '', deptc: '',
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
