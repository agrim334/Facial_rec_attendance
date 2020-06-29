<template>
  <div class="home">
    <PwdResetForm  @userupd='updaterec'> </PwdResetForm>
  </div>

</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import PwdResetForm from '@/components/ResetPasswordmail.vue';

export default {
  name: 'PasswordReset',
  components: {
    PwdResetForm,
  },
  data() {
    return {
      token: '',
    };
  },
  methods: {
    updaterec(userdat) {
      if (this.token !== '' || this.token !== null) {
        const path = 'http://localhost:5000/users/reset_password';
        path.concat(this.token);
        console.log(path);
        axios.post(path, userdat)
          .then(() => {
            console.log(this);
          })
          .catch((error) => {
            console.error(error);
          });
      }
    },
  },
};
</script>
