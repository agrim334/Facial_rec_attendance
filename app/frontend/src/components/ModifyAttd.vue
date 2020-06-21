<template>
  <div id="modify-form">
    <form @submit.prevent="handle">
    <label>Prof/TA ID</label>
    <input type="text" placeholder = "Enter New MarkerID" v-model = 'modattd.markerid'
    value = 'attdrec.markerid' />
    <br>

    <label>Student ID</label>
    <input type="text" placeholder = "Enter New Student ID" v-model = 'modattd.markeeid'
    value = 'attdrec.markeeid'/>
    <br>

    <label>Course ID</label>
    <input type="text" placeholder = "Enter new Course ID" v-model = 'modattd.cid'
    value = 'attdrec.cid'/>
    <br>

    <label>TimeStamp(Date of class) </label>
    <input type="text" placeholder = "Enter new Timestamp" v-model = 'modattd.ts'
    value = 'attdrec.email'/>
    <br>

    <label> Role </label>
    <div id = 'rolerad' v-for='role in roles' :key='role.id'>
      <input type="radio" name= 'role.name' :value = 'role.id' v-model = 'modattd.rolec'>
      <label> {{role.name}} </label>
    </div>
    <br>

    <input type="submit" value="Modify attd" />
    </form>
  </div>
</template>

<script>
export default {
  name: 'ModifyAttdForm',
  props: { attdrec: Array, roles: Array },
  data() {
    return {
      modattd: {
        markerid: '', markeeid: '', cid: '', ts: '', rolec: '',
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
