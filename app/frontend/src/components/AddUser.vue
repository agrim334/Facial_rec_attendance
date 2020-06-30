<template>
  <div id="register-form">
    <b-form @submit.prevent="validate">
    <label>User ID</label>
    <b-input :state='uidstate' placeholder = "Enter UID"
    v-model = 'newuser.username' required>
    </b-input>

    <label>First name</label>
    <b-input :state='fnstate' placeholder = "Enter first name"
    v-model = 'newuser.fname' required>
    </b-input>
    <br>

    <label>Last name</label>
    <b-input :state='lnstate' placeholder = "Enter last name"
    v-model = 'newuser.lname' required>
    </b-input>
    <br>

    <label> User Email </label>
    <b-input :state='emstate' placeholder = "Enter email id"
    v-model = 'newuser.email' required>
    </b-input>
    <br>

    <b-form-group label="Roles">
      <b-form-radio-group :options='roles' name-field='name' html-field='name'
      value-field = 'id' v-model="newuser.rolec">
      </b-form-radio-group>
    </b-form-group>
    <br>

    <b-form-group label="Department">
      <b-form-radio-group :options='depts' name-field='Deptartment' html-field='name'
      value-field = 'id' v-model="newuser.deptc">
      </b-form-radio-group>
    </b-form-group>
    <br>

    <label> Enter Password </label>
    <b-input :state='pwstate' type="password" v-model = 'newuser.pass' required>
    </b-input>
    <br>

    <label> Confirm Password </label>
    <b-input :state='cfpstate' type="password"
    v-model = 'newuser.confirmpass' required>
    </b-input>
    <br>

    <b-button type="submit"> Add user </b-button>

    </b-form>
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
  computed: {
    uidstate() {
      return this.newuser.username.length > 0;
    },
    fnstate() {
      return this.newuser.fname.length > 0;
    },
    lnstate() {
      return this.newuser.lname.length > 0;
    },
    emstate() {
      return (this.newuser.email.length > 0) && validator.validate(this.newuser.email);
    },
    pwstate() {
      return (this.newuser.pass.length > 0) && this.newuser.pass === this.newuser.confirmpass;
    },
    cfpstate() {
      return ((this.newuser.confirmpass.length > 0)
      && this.newuser.pass === this.newuser.confirmpass);
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
        alert('Non admin must have a department');
        f = 1;
      }
      if (this.newuser.pass !== this.newuser.confirmpass || (this.newuser.pass === this.newuser.confirmpass && (this.newuser.pass === null || this.newuser.pass === ''))) {
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
