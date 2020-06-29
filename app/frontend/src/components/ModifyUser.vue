<template>
  <div id="modify-form">
    <b-form @submit.prevent="validate">
    <label>User ID</label>
    <b-input :state='uidstate' placeholder = "Enter UID"
    v-model = 'moduser.username' required>
    </b-input>

    <label>First name</label>
    <b-input :state='fnstate' placeholder = "Enter first name"
    v-model = 'moduser.fname' required>
    </b-input>
    <br>

    <label>Last name</label>
    <b-input :state='lnstate' placeholder = "Enter last name"
    v-model = 'moduser.lname' required>
    </b-input>
    <br>

    <label> User Email </label>
    <b-input :state='emstate' placeholder = "Enter email id"
    v-model = 'moduser.email' required>
    </b-input>
    <br>

    <b-form-group label="Roles">
      <b-form-radio-group :options='roles' name-field='name' html-field='name'
      value-field = 'id' v-model="moduser.rolec">
      </b-form-radio-group>
    </b-form-group>
    <br>

    <b-form-group label="Department">
      <b-form-radio-group :options='depts' name-field='name' html-field='name'
      value-field = 'id' v-model="moduser.deptc">
      </b-form-radio-group>
    </b-form-group>
    <br>

    <label> Enter Password </label>
    <b-input :state='pwstate' type="password" v-model = 'moduser.pass' required>
    </b-input>
    <br>

    <label> Confirm Password </label>
    <b-input :state='cfpstate' type="password"
    v-model = 'moduser.confirmpass' required>
    </b-input>
    <br>

    <b-button type="submit"> Modify user </b-button>

    </b-form>
  </div>
</template>

<script>
const validator = require('email-validator');

export default {
  name: 'ModifyUser',
  props: { userrec: Object, depts: Array, roles: Array },
  data() {
    return {
      moduser: {
        username: this.userrec.username || '',
        fname: this.userrec.fname || '',
        lname: this.userrec.lname || '',
        email: this.userrec.email || '',
        rolec: this.userrec.role || '',
        deptc: this.userrec.dept || '',
        pass: '',
        confirmpass: '',
      },
    };
  },
  computed: {
    uidstate() {
      return this.moduser.username.length > 0;
    },
    fnstate() {
      return this.moduser.fname.length > 0;
    },
    lnstate() {
      return this.moduser.lname.length > 0;
    },
    emstate() {
      return (this.moduser.email.length > 0) && validator.validate(this.moduser.email);
    },
    pwstate() {
      return (this.moduser.pass.length > 0) && this.moduser.pass === this.moduser.confirmpass;
    },
    cfpstate() {
      return ((this.moduser.confirmpass.length > 0)
      && this.moduser.pass === this.moduser.confirmpass);
    },
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
        alert('Non admin must have a department');
        f = 1;
      }
      if (this.moduser.pass !== this.moduser.confirmpass || (this.moduser.pass === this.moduser.confirmpass && (this.moduser.pass === null || this.moduser.pass === ''))) {
        alert('Password no match');
        f = 1;
      }
      if (f === 0) {
        this.$emit('userupd', this.moduser);
      }
    },
  },
};
</script>
