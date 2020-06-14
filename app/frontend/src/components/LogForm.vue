<template>
 <div>
  <form @submit.prevent="logsubmit">
    <label for='username'> Username </label>
    <input id = 'username' type='text' placeholder ="enter name" v-model = 'cred.user'>
    <br>
    <label for='pwd'> Password </label>
    <input id = 'pwd' type='password' placeholder ="enter password" v-model = 'cred.pass'>
    <br>
    <label for='rembme'> Remember me? </label>
    <input id = 'rembme' type='checkbox' v-model = 'cred.rem'>
    <br>
    <input id = 'submit' type = 'submit' value ='Login'>

   </form>
 </div>
</template>

<script>
export default {
  name: 'LogForm',
  data() {
    return { cred: { user: '', pass: '', rem: false } };
  },
  methods: {
    logsubmit() {
      this.$emit('userlogin', this.cred);
    },
  },
};
</script>
