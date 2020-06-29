<template>
  <div id="modify-form">
    <b-form @submit.prevent="validate">

    <label> Enter Username or email id </label>
    <b-input :state='uidstate' v-model = 'moduser.uid' required>
    </b-input>
    <br>

    <b-button type="submit"> Request Reset </b-button>

    </b-form>
  </div>
</template>

<script>
const validator = require('email-validator');

export default {
  name: 'ReqResetForm',
  data() {
    return {
      moduser: {
        uid: '',
      },
    };
  },
  computed: {
    uidstate() {
      return (this.moduser.uid.length > 0) || validator.validate(this.moduser.uid);
    },
  },
  methods: {
    validate() {
      let f = 0;
      if ((this.moduser.uid === null || this.moduser.uid.length === 0)
      && (validator.validate(this.moduser.uid) === false)) {
        alert('Enter username or email');
        f = 1;
      }
      if (f === 0) {
        this.$emit('userupd', this.moduser);
      }
    },
  },
};
</script>
