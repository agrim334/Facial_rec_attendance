<template>
  <div id="modify-form">
    <b-form @submit.prevent="validate">

    <label> Enter New Password </label>
    <b-input :state='npwstate' type="password" v-model = 'moduser.newpass' required>
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

export default {
  name: 'PwdResetForm',
  data() {
    return {
      moduser: {
        newpass: '',
        confirmpass: '',
      },
    };
  },
  computed: {
    npwstate() {
      return (this.moduser.newpass.length > 0) && this.moduser.newpass === this.moduser.confirmpass;
    },
    cfpstate() {
      return ((this.moduser.confirmpass.length > 0)
      && this.moduser.newpass === this.moduser.confirmpass);
    },
  },
  methods: {
    validate() {
      let f = 0;
      if (this.moduser.newpass !== this.moduser.confirmpass || (this.moduser.newpass === this.moduser.confirmpass && (this.moduser.newpass === null || this.moduser.newpass === ''))) {
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
