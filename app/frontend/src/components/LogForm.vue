<template>
 <div>
  <b-form @submit.prevent="logsubmit">
    <label for='username'> Username </label>
    <b-input :state='ustate' type='text' placeholder ="enter name" v-model = 'cred.user'>
    </b-input>
    <br>
    <label for='pwd'> Password </label>
    <b-input :state='pwstate' type='password' placeholder ="enter password" v-model = 'cred.pass'>
    </b-input>
    <br>
    <label for='rembme'> Remember me? </label>
    <b-form-checkbox  v-model = 'cred.rem' value='true'>
    </b-form-checkbox>
    <br>
    <b-button type = 'submit'> Login </b-button>
   </b-form>
    <b-button @click='alert(process.env.VUE_APP_TITLE)'> temp </b-button>

 </div>
</template>

<script>

export default {
  name: 'LogForm',
  data() {
    return { cred: { user: '', pass: '', rem: false } };
  },
  computed: {
    ustate() {
      return this.cred.user.length > 0;
    },
    pwstate() {
      return this.cred.pass.length > 0;
    },
  },
  methods: {
    logsubmit() {
      let f = 0;
      if (this.cred.user === null || this.cred.user === '') {
        alert('Fill in user name');
        f = 1;
      }
      if (this.cred.pass === null || this.cred.pass === '') {
        alert('Fill in password');
        f = 1;
      }
      if (f === 0) {
        this.$emit('login', this.cred);
      }
    },
  },
};
</script>
