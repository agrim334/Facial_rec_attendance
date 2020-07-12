<template>
  <div class="home">
    <ReqResetForm  @userupd='updaterec'> </ReqResetForm>
  </div>

</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import ReqResetForm from '@/components/RequestResetPassword.vue';

export default {
  name: 'RequestReset',
  components: {
    ReqResetForm,
  },
  methods: {
    updaterec(userdat) {
      const path = 'users/reset_password_request';
      this.$store.dispatch('authrequest', { url: path, data: userdat })
        .then((response) => {
          alert(response.data.result);
        })
        .catch((error) => {
          alert(error.response.data.result);
          console.error(error);
        });
    },
  },
};
</script>
