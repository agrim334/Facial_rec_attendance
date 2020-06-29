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
      const path = 'http://localhost:5000/users/reset_password_request';
      axios.post(path, userdat)
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
