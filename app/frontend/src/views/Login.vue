<template>
  <div class="home">
    <LogForm @login="validate"></LogForm>
  </div>
</template>

<script>
// @ is an alias to /src
import LogForm from '@/components/LogForm.vue';
import axios from 'axios';

export default {
  name: 'Login',
  components: {
    LogForm,
  },
  methods: {
    validate(cred) {
      const path = 'users/login/';
      this.$store.dispatch('login', { url: path, data: { user: cred.user, password: cred.pass } })
        .then(() => this.$router.push('/'));
    },
  },
};
</script>
