<template>
  <div id="modify-form">
    <form @submit.prevent="handle">
    <label>attd ID</label>
    <input type="text" placeholder = "Enter UID" v-model = 'modattd.markerid'
    value = 'attdrec.attdid' />
    <br>

    <label>First name</label>
    <input type="text" placeholder = "Enter first name" v-model = 'modattd.markeeid'
    value = 'attdrec.fname'/>
    <br>

    <label>Last name</label>
    <input type="text" placeholder = "Enter last name" v-model = 'modattd.lname'
    value = 'attdrec.lname'/>
    <br>

    <label> attd Email </label>
    <input type="text" placeholder = "Enter email id" v-model = 'modattd.email'
    value = 'attdrec.email'/>
    <br>

    <label> Role </label>
    <div id = 'rolerad' v-for='role in roles' :key='role.id'>
      <input type="radio" name= 'role.name' :value = 'role.id' v-model = 'modattd.rolec'>
      <label> {{role.name}} </label>
    </div>
    <br>

    <label> Department </label>
    <div id = 'deptrad' v-for='dept in depts' :key='dept.id'>
      <input type="radio"  name= 'dept.name' :value = 'dept.id' v-model = 'modattd.deptc'>
      <label> {{dept.name}} </label>
    </div>
    <br>
    <input type="submit" value="Modify attd" />
    </form>
  </div>
</template>

<script>
export default {
  name: 'Modifyattd',
  props: { attdrec: Array, depts: Array, roles: Array },
  data() {
    return {
      modattd: {
        attdid: '', fname: '', lname: '', email: '', rolec: '', deptc: '',
      },
    };
  },
  methods: {
    handle() {
      this.$emit('attdupd', this.modattd);
    },
  },
};
</script>
