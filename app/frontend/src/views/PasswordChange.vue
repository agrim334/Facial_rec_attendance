<template>
  <div class="home">
    <PwdChgForm  @userupd='updaterec'> </PwdChgForm>
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
  methods: {
    updaterec(userdat) {
      const path = 'users/change_pwd';
      this.$store.dispatch('authrequest', { url: path, data: userdat })
        .then(() => {
          console.log(this);
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
};
</script>
