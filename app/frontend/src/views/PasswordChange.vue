<template>
  <div class="home" v-if='isAuthenticated'>
    <PwdChgForm @userupd='updaterec'> </PwdChgForm>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import PwdChgForm from '@/components/ChangePassword.vue';

export default {
  name: 'PasswordChange',
  components: {
    PwdChgForm,
  },
  computed: {
    isAuthenticated() {
      return this.$store.getters.isAuthenticated;
    },
  },
  methods: {
    logout() {
      this.$store.dispatch('logout')
        .then(() => this.$router.push('/login'));
    },
    updaterec(userdat) {
      if (this.isAuthenticated) {
        const path = 'users/change_pwd';
        this.$store.dispatch('authrequest', { url: path, data: userdat })
          .then((response) => {
            alert(response.data.result);
          })
          .catch((error) => {
            console.error(error);
          });
      }
      else {
        alert("Session expired. You have to login again");
        this.logout();
      }
    },
  },
};
</script>
