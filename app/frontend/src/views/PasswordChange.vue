<template>
  <div class="home" v-if='isAuth'>
    <PwdChgForm @userupd='updaterec'> </PwdChgForm>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import PwdChgForm from '@/components/ChangePassword.vue';

export default {
  name: 'PasswordChange',
  computed: {
    isAuth() {
      return this.$store.getters.isAuthenticated;
    },
  },
  components: {
    PwdChgForm,
  },
  methods: {
    logout() {
      this.$store.dispatch('logout')
        .then(() => this.$router.push('/login'));
    },
    updaterec(userdat) {
      const path = 'users/change_pwd';
      this.$store.dispatch('authrequest', { url: path, data: userdat })
        .then((res) => {
          if (res.data.message === 'Invalid token') {
            alert("Bad session logging out");
            this.logout();
          }
          else if (res.data.message === 'Expired token') {
            alert("Session expired. You have to login again");
            this.logout();
          }
          else {
            alert(res.data);
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
};
</script>
