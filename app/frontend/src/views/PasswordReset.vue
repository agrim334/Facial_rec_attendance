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
    getLastSegment(url) {
      return url.replace(/.+\//, '');
    },
    updaterec(userdat) {
      if (this.token !== '' || this.token !== null) {
        let path = 'users';
        path = path.concat(this.$route.path);
        console.log(path);
        this.$store.dispatch('noauthroutrereq', { url: path, data: userdat })
          .then((res) => {
            console.log(res.data.status);
          })
          .catch((error) => {
            console.error(error);
          });
      }
    },
  },
};
</script>
