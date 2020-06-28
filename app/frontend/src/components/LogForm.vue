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
    <input id = 'rembme' type='checkbox' v-model = 'cred.rem'>
    <br>
    <b-button type = 'submit'> Login </b-button>

   </b-form>
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
    authenticate() {
      this.$store.dispatch('login', { email: this.email, password: this.password })
        .then(() => this.$router.push('/'));
    },
    register() {
      this.$store.dispatch('register', { email: this.email, password: this.password })
        .then(() => this.$router.push('/'));
    },
  },
  mounted() {
    EventBus.$on('failedRegistering', (msg) => {
      this.errorMsg = msg;
    });
    EventBus.$on('failedAuthentication', (msg) => {
      this.errorMsg = msg;
    });
  },
  beforeDestroy() {
    EventBus.$off('failedRegistering');
    EventBus.$off('failedAuthentication');
  },
};
</script>
